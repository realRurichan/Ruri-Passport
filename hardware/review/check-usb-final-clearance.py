import zipfile,re,math,json
from pathlib import Path
import argparse
ap=argparse.ArgumentParser();ap.add_argument('gerber');ap.add_argument('--report',required=True);args=ap.parse_args()
z=zipfile.ZipFile(args.gerber)
def segdist(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];q=dx*dx+dy*dy;t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/q))if q else 0
 return math.dist(p,(a[0]+t*dx,a[1]+t*dy))
def inside(p,poly):
 x,y=p;odd=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:odd=not odd
 return odd
res=[]
for name in ['Gerber_TopLayer.GTL','Gerber_InnerLayer1.G1','Gerber_InnerLayer2.G2','Gerber_BottomLayer.GBL']:
 aps={};ap=None;cur=None;reg=None;contour=None;objects=[];unhandled=[]
 for l in z.read(name).decode().splitlines():
  m=re.fullmatch(r'%ADD(\d+)([CRO]),([\d.X]+)\*%',l)
  if m:aps[m[1]]=(m[2],list(map(float,m[3].split('X'))))
  m=re.fullmatch(r'G54D(\d+)\*',l)
  if m:ap=m[1]
  if l=='G36*':reg=[];contour=None
  if l=='G37*':objects.append(('region',reg));reg=None
  m=re.search(r'X(-?\d+)Y(-?\d+)(.*?)D0([123])\*',l)
  if not m:continue
  pt=(int(m[1])/1e5,int(m[2])/1e5);action=m[4];pts=[pt]
  if l.startswith(('G02','G03')) and cur:
   ij=re.search(r'I(-?\d+)J(-?\d+)',m[3]);assert ij,l
   cx,cy=cur[0]+int(ij[1])/1e5,cur[1]+int(ij[2])/1e5;r=math.dist(cur,(cx,cy));a=math.atan2(cur[1]-cy,cur[0]-cx);b=math.atan2(pt[1]-cy,pt[0]-cx);sweep=(b-a)%(2*math.pi)
   if l.startswith('G02'):sweep=-((a-b)%(2*math.pi))
   n=max(1,math.ceil(abs(sweep)/math.radians(.5)));pts=[(cx+r*math.cos(a+sweep*k/n),cy+r*math.sin(a+sweep*k/n))for k in range(1,n+1)]
  if reg is not None:
   if action=='2':contour=[pt];reg.append(contour)
   elif action=='1':contour.extend(pts)
  elif action=='3':
   if ap in aps:objects.append(('flash',pt,aps[ap]))
   else:unhandled.append((ap,pt))
  elif action=='1' and cur:
   if ap in aps:
    last=cur
    for v in pts:objects.append(('stroke',last,v,aps[ap]));last=v
   else:unhandled.append((ap,pt))
  cur=pt
 for hx in [41.11,46.89]:
  p=(hx,6.28);nearest=(1000,None,None)
  for o in objects:
   if o[0]=='region':
    distance=0 if sum(inside(p,c)for c in o[1])%2 else min((segdist(p,a,b)for c in o[1]for a,b in zip(c,c[1:]+c[:1])),default=1000)
   elif o[0]=='stroke':distance=segdist(p,o[1],o[2])-max(o[3][1])/2
   else:
    xy,(typ,dims)=o[1:];dx,dy=abs(p[0]-xy[0]),abs(p[1]-xy[1])
    if typ=='C':distance=math.hypot(dx,dy)-dims[0]/2
    elif typ=='R':distance=math.hypot(max(dx-dims[0]/2,0),max(dy-dims[1]/2,0))
    else:
     w,h=dims;distance=(math.hypot(dx,max(dy-(h-w)/2,0))-w/2)if h>=w else(math.hypot(max(dx-(w-h)/2,0),dy)-h/2)
   if distance<nearest[0]:nearest=(distance,o[0],o)
  nearby_unknown=[x for x in unhandled if math.dist(p,x[1])<2];assert not nearby_unknown,nearby_unknown
  clearance=nearest[0]-.325;res.append({'layer':name,'hole_x_mm':hx,'nominal_copper_clearance_mm':clearance,'nearest_kind':nearest[1],'nearest_geometry':nearest[2] if nearest[1]!='region' else 'region'});assert clearance>=.199, res[-1]
print(json.dumps(res,indent=2));Path(args.report).write_text(json.dumps({'method':'Native final Gerber parsed independently: aperture flashes, strokes, regions and multi-contour even-odd fill; circular arcs subdivided at <=0.5degree. All four copper layers and both USB NPTH checked. Nominal dimensions; fabrication tolerances remain applicable.','results':res},indent=2))
