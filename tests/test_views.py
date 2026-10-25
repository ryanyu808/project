import pandas as pd
import pytest
from views import build_view_data, VIEW_REGISTRY, render_mechanism_bar, render_severity_scatter, render_diagnosis_stack, period_label, visit_axis
from filters import apply_filters, FilterSelection


def test_all_five_views(visits, lookup, context):
    original = visits.copy(deep=True)
    result = build_view_data(visits, context=context, diagnosis_lookup=lookup)
    assert result['status'] == 'ok'
    assert result['headline'] == dict(weighted_ed_visits=120, record_count=5, severe_outcome_pct=pytest.approx(100*50/120, abs=1e-8))
    assert result['quality'] == dict(unknown_disposition_record_count=1, unknown_disposition_weight=40)
    summary = result['mechanism_summary']
    assert summary.injury_mechanism.tolist() == ['Contact','Fall','Unknown/Unclassified']
    assert summary.weighted_ed_visits.tolist() == [60,40,20]
    assert summary.record_count.tolist() == [2,2,1]
    assert summary.severe_outcome_pct.tolist() == pytest.approx([100/3,25,100], abs=1e-8)
    comp = result['diagnosis_composition']
    for mechanism, total in zip(summary.injury_mechanism, summary.weighted_ed_visits):
        group = comp.loc[comp.injury_mechanism.eq(mechanism)]
        assert group.diagnosis_pct.sum() == pytest.approx(100, abs=1e-8)
        assert group.diagnosis_weighted_ed_visits.sum() == pytest.approx(total)
    assert comp.loc[comp.diagnosis_label.eq('Missing diagnosis'), 'diagnosis_pct'].iloc[0] == pytest.approx(200/3, abs=1e-8)
    assert comp.loc[comp.diagnosis_label.eq('53 - CONTUSIONS, ABR.'), 'diagnosis_pct'].iloc[0] == 75
    frame = visits.assign(Diagnosis_2=57)
    pd.testing.assert_frame_equal(build_view_data(frame, context=context, diagnosis_lookup=lookup)['diagnosis_composition'], comp)
    pd.testing.assert_frame_equal(original, visits)
    assert len(VIEW_REGISTRY) == 5
    bar = render_mechanism_bar(result,context)
    assert list(bar.data[0].x) == [60,40,20]
    scatter = render_severity_scatter(result,context)
    assert [(t.x[0],t.y[0]) for t in scatter.data] == pytest.approx([(60,100/3),(40,25),(20,100)])
    assert all(t.marker.size == 12 for t in scatter.data)
    assert sum(len(t.y) for t in scatter.data) == 3
    stack = render_diagnosis_stack(result,context)
    assert list(stack.layout.xaxis.range) == [0,100]
    assert list(stack.layout.yaxis.categoryarray) == summary.injury_mechanism.tolist()
    assert VIEW_REGISTRY['summary_table'](result,context).columns.tolist() == summary.columns.tolist()


@pytest.mark.parametrize('selection,total,count,pct,order', [
    (FilterSelection(mechanisms=('Fall',)),40,2,25,['Fall']),
    (FilterSelection(severities=('Severe',)),50,3,100,['Contact','Unknown/Unclassified','Fall']),
    (FilterSelection(narrative_query='belt'),30,2,100,['Contact','Fall']),
])
def test_filtered(visits, lookup, context, selection, total, count, pct, order):
    result = build_view_data(apply_filters(visits, selection), context=context, diagnosis_lookup=lookup)
    assert result['headline'] == dict(weighted_ed_visits=total,record_count=count,severe_outcome_pct=pct)
    assert result['mechanism_summary'].injury_mechanism.tolist() == order


@pytest.mark.parametrize('field,value', [('Weight',None),('Weight',0),('Weight',-1),('Weight',float('inf')),
    ('CPSC_Case_Number','B'),('CPSC_Case_Number',None),('injury_mechanism',''),('is_severe',False),('Treatment_Date','bad')])
def test_invalid_no_partial_totals(visits,lookup,context,field,value):
    visits[field] = visits[field].astype(object)
    visits.loc[0,field] = value
    result = build_view_data(visits,context=context,diagnosis_lookup=lookup)
    assert result['status'] == 'invalid_input'
    assert result['headline'] is None and result['quality'] is None
    assert result['mechanism_summary'].empty and result['diagnosis_composition'].empty


def test_missing_column(visits,lookup,context):
    result = build_view_data(visits.drop(columns='Weight'), context=context, diagnosis_lookup=lookup)
    assert result['status'] == 'invalid_input' and 'Weight' in result['messages'][0]


def test_empty(visits,lookup,context):
    result = build_view_data(visits.iloc[:0],context=context,diagnosis_lookup=lookup)
    assert result['status'] == 'empty'
    assert result['headline'] == dict(weighted_ed_visits=0,record_count=0,severe_outcome_pct=None)
    assert result['quality']['unknown_disposition_weight'] == 0
    assert not render_mechanism_bar(result,context).data
    assert not render_severity_scatter(result,context).data
    assert not render_diagnosis_stack(result,context).data


def test_fallback_and_dispositions(visits,lookup,context):
    visits.loc[0,'Disposition'] = 8
    visits.loc[3,'Disposition'] = None
    visits.loc[3,'Diagnosis'] = 999
    result = build_view_data(visits,context=context,diagnosis_lookup=lookup)
    assert result['headline']['severe_outcome_pct'] == pytest.approx(100*50/120,abs=1e-8)
    assert result['quality']['unknown_disposition_weight'] == 40
    bucket = result['diagnosis_composition'].query("diagnosis_label == 'Unmapped diagnosis (999)'")
    assert bucket.diagnosis_pct.iloc[0] == pytest.approx(200/3,abs=1e-8)
    diag = lookup.loc[lookup['Format name'].str.strip().eq('DIAG')].iloc[:1]
    duplicate = pd.concat([lookup,diag])
    assert build_view_data(visits,context=context,diagnosis_lookup=duplicate)['status'] == 'invalid_input'


def test_period_and_scope(visits,lookup,context):
    assert build_view_data(visits,context={**context,'source_scope':'sample'},diagnosis_lookup=lookup)['status'] == 'unavailable'
    assert build_view_data(visits.iloc[:0],context={**context,'source_scope':'sample'},diagnosis_lookup=lookup)['status'] == 'unavailable'
    earlier = visits.copy()
    earlier['Treatment_Date'] = pd.Timestamp('2023-01-01')
    earlier['CPSC_Case_Number'] += '-2023'
    context = {**context,'analysis_years':[2023,2025]}
    result = build_view_data(pd.concat([visits,earlier],ignore_index=True),context=context,diagnosis_lookup=lookup)
    assert result['headline']['weighted_ed_visits'] == 240 and result['headline']['record_count'] == 10
    assert result['headline']['severe_outcome_pct'] == pytest.approx(100*50/120,abs=1e-8)
    assert 'Sampling changed' in result['messages'][0]
    assert 'not annual' in period_label(context) and 'not annual' in visit_axis(context)
