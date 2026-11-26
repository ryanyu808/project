"""R4: actionable empty selections and recovery after repeated Reset."""
from dataclasses import replace
from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

import filters
from filters import FilterSelection, apply_filters
from tests.support import fixture_app

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('mechanisms,query,expected', [
    (('Repair/moving',), '', [(('mechanisms',), 24), (('severities',), 8)]),
    (('Entering/exiting',), '', [(('mechanisms',), 24), (('severities',), 4)]),
    (('Repair/moving', 'Entering/exiting'), '',
     [(('mechanisms',), 24), (('severities',), 12)]),
    (('Fall',), 'belt', [(('severities',), 1), (('narrative_query',), 18)]),
])
def test_production_minimal_changes(mechanisms, query, expected):
    data = pd.read_csv(ROOT / 'data/prepared/treadmill_2025.csv')
    selection = FilterSelection(mechanisms, ('Severe',), query)
    before = data.copy(deep=True)
    assert apply_filters(data, selection).empty
    assert filters.minimal_filter_relaxations(data, selection) == expected
    pd.testing.assert_frame_equal(data, before)


def test_combination_is_needed_and_redundant_supersets_are_omitted(visits):
    # Only Contact has belt text, but those records are not Severe.
    data = visits.copy(deep=True)
    data.loc[data.injury_mechanism.eq('Contact'), 'Disposition'] = 1
    data.loc[data.injury_mechanism.eq('Contact'), 'is_severe'] = False
    data.loc[data.injury_mechanism.eq('Fall'), 'Narrative_1'] = 'treadmill fall'
    selection = FilterSelection(('Fall',), ('Severe',), 'belt')
    assert filters.minimal_filter_relaxations(data, selection) == [
        (('narrative_query',), 1), (('mechanisms', 'severities'), 1)]
    assert apply_filters(data, replace(selection, narrative_query='')).shape[0] == 1


def test_no_guidance_for_nonempty_selection_or_empty_source(visits):
    assert filters.minimal_filter_relaxations(visits, FilterSelection()) == []
    assert filters.minimal_filter_relaxations(visits.iloc[:0], FilterSelection()) == []
    assert filters.minimal_filter_relaxations(visits, FilterSelection(narrative_query='  ')) == []


def test_empty_guidance_names_joint_changes_in_ui():
    at = AppTest.from_function(fixture_app, default_timeout=30).run()
    at.multiselect[0].set_value(['Fall'])
    at.multiselect[1].set_value(['Unknown'])
    at.text_input[0].set_value('belt').run()
    assert not at.exception
    message = next(item.value for item in at.info if 'No records match' in item.value)
    assert 'Clear Injury mechanism (Fall) and Narrative search' in message
    assert "('belt')" in message
    assert '1 record' in message
    assert 'Clear Severity (Unknown)' in message
    # Applying guidance is the user's choice, so no controls change automatically.
    assert at.multiselect[0].value == ['Fall']
    assert at.multiselect[1].value == ['Unknown']
    assert at.text_input[0].value == 'belt'


def test_double_reset_restores_selection_and_snapshot_is_consumed():
    at = AppTest.from_function(fixture_app, default_timeout=30).run()
    assert at.button[1].disabled
    # An initial no-op Reset must not create an Undo snapshot.
    at.button[0].click().run()
    assert at.button[1].disabled
    at.multiselect[0].set_value(['Fall'])
    at.multiselect[1].set_value(['Severe'])
    at.text_input[0].set_value('belt').run()
    for _ in range(2):
        at.button[0].click().run()
        assert at.multiselect[0].value == []
        assert at.multiselect[1].value == []
        assert at.text_input[0].value == ''
        assert not at.button[1].disabled
    at.button[1].click().run()
    assert not at.exception
    assert at.multiselect[0].value == ['Fall']
    assert at.multiselect[1].value == ['Severe']
    assert at.text_input[0].value == 'belt'
    assert at.button[1].disabled
    other = AppTest.from_function(fixture_app, default_timeout=30).run()
    assert other.button[1].disabled
    # A later changed selection replaces the saved snapshot on Reset.
    at.button[0].click().run()
    at.text_input[0].set_value('Tripped').run()
    at.button[0].click().run()
    at.button[0].click().run()
    at.button[1].click().run()
    assert at.multiselect[0].value == []
    assert at.multiselect[1].value == []
    assert at.text_input[0].value == 'Tripped'
