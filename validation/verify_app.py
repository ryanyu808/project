"""Exercise the actual configured production app (no injected fixture loader).

This is local/CI UI evidence, never a public-browser or visual-capture claim.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def verify():
    from streamlit.testing.v1 import AppTest
    from configuration import read_config, resolve_path
    from loader import load_dashboard_data
    from validation.verify_dashboard import compare
    import csv
    config = read_config(ROOT / 'config.toml')
    paths = [resolve_path(config['data'][k]) for k in ['prepared_path', 'provenance_path', 'diagnosis_lookup_path']]
    loaded = load_dashboard_data(*paths, config['analysis']['year'])
    with paths[0].open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    expected = compare(loaded, rows)['scenarios']
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=30).run()
    observations = {}
    def check(name):
        assert not app.exception, [str(x) for x in app.exception]
        e = expected[name]
        pct = e['severe_pct']
        metrics = [f"{e['total_weight']:,.0f}", str(e['record_count']), 'N/A' if pct is None else f'{pct:.1f}%']
        actual = [x.value for x in app.metric]
        assert actual == metrics, (name, actual, metrics)
        assert len(app.get('plotly_chart')) >= 3
        observations[name] = dict(metrics=actual, plotly_charts=len(app.get('plotly_chart')), tables=len(app.dataframe))
    check('all')
    assert any('codebook 1.2' in x.label for x in app.expander)
    app.multiselect[0].set_value(['Fall']).run(); check('Fall')
    app.multiselect[1].set_value(['Severe']).run()
    # The baseline is independently checked by compare; inspect its actual UI table.
    population = next(d.value for d in app.dataframe if 'baseline_record_count' in d.value.columns)
    assert population.iloc[0]['baseline_record_count'] == expected['Fall']['record_count']
    app.text_input[0].set_value('belt').run(); check('Fall Severe belt')
    assert any('Narrative_1' in d.value.columns for d in app.dataframe)
    app.button[0].click().run(); check('all')
    app.button[1].click().run(); check('Fall Severe belt')
    assert app.multiselect[0].value == ['Fall'] and app.multiselect[1].value == ['Severe'] and app.text_input[0].value == 'belt'
    app.text_input[0].set_value('__NO_NEISS_NARRATIVE_HAS_THIS_VALIDATION_TOKEN__').run(); check('empty')
    assert any('No records match' in x.value for x in app.info)
    app.button[0].click().run(); check('all')
    return dict(status='PASS', evidence_kind='local/CI production AppTest; not public-app evidence',
                prepared_sha256=loaded['provenance']['prepared_sha256'], scenarios=observations,
                checks=['real loader and configured files', 'headlines', 'baseline table', 'matching narratives',
                        'Reset and Undo preserve all controls', 'empty selection', 'codebook version',
                        'charts and CSV values independently checked by verify_dashboard'])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    report=verify()
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: actual production AppTest; no public verification claimed')

if __name__=='__main__': main()
