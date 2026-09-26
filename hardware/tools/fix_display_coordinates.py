"""Restore the LCD pin hotspot coordinates after native Y-axis normalization.
Idempotent; operates only on the named LCD SYMBOL, preserving other docs.
"""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'eda/Ruri-Passport-RevA/sch/Mainboard/Display.esch2'
rows=[];doc=None;custom=False
for l in p.read_text().splitlines():
 if '||' not in l or not l.removesuffix('|').split('||',1)[1]:continue
 h,b=l.removesuffix('|').split('||',1);h=json.loads(h);b=json.loads(b)
 if h['type']=='DOCHEAD':doc=b['uuid'];custom=False
 if h['type']=='META' and b.get('title')=='RURI_LCD_CL40_40PIN':custom=True
 rows.append((h,b,doc,custom))
customid=next(d for h,b,d,c in rows if c)
numbers={b['parentId']:int(b['value']) for h,b,d,c in rows if d==customid and h['type']=='ATTR' and b.get('key')=='Pin Number'}
coords={pid:(-120 if n<=20 else 120,200-20*((n-1)%20)) for pid,n in numbers.items()}
for h,b,d,c in rows:
 if d!=customid:continue
 if h['type']=='PIN':b['x'],b['y']=coords[h['id']];b['yAxisDirection']='up'
 if h['type']=='ATTR' and b.get('key') in ('Pin Name','Pin Number'):
  x,y=coords[b['parentId']];left=x<0;name=b['key']=='Pin Name'
  b.update(x=x+(15 if left else -15) if name else x,y=y if name else y+5,valueVisible=True,fontSize=7,yAxisDirection='up',align=('LEFT_MIDDLE' if left else 'RIGHT_MIDDLE') if name else ('LEFT_BOTTOM' if left else 'RIGHT_BOTTOM'))
p.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+json.dumps(b,separators=(',',':'))+'|' for h,b,d,c in rows)+'\n')
print('Restored',len(coords),'LCD pin hotspots. Native netlist re-export is REQUIRED.')
