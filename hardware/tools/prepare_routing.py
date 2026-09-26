"""Patch native DSN with holes, antenna reservations and short escape seeds.

The native export omits REGION and multilayer FILL cutouts. Coordinates below
are taken from native geometry, including transformed library NPTH circles.
"""
import argparse, json, math, re, subprocess, sys
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('input',type=Path); p.add_argument('output',type=Path)
p.add_argument('--routing-tools',type=Path,required=True)
p.add_argument('--fresh-wiring',action='store_true')
a=p.parse_args(); root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(a.routing_tools/'dsn_rewrite.py'),str(a.input),
    str(a.output),'--config',str(root/'design/routing-draft.json'),'--min-classes','100'],check=True)
s=a.output.read_text()
if a.fresh_wiring:
    start=s.index('  (wiring'); level=0; end=None
    for i in range(start+2,len(s)):
        if s[i]=='(':level+=1
        elif s[i]==')':
            level-=1
            if level==0:end=i+1;break
    assert end is not None
    # Only the original coil-terminal via survives from existing routing.
    s=s[:start]+'  (wiring\n    (via via1 3334.64567 866.14173 (net ANT_B) (type protect))\n  )'+s[end:]
# FreeRouting 1.9 requires layers to be defined before keepouts referencing them.
layers=re.findall(r'    \(layer \S+\s+\(type (?:signal|power)\)\s*\)',s)
assert len(layers)==4
for layer in layers:s=s.replace(layer,'',1)
s=s.replace('  (structure\n','  (structure\n'+'\n'.join(layers)+'\n',1)
docs={}; doc=None
for line in (root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2').read_text().splitlines():
    h,b=line.split('||',1); h=json.loads(h); v=json.loads(b.removesuffix('|')) if b.removesuffix('|') else None
    if h['type']=='DOCHEAD': doc=v['uuid']; docs[doc]={'type':v['docType'],'rows':[]}
    docs[doc]['rows'].append((h,v))
pcb=next(d['rows'] for d in docs.values() if d['type']=='PCB')
layer_names={1:'TopLayer',15:'Inner1',16:'Inner2',2:'BottomLayer'}
obstacles=[]
for h,v in pcb:
    if h['type']!='REGION' or not v.get('name','').startswith(('RURI_ANT_','RURI_MOUNT_')):continue
    layer=layer_names[v['layerId']]
    for path in v['path']:
        if path[0]=='R':
            _,x,y,w,hh,*_=path
            shape=f'(rect {layer} {x:.5f} {y-hh:.5f} {x+w:.5f} {y:.5f})'
        elif path[0]=='CIRCLE':
            _,x,y,r,*_=path
            shape=f'(circle {layer} {2*r:.5f} {x:.5f} {y:.5f})'
        else:raise ValueError(path)
        obstacles.append(f'    (keepout "" {shape})')
attrs={}
for h,v in pcb:
    if h['type']=='ATTR' and v:attrs.setdefault(v['parentId'],{})[v['key']]=v['value']
# Expand NPTH obstacles by 0.15 mm: added to router 0.16 gives >=0.30 mm
# hole-to-track clearance. Mounting holes already have larger screw reservations.
for h,c in pcb:
    if h['type']!='COMPONENT' or not c:continue
    fp=docs[attrs[h['id']]['Footprint']]['rows']
    ang=math.radians(c['angle']); co,si=math.cos(ang),math.sin(ang)
    for fh,f in fp:
        if fh['type']!='FILL' or not f or f['layerId']!=12:continue
        path=f['path']
        if path[0]=='CIRCLE':
            _,x,y,r,*_=path
        elif len(path)==10 and path[2]==path[6]=='ARC' and all(abs(abs(path[i])-180)<.001 for i in (3,7)) and path[:2]==path[8:]:
            x=(path[0]+path[4])/2; y=(path[1]+path[5])/2
            r=math.hypot(path[4]-path[0],path[5]-path[1])/2
        else:raise ValueError(('Unsupported NPTH',path))
        gx=c['x']+co*x-si*y; gy=c['y']+si*x+co*y
        for layer in layer_names.values():
            obstacles.append(f'    (keepout "" (circle {layer} {2*(r+.15/.0254):.5f} {gx:.5f} {gy:.5f}))')
# Insert immediately after layer declarations, before the first boundary.
s=s.replace('    (boundary', '\n'.join(obstacles)+'\n    (boundary',1)
seed=json.loads((root/'design/critical-routing.json').read_text()); wiring=[]
# 0.50/0.30 mm fanout vias stay within the native board's existing via rules.
assert '(padstack viaSmall' not in s
s=s.replace('  (library\n','  (library\n    (padstack viaSmall\n'+
    '\n'.join(f'      (shape (circle {layer} {.5/.0254:.5f}))' for layer in layer_names.values())+'\n    )\n',1)
s=s.replace('(via via0 via1','(via via0 via1 viaSmall',1)
for path in seed['paths']:
    coords=' '.join(f'{q/.0254:.5f}' for pt in path['points'] for q in pt)
    wiring.append(f'    (wire (path {path["layer"]} {path["width"]/.0254:.5f} {coords}) (net {path["net"]}) (type protect))')
for via in seed['vias']:
    wiring.append(f'    (via {via.get("padstack","via0")} {via["x"]/.0254:.5f} {via["y"]/.0254:.5f} (net {via["net"]}) (type protect))')
assert s.count('(wiring')==1
s=s.replace('  (wiring\n','  (wiring\n'+'\n'.join(wiring)+'\n',1)
a.output.write_text(s)
print(f'Added {len(obstacles)} hole/antenna/mounting obstacles and {len(wiring)} seed paths/vias.')
