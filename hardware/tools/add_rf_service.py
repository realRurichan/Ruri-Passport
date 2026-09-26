"""RF matching and service pads. RF values are starting values, not measured tuning."""
import argparse,json
from pathlib import Path
from schematic_sheet import Sheet,ROOT
p=argparse.ArgumentParser();p.add_argument('--skill',required=True);a=p.parse_args()
s=Sheet(a.skill,'RF_Service')
s.text('RURI PASSPORT - NFC RF MATCHING / SERVICE / ESD',100,-50,16)
s.block('SYMMETRIC RF NETWORK / TXLDO 2.7V / ENABLE AND CALIBRATE DPC',100,-150,2900,-1250)
for i,side in enumerate(['A','B']):
 y=-350-i*550
 # Deliberately use the same per-branch topology and mirrored PCB placement.
 s.ic('RURI_RF_L',f'L{2+i}','160nH LQW18CNR16J00D','LQW18',[(1,'IN'),(2,'OUT')],{1:f'NFC_TX{1+i}',2:f'RF_EMC_{side}'},430,y)
 s.passive('CAP',f'C{40+i}','750pF / 50V C0G 2%',940,y,f'RF_EMC_{side}','GND')
 s.passive('CAP',f'C{42+i}','62pF / 50V C0G 2%',1380,y,f'RF_EMC_{side}',f'RF_MATCH_{side}')
 s.passive('CAP',f'C{44+i}','200pF / 50V C0G 2%',1840,y,f'RF_MATCH_{side}','GND')
 for ref,hi,lo,rx in [(f'R{60+i}',f'RF_MATCH_{side}',f'RF_DAMP_{side}',2320),(f'R{66+i}',f'RF_DAMP_{side}',f'ANT_{side}',2720)]:
  s.place('RES',ref,'1R / 1% / 0.25W C17928',rx,y,90,'RURI_R1206_1R')
  s.wire(hi,(rx,y+20,rx,y+60));s.label(hi,rx,y+60)
  s.wire(lo,(rx,y-20,rx,y-60));s.label(lo,rx,y-60)
s.text('Initial values from an estimated 34x24mm / 4-turn coil. Re-tune on assembled board.',140,-1160)
s.block('RX TAP OPTIONS / NEVER FIT BOTH RESISTOR PAIRS',100,-1400,2900,-2300)
for i,side in enumerate(['A','B']):
 y=-1600-i*350
 s.passive('RES',f'R{62+i}','2.2k / 1%',430,y,f'RF_EMC_{side}',f'RF_RX_{side}')
 s.passive('RES',f'R{64+i}','DNP / 6.8k / 1%',1140,y,f'ANT_{side}',f'RF_RX_{side}')
 s.passive('CAP',f'C{46+i}','1nF / 50V C0G 2%',1910,y,f'RF_RX_{side}','NFC_RXN' if i==0 else 'NFC_RXP')
s.text('Default: R62/R63 fitted, R64/R65 DNP. Alternative antenna tap: exchange the pairs.',140,-2170)
s.text('Never use 0R for antenna RX tap. Verify AGC / ALM / receive voltage before final BOM.',140,-2210)
s.block('PARALLEL TUNING PADS / NOT POPULATED IN INITIAL BOM',100,-2460,2900,-3010)
for i,(ref,hi,lo) in enumerate([('C48','RF_EMC_A','RF_MATCH_A'),('C49','RF_EMC_B','RF_MATCH_B'),('C50','RF_MATCH_A','GND'),('C51','RF_MATCH_B','GND')]):
 s.passive('CAP',ref,'DNP / TUNE C0G 50V',430+i*670,-2680,hi,lo)
s.text('PCB coil connects ANT_A to ANT_B; do not replace the coil with a short copper segment.',140,-2910)
s.run('generate-footprint.js','from-pads',name='RURI_NFC_COIL_34X24',designator='ANT',pads='1:7.874:7.874:15.748:15.748;2:90.5512:118.1102:15.748:15.748',outline='R,0,0,1338.5827,944.8819',description='PCB copper coil; no purchased part; matching requires measurement')
coil=ROOT/'.tmp/library/footprint/RURI_NFC_COIL_34X24.json'
clib=json.loads(coil.read_text())
for k,line in enumerate(clib['footprintDoc']):
 h,b=line.split('||',1);head=json.loads(h);body=json.loads(b.removesuffix('|')) if b.removesuffix('|') else None
 if head['type']=='PAD':
  body.update(topPasteExpansion=-100,bottomPasteExpansion=-100)
  clib['footprintDoc'][k]=h+'||'+json.dumps(body,separators=(',',':'))+'|'
coil.write_text(json.dumps(clib))
s.ic('RURI_PCB_COIL','ANT1','PCB COIL / 34x24mm / 4T / TUNE','RURI_NFC_COIL_34X24',[(1,'A'),(2,'B')],{1:'ANT_A',2:'ANT_B'},500,-3300)
s.block('CONNECTOR ESD / SAME TPD2EUSB30DRTR AS D1-D3',3100,-150,4850,-1400)
for i,nets in enumerate([('SD_MISO','SD_CS_N'),('SD_DAT1','SD_DAT2'),('VBUS_5V',None)],5):
 nm={1:nets[0],3:'GND'}
 if nets[1]:nm[2]=nets[1]
 s.ic('RURI_TPD2EUSB30',f'D{i}','TPD2EUSB30DRTR','TPD2EUSB30',[(1,'IO1'),(2,'IO2'),(3,'GND')],nm,3730,-370-(i-5)*350)
s.text('D7 uses 5.5V working-voltage non-A part; do not substitute TPD2EUSB30A.',3140,-1280)
s.text('ESD clamp is not an input overvoltage disconnect or a USB PD controller.',3140,-1320)
s.block('BARE TEST PADS / NO SMT PARTS / NO PASTE',3100,-1550,4850,-3010)
s.run('generate-footprint.js','from-pads',name='RURI_TP_1MM',designator='TP',pads='1:0:0:39.3701:39.3701',description='Bare 1mm test pad; no paste; not a fitted component')
# Disable paste explicitly in the native footprint record; mask stays open.
fp=ROOT/'.tmp/library/footprint/RURI_TP_1MM.json'
lib=json.loads(fp.read_text())
for k,line in enumerate(lib['footprintDoc']):
 h,b=line.split('||',1);head=json.loads(h);body=json.loads(b.removesuffix('|')) if b.removesuffix('|') else None
 if head['type']=='PAD':
  body['topPasteExpansion']=-100
  body['bottomPasteExpansion']=-100
  lib['footprintDoc'][k]=h+'||'+json.dumps(body,separators=(',',':'))+'|'
fp.write_text(json.dumps(lib))
for i,net in enumerate(['GND','3V18','ESP_EN','BOOT_N','NFC_DWL_REQ','VSYS','VBAT','3V18_PERIPH','NFC_IRQ','NFC_TVDD'],1):
 x=3490+((i-1)%2)*800;y=-1790-((i-1)//2)*220
 s.ic('RURI_TESTPAD',f'TP{i}','BARE PAD / NO BOM','RURI_TP_1MM',[(1,'PAD')],{1:net},x,y)
s.text('ROM download: BOOT low, pulse EN low, release EN then BOOT. USB uses GPIO19/20.',3140,-2900)
s.text('PN7160 download: DWL_REQ=3V18 before VEN rising; use ground reference, not VBAT.',3140,-2940)
s.finish()
