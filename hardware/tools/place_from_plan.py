"""Apply draft placements with the native project CLOSED. Preserve libraries/nets.
Transforms calibrated against native rotated U1 pad readback. This is not DRC.
"""
from pathlib import Path
import json,math,shutil
root=Path(__file__).resolve().parents[1]
p=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
plan=json.loads((root/'design/placement-draft.json').read_text())['placements']
rows=[];doc=None;refs={};comps={}
for line in p.read_text().splitlines():
 h,b=line.split('||',1);h=json.loads(h);b=b.removesuffix('|');v=json.loads(b) if b else None
 if h['type']=='DOCHEAD':doc=v['docType']
 rows.append((h,v,doc))
 if doc=='PCB' and v:
  if h['type']=='COMPONENT':comps[h['id']]=v
  if h['type']=='ATTR' and v.get('key')=='Designator':refs[v['parentId']]=v['value']
transforms={}
for cid,c in comps.items():
 ref=refs.get(cid)
 if ref not in plan:continue
 x,y,a=plan[ref];x/=.0254;y/=.0254
 transforms[cid]=(c['x'],c['y'],x,y,a-c['angle'])
 c.update(x=x,y=y,angle=a)
for h,v,doc in rows:
 if doc!='PCB' or not v or h['type']!='ATTR' or v.get('parentId') not in transforms:continue
 ox,oy,x,y,da=transforms[v['parentId']];angle=math.radians(da)
 if v.get('x') is not None and v.get('y') is not None:
  dx,dy=v['x']-ox,v['y']-oy
  v['x']=x+math.cos(angle)*dx-math.sin(angle)*dy
  v['y']=y+math.sin(angle)*dx+math.cos(angle)*dy
 if v.get('angle') is not None:v['angle']=(v['angle']+da)%360
shutil.copy2(p,'/private/tmp/ruri-before-plan.epcb2')
p.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+(json.dumps(v,separators=(',',':')) if v is not None else '')+'|' for h,v,_ in rows)+'\n')
print('Placed',len(transforms),'components; absent refs:',sorted(set(plan)-set(refs.values())))
