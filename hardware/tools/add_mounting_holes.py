"""Add NPTH mounting cutouts and all-layer screw clearances to a CLOSED PCB.

Native FILL on layer 12 matches the existing microphone/USB NPTH format.
Final Gerber/drill export must independently confirm these are unplated holes.
"""
from pathlib import Path
import json, uuid, shutil

root = Path(__file__).resolve().parents[1]
pcb = root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
manifest = root/'review/mounting-primitives.json'
cfg = json.loads((root/'design/mounting-holes.json').read_text())
old = set(json.loads(manifest.read_text())['primitive_ids']) if manifest.exists() else set()
rows=[]; doc=None
for line in pcb.read_text().splitlines():
    h,b=line.split('||',1); h=json.loads(h); v=json.loads(b.removesuffix('|')) if b.removesuffix('|') else None
    if h['type']=='DOCHEAD': doc=v['docType']
    if doc=='PCB' and h.get('id') in old: continue
    rows.append((h,v,doc))
assert doc=='PCB'
ticket=max(h.get('ticket',0) for h,v,d in rows if d=='PCB'); ids=[]
def add(kind,body):
    global ticket
    ticket+=1; ident=uuid.uuid4().hex[:16]; ids.append(ident)
    rows.append(({'type':kind,'ticket':ticket,'id':ident},body,'PCB'))
for hole in cfg['holes']:
    x,y=hole['x']/.0254,hole['y']/.0254
    add('FILL',dict(partitionId='',groupId=0,netName='',layerId=12,width=.2,
        fillStyle='SOLID',path=['CIRCLE',x,y,cfg['hole_diameter']/2/.0254],
        locked=True,zIndex=-1,isBridgingCopper=False,networkList=[],refs=[]))
    for layer in [1,15,16,2]:
        add('REGION',dict(partitionId='',groupId=0,layerId=layer,width=.2,
            prohibitType=['TRACK','FILL','COPPER','PLANE'],
            path=[['CIRCLE',x,y,cfg['reserved_diameter']/2/.0254]],locked=True,
            name='RURI_MOUNT_'+hole['name']+'_'+str(layer),regionType='PROHIBIT'))
    add('POLY',dict(partitionId='',groupId=0,netName='',layerId=13,width=.1/.0254,
        path=['CIRCLE',x,y,cfg['reserved_diameter']/2/.0254],locked=True,zIndex=-1,polyType='NORMAL'))
    add('STRING',dict(partitionId='',groupId=0,layerId=3,
        x=(hole['x']+3.6 if hole['x']<44 else hole['x']-3.6)/.0254,y=y,
        text=hole['name'],fontFamily='default',fontSize=1/.0254,strokeWidth=.15/.0254,
        bold=0,italic=0,origin='LEFT_MIDDLE' if hole['x']<44 else 'RIGHT_MIDDLE',angle=0,
        reverse=False,expansion=0,mirror=False,locked=True,zIndex=-1))
shutil.copy2(pcb,'/private/tmp/ruri-before-mounting-holes.epcb2')
pcb.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+
    (json.dumps(v,separators=(',',':')) if v is not None else '')+'|' for h,v,d in rows)+'\n')
manifest.write_text(json.dumps({'primitive_ids':ids,'holes':cfg['holes'],
    'drill_export_verified':False},indent=2)+'\n')
print('Added four 2.2 mm NPTH cutouts and 5.2 mm all-layer screw reservations.')
