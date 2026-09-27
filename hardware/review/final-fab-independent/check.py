import json,csv,zipfile,re,hashlib,math
from pathlib import Path
base=Path('hardware');out=base/'review/final-fab-independent'
epro=base/'eda/proposals/Ruri-Passport-Procurement-Bound.epro2';ger=base/'review/Ruri-Passport-Procurement-NFC-REVIEW-20260927.zip'
z=zipfile.ZipFile(epro);rows=[];docs={};current=None
for line in z.read(next(n for n in z.namelist() if n.endswith('.epru'))).decode().splitlines():
 try:a,b=map(json.loads,line.rstrip('|').split('||',1))
 except Exception:continue
 if a['type']=='DOCHEAD':current=b['uuid'];docs.setdefault(current,[])
 docs[current].append((a,b))
pcb=docs['8ba8b91f8fadb6191a9df22976c275b6'];attrs={};comps={}
for a,b in pcb:
 if a['type']=='ATTR':attrs.setdefault(b['parentId'],{})[b['key']]=b['value']
 if a['type']=='COMPONENT':comps[a['id']]=b
refs={attrs[k]['Designator']:(k,b) for k,b in comps.items() if 'Designator' in attrs.get(k,{})}
bom=list(csv.DictReader(open(base/'review/procurement-native-bom-20260927.csv',encoding='utf-8-sig')));cpl=list(csv.DictReader(open(base/'review/procurement-native-cpl-20260927.csv',encoding='utf-8-sig')))
br={};dup=[]
for b in bom:
 for ref in b['Designator'].split(','):
  if ref in br:dup.append(ref)
  br[ref]=b
coord=[];supplier=[]
for c in cpl:
 k,p=refs[c['Designator']];delta=max(abs(float(c['Ref X'])-p['x']*.0254),abs(float(c['Ref Y'])-p['y']*.0254))
 if delta>.0001 or float(c['Rotation'])%360!=p['angle']%360 or c['Layer']!=('T' if p['layerId']==1 else 'B'):coord.append((c['Designator'],delta))
 if c['Supplier Part']!=br[c['Designator']]['Supplier Part']:supplier.append(c['Designator'])
coil=next(b for a,b in pcb if a['type']=='POLY' and a['id']=='e14');bridge=next(b for a,b in pcb if a['type']=='FILL' and b.get('isBridgingCopper'))
p=coil['path'];xy=[p[:2]]+[p[i:i+2] for i in range(3,len(p),2)];seg=list(zip(xy,xy[1:]));rect=(3326.7717,838.5827,3342.5197,866.1418)
def rectgap(s):
 (x1,y1),(x2,y2)=s;r=coil['width']/2
 sx0,sx1=sorted([x1,x2]);sy0,sy1=sorted([y1,y2]);dx=max(rect[0]-sx1,sx0-rect[2],0);dy=max(rect[1]-sy1,sy0-rect[3],0)
 return (math.hypot(dx,dy)-r)*.0254
clearance=[rectgap(s) for s in seg]
gz=zipfile.ZipFile(ger);top=gz.read('Gerber_TopLayer.GTL').decode();ap={};tool=None;previous=None;strokes=[];region=False
for line in top.splitlines():
 m=re.fullmatch(r'%ADD(\d+)([CRO]),([\d.X]+)\*%',line)
 if m:ap[m[1]]=(m[2],[float(v) for v in m[3].split('X')])
 m=re.fullmatch(r'G54D(\d+)\*',line)
 if m:tool=m[1]
 if line=='G36*':region=True
 if line=='G37*':region=False
 m=re.search(r'X(-?\d+)Y(-?\d+).*D0([123])\*',line)
 if m:
  point=(int(m[1])/1e5,int(m[2])/1e5)
  if m[3]=='1' and previous and not region:strokes.append((previous,point,ap.get(tool)))
  previous=point
matches=[]
for s in seg:
 mm=[tuple(v*.0254 for v in pt) for pt in s]
 matches.append(any(max(abs(a[i]-mm[0][i]) for i in [0,1])<.00002 and max(abs(b[i]-mm[1][i]) for i in [0,1])<.00002 and apv and abs(apv[1][0]-.4)<.00002 for a,b,apv in strokes))
npth=gz.read('Drill_NPTH_Through.DRL').decode();pth=gz.read('Drill_PTH_Through.DRL').decode();outline=gz.read('Gerber_BoardOutlineLayer.GKO').decode()
res={'inputs':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [epro,ger]},'bom':{'groups':len(bom),'quantity':sum(int(b['Quantity']) for b in bom),'refs':len(br),'duplicates':dup,'empty_parts':[b['Designator'] for b in bom if not b['Supplier Part']]},'cpl':{'rows':len(cpl),'refset_matches_bom':set(br)=={c['Designator'] for c in cpl},'coordinate_rotation_layer_mismatches':coord,'supplier_mismatches':supplier},'coil':{'segments':len(seg),'gerber_segments_matching_source':sum(matches),'width_mm':coil['width']*.0254,'bridge_overlap_segments':[i+1 for i,c in enumerate(clearance) if c<=0],'bridge_min_nonterminal_clearance_mm':min(clearance[:-1]),'terminal_via':{'x_mm':84.7,'y_mm':22.0,'copper_diameter_mm':.6},'bridge_flag':bridge['isBridgingCopper'],'bridge_nets':bridge['networkList']},'drills':{'npth_hits':len(re.findall(r'^X',npth,re.M)),'usb_alignment_holes_present':all(s in npth for s in ['X46.89Y6.28','X41.11Y6.28','T02C0.65000']),'usb_plated_slots':re.findall(r'^X.*G85.*$',pth,re.M),'usb_slot_width_06': 'T06C0.60000' in pth},'outline':{'88x85_rectangle':all(s in outline for s in ['X0Y8500000D01','X8800000Y8500000D01','X8800000Y0D01'])}}
(out/'checks.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
