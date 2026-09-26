"""Draw IR transmitter/receiver and filtered analog LCD current control.

Engineering draft: compensation, thermal performance and optical range need
prototype validation. Footprints are manufacturer-library candidates.
"""
import argparse
from schematic_sheet import Sheet
p=argparse.ArgumentParser();p.add_argument('--skill',required=True);a=p.parse_args()
s=Sheet(a.skill,'Optics')
def link(kind,ref,value,x,y,left,right):
 s.place(kind,ref,value,x,y,0,'R0603' if kind=='RES' else 'C0603')
 s.stub(left,x-20,y,x-120);s.stub(right,x+20,y,x+160)
s.text('RURI PASSPORT - INFRARED / LCD BACKLIGHT',100,-50,16)
s.block('940nm INFRARED TRANSMITTER / DEFAULT OFF',100,-150,2300,-850)
for ref,y in [('R46',-300),('R47',-530)]:
 link('RES',ref,'200R 1% >=0.125W',440,y,'VSYS','IR_LEDA')
s.ic('RURI_IR91','D4','IR91-21C/TR10','IR91',[(1,'K'),(2,'A')],{1:'IR_LEDK',2:'IR_LEDA'},1020,-380)
s.ic('RURI_AO3400A','Q1','AO3400A','SOT23',[(1,'G'),(2,'S'),(3,'D')],{1:'IR_GATE',2:'GND',3:'IR_LEDK'},1840,-380)
link('RES','R48','1k',970,-640,'IR_TX','IR_GATE')
s.passive('RES','R49','100k',1820,-640,'IR_GATE','GND')
s.text('Two parallel 200R give 100R. VSYS <=4.5V -> <=45.5mA conservative DC bound.',140,-745)
s.text('Top-looking emitter; front optical window. Verify LED derating, 38kHz edges and range.',140,-775)
s.block('38kHz DEMODULATING IR RECEIVER',100,-1000,2300,-1630)
s.ic('RURI_IRM_H638','IR1','IRM-H638T/TR2','IRM_H638',[(1,'GND'),(2,'GND'),(3,'OUT'),(4,'VCC')],{1:'GND',2:'GND',3:'IR_RX',4:'IR_RX_VCC'},550,-1230)
link('RES','R50','47R',1280,-1140,'3V18_PERIPH','IR_RX_VCC')
s.passive('CAP','C24','4.7uF / 10V X5R',1210,-1420,'IR_RX_VCC','GND')
s.passive('CAP','C25','100nF / 10V X7R',1610,-1420,'IR_RX_VCC','GND')
s.passive('RES','R51','47k',2010,-1290,'IR_RX_VCC','IR_RX')
s.text('Active-low demodulated output -> GPIO38. Carrier-specific reception, not raw IR sampling.',140,-1565)
s.block('LOW-SIDE LINEAR BACKLIGHT CURRENT SINK / DRAFT COMPENSATION',100,-1780,2850,-2950)
s.ic('RURI_TLV9001','U9','TLV9001IDBVR','TLV9001_SOT235',[(1,'OUT'),(2,'V-'),(3,'IN+'),(4,'IN-'),(5,'V+')],{1:'BL_OP_OUT',2:'GND',3:'BL_REF',4:'BL_FB',5:'3V18_PERIPH'},1260,-2110)
s.ic('RURI_AO3400A','Q2','AO3400A','SOT23',[(1,'G'),(2,'S'),(3,'D')],{1:'BL_GATE',2:'BL_SENSE',3:'LCD_LEDK'},2240,-2130)
link('RES','R52','20k 1%',380,-1980,'LCD_BL_PWM','BL_REF')
s.passive('RES','R53','1k 1%',420,-2240,'BL_REF','GND')
s.passive('CAP','C27','1uF / 10V X5R',780,-2240,'BL_REF','GND')
link('RES','R54','1k',1760,-1940,'BL_OP_OUT','BL_GATE')
s.passive('RES','R55','100k',2250,-2490,'BL_GATE','GND')
link('RES','R56','10k',1300,-2460,'BL_SENSE','BL_FB')
s.passive('RES','R57','1R 1% >=0.1W',2640,-2480,'BL_SENSE','GND')
link('CAP','C28','1nF / 50V C0G',1320,-2690,'BL_OP_OUT','BL_FB')
s.passive('CAP','C26','100nF / 10V X7R',1880,-2510,'3V18_PERIPH','GND')
# A wire with both labels intentionally names the supply and the LCD pin net.
# Native export will choose one name; use a 0R link to keep both explicit.
link('RES','R58','0R',2600,-1850,'VSYS','LCD_LEDA')
s.text('Nominal full-scale: 3.18V / 21 / 1R = 151mA. PWM >=20kHz, RC ~0.95ms.',140,-2780)
s.text('Static error budget ~163mA; NOT a verified transient bound. Scope current at power-up/dropout.',140,-2810)
s.text('LCD low-battery brightness falls with VSYS headroom. Q2 is linear: reserve thermal copper.',140,-2840)
s.text('Set PWM low before cutting PERIPH power. 1nF feedback is a starting value, verify loop stability.',140,-2870)
s.finish()
