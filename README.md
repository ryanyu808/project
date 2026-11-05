# CPSC Treadmill Injury Dashboard

An investigation aid for a CPSC epidemiology analyst deciding which treadmill injury mechanisms among adults 65-120 deserve closer study. It combines weighted emergency-department visit estimates, recorded severe outcomes, diagnoses and narrative evidence. Product association does not establish causation or risk per treadmill-use hour.

**Public app URL:** [PENDING - not deployed]

**Demo video URL:** [PENDING - not recorded]

**Release status:** software and fixture checks work; the reviewed real-data release is blocked by human review. Opening the app now intentionally shows Dashboard data unavailable. It never substitutes invented results. The latest AI recommendation is 108 Include / 72 Exclude / 8 Unresolved; the workbook has 171 recorded approval entries whose informed-review basis is unestablished, plus 17 priority cases without decisions. These are review-progress counts, not injury findings.

## Audience, data and features

The source is the official full 2025 NEISS Excel annual export: 410,201 rows and 25 original fields, January 1-December 31. Screening produced 188 age/product/text candidates. The intended released cohort restricts age to 65-120, requires product 3277 in any of three fields and a literal treadmill mention, then requires human-confirmed eligibility/mechanism. All other ages/products/mentions, other years and approved exclusions are omitted; totals change accordingly. The final retained count and real weighted results are PENDING. No random sample is presented as a full-year estimate.

Five coordinated views show the headline, burden, severity scatter, primary diagnosis composition and summary. Eight MVP improvements add all-outcome severity and diagnosis baselines, visible record/unknown-outcome evidence, matching narratives, Undo reset, missing-outcome sensitivity, mechanism definitions and full-precision reconciliation/CSV export. Baselines retain mechanism/search and remove only severity. Year is fixed to 2025; no geographic or year-range filter exists.

## Run locally

Install uv, clone the repository, then from its root:

```powershell
uv sync --locked --python 3.13
uv run --locked python -m streamlit run app.py
```

The same commands work in a macOS/Linux shell. This session tested Windows/Python 3.13.15. On this laptop the separate tested environment is `.venv-mvp`; preserve the older `.venv` and use `$env:UV_PROJECT_ENVIRONMENT='.venv-mvp'` before uv, or run `.\.venv-mvp\Scripts\python.exe -m streamlit run app.py` directly. Paths in config.toml resolve against the repository root. The page prints a local URL; stop with Ctrl+C. No API key, external service or database is required.

## Data preparation and genuine human review

The local annual source and existing candidate evidence must not be overwritten. The original source is `dataset_neiss-sports-injuries/data/neiss2025.xlsx`. Acquisition instructions for a fresh source are on the [official NEISS download page](https://www.cpsc.gov/cgibin/NEISSQuery/home.aspx): Archived Annual NEISS Data, year, Excel or tab-delimited. Never concatenate XLSX/TSV twins or substitute a sample.

For a fresh source/export only, use a new directory:

```text
uv run python prepare_data.py candidates --source dataset_neiss-sports-injuries/data/neiss2025.xlsx --year 2025 --source-scope full_annual --output-dir data/new_export_2025
```

The single current review workbook is `data/prepared/treadmill_2025.ai_completed_review.xlsx`. Its AI recommendations supersede earlier suggestion workbooks. Read `data/prepared/final_policy_recommendation.md`: it is a proposed injury-focused refinement of the original broader involvement contract. Direct equipment contact, exertional injury, pain-only evidence, medical events and taxonomy gaps require real team ownership. Original case IDs, narratives and candidate values remain preserved; 171 approval entries were transcribed by the assistant from a blanket chat endorsement. Their saved values do not establish informed case-level human verification; no approval fields were changed in this completion session.

Start with the workbook's Review guide and use Human review as the only input tab. Its first 17 rows contain eight inclusion decisions and nine included mechanism mappings. The other 171 entries pass structural row checks, but all are flagged for unestablished informed review: the assistant copied AI reasons following blanket chat acceptance, including 59 adjudication-flagged entries without independent human resolutions. This does not prove review never happened. Preserve the entries and establish their actual basis before release. `review_tools/review_readiness.py` reports both entry completeness and this provenance limitation. The single current private decision table is `data/prepared/treadmill_2025.mvp_decision_report.md`; the older Approval review sheet remains AI audit evidence.

Follow [review_tools/README.md](review_tools/README.md) for exact validate-only and post-approval execution commands. Every one of the 188 narratives needs a human decision, explicit verification and reviewer; the eight unresolved cases need correction and included taxonomy gaps need a written mapping resolution. The workflow binds the policy and candidate/source fingerprints, exports a separate review CSV, invokes the unchanged finalizer, checks independent numbers and refuses overwrites. Do not edit the original candidate/review CSV or call production finalization on AI suggestions.

Runtime needs only `data/prepared/treadmill_2025.csv`, its matching provenance JSON, the version-1.0 codebook and the complete copied lookup in `data/reference/neiss_code_lookup_2025.csv`. Raw annual files, candidate/review CSVs and workbooks are private preparation inputs and never deployed. Config.toml already points at the intended final runtime pair; neither file exists yet.

## Metrics and limitations

Weights sum to estimated ED visits for the reviewed cohort. Recorded severe outcomes are dispositions 2/4/5/8. Severe percentage uses all selected weight, including unknown dispositions; 0/1/6 are other known, while 9/missing/unrecognized are unknown. One visit contributes one primary Diagnosis bucket, with missing/unmapped buckets retained. Sensitivity endpoints assume none versus all unknown outcomes were severe; they are not confidence intervals. CSV export retains unrounded contributions and identifies filters/period/data hash.

NEISS records visits, not unique people, all injuries or treadmill users. Brief narratives, medical triggers, missing outcomes and cohort decisions limit interpretation. The app does not estimate survey uncertainty, exposure-adjusted risk, brands, geography, trends, causation or product defects. The [CPSC FAQ](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Neiss-Frequently-Asked-Questions) describes the surveillance context. Personas and workflow assumptions still need team/user validation.

## Testing, validation and deployment

```text
uv run --locked python -m pytest -q -p no:cacheprovider
uv run --locked python validation/run_fixture_checks.py --output validation/results/dashboard_fixture_results.json
```

See `validation/results/test_summary.json` for the latest actual run. Invented fixtures exercise source/review gates, filters, all eight change requests, independent arithmetic, CSV precision, taxonomy resolutions and the complete isolated finalization workflow. Fixture agreement is not real-data verification. After genuine finalization, run the independent real-data command in [validation/README.md](validation/README.md), then compare the public interface and exports.

[DEPLOYMENT.md](DEPLOYMENT.md) specifies the runtime manifest, Community Cloud setup and incognito/functional checks. [submission/DEMO_SCRIPT.md](submission/DEMO_SCRIPT.md) contains the five-minute script and recording checklist; [submission/SUBMISSION_CHECKLIST.md](submission/SUBMISSION_CHECKLIST.md) covers final review, links and ZIP creation. No public app or video exists yet.

The fresh full Python 3.13 suite passed 163 tests with no failures, errors or skips on November 5, 2026. [submission/READINESS.md](submission/READINESS.md) records the rubric gates and remaining actions. Ryan's existing [individual HW11 draft](cases/ryan-treadmill-falls-final.md) and claim are preserved; its public evidence and personal verdict are pending.

The root [validation.pdf](validation.pdf) and [validation.md](validation.md) contain exactly Design, Cases, Numbers and Tests after the introduction. They are evidence drafts: real-data totals, public screenshots, user interpretation and live links are visibly pending. The original [one-shot-prompt.md](one-shot-prompt.md) remains unchanged.
