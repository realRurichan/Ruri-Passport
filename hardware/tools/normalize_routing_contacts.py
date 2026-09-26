"""Align near-coincident SAME-NET via/track endpoints after DSN rounding.

Closed project only. EasyEDA exports fixed-pin via centres to 0.01 mil but
retains more precision in the PCB. Native connection DRC reported gaps of
0.002 mil despite overlapping copper. A native single-via correction was
checked first: its three connection errors disappeared.

This does not route missing connections. It only coalesces contacts already
within 0.01 mil (0.000254 mm), preserving net names and widths/diameters.
"""
import collections, json, math, shutil
from pathlib import Path

root=Path(__file__).resolve().parents[1]
pcb=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
rows=[];doc=None;tracks=[];vias=[]
for line in pcb.read_text().splitlines():
    h,b=line.split('||',1);h=json.loads(h);b=b.removesuffix('|')
    v=json.loads(b) if b else None
    if h['type']=='DOCHEAD':doc=v['docType']
    row=[h,v,line];rows.append(row)
    if doc=='PCB' and v and v.get('netName') and v.get('layerId',1) in (1,2,15,16):
        if h['type']=='LINE':tracks.append(row)
        if h['type']=='VIA':vias.append(row)

changes=[]
for vh,v,_ in vias:
    matches=[]
    for th,t,_ in tracks:
        if t['netName']!=v['netName']:continue
        for side in ('start','end'):
            x,y=t[side+'X'],t[side+'Y']
            if math.hypot(x-v['centerX'],y-v['centerY'])<=.01:
                matches.append((th,t,side,x,y))
    if not matches:continue
    target=collections.Counter((round(x,6),round(y,6)) for _,_,_,x,y in matches).most_common(1)[0][0]
    before=(v['centerX'],v['centerY'])
    if math.hypot(target[0]-before[0],target[1]-before[1])>.010001:raise ValueError('Snap exceeds bound')
    v['centerX'],v['centerY']=target
    for th,t,side,x,y in matches:
        t[side+'X'],t[side+'Y']=target
    if before!=target or any((x,y)!=target for _,_,_,x,y in matches):
        changes.append({'via':vh['id'],'net':v['netName'],'before_mil':before,
                        'after_mil':target,'tracks':[th['id'] for th,_,_,_,_ in matches],
                        'via_displacement_mm':math.dist(before,target)*.0254})

shutil.copy2(pcb,'/private/tmp/ruri-before-contact-normalization.epcb2')
changed={id(row) for row in tracks+vias}
pcb.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+json.dumps(v,separators=(',',':'))+'|'
                         if id(row) in changed else line for row in rows for h,v,line in [row])+'\n')
(root/'review/contact-normalization.json').write_text(json.dumps({'tolerance_mil':.01,
    'status':'Native DRC required after normalization','contacts':changes},indent=2)+'\n')
print(f'Normalized {len(changes)} same-net via contact groups; max via displacement '
      f'{max((c["via_displacement_mm"] for c in changes),default=0):.7f} mm')
