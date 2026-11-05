import json
import pandas as pd
import pytest
from contracts import sha256, MECHANISMS
from loader import _load_dashboard_data, load_dashboard_data
from tests.conftest import ROOT


def make_bundle(tmp_path, visits):
    # Loader fixture must satisfy real eligibility; UI fixture keeps prompt narratives.
    frame = visits.copy()
    frame['Narrative_1'] = 'TREADMILL'
    frame['injury_mechanism'] = frame.injury_mechanism.replace({'Contact': 'Belt contact'})
    csv = tmp_path / 'cohort.csv'
    frame.to_csv(csv, index=False)
    prov = dict(schema_version=1, analysis_years=[2025], source_scope='full_annual',
                source_checks_passed=True, source_files=[dict(path='invented', sha256='a'*64, row_count=5, column_count=25, min_date='2025-01-01', max_date='2025-01-01')],
                prepared_sha256=sha256(csv), prepared_row_count=len(frame), review_complete=True,
                reviewed_candidate_count=len(frame), codebook_version='1.2', review_sha256='b'*64, codebook_sha256=sha256(ROOT / 'data/prepared/mechanism-codebook.md'))
    path = tmp_path / 'provenance.json'
    path.write_text(json.dumps(prov))
    return csv, path, ROOT / 'data/reference/neiss_code_lookup_2025.csv', 2025


def test_valid_and_empty_loader(tmp_path, visits):
    for frame in [visits, visits.iloc[:0]]:
        args = make_bundle(tmp_path, frame)
        loaded = _load_dashboard_data(*args, source_validator=lambda p,y: None)
        assert set(loaded) == {'data', 'diagnosis_lookup', 'provenance', 'metadata'}
        assert loaded['metadata']['prepared_record_count'] == len(frame)
        assert loaded['metadata']['record_counts_by_year'] == {2025: len(frame)}
        assert loaded['metadata']['age_min'] == (70 if len(frame) else None)


@pytest.mark.parametrize('failure', ['digest','year','scope','review','evidence','column','duplicate','bool','severe','label','weight','age','product','text'])
def test_bad_bundle(tmp_path, visits, failure):
    csv, path, lookup, year = make_bundle(tmp_path, visits)
    prov = json.loads(path.read_text())
    frame = pd.read_csv(csv)
    if failure == 'digest': prov['prepared_sha256'] = '0'*64
    if failure == 'year': prov['analysis_years'] = [2024]
    if failure == 'scope': prov['source_scope'] = 'test_fixture'
    if failure == 'review': prov['review_complete'] = False
    if failure == 'evidence': prov['source_checks_passed'] = False
    if failure == 'column': frame = frame.drop(columns='PSU')
    if failure == 'duplicate': frame.loc[1, 'CPSC_Case_Number'] = 'A'
    if failure == 'bool': frame['is_severe'] = 'yes'
    if failure == 'severe': frame.loc[0, 'is_severe'] = False
    if failure == 'label': frame.loc[0, 'injury_mechanism'] = ''
    if failure == 'weight': frame.loc[0, 'Weight'] = 0
    if failure == 'age': frame.loc[0, 'Age'] = 64
    if failure == 'product': frame.loc[0, 'Product_1'] = 0
    if failure == 'text': frame.loc[0, 'Narrative_1'] = 'bike'
    frame.to_csv(csv, index=False)
    if failure != 'digest': prov['prepared_sha256'] = sha256(csv)
    path.write_text(json.dumps(prov))
    def toy_source(p, y):
        if p['analysis_years'] != [y] or p['source_scope'] != 'full_annual' or not p['source_checks_passed']:
            raise ValueError('test source evidence')
    with pytest.raises(ValueError):
        _load_dashboard_data(csv, path, lookup, year, source_validator=toy_source)


def test_no_production_toy_counts(tmp_path, visits):
    with pytest.raises(ValueError, match='baseline'):
        load_dashboard_data(*make_bundle(tmp_path, visits))


@pytest.mark.parametrize('code,flag', [(2,True),(4,True),(5,True),(8,True),(0,False),(1,False),(6,False),(9,False),(None,False),(999,False)])
def test_severity(tmp_path, visits, code, flag):
    frame = visits.iloc[:1].copy()
    frame['Disposition'], frame['is_severe'] = code, flag
    loaded = _load_dashboard_data(*make_bundle(tmp_path, frame), source_validator=lambda p,y: None)
    assert bool(loaded['data'].iloc[0].is_severe) is flag
