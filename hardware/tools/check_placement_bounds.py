"""Conservative pad/body screening from native PCB libraries. NOT DRC or 3D proof."""
import json,math,itertools
from pathlib import Path
root=Path(__file__).resolve().parents[1]
docs={};cur=None
for line in (root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2').read_text().splitlines():
 h,b=line.split('||',1);h=json.loads(h);b=b.removesuffix('|');v=json.loads(b) if b else None
 if h['type']=='DOCHEAD':cur=v['uuid'];docs[cur]={'type':v['docType'],'rows':{}}
 docs[cur]['rows'][h.get('id',h['type'])]=(h,v)
pcb=next(d for d in docs.values() if d['type']=='PCB');comps={};attrs={}
for h,v in pcb['rows'].values():
 if not v:continue
 if h['type']=='COMPONENT':comps[h['id']]=v
 if h['type']=='ATTR':attrs.setdefault(v['parentId'],{})[v['key']]=v['value']
def bbox(points):return [min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)]
def gap(a,b):return math.hypot(max(a[0]-b[2],b[0]-a[2],0),max(a[1]-b[3],b[1]-a[3],0))
parts={};errors=[]
for cid,c in comps.items():
 a=attrs[cid];ref=a['Designator'];fp=docs[a['Footprint']];pads=[];bodies=[]
 ang=math.radians(c['angle']);co,si=math.cos(ang),math.sin(ang)
 def transform(x,y):return ((c['x']+co*x-si*y)*.0254,(c['y']+si*x+co*y)*.0254)
 for h,v in fp['rows'].values():
  if not v:continue
  if h['type']=='PAD':
   pad=v['defaultPad'];w,hh=pad.get('width'),pad.get('height')
   if w is None or hh is None:continue
   pa=math.radians(v['padAngle']);pc,ps=math.cos(pa),math.sin(pa)
   corners=[transform(v['centerX']+pc*dx-ps*dy,v['centerY']+ps*dx+pc*dy) for dx,dy in itertools.product([-w/2,w/2],[-hh/2,hh/2])]
   pads.append({'num':v['num'],'bbox':bbox(corners),'element':h['id']})
  if h['type']=='POLY' and v['layerId']==48:
   path=v['path'];pts=[]
   if path[0]=='R':
    _,x,y,w,hh,*_=path;pts=[(x,y),(x+w,y),(x+w,y-hh),(x,y-hh)]
   elif isinstance(path[0],(int,float)):
    nums=[q for q in path if isinstance(q,(int,float))];pts=list(zip(nums[::2],nums[1::2]))
   if pts:bodies.append(bbox([transform(x,y) for x,y in pts]))
 parts[ref]={'pads':pads,'bodies':bodies}
 for p in pads:
  b=p['bbox']
  if min(b[:2])<-.001 or b[2]>88.001 or b[3]>135.001:errors.append(f'{ref}.{p["num"]} pad outside board: {b}')
for (ra,a),(rb,b) in itertools.combinations(parts.items(),2):
 if ra=='ANT1' or rb=='ANT1':continue # coil is audited as copper/topology separately
 closest=min((gap(p['bbox'],q['bbox']) for p in a['pads'] for q in b['pads']),default=999)
 if closest<.15:errors.append(f'{ra}/{rb} conservative pad gap {closest:.3f}mm')
 if any(gap(p,q)==0 for p in a['bodies'] for q in b['bodies']):errors.append(f'{ra}/{rb} body boxes overlap')
out={'method':'orthogonal pad/body bounds; excludes antenna copper, rotations with rounded corners may over-report; no 3D/DRC claim','component_count':len(parts),'findings':errors,'geometry':parts}
(root/'review/placement-bounds-draft.json').write_text(json.dumps(out,indent=2)+'\n')
print(f'{len(parts)} components, {len(errors)} conservative placement findings')
for e in errors:print(e)
