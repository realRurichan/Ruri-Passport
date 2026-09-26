"""Supplementary pin-to-wire audit of an EasyEDA .epro export.
Checks package pin numbers against the manufacturer-reviewed expectations in
check_native_netlist.py. Does not replace a native netlist/ERC/PCB DRC: wire
junction traversal and cross-sheet unnamed nets are intentionally unsupported.
"""
import argparse,json,math,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('--report');a=p.parse_args()
s=Path(__file__).with_name('check_native_netlist.py').read_text();scope={}
exec(s[s.index('expect={}'):s.index('errors=[];count=0')],{},scope)
expected=scope['expect'];errors=[];checks=[];unconnected=[];seen=set()
def segment(p,a,b):
 return abs((p[0]-a[0])*(b[1]-a[1])-(p[1]-a[1])*(b[0]-a[0]))<1e-6 and min(a[0],b[0])-1e-6<=p[0]<=max(a[0],b[0])+1e-6 and min(a[1],b[1])-1e-6<=p[1]<=max(a[1],b[1])+1e-6
with zipfile.ZipFile(a.archive) as z:
 if z.testzip():raise ValueError('ZIP CRC failed')
 def rows(path):return [json.loads(l) for l in z.read(path).decode().splitlines() if l.strip()]
 for fn in z.namelist():
  if not fn.startswith('SHEET/') or not fn.endswith('.esch'):continue
  r=rows(fn);attrs={(v[2],v[3]):v[4] for v in r if v[0]=='ATTR'};wires=[v for v in r if v[0]=='WIRE']
  for c in [v for v in r if v[0]=='COMPONENT']:
   ref=attrs.get((c[1],'Designator'))
   if not ref:continue
   if ref in seen:errors.append(f'{ref}: duplicate designator')
   seen.add(ref)
   if c[6]!=0:errors.append(f'{ref}: unsupported mirror; requires manual review');continue
   sym=attrs.get((c[1],'Symbol'));sy=rows('SYMBOL/'+sym+'.esym');sa={(v[2],v[3]):v[4] for v in sy if v[0]=='ATTR'}
   actual={};ang=math.radians(c[5]);co=math.cos(ang);si=math.sin(ang)
   for pin in [v for v in sy if v[0]=='PIN']:
    num=str(sa.get((pin[1],'NUMBER')));name=sa.get((pin[1],'NAME'));x,y=pin[4:6];xy=(c[3]+x*co-y*si,c[4]+x*si+y*co);nets=set()
    for w in wires:
     for line in w[2]:
      for j in range(0,len(line)-2,2):
       if segment(xy,line[j:j+2],line[j+2:j+4]):nets.add(attrs.get((w[1],'NET'),'<unnamed>'))
    if len(nets)>1:errors.append(f'{ref}.{num}: conflicting nets {sorted(nets)}')
    net=next(iter(nets)) if len(nets)==1 else '';actual[num]=net
    if not nets:unconnected.append({'ref':ref,'pin':num,'name':name})
   if ref in expected:
    for pn,net in expected[ref].items():
     got=actual.get(str(pn),'<missing pin>');checks.append({'ref':ref,'pin':str(pn),'expected':net,'actual':got})
     if got!=net:errors.append(f'{ref}.{pn}: expected {net!r}, got {got!r}')
 for ref in expected.keys()-seen:errors.append(ref+': missing')
report={'status':'supplementary geometry check only; NOT fabrication release','archive':str(Path(a.archive).resolve()),'component_count':len(seen),'checked_pin_count':len(checks),'errors':errors,'unconnected_pins':unconnected,'checks':checks}
if a.report:Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f'{len(seen)} components, {len(checks)} checked pins, {len(errors)} errors, {len(unconnected)} unconnected pins')
for e in errors:print(e)
raise SystemExit(bool(errors))
