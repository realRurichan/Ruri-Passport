"""Add the Rev A display draft once; requires official easyeda-eprj3-skill scripts."""
import argparse, json, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--skill',type=Path,required=True);a=p.parse_args()
S=a.skill/'scripts'; D=Path(__file__).resolve().parents[1]/'eda/Ruri-Passport-RevA'
page=D/'sch/Mainboard/Display.esch2'
if page.exists():raise SystemExit('Display sheet already exists; refusing duplicate generation')
def run(script,*args):
 subprocess.run(['node',str(S/script),*map(str,args)],check=True,capture_output=True)
def cmd(script,**kw):
 args=['--dir',str(D)]
 for k,v in kw.items():args+=['--'+k.replace('_','-'),str(v)]
 run(script,*args)
subprocess.run(['node','-e',"const E=require(process.argv[1]); const p=E.Project.load(process.argv[2]); p.ensureSheetDocument('Mainboard','Display'); p.save();",str(S/'lib/eprj3.js'),str(D)],check=True)
def sym(lib,ref,name,x,y,rot=0,fp=None):
 kw=dict(sch='Mainboard',sheet='Display',symbol=lib,refdes=ref,name=name,x=x,y=y,rotation=rot)
 if fp:kw['footprint']=fp
 cmd('add-symbol.js',**kw)
def wire(segs,net):cmd('add-wire.js',sch='Mainboard',sheet='Display',segs=';'.join(','.join(map(str,s)) for s in segs),net=net)
def label(net,x,y):cmd('add-netlabel.js',sch='Mainboard',sheet='Display',net=net,at=f'{x},{y}')
def text(t,x,y,size=10):cmd('add-text.js',sch='Mainboard',sheet='Display',value=t,x=x,y=y,size=size)
def block(t,x1,y1,x2,y2):
 run('add-shape.js','rect','--dir',D,'--sch','Mainboard','--sheet','Display','--x1',x1,'--y1',y1,'--x2',x2,'--y2',y2);text(t,x1,y1+20,12)
names=['XL','YU','XR','YD','GND','IOVCC','VCC','FMARK','CS','RS','WR','RD','SPI_SDA','SPI_SDO','RESET','GND']+[f'DB{i}' for i in range(16)]+['LEDA','LEDK','LEDK','LEDK','GND','IM0','IM1','IM2']
coords={n:(-120 if n<=20 else 120,200-20*((n-1)%20),0 if n<=20 else 180) for n in range(1,41)}
pins=';'.join(f'{n}:{names[n-1]}:{x}:{y}:{r}' for n,(x,y,r) in coords.items())
run('generate-symbol.js','from-pins','--dir',D,'--name','RURI_LCD_CL40_40PIN','--designator','J','--pins',pins)
sym('RURI_LCD_CL40_40PIN','J1','CL40BC264-40C / WITHOUT RTP',650,-450)
text('RURI PASSPORT - DISPLAY / DRAFT - NOT FOR FABRICATION',100,-45,15)
block('40-PIN FPC / 8080 8-BIT WRITE ONLY',100,-110,1150,-800)
nets={5:'GND',6:'3V18_PERIPH',7:'3V18_PERIPH',9:'LCD_CS_N',10:'LCD_DC',11:'LCD_WR_N',12:'3V18_PERIPH',13:'GND',15:'LCD_RESET_N',16:'GND',33:'LCD_LEDA',34:'LCD_LEDK',35:'LCD_LEDK',36:'LCD_LEDK',37:'GND',38:'3V18_PERIPH',39:'3V18_PERIPH',40:'GND'}
nets.update({17+i:f'LCD_D{i}' for i in range(8)})
# Visible local common ground bus for unused upper data pins.
for n in range(25,33):wire([(770,-450+coords[n][1],930,-450+coords[n][1])],'GND')
wire([(930,-330,930,-470),(930,-470,1010,-470)],'GND');label('GND',1010,-470)
for n,net in nets.items():
 x,y,r=coords[n];x+=650;y-=450;end=310 if n<=20 else 1060
 wire([(x,y,end,y)],net);label(net,end,y)
text('NC: 1-4 (no touch), 8 (TE), 14 (serial output).',130,-710)
text('IM0=1 / IM1=1 / IM2=0; DB8..15 and SPI_SDA grounded.',130,-735)
text('40 pin / 0.5 mm / 0.30 mm FPC. Connector MPN + contact side pending.',130,-760)
text('LEDA/LEDK require current-limited PWM driver; NOT a GPIO load.',130,-785)
block('LOCAL DECOUPLING / CONTROL DEFAULTS',1300,-110,1880,-800)
for ref,val,x in [('C6','100nF / 10V X7R',1390),('C7','4.7uF / 10V X5R',1670)]:
 sym('CAP',ref,val,x,-260,90,'C0603')
 wire([(x,-240,x,-200)],'3V18_PERIPH');label('3V18_PERIPH',x,-200)
 wire([(x,-280,x,-320)],'GND');sym('GND','','GND',x,-320)
sym('RES','R4','10k / 1%',1410,-490,90,'R0603')
wire([(1410,-470,1410,-430)],'3V18_PERIPH');label('3V18_PERIPH',1410,-430)
wire([(1410,-510,1410,-560),(1410,-560,1530,-560)],'LCD_CS_N');label('LCD_CS_N',1530,-560)
sym('RES','R5','10k / 1%',1680,-580,90,'R0603')
wire([(1680,-560,1680,-500),(1680,-500,1800,-500)],'LCD_RESET_N');label('LCD_RESET_N',1800,-500)
wire([(1680,-600,1680,-650)],'GND');sym('GND','','GND',1680,-650)
text('RESET held low until GPIO expander drives high.',1320,-720)
text('Check 3V18_PERIPH tolerance against LCD operating maximum.',1320,-745)
# Adapt generator coordinates to the installed native client; preserve library shapes.
rows=[];doc=None;custom=False;frame=set()
for line in page.read_text().splitlines():
 h,v=line[:-1].split('||',1);h=json.loads(h);v=json.loads(v) if v else None
 if h['type']=='DOCHEAD':doc=v['docType'];custom=False
 if h['type']=='META' and isinstance(v,dict) and v.get('title')=='RURI_LCD_CL40_40PIN':custom=True
 if doc=='SCH_PAGE' and h['type']=='COMPONENT' and v.get('DeviceName','').startswith('Drawing-Symbol'):frame.add(h['id'])
 rows.append((h,v,doc,custom))
out=[]
pin_geometry={h['id']:v for h,v,doc,custom in rows if custom and h['type']=='PIN'}
for h,v,doc,custom in rows:
 if doc=='SCH_PAGE' and (h.get('id') in frame or isinstance(v,dict) and v.get('parentId') in frame):continue
 if isinstance(v,dict):
  if (doc=='SCH_PAGE' or custom) and h['type'] in ['COMPONENT','ATTR','TEXT','WIRE','LINE','RECT','PIN']:v['yAxisDirection']='up'
  if h['type']=='COMPONENT':v.update(groupId='',locked=False)
  if custom and h['type']=='ATTR' and v.get('key') in ['Pin Name','Pin Number']:
   q=pin_geometry[v['parentId']];left=q['x']<0;name=v['key']=='Pin Name'
   v.update(valueVisible=True,fontSize=7,x=q['x']+(15 if left else -15) if name else q['x'],y=q['y'] if name else q['y']+5,align=('LEFT_MIDDLE' if left else 'RIGHT_MIDDLE') if name else ('LEFT_BOTTOM' if left else 'RIGHT_BOTTOM'))
 out.append(json.dumps(h,separators=(',',':'))+'||'+(json.dumps(v,separators=(',',':')) if v is not None else '')+'|')
page.write_text('\n'.join(out)+'\n')
run('validate.js','--dir',D)
print('Display draft added; no fabrication footprint assigned to J1.')
