"""Independent csv/Decimal arithmetic. No pandas or dashboard aggregation imports.

Default input is an INVENTED fixture, never a real NEISS finding.
"""
import argparse
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEVERE = {2, 4, 5, 8}


def calculate(rows):
    total = Decimal(0)
    severe = Decimal(0)
    mechanisms = {}
    seen = set()
    for r in rows:
        case = r['CPSC_Case_Number']
        if not case or case in seen:
            raise ValueError('Missing/duplicate visit ID')
        seen.add(case)
        weight = Decimal(r['Weight'])
        if not weight.is_finite() or weight <= 0:
            raise ValueError('Invalid weight')
        code = int(r['Disposition']) if r['Disposition'] else None
        is_severe = code in SEVERE
        mechanism = r['injury_mechanism']
        if not mechanism:
            raise ValueError('Missing mechanism')
        total += weight
        severe += weight if is_severe else 0
        m = mechanisms.setdefault(mechanism, dict(weight=Decimal(0), count=0, severe_weight=Decimal(0), diagnosis={}))
        m['weight'] += weight
        m['count'] += 1
        m['severe_weight'] += weight if is_severe else 0
        diagnosis = r['Diagnosis'] or 'Missing diagnosis'
        m['diagnosis'][diagnosis] = m['diagnosis'].get(diagnosis, Decimal(0)) + weight
    for m in mechanisms.values():
        m['severe_pct'] = 100*m['severe_weight']/m['weight']
        m['diagnosis_pct'] = {code:100*weight/m['weight'] for code,weight in m['diagnosis'].items()}
    return dict(total_weight=total, record_count=len(rows), severe_weight=severe,
                severe_pct=100*severe/total if total else None, mechanisms=mechanisms)


def select(rows, mechanism=None, severe_only=False, query=''):
    result = []
    for row in rows:
        if mechanism and row['injury_mechanism'] != mechanism:
            continue
        if severe_only and (not row['Disposition'] or int(row['Disposition']) not in SEVERE):
            continue
        if query.strip().casefold() not in row['Narrative_1'].casefold():
            continue
        result.append(row)
    return result


def run_fixture():
    path = HERE/'fixtures/invented_visits.csv'
    with path.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    result = calculate(rows)
    assert result['total_weight'] == 120 and result['record_count'] == 5
    assert result['severe_weight'] == 50 and abs(result['severe_pct']-Decimal(125)/3) < Decimal('1e-20')
    assert {k:v['weight'] for k,v in result['mechanisms'].items()} == {'Fall':40,'Contact':60,'Unknown/Unclassified':20}
    assert result['mechanisms']['Fall']['diagnosis_pct'] == {'57':25,'53':75}
    assert result['mechanisms']['Contact']['diagnosis']['Missing diagnosis'] == 40
    scenarios = {}
    for name,selection,expected in [
        ('Fall',dict(mechanism='Fall'),(40,2,25)),
        ('Severe',dict(severe_only=True),(50,3,100)),
        ('belt',dict(query='  BeLt  '),(30,2,100)),
        ('empty',dict(query='no match whatsoever'),(0,0,None)),
    ]:
        value = calculate(select(rows,**selection))
        assert (value['total_weight'],value['record_count'],value['severe_pct']) == expected
        scenarios[name] = value
    for m in result['mechanisms'].values():
        assert abs(sum(m['diagnosis_pct'].values())-100) < Decimal('1e-20')
    return dict(source_scope='INVENTED_TEST_FIXTURE_NOT_NEISS_FINDINGS',
                method='Python csv + Decimal + explicit loops; hand-worked expected values',
                fixture_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                status='PASS', unfiltered=result, scenarios=scenarios)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'results/fixture_results.json')
    parser.add_argument('--cohort',type=Path)
    parser.add_argument('--provenance',type=Path)
    args = parser.parse_args()
    if args.cohort:
        if not args.provenance:
            parser.error('Real cohort calculation requires matching finalized --provenance')
        prov = json.loads(args.provenance.read_text(encoding='utf-8'))
        if (prov.get('review_complete') is not True or prov.get('source_scope') != 'full_annual'
                or hashlib.sha256(args.cohort.read_bytes()).hexdigest() != prov.get('prepared_sha256')):
            raise ValueError('Reviewed full-annual matching cohort required')
        with args.cohort.open(encoding='utf-8',newline='') as f:
            rows = list(csv.DictReader(f))
        if len(rows) != prov['prepared_row_count']:
            raise ValueError('Prepared count mismatch')
        result = dict(source_scope='full_annual', prepared_sha256=prov['prepared_sha256'],
                      note='Independent arithmetic only; source and genuine human review must also be verified.',
                      values=calculate(rows))
    else:
        result = run_fixture()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
    print(f"Independent arithmetic saved to {args.output}")


if __name__ == '__main__':
    main()
