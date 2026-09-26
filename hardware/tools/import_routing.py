"""Import a first-pass SES into a CLOSED native EasyEDA project.

The pcb skill's SES parser handles units; this writer uses the eprj3 native
LINE/VIA format. Keeps manual antenna copper, components, libraries and rules.
Native readback and DRC are required after import. No fabrication claim.
"""
import argparse, importlib.util, json, shutil, subprocess, sys, uuid
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('session',type=Path)
p.add_argument('--routing-tools',type=Path,required=True)
p.add_argument('--replace',action='store_true',help='Replace only primitive IDs owned by the previous import manifest')
p.add_argument('--dsn',type=Path,help='Exact router input DSN; required for replacement to preserve fixed-pin vias')
a=p.parse_args()
if a.replace and (not a.dsn or not a.dsn.is_file()):
    p.error('--replace requires --dsn: native DSN may represent existing vias as fixed pins')
spec=importlib.util.spec_from_file_location('ses_parser',a.routing_tools/'ses_import.py')
ses=importlib.util.module_from_spec(spec);spec.loader.exec_module(ses)
segments,vias,meta=ses.parse_ses(a.session.read_text())
segments,vias=ses.filter_wiring(segments,vias,protected=['ANT_A','ANT_B'],
                              forbid_layers=['Inner1'])
root=Path(__file__).resolve().parents[1]
pcb=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
manifest=root/'review/autoroute-import.json'
old_ids=set()
if manifest.exists():
    if not a.replace:raise SystemExit('Existing route manifest: use --replace for an explicitly owned replacement.')
    previous=json.loads(manifest.read_text())
    if previous.get('native_routing_continued'):
        raise SystemExit('Native routing has continued this draft; do not merge a fresh SES over those edits. Prepare an explicit clean routing base first.')
    old_ids=set(previous['primitive_ids'])
lines=pcb.read_text().splitlines();doc=None;ticket=0;refs={};net_names=set()
kept=[];removed=set()
for l in lines:
    h,b=l.split('||',1);h=json.loads(h);b=b.removesuffix('|');v=json.loads(b) if b else None
    if h['type']=='DOCHEAD':doc=v['docType']
    if doc=='PCB':
        ticket=max(ticket,h.get('ticket',0))
        if h['type']=='NET':net_names.add(json.loads(h['id'])[1])
        if h.get('id') in old_ids:
            assert h['type'] in ('LINE','VIA') and v and v.get('netName') not in ('ANT_A','ANT_B')
            removed.add(h['id']);continue
    kept.append(l)
assert removed==old_ids, ('Owned route IDs missing',old_ids-removed)
lines=kept
assert doc=='PCB', 'PCB must be final document in native file'
layers={'TopLayer':1,'Inner1':15,'Inner2':16,'BottomLayer':2}
ids=[]
def add(kind,body):
    global ticket
    ticket+=1;ident=uuid.uuid4().hex[:16];ids.append(ident)
    h={'type':kind,'ticket':ticket,'id':ident}
    lines.append(json.dumps(h,separators=(',',':'))+'||'+json.dumps(body,separators=(',',':'))+'|')
def base(net):
    assert net in net_names, ('Unknown native net',net)
    return {'partitionId':'','groupId':0,'netName':net,'locked':False,'zIndex':-1}
for s in segments:
    b=base(s['net']);b.update(layerId=layers[s['layer']],
        startX=s['x1']/.0254,startY=s['y1']/.0254,
        endX=s['x2']/.0254,endY=s['y2']/.0254,width=s['w']/.0254)
    add('LINE',b)
for v in vias:
    assert v['padstack'] in ('via0','viaSmall'), ('Unexpected via stack',v['padstack'])
    b=base(v['net']);b.update(ruleName='',centerX=v['x']/.0254,centerY=v['y']/.0254,
        holeDiameter=.3/.0254,viaDiameter=(.5/.0254 if v['padstack']=='viaSmall' else 24),viaType='NORMAL',
        topSolderExpansion=None,bottomSolderExpansion=None,unusedInnerLayers=[])
    add('VIA',b)
backup=Path('/private/tmp/ruri-before-import-'+a.session.stem+'.epcb2')
shutil.copy2(pcb,backup)
pcb.write_text('\n'.join(lines)+'\n')
manifest.write_text(json.dumps({'status':'FIRST PASS - native readback and DRC pending',
    'input_session':a.session.name,'resolution':meta,'segments':len(segments),
    'vias':len(vias),'manual_nets_excluded':['ANT_A','ANT_B'],
    'replaced_owned_primitives':len(removed),'primitive_ids':ids},indent=2)+'\n')
print(f'Imported {len(segments)} segments and {len(vias)} vias; preserves manual copper.')
if a.dsn:
    subprocess.run([sys.executable,str(Path(__file__).with_name('restore_dsn_vias.py')),
                    str(a.dsn),str(backup)],check=True)
subprocess.run([sys.executable,str(Path(__file__).with_name('normalize_routing_contacts.py'))],check=True)
