"""Cross-check the dashboard against separate Decimal loops and hand arithmetic."""
import csv
from pathlib import Path
from decimal import Decimal
import pandas as pd
import pytest
from validation.independent_numbers import calculate, run_fixture, select
from views import build_view_data


def test_independent_fixture_against_all_dashboard_aggregates(lookup, context):
    result = run_fixture()
    assert result['status'] == 'PASS'
    path = Path(__file__).resolve().parents[1]/'validation/fixtures/invented_visits.csv'
    with path.open(newline='') as f:
        records = list(csv.DictReader(f))
    for selected in [records,select(records,mechanism='Fall'),select(records,severe_only=True),select(records,query='belt'),[]]:
        expected = calculate(selected)
        frame = pd.DataFrame(selected,columns=list(records[0]))
        frame['is_severe'] = frame.Disposition.isin(['2','4','5','8'])
        actual = build_view_data(frame,context=context,diagnosis_lookup=lookup)
        assert actual['headline']['weighted_ed_visits'] == float(expected['total_weight'])
        assert actual['headline']['record_count'] == expected['record_count']
        pct = expected['severe_pct']
        assert actual['headline']['severe_outcome_pct'] == (pytest.approx(float(pct),abs=1e-8) if pct is not None else None)
        for row in actual['mechanism_summary'].itertuples():
            m = expected['mechanisms'][row.injury_mechanism]
            assert row.weighted_ed_visits == float(m['weight']) and row.record_count == m['count']
            assert row.severe_outcome_pct == pytest.approx(float(m['severe_pct']),abs=1e-8)
        for row in actual['diagnosis_composition'].itertuples():
            code = 'Missing diagnosis' if pd.isna(row.diagnosis_code) else str(int(row.diagnosis_code))
            m = expected['mechanisms'][row.injury_mechanism]
            assert row.diagnosis_weighted_ed_visits == float(m['diagnosis'][code])
            assert row.diagnosis_pct == pytest.approx(float(m['diagnosis_pct'][code]),abs=1e-8)


def test_independent_rejects_duplicate_and_bad_weights():
    row = dict(CPSC_Case_Number='X',Weight='10',Disposition='4',Diagnosis='57',injury_mechanism='Fall')
    with pytest.raises(ValueError,match='duplicate'):
        calculate([row,row])
    with pytest.raises(ValueError,match='weight'):
        calculate([{**row,'Weight':'NaN'}])
