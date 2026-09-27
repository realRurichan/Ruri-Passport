"""Check manufacturer pin assignments in a native EDA .enet export.
Never derive expectations from schematic geometry: this catches Y-axis flips.
"""
import argparse,json
p=argparse.ArgumentParser();p.add_argument('netlist');a=p.parse_args()
j=json.load(open(a.netlist));c={x['props']['Designator']:x for x in j['components'].values()}
expect={}
expect['J1']={n:'' for n in range(1,41)}
expect['J1'].update({5:'GND',6:'3V18_PERIPH',7:'3V18_PERIPH',9:'LCD_CS_N',10:'LCD_DC',11:'LCD_WR_N',12:'3V18_PERIPH',13:'GND',15:'LCD_RESET_N',16:'GND',33:'LCD_LEDA',34:'LCD_LEDK',35:'LCD_LEDK',36:'LCD_LEDK',37:'GND',38:'3V18_PERIPH',39:'3V18_PERIPH',40:'GND'})
expect['J1'].update({17+i:f'LCD_D{i}' for i in range(8)})
expect['J1'].update({n:'GND' for n in range(25,33)})
expect['U1']={1:'GND',2:'3V18',3:'ESP_EN',**{4+i:f'LCD_D{i}' for i in range(8)},12:'LCD_WR_N',13:'USB_DM_MCU',14:'USB_DP_MCU',15:'',16:'',17:'LCD_DC',18:'LCD_CS_N',19:'SD_MOSI',20:'SD_SCK',21:'SD_MISO',22:'SD_CS_N',23:'IOX_IRQ_N',24:'NFC_IRQ',25:'IR_TX',26:'',27:'BOOT_N',28:'',29:'',30:'',31:'IR_RX',32:'I2S_BCLK',33:'I2S_WS',34:'I2S_DOUT',35:'I2S_DIN',36:'I2C_SDA',37:'LCD_BL_PWM',38:'I2C_SCL',39:'VBAT_SENSE',40:'GND',41:'GND'}
expect['U2']={1:'IOX_IRQ_N',2:'GND',3:'GND',4:'KEY_UP_N',5:'KEY_DOWN_N',6:'KEY_LEFT_N',7:'KEY_RIGHT_N',8:'KEY_OK_N',9:'SD_DETECT_N',10:'PWR_INT_N',11:'CHG_STATUS_N',12:'GND',13:'LCD_RESET_N',14:'NFC_VEN',15:'AMP_ENABLE',16:'USB_PGOOD_N',17:'CHG_EN1',18:'CHG_EN2',19:'PERIPH_ENABLE',20:'REG_PWM',21:'GND',22:'I2C_SCL',23:'I2C_SDA',24:'3V18'}
expect['U3']={1:'BAT_NTC',2:'VBAT',3:'VBAT',4:'GND',5:'CHG_EN2',6:'CHG_EN1',7:'USB_PGOOD_N',8:'GND',9:'CHG_STATUS_N',10:'VSYS',11:'VSYS',12:'CHG_ILIM',13:'VBUS_5V',14:'',15:'',16:'CHG_ISET',17:'GND'}
expect['U4']={1:'VSYS',2:'REG_PWM',3:'GND',4:'VREG_FB',5:'VREG_PG',6:'3V18',7:'VREG_L2',8:'GND',9:'VREG_L1',10:'VSYS'}
expect['U5']={1:'3V18',2:'GND',3:'PERIPH_ENABLE',4:'',5:'PERIPH_QOD',6:'3V18_PERIPH'}
expect['J3']={1:'VBAT',2:'BAT_NTC',3:'GND',4:'GND',5:'GND'}
expect['L1']={1:'VREG_L1',2:'VREG_L2'}
expect['SW6']={1:'PWR_INT_N',2:'GND'}
for i,k in enumerate(['UP','DOWN','LEFT','RIGHT','OK'],1):expect[f'SW{i}']={1:f'KEY_{k}_N',3:f'KEY_{k}_N',2:'GND',4:'GND'}
expect['J4']={1:'SD_DAT2',2:'SD_CS_N',3:'SD_MOSI_CARD',4:'3V18_PERIPH',5:'SD_SCK_CARD',6:'GND',7:'SD_MISO',8:'SD_DAT1',9:'SD_DETECT_N',10:'GND',11:'GND',12:'GND',13:'GND',14:'GND'}
expect['U7']={1:'I2S_DOUT_AUDIO',2:'GND',3:'GND',4:'AMP_ENABLE',5:'',6:'',7:'3V18_PERIPH',8:'3V18_PERIPH',9:'SPK_OUT_P',10:'SPK_OUT_N',11:'GND',12:'',13:'',14:'I2S_WS_AUDIO',15:'GND',16:'I2S_BCLK_AUDIO',17:'GND'}
expect['MIC1']={1:'I2S_WS_AUDIO',2:'GND',3:'GND',4:'I2S_BCLK_AUDIO',5:'3V18_PERIPH',6:'I2S_DIN'}
expect['J5']={1:'SPK_OUT_P',2:'SPK_OUT_N',3:'GND',4:'GND'}
expect['R44']={1:'VBAT_SENSE',2:'VBAT'}
expect['R45']={1:'GND',2:'VBAT_SENSE'}
expect['C23']={1:'GND',2:'VBAT_SENSE'}
for i,nets in enumerate([('USB_DP_CONN','USB_DM_CONN'),('USB_CC1','USB_CC2'),('SD_SCK_CARD','SD_MOSI_CARD')],1):expect[f'D{i}']={1:nets[0],2:nets[1],3:'GND'}
expect['D4']={1:'IR_LEDK',2:'IR_LEDA'}
expect['IR1']={1:'GND',2:'GND',3:'IR_RX',4:'IR_RX_VCC'}
expect['Q1']={1:'IR_GATE',2:'GND',3:'IR_LEDK'}
expect['Q2']={1:'BL_GATE',2:'BL_SENSE',3:'LCD_LEDK'}
expect['U9']={1:'BL_OP_OUT',2:'GND',3:'BL_REF',4:'BL_FB',5:'3V18_PERIPH'}
expect['U8']={n:'' for n in range(1,42)}
expect['U8'].update({1:'GND',2:'NFC_DWL_REQ',3:'GND',4:'GND',5:'I2C_SDA',6:'3V18',7:'I2C_SCL',8:'NFC_IRQ',9:'GND',10:'NFC_VEN',12:'3V18',13:'3V18',14:'NFC_TVDD',15:'NFC_RXN',16:'NFC_RXP',17:'NFC_VMID',18:'NFC_TVDD',19:'NFC_TX2',20:'GND',21:'NFC_TX1',22:'NFC_TVDD',26:'NFC_VDD18',27:'NFC_VDD18',28:'3V18',29:'NFC_XTAL2',30:'NFC_XTAL1',31:'NFC_VDD18',39:'GND',41:'GND'})
expect['Y1']={1:'NFC_XTAL1',2:'',3:'NFC_XTAL2',4:''}
expect['ANT1']={1:'ANT_A',2:'ANT_B'}
for i,side in enumerate(['A','B']):
 expect[f'L{2+i}']={1:f'NFC_TX{1+i}',2:f'RF_EMC_{side}'}
 expect[f'C{40+i}']={1:'GND',2:f'RF_EMC_{side}'}
 expect[f'C{42+i}']={1:f'RF_MATCH_{side}',2:f'RF_EMC_{side}'}
 expect[f'C{44+i}']={1:'GND',2:f'RF_MATCH_{side}'}
 expect[f'R{60+i}']={1:f'RF_DAMP_{side}',2:f'RF_MATCH_{side}'}
 expect[f'R{66+i}']={1:f'ANT_{side}',2:f'RF_DAMP_{side}'}
 expect[f'R{62+i}']={1:f'RF_RX_{side}',2:f'RF_EMC_{side}'}
 expect[f'R{64+i}']={1:f'RF_RX_{side}',2:f'ANT_{side}'}
 expect[f'C{46+i}']={1:'NFC_RXN' if i==0 else 'NFC_RXP',2:f'RF_RX_{side}'}
 expect[f'C{48+i}']={1:f'RF_MATCH_{side}',2:f'RF_EMC_{side}'}
 expect[f'C{50+i}']={1:'GND',2:f'RF_MATCH_{side}'}
expect['D5']={1:'SD_MISO',2:'SD_CS_N',3:'GND'}
expect['D6']={1:'SD_DAT1',2:'SD_DAT2',3:'GND'}
expect['D7']={1:'VBUS_5V',2:'',3:'GND'}
for i,net in enumerate(['GND','3V18','ESP_EN','BOOT_N','NFC_DWL_REQ','VSYS','VBAT','3V18_PERIPH','NFC_IRQ','NFC_TVDD'],1):expect[f'TP{i}']={1:net}
# 2026-09-27: verified SPI/direct-key/hard-shutdown schematic revision.
expect['J1'].update({11:'LCD_SCK',13:'LCD_MOSI',40:'3V18_PERIPH',**{n:'GND' for n in range(17,33)}})
expect['U1'].update({4:'KEY_UP_N',5:'KEY_DOWN_N',6:'KEY_LEFT_N',7:'KEY_RIGHT_N',8:'KEY_OK_N',9:'LCD_MOSI',10:'NFC_VEN',11:'PWR_INT_N',12:'LCD_SCK',23:'PWR_KILL'})
for i,(pin,port) in enumerate([(4,'P00'),(5,'P01'),(6,'P02'),(7,'P03'),(8,'P04'),(10,'P06'),(14,'P11')]):
 net='IOX_UNUSED_'+port
 expect['U2'][pin]=net
 expect[f'R{77+i}']={1:net,2:'GND'}
expect['U4'].update({1:'VSYS_RUN',10:'VSYS_RUN'})
expect['SW6'][1]='PWR_BUTTON_N'
expect['R44'][2]='VBAT_ADC_SW'
expect['U10']={1:'GND',2:'PWR_ONT',3:'PWR_BUTTON_N',4:'VSYS',5:'PWR_KILL_N',6:'PWR_PDT',7:'PWR_EN',8:'PWR_INT_N',9:'GND'}
expect['Q10']={1:'PWR_KILL',2:'GND',3:'PWR_KILL_N'}
expect['Q11']={1:'PWR_EN',2:'GND',3:'MAIN_SWITCH_D'}
for ref in ['Q12','Q13']:expect[ref]={1:'MAIN_GATE',2:'VSYS',3:'VSYS_RUN'}
expect['Q14']={1:'BAT_ADC_GATE',2:'VBAT',3:'VBAT_ADC_SW'}
expect['Q15']={1:'PWR_EN',2:'GND',3:'BAT_ADC_GATE'}
for ref,nets in {'C60':('VSYS','GND'),'C61':('PWR_ONT','GND'),'C62':('PWR_PDT','GND'),'C63':('VSYS','MAIN_GATE'),'R70':('3V18','PWR_KILL_N'),'R71':('PWR_KILL','GND'),'R72':('VSYS','PWR_EN'),'R73':('MAIN_GATE','MAIN_SWITCH_D'),'R74':('VSYS','MAIN_GATE'),'R75':('VBAT','BAT_ADC_GATE'),'R76':('VSYS_RUN','GND')}.items():expect[ref]=dict(enumerate(nets,1))
# 2026-09-27: direct open-drain KILL control; unnecessary inverter removed.
expect['U1'][23]='PWR_KILL_N'
expect.pop('Q10')
expect.pop('R71')
# Cost revision: one SPI bus, distinct LCD/SD chip selects; freed GPIOs reserved.
expect['J1'].update({11:'SD_SCK',13:'SD_MOSI'})
expect['U1'].update({9:'LCD_RESET_N',12:''})
expect['U2'][13]=''
# Expander/peripheral switch removal: independent GPIO8 amplifier shutdown.
for ref in ['U2','U5','C8','R8','R11','R12','R13','R14','R24','R25','R29','R30','R39',
            *[f'R{i}' for i in range(77,84)]]:
 expect.pop(ref,None)
expect['U1'][12]='AMP_ENABLE'
expect['U3'].update({5:'GND',6:'VBUS_5V',7:'',9:''})
expect['U4'][2]='GND'
expect['J4'][9]=''
for pins in expect.values():
 for pin,net in list(pins.items()):
  if net=='3V18_PERIPH':pins[pin]='3V18'
# Discrete power hold replaces LTC controller; ADC sampling still isolated.
for ref in ['U10','R70','R72','C60','C61','C62','C63']:expect.pop(ref,None)
expect['U1'].update({11:'PWR_KEY_ACTIVE_H',23:'PWR_HOLD'})
expect['SW6'][1]='BUTTON_RAW'
expect['Q11'][1]='PWR_HOLD'
expect['Q15'][1]='PWR_HOLD'
expect['Q16']={1:'BUTTON_RAW',2:'GND',3:'PWR_KEY_ACTIVE_H'}
expect['D8']={1:'BUTTON_RAW',2:'MAIN_SWITCH_D'}
expect['R84']={1:'PWR_HOLD',2:'GND'}
expect['R85']={1:'3V18',2:'PWR_KEY_ACTIVE_H'}
expect['R86']={1:'VSYS',2:'BUTTON_RAW'}
errors=[];count=0
refs=[x['props']['Designator'] for x in j['components'].values()]
for ref in ['Q10','R71','U10','R70','R72','C60','C61','C62','C63','U2','U5','C8','R8','R11','R12','R13','R14','R24','R25','R29','R30','R39',
            *[f'R{i}' for i in range(77,84)]]:
 if ref in c:errors.append(ref+': obsolete KILL inverter still present')
if len(refs)!=len(set(refs)):errors.append('Duplicate component designators')
for ref,pins in expect.items():
 if ref not in c:errors.append(f'{ref}: missing');continue
 for pin,net in pins.items():
  count+=1;actual=c[ref]['pinInfoMap'].get(str(pin),{}).get('net','<missing pin>')
  if actual!=net:errors.append(f'{ref}.{pin}: expected {net!r}, got {actual!r}')
for ref,part in c.items():
 if any(m in str(part['props']) for m in ('LTC2950','MAX17048')):errors.append(ref+': removed costly part still present')
 if not part['props'].get('Footprint'):errors.append(ref+': missing footprint')
 if '?' in ref:errors.append(ref+': unnumbered designator')
for ref in ['ANT1','C4','C5','C48','C49','C50','C51','R64','R65']+[f'TP{i}' for i in range(1,11)]:
 if c.get(ref,{}).get('props',{}).get('Add into BOM')!='no':errors.append(ref+': must be excluded from populated BOM')
print(f'{len(c)} components; {count} checked pin-net assignments; {len(errors)} errors')
for e in errors:print(e)
raise SystemExit(bool(errors))
