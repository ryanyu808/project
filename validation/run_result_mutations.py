"""R8: isolated faulty calculation runs; retain complete actual pytest output."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
METRICS = ['total_weight','severe_pct','fall_weight','fall_severe_pct',
           'belt_severe_pct','fall_severe_records','fall_fracture_pct']


def main():
    source = ROOT/'views.py'
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    evidence = ROOT/'validation/results/r8'
    evidence.mkdir(exist_ok=True)
    results = []
    for metric in METRICS:
        command = [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                   f'tests/test_publisher_results.py::test_main_result[{metric}]']
        env = dict(os.environ, R8_MUTATION=metric, PYTHONIOENCODING='utf-8')
        run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8')
        output = run.stdout + run.stderr
        (evidence/f'{metric}.txt').write_text(output, encoding='utf-8')
        caught = run.returncode == 1 and '1 failed' in output and 'AssertionError' in output and metric in output
        results.append(dict(metric=metric, exit_code=run.returncode, caught=caught,
                            command=command, environment_override={'R8_MUTATION':metric},
                            output=f'validation/results/r8/{metric}.txt'))
        print(f'{metric}: exit={run.returncode}; caught={caught}')
    assert hashlib.sha256(source.read_bytes()).hexdigest() == before
    (evidence/'summary.json').write_text(json.dumps(dict(source_sha256_before=before,
        source_sha256_after=before, mutations=results), indent=2)+'\n')
    if not all(r['caught'] for r in results):
        raise SystemExit('Mutation evidence incomplete: inspect outputs')
    print('All seven faulty calculations caught; on-disk implementation unchanged.')


if __name__ == '__main__':
    main()
