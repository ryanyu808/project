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
        baseline_df = filters.apply_filters(data, filters.without_severity(selection))
        comparison = views.build_severity_comparison(
            filtered, baseline_df, context=context, diagnosis_lookup=loaded['diagnosis_lookup'])
        if comparison is not None:
            rendered['severity_scatter'] = views.render_severity_comparison(comparison, context)
        st.caption('Scatter comparison: x = severe visit weight among the selected records; '
                   'y = severe visit weight / all visit weight in the same mechanism and narrative selection '
                   'with severity removed. The baseline includes unknown dispositions. '
                   'Headlines, burden bars, diagnosis chart, and summary still describe the selected records.')
    left, right = st.columns(2)
    with left:
        st.plotly_chart(rendered['mechanism_bar'], use_container_width=True, key='mechanism_bar')
    with right:
        st.plotly_chart(rendered['severity_scatter'], use_container_width=True, key='severity_scatter')
        st.markdown('**Interpret comparisons cautiously.** [CPSC estimate guidance]('
                    + views.ESTIMATE_GUIDANCE_URL + ') flags estimates below 1,200, fewer than 20 sampled '
                    'records, or coefficient of variation (CV) above 33% as unstable. '
                    'Survey-design CV and confidence intervals are not computed here. '
                    'These screens concern estimated visit totals, not a significance test for severe percentages. '
                    'A higher severe share does not establish a reliable ranking or higher risk per user.')
        screen_result = (views.build_view_data(baseline_df, context=context,
                         diagnosis_lookup=loaded['diagnosis_lookup']) if selection.severities else result)
        with st.expander('Estimate cautions for the scatter population'):
            st.caption('Population: same mechanism and narrative selection, severity unrestricted. '
                       'Under a severity filter these are the scatter comparison baseline, not the headline subset. '
                       'Passing the count and estimate screens does not establish stability; CV is uncomputed. '
                       'Zero unknown outcomes does not remove sampling uncertainty.')
            cautions = views.estimate_cautions(screen_result['mechanism_summary'])
            if not cautions:
                st.info('No baseline records for estimate screening.')
            for item in cautions:
                st.markdown(f"**{item['mechanism']}**: {item['records']} records / "
                            f"{item['weight']:.4f} weighted visits. {item['assessment']}.")
    st.plotly_chart(rendered['diagnosis_stack'], use_container_width=True, key='diagnosis_stack')
    if selection.severities:
        st.subheader('Primary diagnosis · all-outcome comparison baseline')
        st.caption('Baseline keeps the mechanism and narrative selections but removes severity. '
                   'Each diagnosis share divides by all baseline visit weight in that mechanism. '
                   'The preceding diagnosis chart describes only the selected records.')
        baseline_result = views.build_view_data(baseline_df, context=context, diagnosis_lookup=loaded['diagnosis_lookup'])
        if baseline_result['status'] in ('ok', 'empty'):
            st.plotly_chart(views.render_diagnosis_stack(baseline_result, context),
                            use_container_width=True, key='baseline_diagnosis_stack')

    st.subheader(f'Mechanism summary · {period}')
    st.dataframe(rendered['summary_table'], hide_index=True, use_container_width=True, column_config={
        'injury_mechanism': st.column_config.TextColumn('Injury mechanism'),
        'weighted_ed_visits': st.column_config.NumberColumn('Estimated weighted ED visits', format='%.0f'),
        'record_count': st.column_config.NumberColumn('NEISS record count', format='%d'),
        'severe_outcome_pct': st.column_config.NumberColumn('Weighted severe-outcome percentage (%)', format='%.1f'),
    })
    st.subheader('Supporting evidence · selected records')
    st.caption('Population: all active filters. Weighted severe percentage uses all selected visit weight, '
               'including unknown outcomes. Record counts are not confidence intervals; '
               'survey uncertainty is not estimated in this MVP.')
    evidence = views.build_supporting_evidence(filtered, context=context, diagnosis_lookup=loaded['diagnosis_lookup'])
    st.dataframe(evidence, hide_index=True, use_container_width=True, column_config={
        'injury_mechanism': 'Mechanism',
        'weighted_ed_visits': st.column_config.NumberColumn('Selected weighted ED visits', format='%.2f'),
        'record_count': 'NEISS records',
        'severe_outcome_pct': st.column_config.NumberColumn('Recorded severe (%)', format='%.1f'),
        'unknown_disposition_record_count': 'Unknown outcome records',
        'unknown_disposition_weight': st.column_config.NumberColumn('Unknown outcome weight', format='%.2f'),
    })
    if selection.severities and comparison is not None:
        st.subheader('Severity comparison populations')
        st.caption('Baseline: same mechanism and narrative search, severity unrestricted. '
                   'Selected severe burden: severe visit weight remaining after every active filter. '
                   'Zero selected records may coexist with a nonempty baseline.')
        st.dataframe(comparison, hide_index=True, use_container_width=True, column_config={
            'injury_mechanism': 'Mechanism',
            'baseline_weighted_ed_visits': st.column_config.NumberColumn('Baseline all-outcome weight', format='%.2f'),
            'baseline_record_count': 'Baseline records',
            'baseline_severe_outcome_pct': st.column_config.NumberColumn('Baseline severe (%)', format='%.1f'),
            'selected_severe_weighted_ed_visits': st.column_config.NumberColumn('Selected severe weight', format='%.2f'),
            'selected_record_count': 'Selected records',
        })
    with st.expander('Outcome completeness and conditional sensitivity'):
        st.caption('Population: the selected records after every active filter. Unknown share = U/T. '
                   'Conditional endpoints are S/T and (S+U)/T, where S is recorded severe weight, '
                   'U is unknown-outcome weight, and T is total selected weight. '
                   'These are sensitivity endpoints, not confidence intervals or imputed outcomes. '
                   'A severity selection that omits Unknown removes those records from this population.')
        completeness = views.build_outcome_completeness(filtered, context=context, diagnosis_lookup=loaded['diagnosis_lookup'])
        if completeness is None:
            st.info('Outcome completeness unavailable: no selected visit weight.')
        else:
            labels = {'total_weight':'Total selected weight (T)', 'recorded_severe_weight':'Recorded severe weight (S)',
                      'unknown_weight':'Unknown outcome weight (U)', 'unknown_share_pct':'Unknown share (%)',
                      'none_unknown_severe_pct':'Lower conditional endpoint (%)',
                      'all_unknown_severe_pct':'Upper conditional endpoint (%)'}
            st.table([{'Measure':labels[key], 'Value':value} for key,value in completeness.items()])
    with st.expander('Weighted-total reconciliation and download'):
        reconciliation = views.build_weight_reconciliation(result, context, loaded['provenance'])
        st.caption('Contributions are summed before rounding. Separately rounded mechanism values may '
                   'not add to the rounded headline. The download keeps unrounded weights and identifies '
                   'the active filters, analysis period, and prepared-data SHA-256. '
                   'Its selected_total row is a total, not another mechanism contribution.')
        st.dataframe(reconciliation['table'], hide_index=True, use_container_width=True,
                     column_config={'injury_mechanism': 'Mechanism', 'record_count':'NEISS records',
                                    'weighted_ed_visits': st.column_config.NumberColumn('Unrounded weighted ED visits', format='%.17g')})
        st.table([{'Measure':label, 'Value':str(reconciliation[key])} for key,label in [
            ('contribution_sum','Sum of unrounded contributions'), ('headline_unrounded','Unrounded headline'),
            ('rounded_headline','Rounded headline'), ('sum_of_rounded_contributions','Sum of separately rounded contributions')]])
        st.caption(f"Data version: {reconciliation['data_version']}")
        st.download_button('Download weighted breakdown (CSV)', reconciliation['csv'],
                           file_name=f"treadmill_{config['analysis']['year']}_weighted_breakdown.csv", mime='text/csv')
    st.subheader('Matching narrative records' if selection.narrative_query.strip() else 'Selected injury records')
    st.caption('Browse every record matching the active filters, including when search is blank. '
               'Search matches trimmed, case-insensitive literal text, not mechanism labels or synonyms. '
               'Belt contact describes an initiating mechanism, including speed changes; it does not establish '
               'belt wear or a confirmed defect. Each row is one ED visit, not one unique person.')
    with st.expander(f'Browse {len(filtered)} selected narratives', expanded=bool(selection.narrative_query.strip())):
        st.dataframe(filtered[['CPSC_Case_Number', 'Narrative_1', 'injury_mechanism',
                               'Disposition', 'Weight']], hide_index=True, use_container_width=True)
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
