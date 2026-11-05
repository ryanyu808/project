# Independent validation

`independent_numbers.py` retains the original hand-computable five-record fixture. `verify_dashboard.py` adds csv/Decimal loops for severe count, unknown count/weight, outcome sensitivity, primary-diagnosis buckets and mechanism totals, then compares them with actual filters, dashboard builders, baselines and unrounded exported CSVs. Counts/membership are exact; floating results use max(1e-8 absolute, 1e-12 relative). Exported prepared Weight is also compared as exact Decimal against candidates in the finalization workflow.

Run the independent fixture comparison:

```text
uv run --locked python validation/run_fixture_checks.py --output validation/results/dashboard_fixture_results.json
```

The records A-E and historical toy label Contact are INVENTED, never production NEISS findings. Hand results: total 120, five records, severe count 3, severe weight 50, severe share 41.666666...%; unknown count 1/weight 40/share 33.333333...%; conditional upper endpoint 75%. Mechanisms: Fall 40, Contact 60, Unknown 20. Fall diagnosis shares: fracture 25%, contusion 75%. Empty results have unavailable percentages.

After genuine human finalization only, run:

```text
uv run --locked python validation/verify_dashboard.py --cohort data/prepared/treadmill_2025.csv --provenance data/prepared/treadmill_2025.provenance.json --lookup data/reference/neiss_code_lookup_2025.csv --output validation/results/real_2025_dashboard_check.json
```

This command requires a matching reviewed full-annual bundle through the production loader and refuses an existing report. It checks unfiltered, each available mechanism, three outcome states, belt search, literal metacharacters, combined Fall/Severe/belt and empty selections. It compares numerical chart/table inputs and downloads. Public browser presentation and interpretation remain separate checks in DEPLOYMENT.md. No reviewed real-data result exists yet.

See review_tools/README.md for the guarded export/finalize/check workflow. Tests use invented fixtures and explicit internal test injection; there is no CLI production bypass. See results/test_summary.json for the latest actual test run and results/dashboard_fixture_results.json for numerical evidence. Root validation.pdf is an evidence draft with the remaining real/live evidence visibly pending.

## Taxonomy release update - November 5

Ryan's inclusion decisions are complete (109 Include / 79 Exclude). Version 1.1 has 184 complete review entries and four approved-inclusion/pending-mechanism rows. The original 171 personal-review confirmations stand. Final production data, actual independent findings and public evidence remain blocked by those mappings. Browser inventory again reports The browser access host is unavailable. Offline SAPI narration and FFmpeg were verified; no actual public footage or final MP4 exists. See review_tools/README.md and docs/MECHANISM_CHANGELOG.md.
