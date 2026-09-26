"""Place a draft FH12A footprint from Hirose catalog pp.6/10; not fab released."""
import argparse,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--skill',required=True,type=Path);a=p.parse_args()
S=a.skill/'scripts';D=Path(__file__).resolve().parents[1]/'eda/Ruri-Passport-RevA'
if 'RURI_FH12A40_TOP_DRAFT' in (D/'pcb/Mainboard.epcb2').read_text():
 raise SystemExit('J1 candidate already exists; refusing duplicate placement')
def run(name,*args):subprocess.run(['node',str(S/name),*map(str,args)],check=True,capture_output=True)
mm=lambda v:round(v/0.0254,6)
name='RURI_FH12A40_TOP_DRAFT'
# Origin: centre of signal-pad row; positive Y toward mouth; pin1 on right.
pads=[f'{n}:{mm(9.75-(n-1)*.5)}:0:{mm(.3)}:{mm(1.3)}' for n in range(1,41)]
pads += [f'MP{i}:{mm(x)}:{mm(3.25)}:{mm(1.8)}:{mm(2.2)}' for i,x in enumerate([-11.65,11.65],1)]
run('generate-footprint.js','from-pads','--dir',D,'--name',name,'--pads',';'.join(pads),'--outline',f'R,{mm(-12.55)},{mm(-.65)},{mm(25.1)},{mm(6.5)}')
nets={5:'GND',6:'3V3',7:'3V3',9:'LCD_CS_N',10:'LCD_DC',11:'LCD_WR_N',12:'3V3',13:'GND',15:'LCD_RESET_N',16:'GND',33:'LCD_LEDA',34:'LCD_LEDK',35:'LCD_LEDK',36:'LCD_LEDK',37:'GND',38:'3V3',39:'3V3',40:'GND'}
nets.update({17+i:f'LCD_D{i}' for i in range(8)});nets.update({i:'GND' for i in range(25,33)})
run('add-footprint.js','--dir',D,'--pcb','Mainboard','--symbol','RURI_LCD_CL40_40PIN','--footprint',name,'--x',mm(49),'--y',mm(48),'--refdes','J1','--name','FH12A-40S-0.5SH(55) CANDIDATE','--nets',','.join(f'{n}:{v}' for n,v in nets.items()))
run('add-pcb-text.js','--dir',D,'--pcb','Mainboard','--value','J1 TOP CONTACT / PIN ORDER + ASSEMBLY CHECK REQUIRED','--x',mm(25),'--y',mm(44),'--layer','13','--size','30')
run('validate.js','--dir',D)
print('J1 candidate: 40 signal + 2 mechanical pads; unrouted, assembly check required.')
