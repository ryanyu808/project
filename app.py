"""Streamlit setup: configuration, cached loading, controls and placement only."""
import logging
from pathlib import Path
import streamlit as st
from configuration import ROOT, read_config, resolve_path
import loader
import filters
import views

LOG = logging.getLogger(__name__)


def file_fingerprints(paths):
    return tuple((str(Path(p).resolve()), Path(p).stat().st_mtime_ns, Path(p).stat().st_size) for p in paths)


@st.cache_data(show_spinner=False)
def cached_load(fingerprints, year, loader_version):
    return loader.load_dashboard_data(*(entry[0] for entry in fingerprints), year)


def describe(selection):
    return (f"Mechanisms: {', '.join(selection.mechanisms) or 'all'} · "
            f"Severity: {', '.join(selection.severities) or 'all'} · "
            f"Narrative search: {repr(selection.narrative_query.strip()) if selection.narrative_query.strip() else 'none'}")


def render_dashboard(config, loaded):
    data = loaded['data']
    st.sidebar.caption(f"Fixed analysis year: {config['analysis']['year']}")
    selection = filters.render_sidebar(data)
    context = dict(analysis_years=loaded['provenance']['analysis_years'], source_scope=loaded['provenance']['source_scope'], filter_description=describe(selection))
    st.write(context['filter_description'])
    try:
        filtered = filters.apply_filters(data, selection)
    except ValueError as exc:
        LOG.exception('Filtering failed')
        st.error(f'Filtering error: {exc}')
        return
    st.caption(f'Showing {len(filtered):,} of {len(data):,} prepared cases')
    if data.empty:
        st.info('No prepared treadmill cases are available.')
    result = views.build_view_data(filtered, context=context, diagnosis_lookup=loaded['diagnosis_lookup'])
    for message in result['messages']:
        st.info(message)
    if result['status'] in ('invalid_input', 'unavailable'):
        return
    period = views.period_label(context)
    st.caption(f'Analysis period: {period}')
    # Registry and configuration own the exact placement; all use one result.
    rendered = {name: views.VIEW_REGISTRY[name](result, context) for name in config['dashboard']['available_views']}
    headline = rendered['headline']
    slots = st.columns(3)
    slots[0].metric(views.visit_axis(context), f"{headline['weighted_ed_visits']:,.0f}")
    slots[1].metric('NEISS record count', f"{headline['record_count']:,}")
    percentage = headline['severe_outcome_pct']
    slots[2].metric('Weighted severe-outcome percentage', 'N/A' if percentage is None else f'{percentage:.1f}%')
    quality = result['quality']
    st.caption('Severity denominator includes all selected visit weight, including unknown dispositions. '
               f"Unknown disposition: {quality['unknown_disposition_record_count']:,} records / {quality['unknown_disposition_weight']:,.0f} weighted ED visits.")
    if selection.severities:
        st.info('Percentages describe the selected cases; the severity filter changes both numerator and denominator.')
    left, right = st.columns(2)
    with left:
        st.plotly_chart(rendered['mechanism_bar'], use_container_width=True, key='mechanism_bar')
    with right:
        st.plotly_chart(rendered['severity_scatter'], use_container_width=True, key='severity_scatter')
    st.plotly_chart(rendered['diagnosis_stack'], use_container_width=True, key='diagnosis_stack')
    st.subheader(f'Mechanism summary · {period}')
    st.dataframe(rendered['summary_table'], hide_index=True, use_container_width=True, column_config={
        'injury_mechanism': st.column_config.TextColumn('Injury mechanism'),
        'weighted_ed_visits': st.column_config.NumberColumn('Estimated weighted ED visits', format='%.0f'),
        'record_count': st.column_config.NumberColumn('NEISS record count', format='%d'),
        'severe_outcome_pct': st.column_config.NumberColumn('Weighted severe-outcome percentage (%)', format='%.1f'),
    })
    st.caption('Descriptive investigation aid. Visits are not unique people. No exposure denominator, causal conclusion, '
               'or design-defect claim is supported. Record counts do not measure statistical precision.')


def main(config_path=ROOT / 'config.toml', *, _test_loader=None):
    try:
        config = read_config(config_path)
    except ValueError as exc:
        st.error(f'Configuration error: {exc}')
        return
    st.set_page_config(page_title=config['dashboard']['title'], layout=config['dashboard']['layout'])
    st.title(config['dashboard']['title'])
    st.caption(f"Adults ages 65–120 · Calendar year {config['analysis']['year']} · Descriptive investigation aid")
    paths = [resolve_path(config['data'][key]) for key in ['prepared_path','provenance_path','diagnosis_lookup_path']]
    try:
        loaded = _test_loader() if _test_loader else cached_load(file_fingerprints(paths), config['analysis']['year'], loader.LOADER_VERSION)
    except FileNotFoundError as exc:
        st.sidebar.caption(f"Fixed analysis year: {config['analysis']['year']}")
        st.error(f'Dashboard data unavailable: {exc.filename or exc}. Obtain/build the full-year prepared artifact through offline preparation.')
        st.info('Download the annual source at https://www.cpsc.gov/cgibin/NEISSQuery/home.aspx: select affiliation, '
                'Archived Annual NEISS Data, year, Excel or Tab Delimited Text, then Find Data. Save under data/raw/. '
                'Run candidates, have a human review every candidate, then run finalize. See README.md.')
        return
    except ValueError as exc:
        LOG.exception('Prepared data validation failed')
        st.error(f'Prepared data validation failed: {exc}')
        return
    render_dashboard(config, loaded)


if __name__ == '__main__':
    main()
