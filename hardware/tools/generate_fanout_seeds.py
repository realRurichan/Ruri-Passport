"""Derive short pad escapes from native placement geometry and pin net mapping."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'design/critical-routing.json';s=json.loads(p.read_text())
g=json.loads((root/'review/placement-bounds-draft.json').read_text())['geometry']
pm=json.loads((root/'review/pcb-native-pinmap.json').read_text())
refid={v:k for k,v in pm['refs'].items()}
for q in s['paths']:
    if q['net']=='ANT_B':q['points']=[[x,35.55 if y==35.7 else y] for x,y in q['points']]
for v in s['vias']:
    if v['net']=='ANT_B' and v['y']==35.7:v['y']=35.55
s['paths']=[q for q in s['paths'] if q['net'].startswith(('ANT_','VREG_'))]
s['vias']=[v for v in s['vias'] if v['net'].startswith('ANT_')]
def seed(ref,num,target,width=.18,small=True):
    net=pm['pads'][refid[ref]][str(num)]
    if not net:return
    pad=next(p for p in g[ref]['pads'] if p['num']==str(num));b=pad['bbox']
    a=[(b[0]+b[2])/2,(b[1]+b[3])/2]
    s['paths'].append({'net':net,'layer':'TopLayer','width':width,'points':[a,target]})
    s['vias'].append({'net':net,'x':target[0],'y':target[1],'padstack':'viaSmall' if small else 'via0'})
for num in list(range(1,15))+list(range(27,41)):
    pad=next(p for p in g['U1']['pads'] if p['num']==str(num));b=pad['bbox'];y=(b[1]+b[3])/2
    seed('U1',num,[19.4 if num<15 else 6.6,y],.35 if num in (1,2,40) else .2,False)
for num in range(14,20):
    pad=next(p for p in g['U8']['pads'] if p['num']==str(num));b=pad['bbox'];y=(b[1]+b[3])/2
    seed('U8',num,[68.95 if num%2==0 else 69.65,y])
for num,target in [(1,[62.75,30.7]),(3,[63.75,30.7]),(4,[64.25,30.05]),
                   (6,[65.25,30.7]),(9,[66.75,30.7]),(22,[66.7501,39.1]),(28,[63.7501,39.1])]:
    seed('U8',num,target)
seed('U7',9,[16.7499,110.85]);seed('U7',10,[16.2501,110.15])
for x in [13.1001,14.5001,15.9002]:
    for y in [13.8201,15.2201,16.6202]:s['vias'].append({'net':'GND','x':x,'y':y})
for x,y in [(16,108),(64.5,34.5),(65.5,34.5),(64.5,35.5),(65.5,35.5)]:
    s['vias'].append({'net':'GND','x':x,'y':y})
p.write_text(json.dumps(s,indent=2)+'\n')
print(len(s['paths']),'seed paths',len(s['vias']),'vias')
