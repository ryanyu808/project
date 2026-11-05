"""Independent Decimal checks against actual dashboard builders; no AI cohort input."""
import argparse
import csv
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from validation.independent_numbers import calculate

SEVERE={2,4,5,8};KNOWN={0,1,2,4,5,6,8}

def integer(value):
    if value in ('',None):return None
    number=Decimal(str(value))
    if not number.is_finite() or number!=number.to_integral_value():raise ValueError('Invalid integer code')
    return int(number)

def extended(rows):
    normalized=[{**r,'Diagnosis':str(integer(r['Diagnosis'])) if r['Diagnosis'] else '',
                 'Disposition':str(integer(r['Disposition'])) if r['Disposition'] else ''} for r in rows]
    result=calculate(normalized)
    unknown=[r for r in rows if integer(r['Disposition']) not in KNOWN]
    result.update(severe_record_count=sum(integer(r['Disposition']) in SEVERE for r in rows),
                  unknown_record_count=len(unknown),unknown_weight=sum((Decimal(r['Weight']) for r in unknown),Decimal(0)))
    total=result['total_weight']
    result['unknown_pct']=100*result['unknown_weight']/total if total else None
    result['all_unknown_severe_pct']=100*(result['severe_weight']+result['unknown_weight'])/total if total else None
    return result

def close(actual,expected,label):
    if expected is None:
        if actual is not None:raise ValueError(f'{label}: expected unavailable, got {actual}')
    elif abs(Decimal(str(actual))-Decimal(expected))>max(Decimal('1e-8'),abs(Decimal(expected))*Decimal('1e-12')):
        raise ValueError(f'{label}: dashboard {actual} != independent {expected}')

def compare(loaded,rows):
    import pandas as pd
    import views
    from filters import FilterSelection,apply_filters,without_severity
    frame=loaded['data'];lookup=loaded['diagnosis_lookup'];prov=loaded['provenance']
    context=dict(analysis_years=prov['analysis_years'],source_scope=prov['source_scope'],filter_description='independent validation')
    mechanisms=sorted(set(r['injury_mechanism'] for r in rows))
    selections=[('all',FilterSelection())]+[(m,FilterSelection(mechanisms=(m,))) for m in mechanisms]
    selections += [(s,FilterSelection(severities=(s,))) for s in ['Severe','Other known disposition','Unknown']]
    selections += [('literal belt',FilterSelection(narrative_query='  BeLt  ')),('literal metacharacters',FilterSelection(narrative_query='[.*]')),
                   ('empty',FilterSelection(narrative_query='__NO_NEISS_NARRATIVE_HAS_THIS_VALIDATION_TOKEN__'))]
    if 'Fall' in mechanisms:selections.append(('Fall Severe belt',FilterSelection(mechanisms=('Fall',),severities=('Severe',),narrative_query='belt')))
    scenarios={}
    for name,selection in selections:
        def independent_select(selection):
            output=[]
            for row in rows:
                code=integer(row['Disposition'])
                severity='Severe' if code in SEVERE else ('Other known disposition' if code in KNOWN else 'Unknown')
                if selection.mechanisms and row['injury_mechanism'] not in selection.mechanisms:continue
                if selection.severities and severity not in selection.severities:continue
                if selection.narrative_query.strip().casefold() not in row.get('Narrative_1','').casefold():continue
                output.append(row)
            return output
        chosen=independent_select(selection);expected=extended(chosen)
        selected=apply_filters(frame,selection)
        if selected.CPSC_Case_Number.tolist()!=[r['CPSC_Case_Number'] for r in chosen]:raise ValueError(name+': filter membership mismatch')
        result=views.build_view_data(selected,context=context,diagnosis_lookup=lookup)
        if result['status'] not in ('ok','empty'):raise ValueError(str(result['messages']))
        headline=result['headline']
        if headline['record_count']!=expected['record_count']:raise ValueError(name+': count mismatch')
        close(headline['weighted_ed_visits'],expected['total_weight'],name+' total')
        close(headline['severe_outcome_pct'],expected['severe_pct'],name+' severe percentage')
        close(result['quality']['unknown_disposition_weight'],expected['unknown_weight'],name+' unknown weight')
        if result['quality']['unknown_disposition_record_count']!=expected['unknown_record_count']:raise ValueError(name+': unknown count')
        if set(result['mechanism_summary'].injury_mechanism)!=set(expected['mechanisms']):raise ValueError(name+': mechanism set')
        for row in result['mechanism_summary'].itertuples():
            m=expected['mechanisms'][row.injury_mechanism]
            close(row.weighted_ed_visits,m['weight'],name+' mechanism weight')
            close(row.severe_outcome_pct,m['severe_pct'],name+' mechanism severe')
            if row.record_count!=m['count']:raise ValueError(name+': mechanism count')
        actual_buckets={}
        for row in result['diagnosis_composition'].itertuples():
            code='Missing diagnosis' if pd.isna(row.diagnosis_code) else str(int(row.diagnosis_code))
            m=expected['mechanisms'][row.injury_mechanism]
            close(row.diagnosis_weighted_ed_visits,m['diagnosis'][code],name+' diagnosis weight')
            close(row.diagnosis_pct,m['diagnosis_pct'][code],name+' diagnosis share')
            actual_buckets[(row.injury_mechanism,code)]=row.diagnosis_weighted_ed_visits
        if set(actual_buckets)!={(m,c) for m,v in expected['mechanisms'].items() for c in v['diagnosis']}:raise ValueError(name+': diagnosis bucket set')
        completeness=views.build_outcome_completeness(selected,context=context,diagnosis_lookup=lookup)
        if chosen:
            close(completeness['unknown_share_pct'],expected['unknown_pct'],name+' unknown percentage')
            close(completeness['none_unknown_severe_pct'],expected['severe_pct'],name+' lower endpoint')
            close(completeness['all_unknown_severe_pct'],expected['all_unknown_severe_pct'],name+' upper endpoint')
        elif completeness is not None:raise ValueError('Empty sensitivity must be unavailable')
        reconciliation=views.build_weight_reconciliation(result,context,prov)
        exported=list(csv.DictReader(io.StringIO(reconciliation['csv'].decode('utf-8-sig'))))
        if len(exported)!=len(expected['mechanisms'])+1:raise ValueError('CSV contribution count')
        for row in exported:
            value=expected['total_weight'] if row['row_type']=='selected_total' else expected['mechanisms'][row['injury_mechanism']]['weight']
            close(row['weighted_ed_visits'],value,name+' exported CSV precision')
        baseline_selection=without_severity(selection);base_rows=independent_select(baseline_selection)
        baseline=apply_filters(frame,baseline_selection)
        comparison=views.build_severity_comparison(selected,baseline,context=context,diagnosis_lookup=lookup)
        base=extended(base_rows)
        for row in comparison.itertuples():
            m=base['mechanisms'][row.injury_mechanism]
            close(row.baseline_weighted_ed_visits,m['weight'],name+' baseline weight')
            close(row.baseline_severe_outcome_pct,m['severe_pct'],name+' baseline severe')
            close(row.selected_severe_weighted_ed_visits,expected['mechanisms'].get(row.injury_mechanism,{}).get('severe_weight',0),name+' selected severe weight')
        scenarios[name]=expected
    return dict(status='PASS',source_scope=prov['source_scope'],prepared_sha256=prov.get('prepared_sha256'),
                tolerance='max(1e-8 absolute, 1e-12 relative); IDs/counts/sets exact',
                comparison='Actual filter and dashboard builder outputs, baselines, sensitivity and downloaded CSV; public UI capture remains separate',scenarios=scenarios)

def validate_cohort(cohort,provenance,lookup):
    from loader import load_dashboard_data
    prov=json.loads(Path(provenance).read_text(encoding='utf-8'))
    if prov.get('source_scope')!='full_annual':raise ValueError('Reviewed full-annual production bundle required')
    loaded=load_dashboard_data(cohort,provenance,lookup,prov['analysis_years'][0])
    with Path(cohort).open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
    return compare(loaded,rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['cohort','provenance','lookup','output']:parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();result=validate_cohort(args.cohort,args.provenance,args.lookup)
    with args.output.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2,default=str)
    print('PASS: independent dashboard validation; '+str(args.output))

if __name__=='__main__':main()
