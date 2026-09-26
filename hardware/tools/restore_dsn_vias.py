"""Restore native vias that EasyEDA exported as fixed DSN pins.

Use only on a CLOSED project. Some existing vias appear in the DSN library's
single board image as pins, rather than in wiring. SES therefore omits them.
An import that replaces old routing must retain these exact native vias.
"""
import argparse, json, re, shutil
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('dsn',type=Path)
p.add_argument('before_import',type=Path)
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
pcb=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
manifest=root/'review/autoroute-import.json'

def rows(path):
    doc=None
    for line in path.read_text().splitlines():
        h,b=line.split('||',1); h=json.loads(h)
        b=b.removesuffix('|'); v=json.loads(b) if b else None
        if h['type']=='DOCHEAD': doc=v['docType']
        yield doc,h,v

dsn=a.dsn.read_text()
assert re.search(r'\(resolution\s+mil\s+\d+\)',dsn), 'Expected native mil DSN'
assert re.findall(r'\(place\s+(\S+)\s+([-\d.]+)\s+([-\d.]+)\s+(\S+)\s+([-\d.]+)',dsn)==[('u1','0','0','front','0')], 'Expected native flattened board coordinates'
# EasyEDA's exporter also strips some 'e' characters from object IDs. Match
# coordinates as well, within its 0.01 mil rounding, and require a via stack.
fixed=set(re.findall(r'\(pin\s+\S+\s+(\S+)\s',dsn))
via_stacks=set()
for name in re.findall(r'\(padstack\s+(\S+)',dsn):
    start=dsn.index('(padstack '+name); depth=0
    for end in range(start,len(dsn)):
        if dsn[end]=='(':depth+=1
        elif dsn[end]==')':
            depth-=1
            if depth==0:break
    block=dsn[start:end+1]
    if all('(circle '+layer in block for layer in ['TopLayer','Inner1','Inner2','BottomLayer']):
        via_stacks.add(name)
fixed_xy=[(float(x),float(y)) for stack,ident,x,y in
          re.findall(r'\(pin\s+(\S+)\s+(\S+)\s+([-\d.]+)\s+([-\d.]+)\)',dsn)
          if stack in via_stacks]
def is_fixed(h,v):
    return h['id'] in fixed or any(abs(v['centerX']-x)<=.0051 and
                                   abs(v['centerY']-y)<=.0051 for x,y in fixed_xy)
old=[(h,v) for doc,h,v in rows(a.before_import)
     if doc=='PCB' and h['type']=='VIA' and v and is_fixed(h,v)]
existing={h.get('id') for doc,h,v in rows(pcb) if doc=='PCB' and v}
ticket=max(h.get('ticket',0) for doc,h,v in rows(pcb) if doc=='PCB')
added=[]; lines=pcb.read_text().splitlines()
for h,v in old:
    if h['id'] in existing: continue
    ticket+=1; h=dict(h,ticket=ticket)
    lines.append(json.dumps(h,separators=(',',':'))+'||'+json.dumps(v,separators=(',',':'))+'|')
    added.append(h['id'])
shutil.copy2(pcb,'/private/tmp/ruri-before-fixed-via-restore.epcb2')
pcb.write_text('\n'.join(lines)+'\n')
m=json.loads(manifest.read_text())
m['primitive_ids'].extend(added)
m['vias']+=len(added)
m.setdefault('restored_fixed_dsn_vias',[]).extend(added)
m['fixed_via_source']=a.before_import.name
manifest.write_text(json.dumps(m,indent=2)+'\n')
print(f'Restored {len(added)} fixed DSN vias; {len(old)-len(added)} already present.')
