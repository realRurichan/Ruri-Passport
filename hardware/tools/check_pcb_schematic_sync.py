"""Compare saved native PCB pad nets and purchasing attributes with native ENET.

This verifies synchronization, not copper connectivity or electrical correctness.
Run native PCB DRC separately after routing and copper-pour rebuilding.
"""
import argparse
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--pcb', type=Path, default=root/'eda/Ruri-Passport-RevA/pcb/Mainboard.epcb2')
p.add_argument('--netlist', type=Path, default=root/'review/schematic-current.enet')
p.add_argument('--report', type=Path)
a = p.parse_args()
docs = {}
doc = None
for line in a.pcb.read_text().splitlines():
    head, body = line.split('||', 1)
    head = json.loads(head)
    body = body.removesuffix('|')
    value = json.loads(body) if body else None
    if head['type'] == 'DOCHEAD':
        doc = (value['docType'], value['uuid'])
        docs.setdefault(doc, {})
    docs[doc][(head['type'], head.get('id', head['type']))] = value
board = next(rows for (kind, _), rows in docs.items() if kind == 'PCB')
components = {i:v for (t,i),v in board.items() if t == 'COMPONENT' and v}
attrs = {i:dict(v.get('attrs', {})) for i,v in components.items()}
pad_nets = {}
for (kind, ident), value in board.items():
    if not value:
        continue
    if kind == 'ATTR' and value['parentId'] in attrs:
        if value.get('value') is not None:
            attrs[value['parentId']][value['key']] = value['value']
    elif kind == 'PAD_NET':
        _, component, number, _ = json.loads(ident)
        pad_nets.setdefault((component, str(number)), set()).add(value.get('padNet') or '')
for cid, instance in attrs.items():
    device = docs.get(('DEVICE', instance.get('Device')), {})
    defaults = next((v.get('attributes', {}) for (t,_),v in device.items()
                     if t == 'META' and v), {})
    attrs[cid] = {**defaults, **instance}
refs = {v['Designator']:i for i,v in attrs.items()}
sch = json.loads(a.netlist.read_text())['components']
errors = []
checked = 0
if len(refs) != len(components):
    errors.append('PCB has duplicate designators')
expected_refs = set()
for part in sch.values():
    props = part['props']
    if props.get('Convert to PCB') == 'no':
        continue
    ref = props['Designator']
    expected_refs.add(ref)
    if ref not in refs:
        errors.append(f'{ref}: missing PCB component')
        continue
    cid = refs[ref]
    actual = attrs[cid]
    fp = docs.get(('FOOTPRINT', actual.get('Footprint')), {})
    numbers = {str(v['num']) for (t,_),v in fp.items() if t == 'PAD' and v}
    for number, pin in part['pinInfoMap'].items():
        checked += 1
        want = pin.get('net') or ''
        if str(number) not in numbers:
            errors.append(f'{ref}.{number}: no corresponding footprint pad')
        got = pad_nets.get((cid, str(number)), {''})
        if got != {want}:
            errors.append(f'{ref}.{number}: schematic={want!r}, PCB={sorted(got)!r}')
    for key in ('Add into BOM', 'Supplier Part', 'Manufacturer Part'):
        if (props.get(key) or '') != (actual.get(key) or ''):
            errors.append(f'{ref}: {key} differs: schematic={props.get(key)!r}, PCB={actual.get(key)!r}')
for ref in sorted(set(refs)-expected_refs):
    errors.append(f'{ref}: PCB component absent from schematic')
report = {'method':'native PCB PAD_NET/footprint pads vs native schematic ENET; not a routing/DRC check',
          'components':len(components), 'pin_net_checks':checked, 'errors':errors}
if a.report:
    a.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(f'{len(components)} PCB components, {checked} pad-net checks, {len(errors)} mismatches')
for error in errors:
    print(error)
raise SystemExit(bool(errors))
