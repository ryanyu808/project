"""Pure row selection plus session-specific sidebar controls."""
from dataclasses import dataclass, replace
from itertools import combinations
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


def minimal_filter_relaxations(data: pd.DataFrame, selection: FilterSelection) -> list:
    """Return successful sets of cleared filter dimensions, omitting supersets.

    Each returned set is inclusion-minimal: none of its proper subsets can
    restore records. Counts always retain every filter outside that set.
    """
    if not apply_filters(data, selection).empty or data.empty:
        return []
    defaults = {'mechanisms': (), 'severities': (), 'narrative_query': ''}
    active = [field for field in defaults
              if (selection.narrative_query.strip() if field == 'narrative_query'
                  else getattr(selection, field))]
    solutions = []
    for size in range(1, len(active) + 1):
        for fields in combinations(active, size):
            if any(set(previous).issubset(fields) for previous, _ in solutions):
                continue
            relaxed = replace(selection, **{field: defaults[field] for field in fields})
            count = len(apply_filters(data, relaxed))
            if count:
                solutions.append((fields, count))
    return solutions


def empty_selection_message(data: pd.DataFrame, selection: FilterSelection) -> str:
    labels = {
        'mechanisms': f"Injury mechanism ({', '.join(selection.mechanisms)})",
        'severities': f"Severity ({', '.join(selection.severities)})",
        'narrative_query': f"Narrative search ({selection.narrative_query.strip()!r})",
    }
    alternatives = [
        f"Clear {' and '.join(labels[field] for field in fields)} to see "
        f"{count:,} {'record' if count == 1 else 'records'}."
        for fields, count in minimal_filter_relaxations(data, selection)
    ]
    return ('No records match the current filters. '
            'Each alternative keeps the other selections unchanged: '
            + ' Alternatively: '.join(alternatives))


def render_sidebar(data: pd.DataFrame) -> FilterSelection:
    import streamlit as st
    defaults = {'filter_mechanisms': [], 'filter_severities': [], 'filter_query': ''}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    def reset():
        if all(st.session_state[key] == value for key, value in defaults.items()):
            return
        st.session_state['selection_before_reset'] = {
            key: list(st.session_state[key]) if isinstance(value, list) else st.session_state[key]
            for key, value in defaults.items()
        }
        for key, value in defaults.items():
            st.session_state[key] = list(value) if isinstance(value, list) else value

    def undo_reset():
        previous = st.session_state.pop('selection_before_reset', None)
        if previous is not None:
            for key, value in previous.items():
                st.session_state[key] = value

    with st.sidebar:
        mechanisms = st.multiselect('Injury mechanism', sorted(data.injury_mechanism.dropna().unique()), key='filter_mechanisms')
        severities = st.multiselect('Severity', SEVERITIES, key='filter_severities')
        query = st.text_input('Search injury narratives', placeholder='Enter one word or phrase, e.g., belt', key='filter_query')
        st.button('Reset filters', on_click=reset)
        st.button('Undo reset', on_click=undo_reset, disabled='selection_before_reset' not in st.session_state)
        with st.expander('Mechanism definitions · codebook 1.2'):
            from codebook import read_codebook
            st.caption('Use the earliest initiating treadmill mechanism. '
                       'For ties, use the listed priority order (1–7). '
                       'Unknown/Unclassified means reviewed but unclear, never unfinished review.')
            try:
                st.markdown(read_codebook())
            except (OSError, ValueError) as exc:
                st.warning(f'Mechanism definitions unavailable: {exc}')

    return FilterSelection(tuple(mechanisms), tuple(severities), query)


def without_severity(selection: FilterSelection) -> FilterSelection:
    """Keep mechanism and literal search; remove only the severity restriction."""
    return replace(selection, severities=())
