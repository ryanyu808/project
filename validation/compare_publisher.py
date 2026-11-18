"""Compare the independent publisher oracle with actual application results.

This adapter imports the app; publisher_numbers.py deliberately does not.
"""
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from loader import load_dashboard_data
from views import build_view_data


def compare():
    d = load_dashboard_data(ROOT/'data/prepared/treadmill_2025.csv',
        ROOT/'data/prepared/treadmill_2025.provenance.json', ROOT/'data/reference/neiss_code_lookup_2025.csv',2025)
    ctx = dict(analysis_years=[2025],source_scope='full_annual',filter_description='all')
    frame = d['data']
    r = build_view_data(frame, context=ctx, diagnosis_lookup=d['diagnosis_lookup'])
    fall = r['mechanism_summary'].set_index('injury_mechanism').loc['Fall']
    belt = r['mechanism_summary'].set_index('injury_mechanism').loc['Belt contact']
    selected = build_view_data(frame.loc[frame.injury_mechanism.eq('Fall') & frame.is_severe], context=ctx,diagnosis_lookup=d['diagnosis_lookup'])
    c = r['diagnosis_composition']
    actual = dict(total_weight=r['headline']['weighted_ed_visits'],record_count=r['headline']['record_count'],
        severe_pct=r['headline']['severe_outcome_pct'],fall_weight=float(fall.weighted_ed_visits),
        fall_severe_pct=float(fall.severe_outcome_pct),belt_severe_pct=float(belt.severe_outcome_pct),
        fall_severe_records=selected['headline']['record_count'],
        fall_fracture_pct=float(c.loc[c.injury_mechanism.eq('Fall') & c.diagnosis_code.eq(57),'diagnosis_pct'].iloc[0]))
    expected = json.loads((ROOT/'validation/results/publisher_2025.json').read_text())['main_results']
    rows=[]
    for key, value in actual.items():
        difference = value-float(expected[key])
        assert abs(difference) <= max(1e-8,abs(float(expected[key]))*1e-12), key
        rows.append(dict(metric=key, publisher=expected[key],app=value,difference=difference,
                         explanation='Exact agreement' if difference == 0 else 'Binary floating-point representation only; within 1e-8 absolute / 1e-12 relative tolerance'))
    return dict(status='PASS',results=rows)


if __name__ == '__main__':
    output=json.dumps(compare(),indent=2)
    print(output)
    (ROOT/'validation/results/publisher_comparison.json').write_text(output+'\n')
