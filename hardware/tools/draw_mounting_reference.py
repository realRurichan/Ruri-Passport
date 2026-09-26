"""Export a dimensioned enclosure reference from the PCB mounting coordinates.

SVG is a review drawing, DXF is a 1:1 mm mechanical reference, not a fab file.
"""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'design/mounting-holes.json').read_text())
placements=json.loads((root/'design/placement-draft.json').read_text())['placements']
out=root/'mechanical';out.mkdir(exist_ok=True)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="1380" viewBox="0 0 1240 1380">',
'<rect width="1240" height="1380" fill="#f5f6f2"/>',
'<g font-family="Arial,sans-serif" fill="#172c2b">',
'<text x="80" y="52" font-size="29" font-weight="bold">Ruri Passport / enclosure mounting reference</text>',
'<text x="80" y="86" font-size="18">PCB TOP VIEW · mm · rear volumes shown dashed · DRAFT</text>']
def point(x,y):return 100+8*x,120+8*(135-y)
def rect(x,y,w,h,fill,stroke,dash=''):
    sx,sy=point(x,y+h)
    svg.append(f'<rect x="{sx}" y="{sy}" width="{w*8}" height="{h*8}" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-dasharray="{dash}"/>')
def circle(x,y,r,fill,stroke,dash=''):
    sx,sy=point(x,y)
    svg.append(f'<circle cx="{sx}" cy="{sy}" r="{r*8}" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-dasharray="{dash}"/>')
def text(x,y,label,size=17,color='#e6efed'):
    sx,sy=point(x,y)
    svg.append(f'<text x="{sx}" y="{sy}" fill="{color}" font-size="{size}">{label}</text>')
rect(0,0,88,135,'#173c37','#092a25')
rect(13.56,38.5,60.88,94.57,'#ffffff16','#b9d4cf');text(27,126,'4-inch LCD',24)
rect(6,40,65,60,'none','#7cc9be','9 6');text(9,43,'REAR BATTERY ENVELOPE',15,'#7cc9be')
circle(30,117,14,'none','#fdc383','8 5');text(17,116,'REAR SPEAKER',14,'#fdc383')
rect(53,1,34,24,'#395b51','#e7c46a');text(60,12,'NFC coil',19)
rect(0,0,37,6.05,'#795e3b','#e7c46a');text(2,2,'Wi-Fi antenna',16)
for ref,label in [('SW1','UP'),('SW2','DN'),('SW3','LT'),('SW4','RT'),('SW5','OK')]:
    x,y,_=placements[ref]
    circle(x,y,2.55,'#dfebe8','#b9d4cf');text(x-1.9,y-.6,label,11,'#173c37')
text(49,35,'~5 mm gap',14,'#fdc383')
for hole in c['holes']:
    x,y=hole['x'],hole['y'];circle(x,y,2.6,'#adc6bf','#f8faf5')
    circle(x,y,1.1,'#f5f6f2','#173c37');text(x-6 if x>44 else x+3.3,y-1,hole['name'],15)
circle(82.786,110,.2,'#ffffff','#ffffff');text(77,106,'MIC',14)
text(1.5,108,'SPK',14);text(75,73,'SD',15);text(75,89,'PWR',15);text(39,5,'USB-C',15)
svg+=['<path d="M100 1225H804M100 1215V1235M804 1215V1235" fill="none" stroke="#172c2b" stroke-width="2"/>',
'<text x="395" y="1253" font-size="20">88 mm</text>',
'<path d="M70 120V1200M60 120H80M60 1200H80" fill="none" stroke="#172c2b" stroke-width="2"/>',
'<text x="48" y="690" font-size="20" transform="rotate(-90 48 690)">135 mm</text>',
'<text x="845" y="160" font-size="24" font-weight="bold">4 × M2 screw mounts</text>',
'<text x="845" y="204" font-size="20">Hole: Ø2.2 mm NPTH</text>',
'<text x="845" y="238" font-size="20">Reserved area: Ø5.2 mm</text>',
'<text x="845" y="272" font-size="18">Boss OD ≤4.5 mm</text>',
'<text x="845" y="302" font-size="18">Screw head OD ≤4.0 mm</text>']
for i,hole in enumerate(c['holes']):
    svg.append(f'<text x="845" y="{366+i*38}" font-size="20">{hole["name"]}: ({hole["x"]:g}, {hole["y"]:g})</text>')
for i,line in enumerate(['Origin: bottom-left of PCB.','Lower mounts are asymmetric','to clear antennas and battery.','','Rear speaker envelope only:','Ø28 × 5 mm, part TBD.','','Keep the microphone port open.','Add an insulated lower-edge','support ledge to the enclosure.','','This is not enclosure fit approval.','Check FPC fold, component height,','speaker wires and tolerances.']):
    svg.append(f'<text x="845" y="{565+i*31}" font-size="17">{line}</text>')
svg+=['<text x="100" y="1310" font-size="18">Mounting coordinates are authoritative; screen, battery and speaker volumes remain provisional.</text>',
'</g></svg>']
(out/'mounting-reference.svg').write_text('\n'.join(svg)+'\n')
dxf=['0','SECTION','2','HEADER','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
def line(layer,x1,y1,x2,y2):
    dxf.extend(map(str,[0,'LINE',8,layer,10,x1,20,y1,30,0,11,x2,21,y2,31,0]))
def drect(layer,x,y,w,h):
    ps=[(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
    for a,b in zip(ps,ps[1:]):line(layer,*a,*b)
drect('PCB_OUTLINE',0,0,88,135)
drect('LCD_ENVELOPE',13.56,38.5,60.88,94.57)
drect('REAR_BATTERY',6,40,65,60)
for ref in ['SW1','SW2','SW3','SW4','SW5']:
    x,y,_=placements[ref]
    dxf.extend(map(str,[0,'CIRCLE',8,'BUTTON_'+ref,10,x,20,y,30,0,40,2.55]))
for hole in c['holes']:
    for layer,radius in [('NPTH',1.1),('SCREW_RESERVATION',2.6)]:
        dxf.extend(map(str,[0,'CIRCLE',8,layer,10,hole['x'],20,hole['y'],30,0,40,radius]))
dxf.extend(map(str,[0,'CIRCLE',8,'REAR_SPEAKER_ENVELOPE',10,30,20,117,30,0,40,14]))
dxf+=['0','ENDSEC','0','EOF']
(out/'mounting-reference.dxf').write_text('\n'.join(dxf)+'\n')
print('Wrote SVG review drawing and 1:1 mm DXF mechanical reference.')
