"""One pure analytical snapshot and five independently callable renderers."""
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import qualitative
from contracts import validate_visits, normalize_lookup, LOOKUP, KNOWN

SUMMARY = ['injury_mechanism', 'weighted_ed_visits', 'record_count', 'severe_outcome_pct']
COMPOSITION = ['injury_mechanism', 'diagnosis_code', 'diagnosis_label', 'diagnosis_weighted_ed_visits', 'diagnosis_pct']


def build_view_data(filtered_df: pd.DataFrame, *, context: dict, diagnosis_lookup: pd.DataFrame) -> dict:
    result = dict(status='invalid_input', messages=[], context=context, headline=None,
                  mechanism_summary=pd.DataFrame(columns=SUMMARY), diagnosis_composition=pd.DataFrame(columns=COMPOSITION), quality=None)
    try:
        years = context.get('analysis_years')
        if not isinstance(years, list) or not years or any(type(y) is not int for y in years) or years != sorted(set(years)):
            raise ValueError('context.analysis_years: require sorted nonempty distinct integer years')
        if not isinstance(context.get('filter_description'), str):
            raise ValueError('context.filter_description: required string')
        scope = context.get('source_scope')
        if scope not in ['full_annual', 'sample', 'test_fixture']:
            raise ValueError('context.source_scope: invalid scope')
        if scope == 'sample':
            result.update(status='unavailable', messages=['Full annual NEISS data required for national estimates'])
            return result
        frame = validate_visits(filtered_df, years)
        lookup = normalize_lookup(diagnosis_lookup)
        diag = lookup.loc[lookup[LOOKUP[0]].eq('DIAG')]
        labels = dict(zip(pd.to_numeric(diag[LOOKUP[1]]).astype(int), diag[LOOKUP[3]]))
        if 2023 in years and any(y >= 2024 for y in years):
            result['messages'].append('Sampling changed between 2023 and 2024. Combined totals do not establish changes in injury incidence.')
        total = float(frame.Weight.sum())
        severe = float(frame.loc[frame.is_severe, 'Weight'].sum())
        unknown = ~frame.Disposition.isin(KNOWN)
        result.update(status='ok' if len(frame) else 'empty',
                      headline=dict(weighted_ed_visits=total, record_count=len(frame), severe_outcome_pct=100*severe/total if total else None),
                      quality=dict(unknown_disposition_record_count=int(unknown.sum()), unknown_disposition_weight=float(frame.loc[unknown, 'Weight'].sum())))
        if not len(frame):
            result['messages'].append('No records match the current filters')
            return result
        frame['_severe_weight'] = frame.Weight.where(frame.is_severe, 0)
        summary = frame.groupby('injury_mechanism', sort=False).agg(weighted_ed_visits=('Weight','sum'), record_count=('Weight','size'), severe_weight=('_severe_weight','sum')).reset_index()
        summary['severe_outcome_pct'] = 100 * summary.severe_weight / summary.weighted_ed_visits
        summary = summary.sort_values(['weighted_ed_visits','injury_mechanism'], ascending=[False,True], kind='stable')[SUMMARY].reset_index(drop=True)
        result['mechanism_summary'] = summary
        frame['diagnosis_code'] = frame.Diagnosis
        def label(code):
            if pd.isna(code):
                return 'Missing diagnosis'
            code = int(code)
            text = labels.get(code)
            if text is None:
                return f'Unmapped diagnosis ({code})'
            # Annual labels already include the code prefix; do not duplicate it.
            return text if str(text).startswith(str(code) + ' -') else f'{code} - {text}'
        frame['diagnosis_label'] = frame.Diagnosis.map(label)
        composition = frame.groupby(['injury_mechanism','diagnosis_code','diagnosis_label'], dropna=False, sort=False).Weight.sum().reset_index(name='diagnosis_weighted_ed_visits')
        denominators = summary.set_index('injury_mechanism').weighted_ed_visits
        composition['diagnosis_pct'] = 100 * composition.diagnosis_weighted_ed_visits / composition.injury_mechanism.map(denominators)
        composition['_mechanism_order'] = composition.injury_mechanism.map({m:i for i,m in enumerate(summary.injury_mechanism)})
        composition['_bucket_order'] = composition.diagnosis_code.map(lambda c: 2 if pd.isna(c) else (0 if int(c) in labels else 1))
        composition = composition.sort_values(['_mechanism_order','_bucket_order','diagnosis_code'], na_position='last', kind='stable')
        result['diagnosis_composition'] = composition[COMPOSITION].reset_index(drop=True)
        return result
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        result.update(status='invalid_input', messages=[f'Upstream data contract failure: {exc}'], headline=None, quality=None,
                      mechanism_summary=pd.DataFrame(columns=SUMMARY), diagnosis_composition=pd.DataFrame(columns=COMPOSITION))
        return result


def period_label(context):
    years = context['analysis_years']
    if len(years) == 1:
        return f'{years[0]} annual estimate'
    return 'Combined ' + ' and '.join(map(str, years)) + ' total; not annual'


def visit_axis(context):
    return 'Estimated national ED visits' if len(context['analysis_years']) == 1 else 'Estimated ED visits over selected years (combined total; not annual)'


def chart_base(figure, title, context):
    figure.update_layout(template='plotly_white', title=dict(text=f'{title} · {period_label(context)}', font_size=17),
                         margin=dict(l=15,r=25,t=65,b=35), font=dict(family='Arial',size=12),
                         hoverlabel=dict(bgcolor='white'), height=390)
    figure.update_yaxes(automargin=True)
    return figure


def render_headline(result, context):
    return result['headline']


def render_mechanism_bar(result, context):
    data = result['mechanism_summary']
    figure = go.Figure()
    if len(data):
        figure.add_trace(go.Bar(x=data.weighted_ed_visits.tolist(), y=data.injury_mechanism.tolist(), orientation='h', marker_color='#247a86',
                                customdata=data[['record_count','severe_outcome_pct']].to_numpy().tolist(),
                                hovertemplate='%{y}<br>Estimated ED visits: %{x:,.0f}<br>NEISS records: %{customdata[0]:d}<br>Severe outcomes: %{customdata[1]:.1f}%<extra></extra>'))
    figure.update_xaxes(title=visit_axis(context), rangemode='tozero', range=[0,None])
    figure.update_yaxes(title='Injury mechanism', categoryorder='array', categoryarray=data.injury_mechanism.tolist(), autorange='reversed')
    return chart_base(figure, 'Burden by mechanism', context)


def render_severity_scatter(result, context):
    data = result['mechanism_summary']
    figure = go.Figure()
    positions = ['top center','bottom center','middle right','middle left']
    # Separate traces retain independent names/tooltips when coordinates coincide.
    for i, row in data.iterrows():
        if pd.isna(row.severe_outcome_pct):
            continue
        figure.add_trace(go.Scatter(x=[row.weighted_ed_visits], y=[row.severe_outcome_pct], mode='markers+text',
                                   name=row.injury_mechanism, text=[row.injury_mechanism], textposition=positions[i % len(positions)],
                                   marker=dict(size=12, color=qualitative.Safe[i % len(qualitative.Safe)]), cliponaxis=False,
                                   customdata=[[row.injury_mechanism,int(row.record_count)]],
                                   hovertemplate='%{customdata[0]}<br>Estimated ED visits: %{x:,.0f}<br>NEISS records: %{customdata[1]:d}<br>Severe outcomes: %{y:.1f}%<extra></extra>'))
    figure.update_layout(showlegend=False)
    figure.update_xaxes(title=visit_axis(context), rangemode='tozero', range=[0,None])
    figure.update_yaxes(title='Weighted severe-outcome percentage (%)', range=[0,100])
    if data.severe_outcome_pct.isna().any():
        figure.add_annotation(text='Null severe percentages omitted from plot', xref='paper', yref='paper', x=0,y=1.15, showarrow=False)
    return chart_base(figure, 'Frequency and recorded severity', context)


def render_diagnosis_stack(result, context):
    data, summary = result['diagnosis_composition'], result['mechanism_summary']
    figure = go.Figure()
    # All known codes first, then unmapped, then missing, each numeric group ascending.
    buckets = data[['diagnosis_code','diagnosis_label']].drop_duplicates().copy()
    if len(buckets):
        buckets['_order'] = buckets.diagnosis_label.map(lambda s: 2 if s == 'Missing diagnosis' else (1 if s.startswith('Unmapped diagnosis') else 0))
        buckets = buckets.sort_values(['_order','diagnosis_code'], na_position='last')
    for i, bucket in enumerate(buckets.itertuples(index=False)):
        subset = data.loc[data.diagnosis_label.eq(bucket.diagnosis_label)].set_index('injury_mechanism').reindex(summary.injury_mechanism)
        figure.add_trace(go.Bar(name=bucket.diagnosis_label, orientation='h', y=summary.injury_mechanism.tolist(), x=subset.diagnosis_pct.fillna(0).tolist(),
                                marker_color=qualitative.Alphabet[i % len(qualitative.Alphabet)],
                                customdata=[[bucket.diagnosis_label, 'missing' if pd.isna(bucket.diagnosis_code) else str(int(bucket.diagnosis_code)), float(w)] for w in subset.diagnosis_weighted_ed_visits.fillna(0)],
                                hovertemplate='%{y}<br>%{customdata[0]} (code %{customdata[1]})<br>Estimated ED visits: %{customdata[2]:,.0f}<br>Share: %{x:.1f}%<extra></extra>'))
    figure.update_layout(barmode='stack', legend_title='Primary diagnosis', legend_traceorder='normal', height=460)
    figure.update_xaxes(title="Share of mechanism's weighted ED visits (%)", range=[0,100])
    figure.update_yaxes(title='Injury mechanism', categoryorder='array', categoryarray=summary.injury_mechanism.tolist(), autorange='reversed')
    figure = chart_base(figure, 'Primary-diagnosis composition', context)
    figure.update_layout(height=460)
    return figure


def render_summary_table(result, context):
    return result['mechanism_summary'].copy()


VIEW_REGISTRY = dict(headline=render_headline, mechanism_bar=render_mechanism_bar, severity_scatter=render_severity_scatter,
                     diagnosis_stack=render_diagnosis_stack, summary_table=render_summary_table)
