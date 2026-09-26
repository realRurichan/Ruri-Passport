"""Apply copper exclusions to the CLOSED native project; preserve all components.

Uses native REGION records calibrated in EasyEDA Pro 4.1.60 and the official
eprj3 library's EProhibitType names. Explicit layer regions avoid assuming the
SDK's multi-layer enum applies to inner signal layers.
"""
from pathlib import Path
import json, uuid, shutil

root=Path(__file__).resolve().parents[1]
p=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
rows=[];doc=None
for l in p.read_text().splitlines():
    h,b=l.split('||',1);h=json.loads(h);b=b.removesuffix('|')
    v=json.loads(b) if b else None
    if h['type']=='DOCHEAD':doc=v['docType']
    if doc=='PCB' and (h.get('id')=='38bd7247777e96c1' or
                      (h['type']=='REGION' and v and v.get('name','').startswith('RURI_ANT_'))):
        continue
    rows.append((h,v,doc))
ticket=max(h.get('ticket',0) for h,v,d in rows if d=='PCB')
def region(name,layer,rect,prohibit):
    global ticket
    x0,y0,x1,y1=rect;ticket+=1
    path=['R',x0/.0254,y1/.0254,(x1-x0)/.0254,(y1-y0)/.0254,0,0]
    rows.append(({'type':'REGION','ticket':ticket,'id':uuid.uuid4().hex[:16]},
                 {'partitionId':'','groupId':0,'layerId':layer,'width':0.2,
                  'prohibitType':prohibit,'path':[path],'locked':True,
                  'name':'RURI_ANT_'+name,'regionType':'PROHIBIT'},'PCB'))
for layer in (1,15,16,2):
    # Board space beside the module antenna, plus directly below the antenna.
    # The module's own shield/pin area at x=4..22,y>6.05 is intentionally excluded.
    for i,rect in enumerate([(0,0,4,21),(22,0,37,21),(4,0,22,6.05)]):
        region(f'WIFI_{layer}_{i}',layer,rect,['TRACK','FILL','COPPER','PLANE'])
    # NFC allows its designed top coil and bottom inner-terminal escape.
    # No planes under the coil; inner-layer routing is excluded too.
    rules=['COPPER','PLANE'] if layer in (1,2) else ['TRACK','FILL','COPPER','PLANE']
    region(f'NFC_{layer}',layer,(52.8,0.5,87.5,25.3),rules)
shutil.copy2(p,'/private/tmp/ruri-before-antenna-keepouts.epcb2')
p.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+
             (json.dumps(v,separators=(',',':')) if v is not None else '')+'|'
             for h,v,d in rows)+'\n')
print('Created 16 explicit copper-layer antenna exclusion regions.')
