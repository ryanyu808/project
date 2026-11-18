"""R7/R8 oracle: independent original-source results versus real app builders.

R8_MUTATION is used only in isolated child pytest runs. The source on disk is
never modified; each mutant compiles a changed copy of the actual views module.
"""
import json
import os
from pathlib import Path
import types
import pandas as pd
import pytest
import views
from loader import load_dashboard_data

ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = {
    'total_weight': ('total = float(frame.Weight.sum())', 'total = float(frame.Weight.sum()) + 1'),
    'severe_pct': ('severe_outcome_pct=100*severe/total if total else None',
                   'severe_outcome_pct=99*severe/total if total else None'),
    'fall_weight': ("result['mechanism_summary'] = summary", "summary.loc[summary.injury_mechanism.eq('Fall'), 'weighted_ed_visits'] += 1\n        result['mechanism_summary'] = summary"),
    'fall_severe_pct': ("result['mechanism_summary'] = summary", "summary.loc[summary.injury_mechanism.eq('Fall'), 'severe_outcome_pct'] += 1\n        result['mechanism_summary'] = summary"),
    'belt_severe_pct': ("result['mechanism_summary'] = summary", "summary.loc[summary.injury_mechanism.eq('Belt contact'), 'severe_outcome_pct'] += 1\n        result['mechanism_summary'] = summary"),
    'fall_severe_records': ('record_count=len(frame),', 'record_count=len(frame)+1,'),
    'fall_fracture_pct': ("composition['diagnosis_pct'] = 100 *", "composition['diagnosis_pct'] = 99 *"),
}


@pytest.fixture(scope='module')
def observed():
    module = views
    mutation = os.environ.get('R8_MUTATION')
    if mutation:
        before, after = MUTATIONS[mutation]
        source = Path(views.__file__).read_text(encoding='utf-8')
        assert source.count(before) == 1, 'Mutation target must be unambiguous'
        module = types.ModuleType('r8_mutant_views')
        exec(compile(source.replace(before, after), '<controlled R8 mutant>', 'exec'), module.__dict__)
    loaded = load_dashboard_data(ROOT/'data/prepared/treadmill_2025.csv',
        ROOT/'data/prepared/treadmill_2025.provenance.json',
        ROOT/'data/reference/neiss_code_lookup_2025.csv', 2025)
    frame = loaded['data']
    ctx = dict(analysis_years=[2025], source_scope='full_annual', filter_description='all')
    def build(df):
        r = module.build_view_data(df, context=ctx, diagnosis_lookup=loaded['diagnosis_lookup'])
        assert r['status'] == 'ok', r['messages']
        return r
    all_results = build(frame)
    by = all_results['mechanism_summary'].set_index('injury_mechanism')
    severe_fall = build(frame.loc[frame.injury_mechanism.eq('Fall') & frame.is_severe])
    diagnoses = all_results['diagnosis_composition']
    fracture = diagnoses.loc[diagnoses.injury_mechanism.eq('Fall') & diagnoses.diagnosis_code.eq(57)]
    return dict(total_weight=all_results['headline']['weighted_ed_visits'],
                record_count=all_results['headline']['record_count'],
                severe_pct=all_results['headline']['severe_outcome_pct'],
                fall_weight=by.loc['Fall','weighted_ed_visits'],
                fall_severe_pct=by.loc['Fall','severe_outcome_pct'],
                belt_severe_pct=by.loc['Belt contact','severe_outcome_pct'],
                fall_severe_records=severe_fall['headline']['record_count'],
                fall_fracture_pct=fracture.iloc[0].diagnosis_pct)


@pytest.mark.parametrize('metric', ['record_count', *MUTATIONS])
def test_main_result(metric, observed):
    expected = json.loads((ROOT/'validation/results/publisher_2025.json').read_text())['main_results']
    assert observed[metric] == pytest.approx(float(expected[metric]), rel=1e-12, abs=1e-8), metric


def test_independent_checker_has_no_application_imports():
    import ast
    tree = ast.parse((ROOT/'validation/publisher_numbers.py').read_text())
    allowed = {'argparse','csv','hashlib','json','collections','decimal','pathlib','openpyxl'}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(n.name.split('.')[0] in allowed for n in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.module.split('.')[0] in allowed
