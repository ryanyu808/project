import pandas as pd
import pytest
from filters import apply_filters, FilterSelection


@pytest.mark.parametrize('mechanisms,severities,query,ids', [
    ((),(),'', 'ABCDE'), (('Fall',),(),'', 'AB'),
    (('Fall',),('Severe',),'belt', 'A'), ((),('Severe','Unknown'),'', 'ACDE'),
    ((),(),'  belt  ', 'AC'), ((),(),'   ', 'ABCDE'), ((),(),'fall.*', ''),
    ((),('Unknown',),'', 'D'), ((),('Other known disposition',),'', 'B'),
])
def test_filters(visits, mechanisms, severities, query, ids):
    original = visits.copy(deep=True)
    selected = apply_filters(visits, FilterSelection(mechanisms, severities, query))
    assert selected.CPSC_Case_Number.tolist() == list(ids)
    pd.testing.assert_frame_equal(visits, original)
    pd.testing.assert_frame_equal(selected, visits.loc[visits.CPSC_Case_Number.isin(list(ids))])
    assert 'Severity' not in selected


def test_invalid_selection(visits):
    with pytest.raises(ValueError, match='invalid selection'):
        apply_filters(visits, FilterSelection(severities=('Mild',)))
    with pytest.raises(ValueError, match='Narrative_1'):
        apply_filters(visits.drop(columns='Narrative_1'), FilterSelection())


@pytest.mark.parametrize('disposition', [None, 999, 9])
def test_unknown(visits, disposition):
    visits.loc[3, 'Disposition'] = disposition
    assert apply_filters(visits, FilterSelection(severities=('Unknown',))).CPSC_Case_Number.tolist() == ['D']


def test_exact_section_04_fixture():
    frame = pd.DataFrame({
        'injury_mechanism':['Fall','Fall','Belt contact','Unknown/Unclassified'],
        'Disposition':[4,1,2,9], 'is_severe':[True,False,True,False],
        'Narrative_1':['FELL from treadmill belt','Tripped beside treadmill','Hand caught in BELT',None],
        'Weight':[10,20,30,40]}, index=list('ABCD'))
    assert apply_filters(frame,FilterSelection()).index.tolist() == list('ABCD')
    assert apply_filters(frame,FilterSelection(mechanisms=('Fall','Belt contact'))).index.tolist() == list('ABC')
    assert apply_filters(frame,FilterSelection(mechanisms=('Fall',),severities=('Severe',))).index.tolist() == ['A']
    assert apply_filters(frame,FilterSelection(severities=('Severe','Unknown'))).index.tolist() == list('ACD')
    assert apply_filters(frame,FilterSelection(narrative_query='  belt  ')).index.tolist() == list('AC')
    assert apply_filters(frame,FilterSelection(narrative_query='fall.*')).empty
    assert apply_filters(frame,FilterSelection(narrative_query=' ')).Weight.tolist() == [10,20,30,40]
