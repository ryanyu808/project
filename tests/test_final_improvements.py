"""Decision interpretation and complete evidence browsing; invented boundary cases."""
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from tests.support import fixture_app
from views import estimate_cautions


@pytest.mark.parametrize('weight,count,reasons',[
    (1199.9999,20,['estimate below 1,200']),
    (1200,19,['fewer than 20 records']),
    (1200,20,[]),
    (0,0,['estimate below 1,200','fewer than 20 records']),
])
def test_cpsc_strict_boundaries_without_claiming_cv(weight,count,reasons):
    table=pd.DataFrame([dict(injury_mechanism='Invented',weighted_ed_visits=weight,record_count=count)])
    before=table.copy(deep=True)
    row=estimate_cautions(table)[0]
    assert row['reasons']==reasons
    if not reasons:assert 'stability not established' in row['assessment']
    pd.testing.assert_frame_equal(table,before)


def test_browse_blank_search_and_exact_membership_after_reset():
    app=AppTest.from_function(fixture_app,default_timeout=20).run()
    table=lambda:next(d.value for d in app.dataframe if 'Narrative_1' in d.value.columns)
    assert set(table().CPSC_Case_Number)=={'A','B','C','D','E'}
    app.multiselect[0].set_value(['Fall']).run()
    assert table().CPSC_Case_Number.tolist()==['A','B']
    app.multiselect[1].set_value(['Severe']).run()
    assert table().CPSC_Case_Number.tolist()==['A']
    app.text_input[0].set_value('nothing matches').run()
    assert table().empty and not app.exception
    app.button[0].click().run()
    assert len(table())==5 and app.metric[1].value=='5'
    assert any('not mechanism labels' in c.value for c in app.caption)


def test_scatter_cautions_use_baseline_when_selected_subset_empty():
    app=AppTest.from_function(fixture_app,default_timeout=20).run()
    app.multiselect[0].set_value(['Fall']).run()
    app.multiselect[1].set_value(['Other known disposition']).run()
    app.text_input[0].set_value('belt').run()
    assert app.metric[1].value=='0'
    # Original severe visit A is retained in the all-outcome baseline.
    assert any('**Fall**: 1 records / 10.0000 weighted visits' in m.value for m in app.markdown)
    app.text_input[0].set_value('no match').run()
    assert any('No baseline records' in i.value for i in app.info)
    assert not app.exception
