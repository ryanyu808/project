# CPSC Treadmill Injury Dashboard

A Streamlit investigation aid for a CPSC epidemiology analyst deciding which
treadmill mechanisms among older adults warrant deeper investigation. It helps
compare burden with recorded severity and inspect the supporting evidence. It
does not establish exposure-adjusted risk or a product defect.

**Public app URL:** [PENDING — not deployed]

**Demo video URL:** [PENDING — not recorded]

The dashboard describes treadmill-related emergency-department
visits among adults ages 65–120. It implements the supplied one-shot prompt:
weighted burden, recorded severity, primary-diagnosis composition, and supporting
NEISS counts describe the selected records. Explicit comparison baselines remove
only severity and keep the same mechanism and literal narrative selections. No geographic or year-range controls.

**Production data is awaiting human review.** The software runs, but the default
2025 page intentionally displays `Dashboard data unavailable` until a reviewed
full-year artifact is installed. It never substitutes samples or invented data.
All 188 real 2025 candidates must be reviewed before finalization. The local
annual Excel export passed 410,201-row/25-column/full-year source checks. Older
build reports mention 2023/2024 exports; those audit bundles are not present in
this checkout. Candidate counts are screening counts, not reviewed injury estimates. See [BUILD_REPORT.md](BUILD_REPORT.md).

## Install and run from a fresh clone

Install [uv](https://docs.astral.sh/uv/getting-started/installation/); it installs
Python 3.13 and the locked dependencies when needed. Python 3.11–3.13
is declared supported; this session tested Windows/Python 3.13.15. The existing
Python 3.14 .venv was preserved; to use the separate tested environment, set
`UV_PROJECT_ENVIRONMENT=.venv-mvp` (PowerShell: `$env:UV_PROJECT_ENVIRONMENT =
'.venv-mvp'`; macOS/Linux: `export UV_PROJECT_ENVIRONMENT=.venv-mvp`).
No Node, database, external AI service, annual-data download, or operating-system
service is needed to launch the page.

macOS:

```bash
uv sync --locked --python 3.13
uv run --locked streamlit run app.py
```

Windows PowerShell:

```powershell
uv sync --locked --python 3.13
uv run --locked streamlit run app.py
```

The page opens at the URL Streamlit prints.
To choose a free port, append `--server.port 8502` (choose another if occupied).
Stop with Ctrl+C. Configured paths always resolve against this repository,
regardless of the shell's working directory.

## Features added for the MVP

- Severity comparison retains an all-outcome baseline when severity is restricted;
  its x-axis shows severe visit weight among selected records and its y-axis
  shows the baseline severe share. Denominators and populations are explicit.
- Visible mechanism evidence includes record counts and unknown-outcome counts
  and weights. Counts are not confidence intervals; uncertainty is not estimated.
- Search shows matching IDs and verbatim narratives after all active filters.
- Mechanism definitions and precedence are available beside the controls.
- A diagnosis baseline preserves context under severity restrictions.
- Undo reset restores the last reset selection within the current session.
- Outcome completeness shows U/T, S/T, and (S+U)/T as conditional sensitivity
  endpoints, not confidence intervals or changes to recorded outcomes.
- A reconciliation panel and CSV download expose unrounded contributions,
  rounding differences, active filters, period, and prepared-data hash.

## Data coverage and limitations

The intended release uses the complete 2025 annual source, restricted to ages
65–120, any product code 3277, a treadmill narrative mention, and genuine human
review. It is a cohort restriction, not a random downsample. Other ages, years,
products, narratives without treadmill text, and documented human exclusions are
left out. Consequently estimates describe the reviewed cohort, not all exercise
equipment injuries or all older adults. Retained/excluded counts and real-data
totals remain PENDING. No real numeric results currently display.

NEISS describes ED visits, not unique people or non-ED injuries. These files do
not supply treadmill hours, users, brands, or usable geography. Disposition is a
limited recorded outcome measure. No causal, design-defect, risk-per-hour, trend,
statistical-significance, or confidence-interval claims are made. Medical-only
events and stationary-equipment scope require a documented team decision.

## Acquire and prepare production data offline

The copied complete lookup in `data/reference/neiss_code_lookup_2025.csv` comes
unchanged from the dataset repository (1,250 rows, four columns). The sports
product list is not a cohort restriction and is not modified or needed at runtime.
Raw annual files and audit CSVs are intentionally excluded from git.

1. Visit the official [NEISS download page](https://www.cpsc.gov/cgibin/NEISSQuery/home.aspx).
   Select affiliation, **Archived Annual NEISS Data**, year, Excel or Tab Delimited
   Text, then **Find Data**. Save under `data/raw/` (create it if absent). If a link
   is blocked, use these browser instructions; the app does not retry downloads.
2. Use **one** case-data representation per year. Excel explicitly reads
   `NEISS_2023`, `NEISS_2024`, or `NEISS_2025`; `NEISS_FMT` is the lookup sheet.
   The 2025 TSV is faster and uses MM/DD/YYYY dates. Samples use ISO dates and
   cannot produce national views. Baseline row counts are 338,262 / 361,672 /
   410,201 and exactly 25 columns, with January 1–December 31 coverage.
3. This checkout already has a valid 2025 export under data/prepared/ from
   dataset_neiss-sports-injuries/data/neiss2025.xlsx. Preserve it and the raw file;
   do not rerun into the same output directory. For a new export/revision only:

```text
uv run python prepare_data.py candidates --source data/raw/neiss2025.tsv --year 2025 --source-scope full_annual --lookup data/reference/neiss_code_lookup_2025.csv --output-dir data/prepared
```

For Excel, replace the source with `data/raw/neiss2025.xlsx`; use the matching
year for 2023 or 2024. Do not combine TSV/XLSX twins. Each year is independent.
The export writes the candidates, blank reviews, source evidence, quality report,
approved codebook and derived-field README. It refuses to overwrite existing
candidate/review files; use a new output directory for a new revision. On a
structural failure, inspect the quality report, correct the upstream source,
and rerun; source count/schema/date revisions require official confirmation.

4. A **human** must inspect every candidate narrative using
   `data/prepared/mechanism-codebook.md`, confirm treadmill involvement, and fill
   `treadmill_2025.reviews.csv`. Keep IDs unchanged. Set `reviewed=true` for every
   row, `treadmill_confirmed=true/false`, an approved `injury_mechanism` for retained
   rows, and a nonblank `review_note` explaining each exclusion. Use explicit
   true/false values. `Unknown/Unclassified` is for reviewed unclear narratives.
   Do not edit candidates or replace review with automated classification.
5. Finalize:

```text
uv run python prepare_data.py finalize --candidates data/prepared/treadmill_2025.candidates.csv --reviews data/prepared/treadmill_2025.reviews.csv --codebook data/prepared/mechanism-codebook.md --output-dir data/prepared
```

The finalizer checks the raw-source and candidate fingerprints, source evidence,
complete matching review ID sets, labels and reasons, then publishes CSV and
provenance. Preserve candidate/review/source/quality evidence locally; these files
are not read by the page. Commit only the final small CSV/provenance and the
runtime lookup if publishing a reviewed data bundle. Never commit annual files.
A missing review, changed candidate or malformed visit prevents finalization.

The app initially uses 2025, all mechanisms and severities, and blank search.
To switch the fixed year, edit `analysis.year` and both artifact paths in
`config.toml` to a reviewed matching bundle, then restart. No fallback occurs.
Changed prepared/provenance/lookup fingerprints invalidate the loader cache.
The denominator for severe outcomes includes unknown disposition weight; selecting
severity changes both numerator and denominator. Primary Diagnosis alone defines
composition. Survey uncertainty, exposure risk and causal conclusions are outside
this application.

The consolidated local suggestion workbook is
`data/prepared/treadmill_2025.consolidated_review.xlsx`. It compares all 188 IDs,
preserves narratives, displays prior assistant assessments, and leaves human
decisions blank. Review policy notes before using the priority queue. It is
ignored by git and is not a deployment input. Agreement between AI columns is
not human verification. The original review CSV remains authoritative for the
eventual human-reviewed finalization step.

## Checks and structure

```text
uv run --locked python -m pytest -q -p no:cacheprovider
uv run --locked python validation/independent_numbers.py
```

The tests use invented records and an explicit test-only loader, never a
production configuration accepting fixture source counts. They verify preparation,
artifact rejection, unrounded arithmetic, renderers, filters, widget/reset cycles,
cache reuse/invalidation and error states. Pytest temporary files follow the
platform temporary directory; set `TMPDIR` to a spacious directory if needed.

- `configuration.py`, `app.py`: strict TOML, cache boundary, session controls and layout.
- `prepare_data.py`: offline export and human-review-gated finalization.
- `contracts.py`, `loader.py`: shared representations and artifact validation.
- `filters.py`: pure row selection and sidebar.
- `views.py`: pure summaries and five registered renderers.

See [DEPLOYMENT.md](DEPLOYMENT.md) for the release checklist. No public
deployment has occurred. See [validation.md](validation.md) for the draft
validation, with pending real-data/live evidence clearly marked. The full prompt is preserved unchanged in
[one-shot-prompt.md](one-shot-prompt.md).
