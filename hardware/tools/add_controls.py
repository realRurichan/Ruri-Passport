"""Create the controls sheet. Pin numbers follow TI TCA9535 PW datasheet."""
import argparse
from schematic_sheet import Sheet
p=argparse.ArgumentParser();p.add_argument('--skill',required=True);a=p.parse_args()
s=Sheet(a.skill,'Controls')
names=['INT_N','A1','A2','P00','P01','P02','P03','P04','P05','P06','P07','GND','P10','P11','P12','P13','P14','P15','P16','P17','A0','SCL','SDA','VCC']
coords={n:(-130 if n<=12 else 130,220-40*((n-1)%12),0 if n<=12 else 180) for n in range(1,25)}
s.symbol('RURI_TCA9535_PW',[(n,names[n-1],*coords[n]) for n in range(1,25)])
s.place('RURI_TCA9535_PW','U2','TCA9535PWR / TSSOP24',550,-400)
s.text('RURI PASSPORT - CONTROLS / SCHEMATIC DRAFT',100,-45,15)
s.block('I2C GPIO EXPANDER / ADDRESS 0x20',100,-110,1020,-850)
nets={1:'IOX_IRQ_N',2:'GND',3:'GND',4:'KEY_UP_N',5:'KEY_DOWN_N',6:'KEY_LEFT_N',7:'KEY_RIGHT_N',8:'KEY_OK_N',9:'SD_DETECT_N',10:'PWR_INT_N',11:'CHG_STATUS_N',12:'GND',13:'LCD_RESET_N',14:'NFC_VEN',15:'AMP_ENABLE',16:'USB_PGOOD_N',17:'CHG_EN1',18:'CHG_EN2',19:'PERIPH_ENABLE',20:'REG_PWM',21:'GND',22:'I2C_SCL',23:'I2C_SDA',24:'3V18'}
for n,net in nets.items():
 x,y,_=coords[n];s.stub(net,550+x,-400+y,240 if n<=12 else 910)
s.text('Power-on: all ports INPUT. External bias is required.',140,-730)
s.text('Write output latch BEFORE configuring output direction.',140,-755)
s.text('P10..12 start LOW: display reset, NFC off, amplifier off.',140,-780)
s.text('No physical footprint assigned to U2 or switches yet.',140,-805)
s.block('BUS PULLUPS / LOCAL DECOUPLING',1100,-110,2070,-400)
for ref,val,x,net in [('R6','4.7k',1200,'I2C_SDA'),('R7','4.7k',1450,'I2C_SCL'),('R8','10k',1700,'IOX_IRQ_N')]:s.passive('RES',ref,val,x,-250,'3V18',net)
s.passive('CAP','C8','100nF / 10V X7R',1950,-250,'3V18','GND')
s.block('CONTROL DEFAULTS / UNUSED INPUT BIAS',1100,-470,2520,-850)
for i,net in enumerate(['NFC_VEN','AMP_ENABLE','CHG_EN1','CHG_EN2','PERIPH_ENABLE','REG_PWM']):
 s.passive('RES',f'R{9+i}','100k',1200+i*240,-620,net,'GND')
s.text('LCD_RESET_N pulldown R5 is on Display sheet.',1140,-760)
s.text('SD / power / charge / USB sense bias belongs at the source circuit.',1140,-790)
s.block('FIVE FRONT KEYS / ACTIVE LOW / FIRMWARE DEBOUNCE',100,-970,2520,-1430)
s.symbol('RURI_SW_NO',[(1,'A',-30,0,0),(2,'B',30,0,180)],'SW')
for i,net in enumerate(['KEY_UP_N','KEY_DOWN_N','KEY_LEFT_N','KEY_RIGHT_N','KEY_OK_N']):
 x=250+i*470
 s.place('RES',f'R{15+i}','10k',x,-1110,90,'R0603')
 s.wire('3V18',(x,-1090,x,-1040));s.label('3V18',x,-1040)
 s.wire(net,(x,-1130,x,-1210),(x,-1210,x+100,-1210))
 s.label(net,x,-1170)
 # Separate RC capacitors suppressed: clean contact input, 20 ms software debounce.
 s.place('RURI_SW_NO',f'SW{i+1}',net.removeprefix('KEY_').removesuffix('_N')+' / N.O.',x+130,-1210)
 s.wire('GND',(x+160,-1210,x+200,-1210));s.label('GND',x+200,-1210)
s.text('SW1 UP / SW2 DOWN / SW3 LEFT / SW4 RIGHT / SW5 OK. Side POWER is independent.',140,-1360)
s.finish()
