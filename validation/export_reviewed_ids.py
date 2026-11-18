"""One-time R7 export of existing genuine decisions; no new adjudication.

Private notes never enter the public allowlist. Original source-bound review hash
must match the release provenance. This is not the independent number checker.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    review = ROOT/'data/prepared/treadmill_2025.human_approved.reviews.csv'
    prov = json.loads((ROOT/'data/prepared/treadmill_2025.provenance.json').read_text())
    assert hashlib.sha256(review.read_bytes()).hexdigest() == prov['review_sha256']
    with review.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == prov['reviewed_candidate_count']
    assert len({r['CPSC_Case_Number'] for r in rows}) == len(rows)
    assert all(r['reviewed'] == 'True' for r in rows)
    included = [r for r in rows if r['treadmill_confirmed'] == 'True']
    assert len(included) == prov['prepared_row_count']
    target = ROOT/'validation/reviewed_ids.csv'
    with target.open('x', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['CPSC_Case_Number','injury_mechanism'], lineterminator='\n')
        writer.writeheader()
        writer.writerows({k:r[k] for k in writer.fieldnames} for r in included)
    print(f'Exported {len(included)} existing reviewed ID/label decisions; {len(rows)-len(included)} exclusions remain excluded; no private notes exported.')


if __name__ == '__main__':
    main()
