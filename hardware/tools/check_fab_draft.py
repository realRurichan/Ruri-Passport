"""Focused independent checks of the native Gerber ZIP (not a full DFM signoff)."""
import argparse
import hashlib
import json
import math
import re
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('zip')
parser.add_argument('--report', required=True)
parser.add_argument('--profile', choices=['compact-88x85', 'legacy-88x135'], default='compact-88x85')
args = parser.parse_args()
checks = []

def check(name, passed):
    checks.append({'check': name, 'passed': bool(passed)})

def drill(text):
    tools, hits, slots, tool = {}, [], [], None
    for line in text.splitlines():
        m = re.fullmatch(r'T(\d+)C([\d.]+)', line)
        if m:
            tools[m[1]] = float(m[2])
        elif re.fullmatch(r'T\d+', line):
            tool = line[1:]
        elif line.startswith('X'):
            pts = re.findall(r'X(-?[\d.]+)Y(-?[\d.]+)', line)
            record = [tools[tool], *[float(v) for xy in pts for v in xy]]
            (slots if 'G85' in line else hits).append(record)
    return hits, slots

def gerber(text):
    # This export explicitly declares mm, absolute 4.5 coordinates.
    assert '%FSLAX45Y45*%' in text and '%MOMM*%' in text
    apertures, flashes, regions = {}, [], []
    ap, region = None, None
    for line in text.splitlines():
        m = re.fullmatch(r'%ADD(\d+)([CRO]),([\d.X]+)\*%', line)
        if m:
            apertures[m[1]] = [m[2], *map(float, m[3].split('X'))]
        m = re.fullmatch(r'G54D(\d+)\*', line)
        if m:
            ap = m[1]
        if line == 'G36*':
            region = []
        elif line == 'G37*':
            regions.append(region)
            region = None
        m = re.search(r'X(-?\d+)Y(-?\d+).*D0([123])\*', line)
        if m:
            xy = [int(m[1])/1e5, int(m[2])/1e5]
            if region is not None:
                region.append(xy)
            elif m[3] == '3':
                flashes.append([xy, apertures.get(ap)])
    return flashes, regions

def near(a, b, tolerance=0.00002):
    return len(a) == len(b) and all(abs(x-y) < tolerance for x,y in zip(a,b))

with zipfile.ZipFile(args.zip) as z:
    names = set(z.namelist())
    read = lambda name: z.read(name).decode('utf-8-sig')
    copper = ['Gerber_TopLayer.GTL', 'Gerber_InnerLayer1.G1',
              'Gerber_InnerLayer2.G2', 'Gerber_BottomLayer.GBL']
    check('Four nonempty copper layers exported', all(n in names and len(z.read(n)) > 1000 for n in copper))
    npth, _ = drill(read('Drill_NPTH_Through.DRL'))
    if args.profile == 'compact-88x85':
        mounting = json.loads((Path(__file__).resolve().parents[1] / 'design/mounting-holes.json').read_text())
        expected = [[.4,82.786,55], [.65,46.89,6.28], [.65,41.11,6.28]]
        expected += [[mounting['hole_diameter'], h['x'], h['y']] for h in mounting['holes']]
        board_height, ir_x, ir_y = 85, 70, 82
    else:
        expected = [[.4,82.786,110], [.65,46.89,6.28], [.65,41.11,6.28],
                    [2.2,3,132], [2.2,84.5,132], [2.2,3.5,38], [2.2,84.5,50]]
        board_height, ir_x, ir_y = 135, 82, 127
    check('Seven NPTH drill hits, correct diameters and positions',
          len(npth)==len(expected) and all(any(near(a,b) for a in npth) for b in expected))
    pth, slots = drill(read('Drill_PTH_Through.DRL'))
    via, _ = drill(read('Drill_PTH_Through_Via.DRL'))
    expected_slots = [[.6,39.68,7.33,39.68,6.23], [.6,48.32,7.33,48.32,6.23],
                      [.6,48.32,3,48.32,2.2], [.6,39.68,3,39.68,2.2]]
    check('Four USB plated slots: 0.60 mm width, 1.70/1.40 mm overall length',
          len(slots)==4 and all(any(near(a,b) for a in slots) for b in expected_slots))
    check('Separate via drill is a subset of combined PTH drill',
          all(tuple(v) in set(map(tuple,pth)) for v in via))
    flashes, _ = gerber(read('Gerber_TopLayer.GTL'))
    xs = [40.65,40.95,41.45,41.75,42.25,42.75,43.25,43.75,
          44.25,44.75,45.25,45.75,46.25,46.55,47.05,47.35]
    check('Sixteen USB copper pads: 0.30 x 1.15 mm at y=7.355',
          all(any(near(pt,[x,7.355]) and shape and shape[0]=='R' and near(shape[1:],[.3,1.15])
                  for pt,shape in flashes) for x in xs))
    _, regions = gerber(read('Gerber_TopPasteMaskLayer.GTP'))
    boxes = [[min(x for x,y in r),min(y for x,y in r),max(x for x,y in r),max(y for x,y in r)] for r in regions if r]
    paste = [(40.8,.6),(41.6,.6),(46.4,.6),(47.2,.6)] + [(x,.3) for x in [42.25,42.75,43.25,43.75,44.25,44.75,45.25,45.75]]
    check('Twelve USB signal paste regions match target land pattern',
          all(any(near(box,[x-w/2,6.78,x+w/2,7.93]) for box in boxes) for x,w in paste))
    outline = read('Gerber_BoardOutlineLayer.GKO')
    height = board_height * 100000
    check(f'88 x {board_height} mm closed rectangular outline present',
          f'G01X0Y0D02*\nG01X0Y{height}D01*\nG01X8800000Y{height}D01*\nG01X8800000Y0D01*\nG01X0Y0D01*' in outline)
    left, right, cy = round((ir_x-1.65)*100000), round((ir_x+1.65)*100000), ir_y*100000
    check(f'D4 cutout: diameter 3.30 mm, centered at ({ir_x},{ir_y})',
          f'G01X{left}Y{cy}D02*\nG02X{right}Y{cy}I165000J0D01*' in outline
          and f'G02X{left}Y{cy}I-165000J0D01*' in outline)


report = {
    'profile': args.profile, 'archive': args.zip, 'sha256': hashlib.sha256(Path(args.zip).read_bytes()).hexdigest(),
    'checks': checks, 'npth_hits': npth, 'usb_slots': slots,
    'pth_round_hits': len(pth), 'via_reference_hits': len(via),
    'usb_npth_copper_clearance_mm': math.hypot(.01,.5)-.325,
    'manufacturing_released': False,
    'limitations': [
        'This checks selected exported geometry, not all clearances or connectivity.',
        'USB nominal 0.1751 mm NPTH clearance still requires JLC DFM acceptance.',
        'Combined PTH and separate via-reference drill overlap; do not count/drill them twice.',
        f'GKO carries D4 circular cutout at ({ir_x},{ir_y}), diameter 3.3 mm; assembly qualification remains open.',
        'Paste geometry correspondence does not approve stencil thickness or solder volume.'
    ]
}
Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
for c in checks:
    print(('PASS' if c['passed'] else 'FAIL')+': '+c['check'])
raise SystemExit(not all(c['passed'] for c in checks))
