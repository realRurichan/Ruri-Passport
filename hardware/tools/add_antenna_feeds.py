"""Write the manually planned ANT_A/B feeds to a CLOSED native PCB."""
import json, uuid, shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
pcb=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
manifest=root/'review/antenna-feed-primitives.json'
old=set(json.loads(manifest.read_text())['primitive_ids']) if manifest.exists() else set()
rows=[];doc=None
for l in pcb.read_text().splitlines():
    h,b=l.split('||',1);h=json.loads(h);v=json.loads(b.removesuffix('|')) if b.removesuffix('|') else None
    if h['type']=='DOCHEAD':doc=v['docType']
    if doc=='PCB' and h.get('id') in old:continue
    rows.append((h,v,doc))
assert doc=='PCB'
ticket=max(h.get('ticket',0) for h,v,d in rows if d=='PCB');ids=[]
def add(kind,net,**body):
    global ticket
    ticket+=1;ident=uuid.uuid4().hex[:16];ids.append(ident)
    rows.append(({'type':kind,'ticket':ticket,'id':ident},
        dict(partitionId='',groupId=0,netName=net,locked=True,zIndex=-1,**body),'PCB'))
seeds=json.loads((root/'design/critical-routing.json').read_text())
for path in seeds['paths']:
    if path['net'] not in ('ANT_A','ANT_B'):continue
    for a,b in zip(path['points'],path['points'][1:]):
        add('LINE',path['net'],layerId={'TopLayer':1,'BottomLayer':2}[path['layer']],
            startX=a[0]/.0254,startY=a[1]/.0254,endX=b[0]/.0254,endY=b[1]/.0254,width=path['width']/.0254)
for v in seeds['vias']:
    if v['net'] not in ('ANT_A','ANT_B'):continue
    add('VIA',v['net'],ruleName='',centerX=v['x']/.0254,centerY=v['y']/.0254,
        holeDiameter=.3/.0254,viaDiameter=24,viaType='NORMAL',
        topSolderExpansion=None,bottomSolderExpansion=None,unusedInnerLayers=[])
shutil.copy2(pcb,'/private/tmp/ruri-before-antenna-feeds.epcb2')
pcb.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+
    (json.dumps(v,separators=(',',':')) if v is not None else '')+'|' for h,v,d in rows)+'\n')
manifest.write_text(json.dumps({'primitive_ids':ids,'status':'draft - native DRC pending'},indent=2)+'\n')
print(f'Added {len(ids)} antenna feed primitives.')
