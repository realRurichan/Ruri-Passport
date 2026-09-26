"""PN7160 host, power and crystal; RF matching is a separate design block."""
import argparse
from schematic_sheet import Sheet
p=argparse.ArgumentParser();p.add_argument('--skill',required=True);a=p.parse_args()
s=Sheet(a.skill,'NFC')
s.text('RURI PASSPORT - PN7160 / READER + TYPE 4 CARD EMULATION',100,-50,16)
s.block('PN7160A1HN / I2C 0x28 / CORE AND IO ALWAYS SUPPLIED',100,-150,1400,-1300)
names=['ADR0','DWL_REQ','ADR1','VSS_PAD','SDA','VDD_PAD','SCL','IRQ','VSS_A','VEN','IC','VBAT2','VDD_UP','VDD_TX','RXN','RXP','VDD_VMID','TVDD_IN','TX2','VSS_TX','TX1','TVDD_IN2','ANT1','ANT2','VDD_HF','VDD_A','VDD','VBAT','XTAL2','XTAL1','VDD_D','NC','NC','NC','NC','NC','DCDC_EN','IC','WKUP_REQ','CLK_REQ','EP']
nets={1:'GND',2:'NFC_DWL_REQ',3:'GND',4:'GND',5:'I2C_SDA',6:'3V18',7:'I2C_SCL',8:'NFC_IRQ',9:'GND',10:'NFC_VEN',12:'3V18',13:'3V18',14:'NFC_TVDD',15:'NFC_RXN',16:'NFC_RXP',17:'NFC_VMID',18:'NFC_TVDD',19:'NFC_TX2',20:'GND',21:'NFC_TX1',22:'NFC_TVDD',26:'NFC_VDD18',27:'NFC_VDD18',28:'3V18',29:'NFC_XTAL2',30:'NFC_XTAL1',31:'NFC_VDD18',39:'GND',41:'GND'}
s.ic('RURI_PN7160','U8','PN7160A1HN/C100Y','PN7160',list(enumerate(names,1)),nets,650,-680)
s.text('I2C pullups and VEN pulldown already on Controls sheet. I2C wake, WKUP_REQ=GND.',140,-1160)
s.text('ANT1/ANT2/VDD_HF left open per AN12988 Fig1. RF receiver uses RXP/RXN.',140,-1190)
s.text('IC/NC and unused DCDC_EN/CLK_REQ left open. Pins 14/18/22 and 26/27/31 linked.',140,-1220)
s.block('LOCAL DECOUPLING / INTERNAL REGULATOR OUTPUTS ARE NOT EXTERNAL RAILS',1530,-150,3330,-1300)
caps=[('C29','4.7uF / 10V X5R','3V18','near VBAT 28'),('C30','100nF / 10V X7R','3V18','near VBAT2 12'),('C31','4.7uF / 10V X5R','3V18','near VDD_UP 13'),('C32','1uF / 10V X5R','3V18','near VDD_PAD 6'),('C33','2.2uF / 10V X5R','NFC_VDD18','near VDD_A 26'),('C34','2.2uF / 10V X5R','NFC_VDD18','near VDD_D 31'),('C35','2.2uF / 10V X5R','NFC_TVDD','near TVDD_IN 18'),('C36','2.2uF / 10V X5R','NFC_TVDD','near TVDD_IN2 22'),('C37','100nF / 10V X7R','NFC_VMID','near VMID 17')]
for i,(ref,value,net,note) in enumerate(caps):
 x=1770+(i%3)*530;y=-350-(i//3)*300
 s.passive('CAP',ref,value,x,y,net,'GND');s.text(note,x-100,y-100,8)
s.text('Supply configuration CFG2: VBAT / VDD_PAD / VDD_UP all from regulated 3V18.',1580,-1170)
s.text('TXLDO=2.7V. Disable incompatible TXLDO Check; validate rail stays >3.0V under RF load.',1580,-1200)
s.block('27.12MHz CRYSTAL / NXP RECOMMENDED PART / LOAD CAPS REQUIRE TRIM',100,-1460,2250,-2110)
s.ic('RURI_XRCGB','Y1','XRCGB27M120F3M10R0','XRCGB2016',[(1,'XTAL'),(2,'NC'),(3,'XTAL'),(4,'NC')],{1:'NFC_XTAL1',3:'NFC_XTAL2'},520,-1710)
s.passive('CAP','C38','16pF / 50V C0G 2%',1130,-1710,'NFC_XTAL1','GND')
s.passive('CAP','C39','16pF / 50V C0G 2%',1650,-1710,'NFC_XTAL2','GND')
s.text('CL=10pF, ESR80R. Pins 2/4 MUST remain NC (Murata part); do not use grounded-case substitute.',140,-1910)
s.text('16pF caps are initial values: 8pF effective + estimated 2pF stray. Trim in assembled PCB.',140,-1940)
s.text('Firmware selects 27.12MHz crystal. Measure RF frequency and cold-start reliability.',140,-1970)
s.block('SERVICE / CARD MODE LIMITS',100,-2290,2250,-2780)
s.passive('RES','R59','100k',450,-2470,'NFC_DWL_REQ','GND')
s.text('DWL_REQ test access to be added: drive to 3V18 before VEN rising for firmware maintenance.',140,-2600)
s.text('NFC-A/B card emulation is ISO-DEP only; reader MIFARE Classic support is NOT card emulation.',140,-2640)
s.text('RevA card mode is powered operation. VEN low during soft-off; no batteryless-card promise.',140,-2680)
s.text('RF matching, antenna, DPC calibration and final enclosure measurements remain required.',140,-2720)
s.finish()
