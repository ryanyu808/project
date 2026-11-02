"""Candidate Module 10 property tests on invented records."""
import pandas as pd
import pytest
from views import build_view_data


def test_record_order_does_not_change_reported_numbers(visits, lookup, context):
    original = visits.copy(deep=True)
    reordered = visits.iloc[[4, 2, 0, 3, 1]].reset_index(drop=True)
    before = build_view_data(visits, context=context, diagnosis_lookup=lookup)
    after = build_view_data(reordered, context=context, diagnosis_lookup=lookup)
    assert before['status'] == after['status'] == 'ok'
    assert after['headline'] == before['headline']
    assert after['quality'] == before['quality']
    for name, keys in [
        ('mechanism_summary', ['injury_mechanism']),
        ('diagnosis_composition', ['injury_mechanism', 'diagnosis_label']),
    ]:
        expected = before[name].sort_values(keys).reset_index(drop=True)
        actual = after[name].sort_values(keys).reset_index(drop=True)
        pd.testing.assert_frame_equal(actual, expected)
    pd.testing.assert_frame_equal(visits, original)


def test_uniform_weight_scaling_preserves_shares_and_counts(visits, lookup, context):
    scaled = visits.copy(deep=True)
    scaled['Weight'] = scaled['Weight'] * 2.5
    before = build_view_data(visits, context=context, diagnosis_lookup=lookup)
    after = build_view_data(scaled, context=context, diagnosis_lookup=lookup)
    assert before['status'] == after['status'] == 'ok'
    assert after['headline']['weighted_ed_visits'] == pytest.approx(300)
    assert after['headline']['record_count'] == 5
    assert after['headline']['severe_outcome_pct'] == pytest.approx(100 * 125 / 300)
    assert after['quality']['unknown_disposition_weight'] == pytest.approx(100)
    assert after['quality']['unknown_disposition_record_count'] == 1
    for name, keys, weight_column, share_column in [
        ('mechanism_summary', ['injury_mechanism'], 'weighted_ed_visits', 'severe_outcome_pct'),
        ('diagnosis_composition', ['injury_mechanism', 'diagnosis_label'], 'diagnosis_weighted_ed_visits', 'diagnosis_pct'),
    ]:
        expected = before[name].sort_values(keys).reset_index(drop=True)
        actual = after[name].sort_values(keys).reset_index(drop=True)
        assert actual[weight_column].tolist() == pytest.approx((expected[weight_column] * 2.5).tolist())
        assert actual[share_column].tolist() == pytest.approx(expected[share_column].tolist())
        if name == 'mechanism_summary':
            assert actual['record_count'].tolist() == expected['record_count'].tolist()
