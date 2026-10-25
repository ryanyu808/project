"""Pure row selection plus session-specific sidebar controls."""
from dataclasses import dataclass
import pandas as pd
from contracts import require_columns, severity_display

SEVERITIES = ['Severe', 'Other known disposition', 'Unknown']


@dataclass(frozen=True)
class FilterSelection:
    mechanisms: tuple[str, ...] = ()
    severities: tuple[str, ...] = ()
    narrative_query: str = ''


def apply_filters(data: pd.DataFrame, selection: FilterSelection) -> pd.DataFrame:
    require_columns(data, ['injury_mechanism', 'is_severe', 'Disposition', 'Narrative_1'])
    if not isinstance(selection, FilterSelection):
        raise ValueError('selection: expected FilterSelection')
    if not isinstance(selection.narrative_query, str):
        raise ValueError('narrative_query: expected string')
    for field, allowed in [('mechanisms', set(data.injury_mechanism)), ('severities', set(SEVERITIES))]:
        values = getattr(selection, field)
        if not isinstance(values, tuple):
            raise ValueError(f'{field}: expected tuple of labels')
        for value in values:
            if value not in allowed:
                raise ValueError(f'{field}: invalid selection label {value!r}')
    mask = pd.Series(True, index=data.index)
    if selection.mechanisms:
        mask &= data.injury_mechanism.isin(selection.mechanisms)
    if selection.severities:
        mask &= severity_display(data.Disposition).isin(selection.severities)
    query = selection.narrative_query.strip()
    if query:
        mask &= data.Narrative_1.astype('string').str.contains(query, case=False, regex=False, na=False)
    return data.loc[mask].copy()


def render_sidebar(data: pd.DataFrame) -> FilterSelection:
    import streamlit as st
    defaults = {'filter_mechanisms': [], 'filter_severities': [], 'filter_query': ''}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    def reset():
        for key, value in defaults.items():
            st.session_state[key] = value

    with st.sidebar:
        mechanisms = st.multiselect('Injury mechanism', sorted(data.injury_mechanism.dropna().unique()), key='filter_mechanisms')
        severities = st.multiselect('Severity', SEVERITIES, key='filter_severities')
        query = st.text_input('Search injury narratives', placeholder='Enter one word or phrase, e.g., belt', key='filter_query')
        st.button('Reset filters', on_click=reset)
    return FilterSelection(tuple(mechanisms), tuple(severities), query)
