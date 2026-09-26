"""Resolve measured redundant vias and tight QFN fanout clearances, offline.

Requires the closed, contact-normalized routing draft. All moved contacts
retain their net and attached endpoints. Native DRC must be rerun afterwards.
"""
import json, math, shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
pcb=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
rows=[];doc=None;byid={};tracks=[]
for line in pcb.read_text().splitlines():
    h,b=line.split('||',1);h=json.loads(h);b=b.removesuffix('|');v=json.loads(b) if b else None
    if h['type']=='DOCHEAD':doc=v['docType']
    rows.append([h,v,line])
    if doc=='PCB' and v and h.get('id'):
        byid[h['id']]=(h,v)
        if h['type']=='LINE':tracks.append(v)
removed=set();changed=set();log=[]
def relocate(ident,net,target,delete=False):
    if delete and ident not in byid:return
    h,v=byid[ident];assert h['type']=='VIA' and v['netName']==net
    old=(v['centerX'],v['centerY']);count=0
    for t in tracks:
        if t.get('netName')!=net:continue
        for side in ('start','end'):
            if math.hypot(t[side+'X']-old[0],t[side+'Y']-old[1])<.011:
                t[side+'X'],t[side+'Y']=target;changed.add(id(t));count+=1
    if delete:removed.add(ident)
    else:v['centerX'],v['centerY']=target;changed.add(id(v))
    log.append({'via':ident,'net':net,'from_mil':old,'to_mil':target,'removed':delete,'attached_endpoints':count})

# A seed and the previous DSN fixed via represented the same speaker contact.
# Keep the 0.50 mm seed; its position also clears the adjacent SPK_OUT_P stub.
keep=byid['4abe55f20a894e9c'][1]
relocate('033328a0ce074bf4','SPK_OUT_N',(keep['centerX'],keep['centerY']),True)
# JRouter added a coincident via at an existing NFC_IRQ contact.
keep=byid['0796b5f04c49464d'][1]
relocate('39b4b696890ba3e5','NFC_IRQ',(keep['centerX'],keep['centerY']),True)
# 0.50/0.30 mm vias meet the existing native via rule and clear 0.5 mm-pitch
# QFN fanout traces. Stagger their neighbours to maintain hole spacing.
for ident,net in [('6669b6f363b5445a','NFC_IRQ'),('8916e9303370460f','I2C_SDA')]:
    h,v=byid[ident];assert v['netName']==net
    v['viaDiameter']=.5/.0254;changed.add(id(v))
    log.append({'via':ident,'net':net,'diameter_mm':.5,'drill_unchanged':True})
for ident,net,y in [('5d8511f140424c12','GND',30.4),
                    ('f981c9a11fff4a2c','3V18',30.7),
                    ('8916e9303370460f','I2C_SDA',31.2)]:
    v=byid[ident][1]
    relocate(ident,net,(v['centerX'],y/.0254))

shutil.copy2(pcb,'/private/tmp/ruri-before-fanout-refinement.epcb2')
pcb.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+json.dumps(v,separators=(',',':'))+'|'
                         if id(v) in changed else line for h,v,line in rows if h.get('id') not in removed)+'\n')
mfile=root/'review/autoroute-import.json';m=json.loads(mfile.read_text())
m['primitive_ids']=[x for x in m['primitive_ids'] if x not in removed]
m['status']='Native JRouter continued this route; import manifest describes the imported subset only'
m['native_routing_continued']=True
mfile.write_text(json.dumps(m,indent=2)+'\n')
(root/'review/fanout-refinement.json').write_text(json.dumps({'status':'Native DRC pending','changes':log},indent=2)+'\n')
print('Removed two redundant vias; refined four QFN fanout vias.')
