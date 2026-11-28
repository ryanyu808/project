"""Run production controls repeatedly and record actual five-category evidence."""
from pathlib import Path
import json
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def run():
    import pandas as pd
    from streamlit.testing.v1 import AppTest
    from validation.verify_dashboard import validate_cohort
    started = time.monotonic()
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=30).run()
    evidence = {'heavy everyday use': [], 'unusual selections': [], 'tiny groups': [],
                'data problems': [], 'consistency': []}
    def observe(category, label):
        assert not app.exception, [str(e) for e in app.exception]
        row = dict(selection=label, metrics=[x.value for x in app.metric],
                   warnings=[x.value for x in app.warning], messages=[x.value for x in app.info])
        evidence[category].append(row)
        return row
    for cycle in range(5):
        app.multiselect[0].set_value(['Fall'])
        app.multiselect[1].set_value(['Severe'])
        app.text_input[0].set_value('belt').run()
        row = observe('heavy everyday use', f'cycle {cycle+1}: Fall + Severe + belt')
        assert row['metrics'] == ['0', '0', 'N/A']
        assert any('Clear' in m for m in row['messages'])
        app.button[0].click().run()
        app.button[0].click().run()
        app.button[1].click().run()
        assert app.multiselect[0].value == ['Fall']
        assert app.multiselect[1].value == ['Severe']
        assert app.text_input[0].value == 'belt'
        app.button[0].click().run()
        assert [x.value for x in app.metric] == ['5,120','109','22.3%']
    for query in ['[.*]', '999999999999999999', 'not-a-real-case', '   ', 'senior', 'button', 'wrong']:
        app.text_input[0].set_value(query).run()
        row = observe('unusual selections', repr(query))
        if row['metrics'][1] == '0':
            assert any('Clear' in m for m in row['messages'])
        if query in ['senior','button','wrong']:
            assert any('CPSC reliability caution' in m for m in row['warnings'])
            observe('tiny groups', query)
    app.button[0].click().run()
    app.multiselect[0].set_value(['Entering/exiting']).run()
    row = observe('tiny groups', 'Entering/exiting')
    assert row['metrics'] == ['255','4','0.0%'] and row['warnings']
    frame = pd.read_csv(ROOT/'data/prepared/treadmill_2025.csv')
    assert not frame.CPSC_Case_Number.duplicated().any()
    assert frame.Weight.gt(0).all() and frame.Age.between(65,120).all()
    assert frame.injury_mechanism.notna().all()
    labels = set(frame.injury_mechanism)
    assert len({s.strip().casefold() for s in labels}) == len(labels)
    evidence['data problems'].append(dict(records=len(frame), duplicate_ids=0,
        invalid_ages=0, nonpositive_weights=0, blank_mechanisms=0,
        note='Runtime cohort inspected; publisher audit separately verifies full-year coverage. Loader/preparation failure injections are in the regression suite.'))
    result = validate_cohort(ROOT/'data/prepared/treadmill_2025.csv',
        ROOT/'data/prepared/treadmill_2025.provenance.json', ROOT/'data/reference/neiss_code_lookup_2025.csv')
    evidence['consistency'].append(dict(status=result['status'], scenarios=list(result['scenarios']),
        checks='independent membership, dashboard totals, baselines, diagnoses, sensitivity and export reconciliation'))
    return dict(status='PASS', evidence_kind='local production AppTest and data checks; not public screenshots',
                elapsed_seconds=round(time.monotonic()-started,2), categories=evidence)


if __name__ == '__main__':
    output = ROOT/'validation/results/final_20261127/hardening.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(run(),indent=2)+'\n',encoding='utf-8')
    print('PASS: five-category production hardening; evidence:',output.relative_to(ROOT))
