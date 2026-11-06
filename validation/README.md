# Independent production and fixture validation

The reviewed 2025 production bundle is complete: 109 retained visits from 188 completed human decisions (79 excluded), codebook1.2. See REAL_DATA_RESULTS.md and results/real_2025_results.json, real_2025_dashboard_check.json and real_2025_app_check.json. These are actual local production checks; public-browser evidence is separately verified in results/public_dashboard_verification.json, with authentic screenshots, actual downloaded CSV and metadata checks. The Unlisted demo playback proof is in results/youtube_verification.json.

independent_numbers.py uses csv/Decimal without the application aggregators. verify_dashboard.py independently checks severe/unknown counts and weights, endpoints, every primary-diagnosis bucket and mechanism, exact filter IDs, severity/diagnosis baselines and unrounded CSV. All14real scenarios pass; weights/percentages tolerate max(1e-8 absolute,1e-12relative) only for floating dashboard output. IDs/counts/sets are exact. The finalizer compares each retained source Weight as exact Decimal.

```text
uv run --locked python validation/independent_numbers.py --cohort data/prepared/treadmill_2025.csv --provenance data/prepared/treadmill_2025.provenance.json --output ../independent-new.json
uv run --locked python validation/verify_dashboard.py --cohort data/prepared/treadmill_2025.csv --provenance data/prepared/treadmill_2025.provenance.json --lookup data/reference/neiss_code_lookup_2025.csv --output ../dashboard-new.json
uv run --locked python validation/verify_app.py --output ../app-new.json
```

Use new report paths; preserve earlier evidence. verify_dashboard refuses an existing output. The actual configured AppTest uses no fixture loader and checks real headlines, controls, baseline table, narratives, zero selections, codebook, charts and Reset/Undo. Local/CI AppTest is not a screenshot or public access test. Follow ../DEPLOYMENT.md for signed-out public checks/downloads and genuine captures.

The original hand-computable five-record fixture is retained in fixtures/invented_visits.csv. A-E and historical label Contact are INVENTED. Hand results: total120, five records, severe3/weight50/share41.666667%; unknown1/weight40/share33.333333%; conditional upper75%. Fall40, Contact60, Unknown20. Run python validation/run_fixture_checks.py --output <new-report.json>. Never publish fixture totals as NEISS findings. Real and fixture reports are distinctly named.

All180tests pass on Windows/Python 3.13.15, with module counts in results/test_summary.json. Read ../deployment/CI_RESULTS.md for observed Ubuntu/Python 3.13 results, including the identified fixture-only newline mismatch and correction. Raw annual sources, human workbook and review/audit files remain private; only safe aggregate numerical evidence is committed.
