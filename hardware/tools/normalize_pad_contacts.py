"""Align existing near-coincident track endpoints to fixed native pad centres.

Run with the native project closed. Does not move pads or route missing wires.
The 0.01 mil limit is 0.000254 mm; net and copper layer must both match.
Always rerun native DRC afterwards. Optional --net limits a trial to one net.
"""
import argparse, json, math, shutil
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--net')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
pcb=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
rows=[]; docs={}; current=None
for line in pcb.read_text().splitlines():
    h,b=line.split('||',1);h=json.loads(h);b=b.removesuffix('|')
    v=json.loads(b) if b else None
    if h['type']=='DOCHEAD':
        current=v['uuid'];docs[current]={'type':v['docType'],'rows':[]}
    row=[h,v,line];rows.append(row);docs[current]['rows'].append(row)
main=next(d['rows'] for d in docs.values() if d['type']=='PCB')
components={h['id']:v for h,v,_ in main if h['type']=='COMPONENT' and v}
attrs={};nets={}
for h,v,_ in main:
    if not v:continue
    if h['type']=='ATTR':attrs.setdefault(v['parentId'],{})[v['key']]=v['value']
    if h['type']=='PAD_NET':
        ident=json.loads(h['id']);nets[(ident[1],ident[3])]=v['padNet']
anchors={}
for cid,c in components.items():
    if c['layerId']!=1:raise ValueError('Bottom-side component transforms require explicit support')
    a=attrs[cid];angle=math.radians(c['angle']);co,si=math.cos(angle),math.sin(angle)
    for h,p,_ in docs[a['Footprint']]['rows']:
        if h['type']!='PAD' or not p:continue
        net=nets.get((cid,h['id']))
        if not net or (args.net and net!=args.net):continue
        x=c['x']+co*p['centerX']-si*p['centerY']
        y=c['y']+si*p['centerX']+co*p['centerY']
        for layer in ((1,2,15,16) if p['layerId']==12 else (p['layerId'],)):
            anchors.setdefault((net,layer),[]).append((x,y,a['Designator']+'_'+p['num']))
changes=[];changed=set()
for h,t,_ in main:
    if h['type']!='LINE' or not t:continue
    candidates=anchors.get((t.get('netName'),t['layerId']),[])
    for side in ('start','end'):
        before=(t[side+'X'],t[side+'Y'])
        matches=[(x,y,p) for x,y,p in candidates if math.dist(before,(x,y))<=.01]
        if not matches:continue
        target=min(matches,key=lambda p:math.dist(before,p[:2]))
        if math.dist(before,target[:2])<1e-10:continue
        t[side+'X'],t[side+'Y']=target[:2];changed.add(id(t))
        changes.append({'track':h['id'],'side':side,'net':t['netName'],'pad':target[2],
                        'before_mil':before,'after_mil':target[:2],
                        'displacement_mm':math.dist(before,target[:2])*.0254})
shutil.copy2(pcb,'/private/tmp/ruri-before-pad-normalization'+('-'+args.net if args.net else '')+'.epcb2')
pcb.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+json.dumps(v,separators=(',',':'))+'|'
                         if id(v) in changed else line for h,v,line in rows)+'\n')
report={'status':'Native DRC required','tolerance_mil':.01,'net_filter':args.net,'changes':changes}
(root/'review'/('pad-contact-normalization'+('-'+args.net if args.net else '')+'.json')).write_text(json.dumps(report,indent=2)+'\n')
print(f'Aligned {len(changes)} endpoints to fixed pads.')
