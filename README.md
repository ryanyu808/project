# CPSC Treadmill Injury Dashboard

This dashboard helps a CPSC epidemiology analyst decide which treadmill injury mechanisms among adults 65-120 deserve closer investigation. It brings weighted emergency-department visit estimates, recorded severe outcomes, primary diagnoses and narrative evidence together. It is an investigation aid; product association does not establish causation or injury risk per treadmill user.

**Public app URL:** [Open the dashboard](https://treadmill-injury-dashboard.streamlit.app/)

**Demo video URL:** [Watch the Unlisted five-minute demonstration](https://www.youtube.com/watch?v=f45CShykzbI)

**Reviewed production release and public verification complete; team submission requirements remain.** All 188 screened candidates have complete, source-bound human decisions: 109 retained injury visits, 79 exclusions. The genuine production CSV/provenance are included. Local production checks show **5,119.6280 weighted ED visits**, **24 severe records** and **22.3028% weighted severe outcomes**. The actual public app and downloaded CSV match these independent results; a separate browser session opened the app without signing in. [Live evidence](validation/results/public_dashboard_verification.json). See [independent real-data evidence](validation/REAL_DATA_RESULTS.md).

## User, cohort and scope

The official full 2025 NEISS source contains 410,201 visits and 25 fields. Screening requires age 65-120, product 3277 in any product field and a literal treadmill narrative mention. All 188 candidates were reviewed under Ryan Yu's explicitly accepted injury-focused policy. Documented treadmill use/handling injuries and medically triggered injuries are included; medical-only episodes and incidental unrelated contacts are excluded. This deliberate scope refinement of the original broader involvement vision changes totals and is recorded with its fingerprint. Other ages, years, products, records lacking the required mention and 79 reviewed exclusions are outside this released cohort. No sample is presented as an annual source.

Codebook 1.2 separates Equipment/cord obstacle or landing falls from on/from-surface Fall, without inferring motor state, exercise use or the initiating cause of imbalance. Specific moving/repair, mounting and initiating belt mechanisms retain precedence. Earlier definitions and the original one-shot prompt are preserved. [Taxonomy history](docs/MECHANISM_CHANGELOG.md).

## Use and run

Five coordinated views show headlines, mechanism burden, severe outcomes, primary diagnosis composition and summary. The eight implemented improvements add all-outcome baselines, visible supporting counts and unknowns, matching narratives, Undo reset, sensitivity endpoints, codebook definitions and full-precision reconciliation/download. Baselines remove severity only, preserving mechanism/search. Year is fixed to 2025; no geography or year-range filter exists.

```text
uv sync --locked --python 3.13
uv run --locked python -m streamlit run app.py
```

These commands work from the repository root in PowerShell or macOS/Linux. On Ryan's laptop the tested separate environment is `.venv-mvp`; use `.\.venv-mvp\Scripts\python.exe -m streamlit run app.py`. Preserve the older environment. No credentials, external database or API keys are needed. Paths resolve against the repository root. Community Cloud needs main / app.py / Python 3.13 and the committed runtime pair; [deployment instructions](DEPLOYMENT.md).

## Definitions and limits

Weights estimate ED visits, not unique people, all injuries or exposure-adjusted risk. Severe means disposition 2/4/5/8; the denominator is all selected weight, including unknown dispositions. Codes 0/1/6 are other known, 9/missing/unrecognized unknown. Primary diagnosis is one bucket per visit. Sensitivity endpoints assume none/all unknown outcomes severe; they are not confidence intervals. This cohort has no unknown dispositions, but missingness and sampling uncertainty are different issues.

Brief narratives, medical triggers, selection and taxonomy decisions constrain interpretation. The app estimates no survey-design uncertainty, brands, geography, trends, causal defects or automatic priorities. Counts do not measure statistical precision. Use official [CPSC surveillance and follow-back guidance](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Neiss-Frequently-Asked-Questions) and uncertainty outputs alongside the app. Personas are research-backed scenarios, not interviewed users.

## Validation, review and submission

```text
uv run --locked python -m pytest -q -p no:cacheprovider
uv run --locked python validation/verify_app.py --output ../local-app-check.json
```

Full suite: **180 passed**, no failures/errors/skips, Windows/Python 3.13.15. All eight original CRs, review/source guards, taxonomy, filters/exports, empty states and Git byte preservation are covered. [Results](validation/results/test_summary.json). Ubuntu/Python 3.13.18 also passed all 180 tests, genuine production validators/AppTest and HTTP health. [Actual CI evidence](deployment/CI_RESULTS.md).

[validation.md](validation.md) and root [validation.pdf](validation.pdf) retain Design / Cases / Numbers / Tests and genuine public screenshots. Ryan's [individual HW11 case](cases/ryan-treadmill-falls-final.md) includes his explicitly accepted break verdict and open CR-09. Its final PDF is separate from the team ZIP. A genuine five-minute, 1920x1080 public-app MP4 with AI narration is complete outside the repository. The Unlisted video plays in a separate browser session without signing in. Five distinct cases are integrated in the final validation: investigation priority, belt inspections, orientation, rehabilitation supervision and hospital education. [Readiness](submission/READINESS.md), [demo sequence](submission/DEMO_SCRIPT.md), and [release guard](submission/check_release.py).

The final small runtime CSV, matching provenance, 1.2 codebook and official lookup are sufficient for hosting. Raw annual files, private reviews/workbooks and audit inputs are excluded. The existing source/candidate/review template, original 171 approval rows and one-shot-prompt.md remain unchanged. [Review workflow/history](review_tools/README.md). Do not rerun finalization over existing outputs or publish private review material. The submission ZIP is generated from the final committed HEAD; its manifest and release audit are checked before hand-in.
