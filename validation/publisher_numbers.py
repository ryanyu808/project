"""R7: standalone original-workbook audit; imports no application modules.

Get neiss2025.xlsx via CPSC > Access NEISS > Archived Annual Data > 2025:
https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data
https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/2025/neiss2025.xlsx
Only the immutable reviewed ID/label decisions are supplied separately.
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from openpyxl import load_workbook

SOURCE_SHA = 'a784574c98a95175342f34d59cf19c61e73dc343e77791bf6b6564e49bbbb066'


def audit(source, decisions):
    source, decisions = Path(source), Path(decisions)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != SOURCE_SHA:
        raise ValueError('Source differs from the reviewed original workbook; investigate before proceeding')
    with decisions.open(encoding='utf-8-sig', newline='') as f:
        labels = list(csv.DictReader(f))
    ids = {r['CPSC_Case_Number']: r['injury_mechanism'] for r in labels}
    if len(ids) != len(labels) or not ids or not all(ids.values()):
        raise ValueError('Duplicate IDs, missing labels or empty reviewed decisions')
    book = load_workbook(source, read_only=True, data_only=True)
    sheet = book['NEISS_2025']
    rows = sheet.iter_rows(values_only=True)
    header = next(rows)
    total_rows = 0
    screened = set()
    kept = []
    dates = set()
    for values in rows:
        if all(v is None for v in values):
            continue
        total_rows += 1
        r = dict(zip(header, values))
        case = str(int(r['CPSC_Case_Number']))
        date = r['Treatment_Date']
        dates.add(date.date().isoformat())
        if not (date.year == 2025 and 65 <= r['Age'] <= 120
                and any(r[f'Product_{i}'] == 3277 for i in (1, 2, 3))
                and 'treadmill' in str(r['Narrative_1'] or '').casefold()):
            continue
        if case in screened:
            raise ValueError('Duplicate screened source ID')
        screened.add(case)
        if case in ids:
            kept.append((ids[case], Decimal(str(r['Weight'])), r['Disposition'], r['Diagnosis']))
    book.close()
    if not set(ids) <= screened:
        raise ValueError('Reviewed ID outside independently screened source population')
    groups = defaultdict(lambda: dict(records=0, weight=Decimal(0), severe_records=0,
                                     severe_weight=Decimal(0), fracture_weight=Decimal(0)))
    for mechanism, weight, disposition, diagnosis in kept:
        for key in ('ALL', mechanism):
            g = groups[key]
            g['records'] += 1
            g['weight'] += weight
            if disposition in (2, 4, 5, 8):
                g['severe_records'] += 1
                g['severe_weight'] += weight
            if diagnosis == 57:
                g['fracture_weight'] += weight
    for g in groups.values():
        g['severe_pct'] = 100 * g['severe_weight'] / g['weight']
        g['fracture_pct'] = 100 * g['fracture_weight'] / g['weight']
    a, fall, belt = (groups[k] for k in ('ALL', 'Fall', 'Belt contact'))
    main = dict(total_weight=a['weight'], record_count=a['records'], severe_pct=a['severe_pct'],
                fall_weight=fall['weight'], fall_severe_pct=fall['severe_pct'],
                belt_severe_pct=belt['severe_pct'], fall_severe_records=fall['severe_records'],
                fall_fracture_pct=fall['fracture_pct'])
    return dict(source_filename=source.name, source_bytes=source.stat().st_size,
                source_sha256=digest, source_rows=total_rows, source_columns=len(header),
                first_date=min(dates), last_date=max(dates), screened=len(screened),
                included=len(kept), excluded=len(screened)-len(kept),
                decisions_sha256=hashlib.sha256(decisions.read_bytes()).hexdigest(),
                main_results=main, mechanisms=dict(groups))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--decisions', type=Path, default=Path(__file__).with_name('reviewed_ids.csv'))
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    result = json.dumps(audit(args.source, args.decisions), indent=2, default=str)
    print(result)
    if args.output:
        args.output.write_text(result+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
