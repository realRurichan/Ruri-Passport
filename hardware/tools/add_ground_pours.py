"""Add top, Inner1 reference and bottom GND pour boundaries to a CLOSED PCB.

Native client must rebuild these pours; the boundary alone is not copper.
"""
import json, uuid, shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
pcb=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
rows=[];doc=None
for l in pcb.read_text().splitlines():
    h,b=l.split('||',1);h=json.loads(h);v=json.loads(b.removesuffix('|')) if b.removesuffix('|') else None
    if h['type']=='DOCHEAD':doc=v['docType']
    if doc=='PCB' and h['type']=='POUR' and v and v.get('name','').startswith('RURI_GND_'):continue
    rows.append((h,v,doc))
assert doc=='PCB'
ticket=max(h.get('ticket',0) for h,v,d in rows if d=='PCB')
for layer,name in [(1,'TOP'),(15,'REFERENCE'),(2,'BOTTOM')]:
    ticket+=1
    rows.append(({'type':'POUR','ticket':ticket,'id':uuid.uuid4().hex[:16]},
        dict(partitionId='',groupId=0,netName='GND',layerId=layer,width=.2,
             name='RURI_GND_'+name,order=0,
             path=[['R',.3/.0254,134.7/.0254,87.4/.0254,134.4/.0254,0,0]],
             pourType={'pourType':'SOLID','fineness':8},keepIsland=False,locked=False,zIndex=-1),'PCB'))
shutil.copy2(pcb,'/private/tmp/ruri-before-ground-pours.epcb2')
pcb.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+
    (json.dumps(v,separators=(',',':')) if v is not None else '')+'|' for h,v,d in rows)+'\n')
print('Added three GND boundaries; native rebuild required.')
