"""New MVP behavior, using invented records only."""
import json
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from tests.support import fixture_app
from filters import apply_filters, FilterSelection, without_severity
from views import build_severity_comparison, render_severity_comparison


def test_cr01_baseline_and_selected_burden(visits, lookup, context):
    selection = FilterSelection(severities=('Severe',))
    original = visits.copy(deep=True)
    selected = apply_filters(visits, selection)
    table = build_severity_comparison(selected, visits, context=context, diagnosis_lookup=lookup).set_index('injury_mechanism')
    assert table.loc['Fall', 'baseline_severe_outcome_pct'] == 25
    assert table.loc['Fall', 'selected_severe_weighted_ed_visits'] == 10
    assert table.loc['Contact', 'baseline_severe_outcome_pct'] == pytest.approx(100/3)
    assert table.loc['Contact', 'baseline_weighted_ed_visits'] == 60
    assert table.selected_severe_weighted_ed_visits.sum() == 50
    pd.testing.assert_frame_equal(visits, original)
    empty = build_severity_comparison(selected.iloc[:0], visits, context=context, diagnosis_lookup=lookup)
    assert empty.selected_severe_weighted_ed_visits.sum() == 0
    assert build_severity_comparison(selected, visits, context={**context, 'source_scope':'sample'}, diagnosis_lookup=lookup) is None


def test_cr01_baseline_respects_search_and_mechanism(visits, lookup, context):
    choice = FilterSelection(('Fall',), ('Other known disposition',), 'belt')
    base_choice = without_severity(choice)
    assert base_choice.mechanisms == ('Fall',) and base_choice.narrative_query == 'belt'
    assert not base_choice.severities and choice.severities
    baseline = apply_filters(visits, base_choice)
    table = build_severity_comparison(apply_filters(visits, choice), baseline, context=context, diagnosis_lookup=lookup)
    assert table.baseline_weighted_ed_visits.tolist() == [10]
    assert table.baseline_severe_outcome_pct.tolist() == [100]
    assert table.selected_severe_weighted_ed_visits.tolist() == [0]


def test_cr01_ui_baseline_reset():
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    at.multiselect[1].set_value(['Severe']).run()
    assert not at.exception
    assert [m.value for m in at.metric] == ['50','3','100.0%']
    chart = json.loads(at.get('plotly_chart')[1].proto.spec)
    assert 'baseline' in chart['layout']['yaxis']['title']['text']
    points = {t['text'][0]:(t['x'][0],t['y'][0]) for t in chart['data']}
    assert points['Fall'] == (10,25)
    at.button[0].click().run()
    chart = json.loads(at.get('plotly_chart')[1].proto.spec)
    assert 'baseline' not in chart['layout']['yaxis']['title']['text']


def test_cr02_unknowns_by_mechanism(visits, lookup, context):
    from views import build_supporting_evidence
    table = build_supporting_evidence(visits, context=context, diagnosis_lookup=lookup).set_index('injury_mechanism')
    assert table.loc['Contact', 'unknown_disposition_record_count'] == 1
    assert table.loc['Contact', 'unknown_disposition_weight'] == 40
    assert table.loc['Contact', 'record_count'] == 2
    assert table.loc['Contact', 'severe_outcome_pct'] == pytest.approx(100/3)
    assert table.loc['Unknown/Unclassified', 'record_count'] == 1
    assert table.loc['Fall', 'unknown_disposition_weight'] == 0
    for code in [None, 999]:
        changed = visits.copy()
        changed.loc[3, 'Disposition'] = code
        assert build_supporting_evidence(changed, context=context, diagnosis_lookup=lookup).unknown_disposition_weight.sum() == 40
    assert build_supporting_evidence(visits.iloc[:0], context=context, diagnosis_lookup=lookup).empty
    assert build_supporting_evidence(visits, context={**context,'source_scope':'sample'}, diagnosis_lookup=lookup) is None


def test_cr02_visible_evidence_and_severity_population():
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    evidence = at.dataframe[1].value
    assert evidence.record_count.sum() == 5
    assert evidence.unknown_disposition_weight.sum() == 40
    assert any('not confidence intervals' in c.value for c in at.caption)
    at.multiselect[1].set_value(['Severe']).run()
    assert at.dataframe[1].value.record_count.sum() == 3
    assert at.dataframe[1].value.unknown_disposition_record_count.sum() == 0
    assert at.dataframe[2].value.baseline_record_count.sum() == 5
    at.text_input[0].set_value('nothing matches this').run()
    assert not at.exception and at.dataframe[1].value.empty


def test_cr04_exact_search_records_respect_all_filters():
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    assert not any('Matching narrative records' == x.value for x in at.subheader)
    at.text_input[0].set_value('  BeLt  ').run()
    matches = at.dataframe[-1].value
    assert matches.CPSC_Case_Number.tolist() == ['A','C']
    assert matches.Narrative_1.tolist() == ['FELL from treadmill belt','Hand caught in BELT']
    at.multiselect[0].set_value(['Fall']).run()
    assert at.dataframe[-1].value.CPSC_Case_Number.tolist() == ['A']
    at.multiselect[1].set_value(['Other known disposition']).run()
    assert at.dataframe[-1].value.empty and not at.exception
    at.text_input[0].set_value('fall.*').run()
    assert at.dataframe[-1].value.empty
    at.button[0].click().run()
    assert not any('Matching narrative records' == x.value for x in at.subheader)


def test_cr07_committed_codebook_visible_and_review_meaning():
    from codebook import read_codebook
    text = read_codebook()
    assert text.startswith('Version: 1.2')
    assert 'if a general fall merely lands on the belt' in text
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    assert any(e.label == 'Mechanism definitions · codebook 1.2' for e in at.expander)
    assert any(text.strip() == m.value.strip() for m in at.markdown)
    assert any('never unfinished review' in c.value for c in at.caption)
    at.multiselect[0].set_value(['Fall']).run()
    assert not at.exception and at.metric[1].value == '2'


def test_cr07_missing_or_wrong_version_is_explicit(tmp_path):
    from codebook import read_codebook
    with pytest.raises(FileNotFoundError):
        read_codebook(tmp_path/'missing.md')
    path = tmp_path/'wrong.md'
    path.write_text('Version: 2.0')
    with pytest.raises(ValueError, match='version 1.2'):
        read_codebook(path)


def test_cr03_diagnosis_baseline_preserves_overall_mix(visits, lookup, context):
    from views import build_view_data
    selection = FilterSelection(('Fall',), ('Severe',), '')
    selected = build_view_data(apply_filters(visits, selection), context=context, diagnosis_lookup=lookup)['diagnosis_composition']
    base = build_view_data(apply_filters(visits, without_severity(selection)), context=context, diagnosis_lookup=lookup)['diagnosis_composition']
    assert selected.diagnosis_pct.tolist() == [100]
    assert dict(zip(base.diagnosis_code, base.diagnosis_pct)) == {53:75,57:25}
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    at.multiselect[0].set_value(['Fall']).run()
    at.multiselect[1].set_value(['Severe']).run()
    assert len(at.get('plotly_chart')) == 4 and not at.exception
    chart = json.loads(at.get('plotly_chart')[3].proto.spec)
    shares = {t['name']:t['x'][0] for t in chart['data']}
    assert shares['53 - CONTUSIONS, ABR.'] == 75
    assert shares['57 - FRACTURE'] == 25
    at.text_input[0].set_value('nothing matches').run()
    assert not at.exception
    at.button[0].click().run()
    assert len(at.get('plotly_chart')) == 3


def test_cr05_undo_restores_all_controls_and_is_session_local():
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    assert at.button[1].disabled
    at.multiselect[0].set_value(['Fall']).run()
    at.multiselect[1].set_value(['Severe']).run()
    at.text_input[0].set_value('belt').run()
    at.button[0].click().run()
    assert at.metric[1].value == '5' and not at.button[1].disabled
    at.button[1].click().run()
    assert at.multiselect[0].value == ['Fall'] and at.multiselect[1].value == ['Severe']
    assert at.text_input[0].value == 'belt' and at.metric[1].value == '1'
    assert at.button[1].disabled and not at.exception
    other = AppTest.from_function(fixture_app, default_timeout=20).run()
    assert other.button[1].disabled and other.metric[1].value == '5'
    at.button[0].click().run()
    at.button[0].click().run()
    at.button[1].click().run()
    assert at.multiselect[0].value == [] and at.text_input[0].value == ''


def test_cr06_conditional_endpoints_and_empty(visits, lookup, context):
    from views import build_outcome_completeness
    result = build_outcome_completeness(visits, context=context, diagnosis_lookup=lookup)
    assert result['total_weight'] == 120 and result['recorded_severe_weight'] == 50
    assert result['unknown_weight'] == 40
    assert result['unknown_share_pct'] == pytest.approx(100/3)
    assert result['none_unknown_severe_pct'] == pytest.approx(100*50/120)
    assert result['all_unknown_severe_pct'] == 75
    severe = apply_filters(visits, FilterSelection(severities=('Severe',)))
    result = build_outcome_completeness(severe, context=context, diagnosis_lookup=lookup)
    assert result['unknown_weight'] == 0 and result['all_unknown_severe_pct'] == 100
    unknown = apply_filters(visits, FilterSelection(severities=('Unknown',)))
    result = build_outcome_completeness(unknown, context=context, diagnosis_lookup=lookup)
    assert result['none_unknown_severe_pct'] == 0 and result['all_unknown_severe_pct'] == 100
    assert build_outcome_completeness(visits.iloc[:0], context=context, diagnosis_lookup=lookup) is None


def test_cr06_ui_population_and_unavailable():
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    assert at.table[0].value.set_index('Measure').loc['Upper conditional endpoint (%)','Value'] == 75
    assert any('not confidence intervals' in c.value for c in at.caption)
    at.multiselect[1].set_value(['Severe']).run()
    assert at.table[0].value.set_index('Measure').loc['Unknown outcome weight (U)','Value'] == 0
    at.text_input[0].set_value('no records here').run()
    assert not at.exception and len(at.table) == 1
    assert any('Outcome completeness unavailable' in i.value for i in at.info)


def test_cr08_rounding_export_precision_and_metadata(visits, lookup, context):
    import csv, io
    from decimal import Decimal
    from views import build_view_data, build_weight_reconciliation
    frame = visits.iloc[[0,2,4]].copy()
    frame['Weight'] = 10.4
    result = build_view_data(frame, context=context, diagnosis_lookup=lookup)
    report = build_weight_reconciliation(result, context, {'prepared_sha256':'a'*64})
    assert report['contribution_sum'] == pytest.approx(31.2)
    assert report['rounded_headline'] == '31'
    assert report['sum_of_rounded_contributions'] == 30
    rows = list(csv.DictReader(io.StringIO(report['csv'].decode('utf-8-sig'))))
    contributions = [r for r in rows if r['row_type']=='mechanism']
    assert sum(Decimal(r['weighted_ed_visits']) for r in contributions) == Decimal('31.2')
    assert all(r['prepared_sha256']=='a'*64 and r['active_filters']=='all' for r in rows)
    assert rows[-1]['row_type']=='selected_total' and rows[-1]['record_count']=='3'
    result['headline']['weighted_ed_visits'] = 100
    with pytest.raises(ValueError, match='reconcile'):
        build_weight_reconciliation(result, context, {})


def test_cr08_ui_download_and_empty():
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    assert len(at.get('download_button')) == 1 and not at.exception
    assert any('test_fixture' in c.value for c in at.caption)
    at.text_input[0].set_value('no match').run()
    assert not at.exception and len(at.get('download_button')) == 1
