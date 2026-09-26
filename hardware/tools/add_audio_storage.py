"""Draw SPI microSD, I2S speaker/microphone, battery voltage sensing and connector ESD."""
import argparse
from schematic_sheet import Sheet
p=argparse.ArgumentParser();p.add_argument('--skill',required=True);a=p.parse_args()
s=Sheet(a.skill,'Audio_Storage');ic=s.ic
s.text('RURI PASSPORT - AUDIO / STORAGE / MONITORING',100,-50,16)
s.block('MICROSD / SPI / PUSH-PUSH / CARD DETECT',100,-140,2450,-860)
names=['DAT2','DAT3_CS','CMD_MOSI','VDD','CLK','VSS','DAT0_MISO','DAT1','SW_B','SHIELD','SW_A','SHIELD','SHIELD','SHIELD']
nets={1:'SD_DAT2',2:'SD_CS_N',3:'SD_MOSI_CARD',4:'3V18_PERIPH',5:'SD_SCK_CARD',6:'GND',7:'SD_MISO',8:'SD_DAT1',9:'SD_DETECT_N',10:'GND',11:'GND',12:'GND',13:'GND',14:'GND'}
ic('RURI_DM3AT','J4','DM3AT-SF-PEJM5','DM3AT',list(enumerate(names,1)),nets,500,-420)
def linkres(ref,value,x,y,a,b):
 s.place('RES',ref,value,x,y,0,'R0603');s.stub(a,x-20,y,x-100);s.stub(b,x+20,y,x+140)
linkres('R32','33R',1120,-260,'SD_MOSI','SD_MOSI_CARD');linkres('R33','33R',1530,-260,'SD_SCK','SD_SCK_CARD')
for i,net in enumerate(['SD_DAT2','SD_CS_N','SD_MOSI_CARD','SD_MISO','SD_DAT1','SD_DETECT_N']):s.passive('RES',f'R{34+i}','47k',1030+(i%3)*450,-480-(i//3)*240,'3V18' if net=='SD_DETECT_N' else '3V18_PERIPH',net)
s.passive('CAP','C18','10uF / 10V X5R',2230,-350,'3V18_PERIPH','GND');s.passive('CAP','C19','100nF / 10V X7R',2230,-620,'3V18_PERIPH','GND')
s.text('All SD data/CMD pins biased high; CLK has no pullup. Card detect closes 9 to 11.',140,-805)
s.block('I2S CLASS-D AMPLIFIER / 8-OHM SPEAKER',100,-980,2450,-1710)
a=['DIN','GAIN_SLOT','GND','SD_MODE','NC','NC','VDD','VDD','OUTP','OUTN','GND','NC','NC','LRCLK','GND','BCLK','EP']
an={1:'I2S_DOUT_AUDIO',2:'GND',3:'GND',4:'AMP_ENABLE',7:'3V18_PERIPH',8:'3V18_PERIPH',9:'SPK_OUT_P',10:'SPK_OUT_N',11:'GND',14:'I2S_WS_AUDIO',15:'GND',16:'I2S_BCLK_AUDIO',17:'GND'}
ic('RURI_MAX98357','U7','MAX98357AETE+T','MAX98357_TQFN',list(enumerate(a,1)),an,500,-1260)
for ref,x,y,a,b in [('R40',1100,-1080,'I2S_BCLK','I2S_BCLK_AUDIO'),('R41',1560,-1080,'I2S_WS','I2S_WS_AUDIO'),('R42',2020,-1080,'I2S_DOUT','I2S_DOUT_AUDIO')]:linkres(ref,'33R',x,y,a,b)
s.passive('CAP','C20','10uF / 10V X5R',1110,-1340,'3V18_PERIPH','GND');s.passive('CAP','C21','100nF / 10V X7R',1410,-1340,'3V18_PERIPH','GND')
ic('RURI_SPEAKER_PH2','J5','S2B-PH-SM4-TB(LF)(SN)','JSTPH2',[(1,'SPK+'),(2,'SPK-'),(3,'MP'),(4,'MP')],{1:'SPK_OUT_P',2:'SPK_OUT_N',3:'GND',4:'GND'},1970,-1390)
s.text('Gain 12dB. AMP_ENABLE high selects left channel; default LOW via Controls/R10.',140,-1590)
s.text('8 ohm >=1W speaker. Differential outputs: NEVER connect SPK- to ground.',140,-1620)
s.text('Keep speaker wires short/twisted; footprints for output EMI filter remain to add.',140,-1650)
s.block('BOTTOM-PORT I2S MICROPHONE',100,-1840,1230,-2390)
m=['WS','SELECT','GND','BCLK','VDD','DOUT']
ic('RURI_SPH0645','MIC1','SPH0645LM4H-B','SPH0645',list(enumerate(m,1)),{1:'I2S_WS_AUDIO',2:'GND',3:'GND',4:'I2S_BCLK_AUDIO',5:'3V18_PERIPH',6:'I2S_DIN'},500,-2070)
s.passive('CAP','C22','100nF / 10V X7R',1040,-1980,'3V18_PERIPH','GND');s.passive('RES','R43','100k',1040,-2220,'I2S_DIN','GND')
s.text('Left slot; MCU provides shared 64-BCLK stereo frames.',140,-2290)
s.text('PCB acoustic hole + gasket needed; no paste or vias in port.',140,-2320)
s.block('BATTERY VOLTAGE / ADC / LOW-COST ESTIMATE',1330,-1840,2450,-2390)
s.passive('RES','R44','1M 1%',1560,-2030,'VBAT','VBAT_SENSE')
s.passive('RES','R45','330k 1%',2000,-2030,'VBAT_SENSE','GND')
s.passive('CAP','C23','100nF / 10V X7R',2240,-2190,'VBAT_SENSE','GND')
s.text('VBAT_SENSE -> GPIO1 ADC1. 4.2V battery -> 1.042V nominal; divider ~3.16uA.',1370,-2280)
s.text('ADC calibration + averaging required. Voltage estimate is NOT coulomb-counted SOC.',1370,-2310)
s.text('Warn/unmount SD before low battery cutoff. Approx RC=25ms; settle before sampling.',1370,-2340)
s.block('CONNECTOR ESD / PLACE AT CONNECTORS',100,-2510,2450,-2980)
for i,(n1,n2,x) in enumerate([('USB_DP_CONN','USB_DM_CONN',480),('USB_CC1','USB_CC2',1250),('SD_SCK_CARD','SD_MOSI_CARD',2020)],1):
 ic('RURI_TPD2EUSB30',f'D{i}','TPD2EUSB30DRTR','TPD2EUSB30',[(1,'IO1'),(2,'IO2'),(3,'GND')],{1:n1,2:n2,3:'GND'},x,-2680)
s.text('ESD clamps need short ground returns. VBUS protection and remaining SD lines remain to add.',140,-2880)
s.finish()
