import json
from pathlib import Path
import pandas as pd
import pytest
from contracts import ORIGINAL, sha256
from prepare_data import candidates, finalize

ROOT = Path(__file__).resolve().parents[1]


def toy_source(tmp_path):
    rows = []
    for index, age in enumerate([0, 205, 64, 121, 65, 120, 75, 75, 75, 75]):
        row = dict.fromkeys(ORIGINAL, '')
        row.update(CPSC_Case_Number=str(index), Treatment_Date='2025-01-01', Age=age, Product_1=0, Product_2=0, Product_3=0,
                   Narrative_1='tReAdMiLl', Weight=10 * (index + 1), Disposition=4, Diagnosis=57)
        row['Product_' + str(index % 3 + 1)] = 3277
        rows.append(row)
    rows[7]['Narrative_1'] = 'bike'
    rows[8]['Product_3'] = 0
    rows[9]['Narrative_1'] = None
    source = tmp_path / 'toy.csv'
    pd.DataFrame(rows)[ORIGINAL].to_csv(source, index=False)
    return source


def toy_validator(prov, year):
    assert year == 2025
    assert prov['source_checks_passed']


def export(tmp_path):
    source = toy_source(tmp_path)
    digest = sha256(source)
    target = candidates(source, 2025, 'sample', tmp_path / 'out', ROOT / 'data/reference/neiss_code_lookup_2025.csv', _source_validator=toy_validator)
    assert sha256(source) == digest
    return target


def test_eligibility_and_review_gate(tmp_path):
    target = export(tmp_path)
    data = pd.read_csv(target)
    assert data.CPSC_Case_Number.tolist() == [4, 5, 6]
    with pytest.raises(ValueError, match='review'):
        finalize(target, target.with_name('treadmill_2025.reviews.csv'), target.parent / 'mechanism-codebook.md', target.parent, _source_validator=toy_validator)
    assert not (target.parent / 'treadmill_2025.csv').exists()


@pytest.mark.parametrize('failure', [None, 'missing', 'foreign', 'duplicate', 'pending', 'changed', 'excluded_reason', 'label'])
def test_finalize_boundary(tmp_path, failure):
    target = export(tmp_path)
    frame = pd.read_csv(target, dtype={'CPSC_Case_Number': str})
    frame['CPSC_Case_Number'] = ['P', 'Q', 'R']
    frame['Weight'] = [10, 20, 30]
    frame.to_csv(target, index=False)
    evidence_path = target.with_name('treadmill_2025.source.json')
    evidence = json.loads(evidence_path.read_text())
    evidence['candidate_sha256'] = sha256(target)
    evidence_path.write_text(json.dumps(evidence))
    reviews = pd.DataFrame({'CPSC_Case_Number': ['P','Q','R'], 'treadmill_confirmed': [True,True,False], 'injury_mechanism': ['Toy A','Toy B',''], 'reviewed': True, 'review_note': ['','','false mention']})
    if failure == 'missing': reviews = reviews.iloc[:2]
    if failure == 'foreign': reviews.loc[2, 'CPSC_Case_Number'] = 'X'
    if failure == 'duplicate': reviews.loc[2, 'CPSC_Case_Number'] = 'Q'
    if failure == 'pending': reviews.loc[1, 'reviewed'] = False
    if failure == 'changed': target.write_text(target.read_text() + '\n')
    if failure == 'excluded_reason': reviews.loc[2, 'review_note'] = ''
    if failure == 'label': reviews.loc[0, 'injury_mechanism'] = 'Other'
    review_path = target.with_name('treadmill_2025.reviews.csv')
    reviews.to_csv(review_path, index=False)
    args = (target, review_path, target.parent / 'mechanism-codebook.md', target.parent)
    if failure:
        with pytest.raises(ValueError):
            finalize(*args, _source_validator=toy_validator, _labels=['Toy A', 'Toy B'])
        assert not (target.parent / 'treadmill_2025.csv').exists()
    else:
        result = finalize(*args, _source_validator=toy_validator, _labels=['Toy A', 'Toy B'])
        final = pd.read_csv(result)
        assert final.CPSC_Case_Number.tolist() == ['P', 'Q']
        assert final.Weight.tolist() == [10, 20]
        prov = json.loads(result.with_suffix('.provenance.json').read_text())
        assert prov['prepared_row_count'] == 2 and prov['reviewed_candidate_count'] == 3
        assert prov['prepared_sha256'] == sha256(result)


@pytest.mark.parametrize('field,value', [('Weight', 0), ('CPSC_Case_Number', None), ('Treatment_Date', 'bad')])
def test_structural_source_failures(tmp_path, field, value):
    source = toy_source(tmp_path)
    data = pd.read_csv(source)
    data.loc[0, field] = value
    data.to_csv(source, index=False)
    with pytest.raises(ValueError, match='Structural'):
        candidates(source, 2025, 'sample', tmp_path / 'out', _source_validator=toy_validator)
    assert json.loads((tmp_path / 'out/treadmill_2025.quality.json').read_text())['exceptions']


def test_valid_zero_candidate_finalization(tmp_path):
    source = toy_source(tmp_path)
    data = pd.read_csv(source)
    data['Age'] = 20
    data.to_csv(source,index=False)
    target = candidates(source,2025,'sample',tmp_path/'out',_source_validator=toy_validator)
    result = finalize(target,target.with_name('treadmill_2025.reviews.csv'),target.parent/'mechanism-codebook.md',target.parent,_source_validator=toy_validator)
    assert pd.read_csv(result).empty
    prov = json.loads(result.with_suffix('.provenance.json').read_text())
    assert prov['prepared_row_count'] == prov['reviewed_candidate_count'] == 0
    assert prov['prepared_sha256'] == sha256(result)
