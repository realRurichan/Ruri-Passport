"""Stage current BOM and historical quote candidates without approving matches.

Missing purchase fields never imply identical parts. Historical matches/prices are
reference-only and must be qualified against current specifications and footprints.
"""
import csv
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
review = root / 'review'
netlist = json.loads((review / 'schematic-current.enet').read_text())
history = json.loads((review / 'jlc-quote-round2-20260926.json').read_text())
by_ref = {}
by_code = {}
for row in history['rows']:
    for ref in row['designators'].split(','):
        by_ref[ref.strip()] = row
    if row.get('candidate_lcsc'):
        by_code[row['candidate_lcsc']] = row
rows = []
for part in netlist['components'].values():
    p = part['props']
    if p.get('Add into BOM') != 'yes':
        continue
    ref = p['Designator']
    current = p.get('Supplier Part', '')
    old = by_ref.get(ref, {})
    source = 'CURRENT_PROJECT_FIELD' if current else 'HISTORICAL_UNQUALIFIED_MATCH'
    code = current or old.get('candidate_lcsc', '')
    price = by_code.get(code, {}).get('unit_cny', '')
    rows.append(dict(designator=ref, current_value=p.get('Name', ''),
                     current_footprint=p.get('FootprintName', ''),
                     current_lcsc=current, candidate_lcsc=code,
                     candidate_mpn=p.get('Manufacturer Part', '') if current else old.get('candidate_mpn', ''),
                     mapping_source=source if code else 'MISSING',
                     historic_unit_cny=price, price_status='HISTORICAL_2026_09_26_NOT_LIVE' if price else 'UNPRICED',
                     historic_candidate_superseded=old.get('candidate_lcsc', '') if current and current != old.get('candidate_lcsc', '') else '',
                     release_status='NOT_FOR_ORDER'))
rows.sort(key=lambda r: (''.join(c for c in r['designator'] if not c.isdigit()), int(''.join(c for c in r['designator'] if c.isdigit()) or 0)))
with (review / 'quote-candidates-20260927.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
summary = dict(populated_components=len(rows), mapping_counts=dict(Counter(r['mapping_source'] for r in rows)),
               unpriced_components=[r['designator'] for r in rows if not r['historic_unit_cny']],
               changed_historical_matches=[{k:r[k] for k in ('designator','current_lcsc','historic_candidate_superseded')} for r in rows if r['historic_candidate_superseded']],
               manufacturing_released=False,
               warning='No total: historical candidate prices exclude setup, attrition, PCB and new/unpriced parts. Candidates are not qualified purchase selections.')
(review / 'quote-candidates-20260927.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(summary, ensure_ascii=False, indent=2))
