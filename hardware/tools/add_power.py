"""Draw USB, power path, buck/boost and soft-off side power button and switched peripheral rail.
Requires staged manufacturer/library footprints (see Power design notes).
"""
import argparse
from schematic_sheet import Sheet
p=argparse.ArgumentParser();p.add_argument('--skill',required=True);a=p.parse_args()
s=Sheet(a.skill,'Power')
def ic(name,ref,mpn,fp,pins,nets,x,y):
 n=len(pins);half=(n+1)//2
 coords={pin:(-120 if i<half else 120,40*(half-1)/2-40*(i%half),0 if i<half else 180) for i,(pin,label) in enumerate(pins)}
 s.symbol(name,[(pin,label,*coords[pin]) for pin,label in pins],ref.rstrip('0123456789'))
 s.place(name,ref,mpn,x,y,footprint=fp)
 for pin,net in nets.items():
  px,py,_=coords[pin];s.stub(net,x+px,y+py,x+(-280 if px<0 else 280))
 return coords
s.text('RURI PASSPORT - POWER / ENGINEERING DRAFT',100,-50,16)
s.block('USB-C USB2 DEVICE / NO PD',100,-130,1120,-800)
u=[('A1','GND'),('A4','VBUS'),('A5','CC1'),('A6','D+'),('A7','D-'),('A8','SBU1'),('A9','VBUS'),('A12','GND'),('B1','GND'),('B4','VBUS'),('B5','CC2'),('B6','D+'),('B7','D-'),('B8','SBU2'),('B9','VBUS'),('B12','GND'),('1','SHIELD'),('2','SHIELD'),('3','SHIELD'),('4','SHIELD')]
u_net={n:('GND' if label in ('GND','SHIELD') else 'VBUS_5V' if label=='VBUS' else 'USB_DP_CONN' if label=='D+' else 'USB_DM_CONN' if label=='D-' else 'USB_'+label) for n,label in u if label not in ('SBU1','SBU2')}
ic('RURI_USB4105','J2','USB4105-GF-A','USB4105',u,u_net,510,-420)
s.passive('RES','R20','5.1k 1%',920,-330,'USB_CC1','GND');s.passive('RES','R21','5.1k 1%',920,-570,'USB_CC2','GND')
s.text('A8/B8 SBU unconnected. Shield lands grounded.',130,-710)
s.text('ESD and input protection must be added before release.',130,-740)
s.block('SINGLE-CELL CHARGER / LOAD SHARING',1200,-130,2370,-800)
bq=['TS','BAT','BAT','CE_N','EN2','EN1','PGOOD_N','VSS','CHG_N','OUT','OUT','ILIM','IN','TMR','ITERM','ISET','EP']
bqn={1:'BAT_NTC',2:'VBAT',3:'VBAT',4:'GND',5:'CHG_EN2',6:'CHG_EN1',7:'USB_PGOOD_N',8:'GND',9:'CHG_STATUS_N',10:'VSYS',11:'VSYS',12:'CHG_ILIM',13:'VBUS_5V',16:'CHG_ISET',17:'GND'}
ic('RURI_BQ24074','U3','BQ24074RGTR','BQ24074_RGT',list(enumerate(bq,1)),bqn,1660,-400)
s.passive('RES','R22','1.78k 1% / 500mA',2110,-300,'CHG_ISET','GND')
s.passive('RES','R23','3.48k 1%',2110,-580,'CHG_ILIM','GND')
s.text('TMR floating: default timers. ITERM floating: 10% termination.',1240,-720)
s.text('EN1/EN2 default LOW: 100mA. Firmware must manage USB limits.',1240,-750)
s.block('CAPACITORS / STATUS / PROTECTED PACK WITH NTC',100,-910,2370,-1420)
for ref,val,x,net in [('C9','1uF / 16V X7R',230,'VBUS_5V'),('C10','10uF / 10V X5R',520,'VBAT'),('C11','10uF / 10V X5R',810,'VSYS')]:s.passive('CAP',ref,val,x,-1090,net,'GND')
s.passive('RES','R24','100k',1100,-1090,'3V18','CHG_STATUS_N');s.passive('RES','R25','100k',1390,-1090,'3V18','USB_PGOOD_N')
ic('RURI_BAT_PH3','J3','B3B-PH-SM4-TB(LF)(SN)','JSTPH3',[(1,'BAT+'),(2,'NTC'),(3,'BAT-'),(4,'MP'),(5,'MP')],{1:'VBAT',2:'BAT_NTC',3:'GND',4:'GND',5:'GND'},1990,-1110)
s.text('Battery: protected 1S 4.2V Li-ion, approx 2000mAh; pack wiring MUST match J3.',140,-1300)
s.text('NTC: 10k 103AT-2 attached to cell. No fixed-resistor temperature bypass.',140,-1330)
s.text('J3 1=BAT+, 2=NTC, 3=BAT-. 4/5 retention pads -> GND.',140,-1360)
s.block('3.18V ALWAYS-ON REGULATOR / PFM IN STANDBY',100,-1540,2370,-2220)
tps=['EN','MODE','AGND','FB','PG','VOUT','L2','PGND','L1','VIN']
tpsn={1:'VSYS',2:'REG_PWM',3:'GND',4:'VREG_FB',5:'VREG_PG',6:'3V18',7:'VREG_L2',8:'GND',9:'VREG_L1',10:'VSYS'}
ic('RURI_TPS63802','U4','TPS63802DLAR','TPS63802_DLA',list(enumerate(tps,1)),tpsn,600,-1830)
s.symbol('RURI_INDUCTOR',[(1,'L1',-30,0,0),(2,'L2',30,0,180)],'L')
s.place('RURI_INDUCTOR','L1','XFL4015-471MEC / 0.47uH',1130,-1720,footprint='XFL4015');s.stub('VREG_L1',1100,-1720,980);s.stub('VREG_L2',1160,-1720,1280)
s.passive('RES','R26','53.6k 0.1%',1510,-1740,'3V18','VREG_FB');s.passive('RES','R27','10k 0.1%',1510,-1980,'VREG_FB','GND')
s.passive('CAP','C12','10uF / 10V X5R',1110,-1980,'VSYS','GND')
s.passive('CAP','C13','22uF / 10V X5R',1800,-1740,'3V18','GND');s.passive('CAP','C14','22uF / 10V X5R',2090,-1740,'3V18','GND')
s.passive('RES','R28','100k',1800,-1980,'3V18','VREG_PG')
s.text('MODE low: PFM; IOX P17 high selects PWM while active. Vout=0.5*(1+53.6k/10k)=3.18V.',140,-2110)
s.text('LCD operating max 3.3V; verify ripple and Wi-Fi load transients on prototype.',140,-2140)
s.text('Minimum effective output capacitance 7uF; confirm capacitor DC-bias data.',140,-2170)
s.block('SOFT-OFF / RTC WAKE / SWITCHED PERIPHERALS',100,-2340,2370,-3060)
s.symbol('RURI_SIDE_SW',[(1,'A',-30,0,0),(2,'B',30,0,180)],'SW')
s.place('RURI_SIDE_SW','SW6','B3U-3000P / SIDE POWER',420,-2500,footprint='B3U3000');s.stub('PWR_INT_N',390,-2500,250);s.stub('GND',450,-2500,570)
s.passive('RES','R31','100k',800,-2500,'3V18','PWR_INT_N')
ic('RURI_TPS22919','U5','TPS22919DCKR','TPS22919_SC70',[(1,'VIN'),(2,'GND'),(3,'ON'),(4,'NC'),(5,'QOD'),(6,'VOUT')],{1:'3V18',2:'GND',3:'PERIPH_ENABLE',5:'PERIPH_QOD',6:'3V18_PERIPH'},1300,-2580)
s.passive('RES','R29','100R',1760,-2470,'3V18_PERIPH','PERIPH_QOD')
s.passive('CAP','C15','1uF / 10V X7R',2050,-2470,'3V18','GND')
s.passive('CAP','C16','1uF / 10V X7R',1760,-2730,'3V18_PERIPH','GND')
s.text('3V18 powers ESP32 + TCA9535 continuously. Peripheral rail is OFF at reset.',140,-2880)
s.text('PWR key -> IOX P06 -> INT -> ESP32 GPIO21 (RTC). Other input changes can also wake.',140,-2910)
s.text('Before OFF: flush/unmount SD, disable amp/backlight, hold peripheral IO LOW/Hi-Z.',140,-2940)
s.text('Drive PERIPH_ENABLE LOW, wait for discharge, clear IOX interrupt, enter deep sleep.',140,-2970)
s.text('Wake: enable rail, wait for stabilization, initialize peripherals and mount SD anew.',140,-3000)
s.finish()
