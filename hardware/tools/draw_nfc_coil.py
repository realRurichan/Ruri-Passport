"""Draw the draft NFC coil with the native project CLOSED.

POLY and bridging FILL formats were captured from EasyEDA Pro 4.1.60.
This is geometry generation, not RF validation or manufacturing approval.
"""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / 'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2'
rows = []
doc = None
for line in PCB.read_text().splitlines():
    h, b = line.split('||', 1)
    h = json.loads(h)
    b = b.removesuffix('|')
    v = json.loads(b) if b else None
    if h['type'] == 'DOCHEAD':
        doc = v['docType']
    rows.append((h, v, doc))

# The end is inside the innermost turn, never joined to the start of that turn.
points = [(0.2, 0.2)]
for i in range(4):
    d = i * 0.7
    points.extend([(33.8-d, 0.2+d), (33.8-d, 23.8-d),
                   (0.2+d, 23.8-d), (0.2+d, 0.2+(i+1)*0.7)])
points = [(87-x, 25-y) for x,y in points]
# Leave a 0.4 mm gap to the ANT_B pad centre, bridged only by the local fill.
points[-1] = (84.7, 21.3)
mil = lambda mm: round(mm / 0.0254, 6)
path = [mil(points[0][0]), mil(points[0][1]), 'L']
path.extend(mil(a) for p in points[1:] for a in p)
seen = set()
circles = ['656616e67d024db4', '299456bad27d416c', '65c6dd6014fe4c41',
           '1b9d8973c1284248', '5ed662331ea74a59']
placements = json.loads((ROOT/'design/placement-draft.json').read_text())['placements']
centres = [placements[ref][:2] for ref in ['SW1','SW2','SW3','SW4','SW5']]
for h, v, doc in rows:
    if doc != 'PCB' or not v:
        continue
    if h.get('id') == '6dc0cc0ee7938543':
        v.update(layerId=1, netName='ANT_A', width=mil(0.4), path=path,
                 locked=True)
        seen.add('coil')
    if h.get('id') == 'c07ef8df2eb0219c':
        v.update(layerId=1, netName='', width=0,
                 path=[['R',mil(84.4),mil(22.35),mil(0.6),mil(1.2),0,0]],
                 isBridgingCopper=True, networkList=['ANT_A','ANT_B'], locked=True)
        seen.add('bridge')
    if h.get('id') in circles:
        x,y = centres[circles.index(h['id'])]
        v['path'] = ['CIRCLE',mil(x),mil(y),mil(2.5)]
assert seen == {'coil','bridge'}, 'Expected native calibration objects missing'
shutil.copy2(PCB, '/private/tmp/ruri-before-coil.epcb2')
PCB.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+
               (json.dumps(v,separators=(',',':')) if v is not None else '')+'|'
               for h,v,_ in rows)+'\n')
(ROOT/'review/nfc-coil-geometry.json').write_text(json.dumps({
    'status':'DRAFT: no RF/DRC/manufacturing approval',
    'native_poly_id':'6dc0cc0ee7938543', 'native_bridge_id':'c07ef8df2eb0219c',
    'turns':4,'width_mm':0.4,'nominal_gap_mm':0.3,
    'centreline_points_mm':points,'bridge_networks':['ANT_A','ANT_B'],
    'remaining':'Inner-terminal escape, feed routing, all-layer copper exclusions and RF tuning'
},indent=2)+'\n')
print('Generated four-turn NFC spiral and local ANT_A/ANT_B bridge; no RF signoff.')
