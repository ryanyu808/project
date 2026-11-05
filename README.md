# CPSC Treadmill Injury Dashboard

An investigation aid for a CPSC epidemiology analyst deciding which treadmill injury mechanisms among adults 65-120 deserve closer study. It combines weighted emergency-department visit estimates, recorded severe outcomes, diagnoses and narrative evidence. Product association does not establish causation or risk per treadmill-use hour.

**Public app URL:** [PENDING - not deployed]

**Demo video URL:** [PENDING - not recorded]

**Release status:** real-data production finalization is blocked by four conditional mechanism mappings. Ryan Yu personally confirms the original 171 decisions and explicitly supplied all remaining inclusion decisions: 109 Include / 79 Exclude. There are 184 complete review entries and four approved inclusions with pending mechanisms. No final runtime CSV/provenance exists, so the app honestly shows Dashboard data unavailable. Inclusion-progress counts are not production injury findings.

## Audience, data and features

The source is the official full 2025 NEISS Excel annual export: 410,201 rows and 25 original fields, January 1-December 31. Screening produced 188 age/product/text candidates. The intended released cohort restricts age to 65-120, requires product 3277 in any of three fields and a literal treadmill mention, then requires human-confirmed eligibility/mechanism. All other ages/products/mentions, other years and approved exclusions are omitted; totals change accordingly. Human inclusion decisions specify 109 retained visits and 79 exclusions, but final artifact reconciliation and real weighted results remain PENDING. No random sample is presented as a full-year estimate.

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

The single current review workbook is `data/prepared/treadmill_2025.ai_completed_review.xlsx`. Its AI recommendations supersede earlier suggestion workbooks. Read `data/prepared/final_policy_recommendation.md`: Ryan accepts this injury-focused refinement of the original broader involvement contract. Direct equipment contact, exertional injury, pain-only evidence, medical events and taxonomy gaps require real team ownership. Original case IDs, narratives and candidate values remain preserved; Ryan subsequently gave explicit personal-review confirmation for the 171 prior decisions and supplied the remaining inclusion decisions. Current status and held mechanisms are documented below; original source and AI fields remain intact.

Use Human review as the input tab; all original AI/source tabs and the original 171 approval rows are preserved. The single private decision report now records Ryan's explicit decisions and the four remaining mappings. Codebook 1.1 adds Non-use equipment/cord-related falls and explicitly covers an unpowered supporting-surface Fall; see [version history](docs/MECHANISM_CHANGELOG.md). Non-use is never inferred from missing context. The original v2 injury policy and one-shot prompt are retained unchanged.

Follow [review_tools/README.md](review_tools/README.md) for exact validate-only and post-approval execution commands. Every one of the 188 narratives requires a complete human decision, explicit verification and reviewer; the eight inclusion adjudications are recorded and only four included mechanism mappings remain held. The workflow binds the policy and candidate/source fingerprints, exports a separate review CSV, invokes the existing finalizer with version 1.1 taxonomy checks, checks independent numbers and refuses overwrites. Do not edit the original candidate/review CSV or call production finalization on AI suggestions.

Runtime needs only `data/prepared/treadmill_2025.csv`, its matching provenance JSON, the version-1.1 codebook and the complete copied lookup in `data/reference/neiss_code_lookup_2025.csv`. Raw annual files, candidate/review CSVs and workbooks are private preparation inputs and never deployed. Config.toml already points at the intended final runtime pair; neither file exists yet.

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

See validation/results/test_summary.json for the fresh full Python 3.13 run after the taxonomy and video-tool changes. [submission/READINESS.md](submission/READINESS.md) records the rubric gates and remaining actions. Ryan's existing [individual HW11 draft](cases/ryan-treadmill-falls-final.md) and claim are preserved; its public evidence and personal verdict are pending.

The root [validation.pdf](validation.pdf) and [validation.md](validation.md) contain exactly Design, Cases, Numbers and Tests after the introduction. They are evidence drafts: real-data totals, public screenshots, user interpretation and live links are visibly pending. The original [one-shot-prompt.md](one-shot-prompt.md) remains unchanged.

Latest full repository verification: **178 passed**, no failures/errors/skips, Python 3.13.15, JUnit 37.128 seconds. Git byte-preservation tests protect the runtime CSV, provenance and codebook fingerprints across Windows/Linux checkout.
