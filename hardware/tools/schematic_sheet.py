"""Small wrapper for the official EasyEDA generator, with native-client fixes."""
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'eda/Ruri-Passport-RevA'
class Sheet:
 def __init__(self,skill,name):
  self.s=Path(skill)/'scripts';self.name=name;self.custom=set()
  self.path=ROOT/'sch/Mainboard'/f'{name}.esch2'
  if self.path.exists():raise SystemExit(f'{name} exists; refusing overwrite')
  subprocess.run(['node','-e',"const E=require(process.argv[1]);const p=E.Project.load(process.argv[2]);p.ensureSheetDocument('Mainboard',process.argv[3]);p.save()",str(self.s/'lib/eprj3.js'),str(ROOT),name],check=True,capture_output=True)
 def run(self,script,*args,**kw):
  argv=['node',str(self.s/script),*map(str,args),'--dir',str(ROOT)]
  for k,v in kw.items():argv+=['--'+k.replace('_','-'),str(v)]
  r=subprocess.run(argv,text=True,capture_output=True)
  if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 def page(self,script,**kw):self.run(script,sch='Mainboard',sheet=self.name,**kw)
 def symbol(self,name,pins,prefix='U'):
  self.custom.add(name)
  self.run('generate-symbol.js','from-pins',name=name,designator=prefix,pins=';'.join(':'.join(map(str,p)) for p in pins))
 def place(self,lib,ref,value,x,y,rotation=0,footprint=None):
  kw=dict(symbol=lib,refdes=ref,name=value,x=x,y=y,rotation=rotation)
  if footprint:kw['footprint']=footprint
  self.page('add-symbol.js',**kw)
 def wire(self,net,*segments):self.page('add-wire.js',net=net,segs=';'.join(','.join(map(str,s)) for s in segments))
 def label(self,net,x,y):self.page('add-netlabel.js',net=net,at=f'{x},{y}')
 def stub(self,net,x,y,end):self.wire(net,(x,y,end,y));self.label(net,end,y)
 def text(self,value,x,y,size=10):self.page('add-text.js',value=value,x=x,y=y,size=size)
 def block(self,title,x1,y1,x2,y2):
  self.run('add-shape.js','rect',sch='Mainboard',sheet=self.name,x1=x1,y1=y1,x2=x2,y2=y2);self.text(title,x1,y1+20,12)
 def passive(self,kind,ref,value,x,y,upper,lower):
  self.place(kind,ref,value,x,y,90,'R0603' if kind=='RES' else 'C0603')
  self.wire(upper,(x,y+20,x,y+60));self.label(upper,x,y+60)
  self.wire(lower,(x,y-20,x,y-60));self.label(lower,x,y-60)
 def ic(self,name,ref,mpn,fp,pins,nets,x,y):
  half=(len(pins)+1)//2
  coords={pin:(-120 if i<half else 120,40*(half-1)/2-40*(i%half),0 if i<half else 180) for i,(pin,label) in enumerate(pins)}
  self.symbol(name,[(pin,label,*coords[pin]) for pin,label in pins],ref.rstrip('0123456789'))
  self.place(name,ref,mpn,x,y,footprint=fp)
  for pin,net in nets.items():
   px,py,_=coords[pin];self.stub(net,x+px,y+py,x+(-280 if px<0 else 280))
  return coords
 def finish(self):
  rows=[];doc=None;uid=None;custom=False;frames=set();pins={}
  for line in self.path.read_text().splitlines():
   h,v=line[:-1].split('||',1);h=json.loads(h);v=json.loads(v) if v else None
   if h['type']=='DOCHEAD':doc=v['docType'];uid=v['uuid'];custom=False
   if h['type']=='META' and isinstance(v,dict):custom=v.get('title') in self.custom
   if custom and h['type']=='PIN':pins[(uid,h['id'])]=v
   if doc=='SCH_PAGE' and h['type']=='COMPONENT' and isinstance(v,dict) and 'Drawing-Symbol' in str(v.get('attrs',{}).get('DeviceName','')):frames.add(h['id'])
   if doc=='SCH_PAGE' and h['type']=='ATTR' and isinstance(v,dict) and v.get('key')=='DeviceName' and 'Drawing-Symbol' in str(v.get('value','')):frames.add(v['parentId'])
   rows.append((h,v,doc,uid,custom))
  out=[]
  for h,v,doc,uid,custom in rows:
   if doc=='SCH_PAGE' and (h.get('id') in frames or isinstance(v,dict) and v.get('parentId') in frames):continue
   if isinstance(v,dict):
    if (doc=='SCH_PAGE' or custom) and h['type'] in ['COMPONENT','ATTR','TEXT','WIRE','LINE','RECT','PIN']:v['yAxisDirection']='up'
    if h['type']=='COMPONENT':v.update(groupId='',locked=False)
    if custom and h['type']=='ATTR' and v.get('key') in ['Pin Name','Pin Number']:
     p=pins[(uid,v['parentId'])];left=p['x']<0;name=v['key']=='Pin Name'
     v.update(valueVisible=True,fontSize=7,x=p['x']+(15 if left else -15) if name else p['x'],y=p['y'] if name else p['y']+5,align=('LEFT_MIDDLE' if left else 'RIGHT_MIDDLE') if name else ('LEFT_BOTTOM' if left else 'RIGHT_BOTTOM'))
   out.append(json.dumps(h,separators=(',',':'))+'||'+(json.dumps(v,separators=(',',':')) if v is not None else '')+'|')
  self.path.write_text('\n'.join(out)+'\n')
  self.run('validate.js')
