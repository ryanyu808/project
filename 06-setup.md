# 06 — Setup, configuration, and application wiring

## Purpose and design

Provide a single-page Streamlit dashboard where a CPSC epidemiology staff member can compare treadmill injury mechanisms among adults ages 65–120 and choose candidates for further investigation. Put burden and severity together before diagnosis detail so this decision requires less manual comparison. The dashboard describes ED visits; it does not establish causation, exposure-adjusted risk, or a treadmill design defect.

Setup owns configuration, initial state, page layout, navigation, and component calls. Data preparation owns cohort eligibility and classification; loading owns reading and validating prepared data; filtering owns selections and matching; views own calculations and chart construction. Keep their logic in those components. All views consume one filtered snapshot to prevent contradictory totals.

## Initial state and layout

Default to the complete 2025 calendar year, all mechanisms, all severity groups, and blank narrative search. The dataset documentation lists the full 2025 workbook (410,201 original records, 25 columns), and full 2025 XLSX/TSV files are present locally. These are source-file counts, **not** dashboard cohort totals. Require a validated 2025 prepared artifact before displaying national estimates; do not fall back to another year or a sample if it is missing.

Use one scrolling page, wide layout, with no tabs or separate pages. Configure the page before rendering content. Display:

1. Title: `CPSC Treadmill Injury Dashboard`; subtitle: adults ages 65–120, selected calendar year, descriptive investigation aid.
2. Sidebar: fixed analysis-year text from configuration, then call `filters.render_sidebar(data)` for mechanism and severity multiselects, narrative search, and reset in the order specified in `04-filters.md`. The analysis year is configured, not another interactive filter. Empty multiselects mean all; blank search means no restriction.
3. Above results: active-filter description and `Showing X of Y prepared cases`, where X is filtered row count and Y is the loaded cohort count for the configured year. Show one count caption, avoiding duplication if the filter renderer already emits it.
4. Three headline metrics in one row: estimated national ED visits, NEISS record count, weighted severe-outcome percentage, using `headline` from `05-views.md` without recomputation.
5. Next row: horizontal burden bar chart on the left; frequency–severity scatter plot on the right. On narrow screens they may stack in that order.
6. Full-width weighted primary-diagnosis composition stacked chart.
7. Full-width mechanism summary table.

Use the five views' axes, sorting, tooltips, labels, rounding, and missing-value rules exactly as specified in `05-views.md`. They are all visible initially; there is no chart picker or chart-driven filtering. Show the period and active selections alongside results. Below the headlines, show a brief severity-denominator note and the returned unknown-disposition count/weight, including zero. Explain that percentages describe the selected cases when severity is restricted. Leave decorative styling to the coding agent.

## Configuration contract

The future implementation reads `config.toml` beside `app.py` using Python 3.11+ `tomllib`. Resolve relative paths against that directory, not the shell's working directory. Proposed artifact paths below are integration targets, pending the preparation/loader specifications; setup must not generate them.

```toml
[dashboard]
title = "CPSC Treadmill Injury Dashboard"
layout = "wide"
available_views = ["headline", "mechanism_bar", "severity_scatter", "diagnosis_stack", "summary_table"]

[analysis]
year = 2025

[defaults]
mechanisms = []
severities = []
narrative_query = ""

[data]
prepared_path = "data/prepared/treadmill_2025.csv"
provenance_path = "data/prepared/treadmill_2025.provenance.json"
diagnosis_lookup_path = "dataset_neiss-sports-injuries/sample/neiss_code_lookup_2025.csv"
```

For this MVP, validate the exact sections/keys shown, their types, nonblank paths/title, `layout="wide"`, and a single integer year in `{2023, 2024, 2025}`. Reject unknown keys to expose typos. `available_views` must contain each of the five registered IDs exactly once; use its order for placement and require the sequence above for this specification. Defaults must be the empty arrays and empty string shown, matching `04-filters.md`'s current API; reject unsupported nonempty defaults rather than ignore them. This config records the agreed starting state without inventing another sidebar interface. Supporting alternative defaults later requires an explicit filter-contract update.

Changing year requires a matching prepared artifact and validated provenance for that year. No multi-year mode is exposed in this MVP, avoiding misleading year-to-year comparisons across the 2023/2024 sampling change. Do not add growth metrics or trends. `05-views.md`'s multi-year contract remains available for a later agreed extension.

## Component integration and contracts

`02-data.md` and `03-loader.md` are currently empty. The following loader boundary and artifact locations are **proposed integration contracts**, not claims that these functions already exist. Reconcile them before the build; a coding agent must report incompatible contracts rather than quietly rename fields or implement preparation inside setup.

| Component | Receives | Returns / responsibility | When |
|---|---|---|---|
| Preparation (`02`) | Full annual NEISS source and its code documentation | Prepared cohort and provenance artifact | Separate offline step, never on dashboard reruns |
| Loader (`03`), proposed `load_dashboard_data(prepared_path, provenance_path, diagnosis_lookup_path, analysis_year)` | Resolved paths and configured year | Dictionary with `data` (validated pandas DataFrame), `diagnosis_lookup` (complete lookup DataFrame), and `provenance` (dictionary below); raises an actionable load/validation error on failure | First successful load; cache thereafter |
| Filters (`04`) | `data` | `render_sidebar(data) -> FilterSelection`, then `apply_filters(data, selection) -> pd.DataFrame`, preserving rows' columns and values | Initial run and each widget rerun |
| Views (`05`) | The single filtered DataFrame, context, lookup | `build_view_data(filtered_df, *, context, diagnosis_lookup) -> dict`, exactly as specified in `05-views.md` | Initial run and every filter change |
| Setup (`06`) | Validated config and component results | Streamlit page, state messages, and placement of view renderers; no numerical aggregations | Every Streamlit rerun, reusing cached loading |

The loader must supply the union of required columns from `04` and `05`, preserving original `CPSC_Case_Number`, `Treatment_Date`, `Weight`, `Disposition`, `Diagnosis`, `Narrative_1`, `Stratum`, and `PSU`. Views additionally require derived `injury_mechanism` and `is_severe`; filters currently additionally require derived `Injury_Mechanism` and `Severity`. **This naming conflict is unresolved.** Setup must neither derive flags nor add aliases. Once reconciled upstream, each component must receive its documented schema; if both mechanism columns are supplied as an interim agreed contract, the loader must validate identical labels row by row. Severity labels and flags must likewise be consistent under their existing definitions. The unknown-mechanism spelling is a separate team issue; setup must not merge or recode labels.

Proposed provenance JSON contains `analysis_years` (one-element integer list), `source_scope` (`full_annual` or `sample`), and `source_files` (nonempty list of source filenames). Preparation records this evidence; the loader validates it against the prepared artifact and configured year. Filename, row count of the small prepared cohort, or a configuration claim alone cannot certify full-file provenance. Loading must reject partial-year or unverified inputs for national estimates. In particular, do not ingest both the XLSX and TSV versions of the same annual file as separate visits.

After configuration and loading succeed:

```text
selection = filters.render_sidebar(loaded["data"])
filtered_df = filters.apply_filters(loaded["data"], selection)
context = {
    "analysis_years": loaded["provenance"]["analysis_years"],
    "source_scope": loaded["provenance"]["source_scope"],
    "filter_description": <description of selection>
}
result = views.build_view_data(
    filtered_df, context=context,
    diagnosis_lookup=loaded["diagnosis_lookup"])
```

Build `filter_description` from `FilterSelection.mechanisms`, `.severities`, and `.narrative_query`: say “all” for empty tuples, list selected labels otherwise, and quote the trimmed search phrase or say “none”. Include search in this text even though the original views context mentioned only mechanism/severity. This is presentation of filter state, not a second implementation of matching. Escape user text through normal Streamlit text APIs.

Dispatch the five registered renderers with `result.headline`, `result.mechanism_summary`, or `result.diagnosis_composition` as specified in `05`; use `context`, `quality`, and `messages` for annotations. Treat these as dictionary keys, not object attributes. `mechanism_bar`, `severity_scatter`, and `summary_table` share the exact same mechanism summary. Renderer function names may be chosen in views; their returned chart/table objects are placed here. Never calculate weights, diagnosis shares, or severity in setup.

Initialize filter widget state once per session through `04`'s defaults. Ordinary reruns preserve selections. Reset uses `04`'s callback and returns all controls to the initial state without reloading source data. Cache contains no user selections; session state contains no alternative authoritative dataset.

## Performance and state handling

Keep raw annual files on disk and preparation offline. Read only the prepared cohort and complete lookup at startup; pandas in memory is sufficient for this restricted cohort, with no SQL server needed. Use `st.cache_data` around the loader boundary, keyed by resolved paths, file modification times/sizes (including provenance/lookup), configured year, and loader/schema version. Changed artifacts must invalidate the cache. Never cache a failed load as a successful result or substitute a stale successful result after a failed refresh.

The cached loader may provide optional startup summaries per `01-design.md`; setup must not use them as filtered results. Recompute filtering and `build_view_data` for the current snapshot on each interaction, then rerender all five views. Do not cache filtered results in a shared global variable. Read/validate the small TOML each rerun; its defaults are initialized only when a session starts. After editing configuration, restart the application to establish a fresh session. Instrument loader call counts in tests instead of requiring raw workbook timing on every interaction.

## Errors and empty states

| Condition | User-visible behavior |
|---|---|
| Missing/unparseable config, bad type/key/view ID/order/default/year | Show `Configuration error` with file, key, and correction needed; stop before loading data or rendering widgets/results. |
| Missing prepared data, provenance, or lookup | Show `Dashboard data unavailable` with the missing path and instruction to obtain/build the full-year prepared artifact through preparation; retain title/year, no numeric results. Do not download or prepare within the page. |
| Invalid loader schema, conflicting derived columns, inconsistent year/provenance | Show `Prepared data validation failed` with the actionable component error; stop results, with no partial estimates. |
| Sample provenance | Show `Full annual NEISS data required for national estimates`; no national metrics or charts. Never switch to sample files automatically. |
| Filtering error | Keep page context and controls where possible; show its actionable error; suppress results for that rerun. |
| Views `invalid_input` or `unavailable` | Render returned messages only in the results area; respect null headline/quality and empty tables. Clear any prior results. |
| Views `empty` | Keep filters and reset; show the empty-state message, 0 estimated visits, 0 records, N/A severity, and no chart marks or table rows per `05`. |
| Valid loaded cohort itself empty | Also show `No prepared treadmill cases are available.` This is distinct from a selection excluding otherwise available cases. |

No raw traceback is necessary in the user interface; retain technical details in local logs. On each rerun render only the current result so an error or empty selection cannot leave old numbers visible. Unknown diagnosis/disposition handling remains with loader/views as documented; it is not a setup error unless a component reports a contract violation.

## Local execution and future deployment

Future application entry point: repository-root `app.py`, with `config.toml` beside it. Use Python 3.11+, `streamlit`, `pandas`, and `plotly` for the chart implementation; TOML parsing uses the standard library. The future agent must declare dependencies in the project's environment and lock resolved compatible versions. `openpyxl` is needed only by offline preparation if it reads XLSX; CSV loading in the dashboard does not require it. No application code or dependency files are created by this specification.

From the team repository, the future local launch is:

```powershell
python -m pip install streamlit pandas plotly
python -m streamlit run app.py
```

Before launching, obtain full annual data using section 4 of the dataset overview (browser download where required), complete preparation according to `02`, and place the validated prepared/provenance artifacts at the configured locations. The complete lookup under `sample/` is valid reference data; the injury sample CSVs are not valid production inputs. The precise preparation command remains blocked on `02` and must be included in the combined prompt before handoff.

For later Streamlit hosting, deploy the same entry point and locked dependencies, prepare the cohort once outside the web process, and stage versioned prepared/provenance/lookup artifacts in deployment storage. Configure their paths there; avoid downloading the annual workbooks during requests. Verify memory limits and the same acceptance checks on the host, keep widget state session-specific, and invalidate caches when artifact versions change. No cloud deployment is part of this task.

## Build order and acceptance checks

Build configuration validation and page skeleton first; integrate the validated loader next; connect `04` and `05` only after their schema disagreement is reconciled; then verify layout and interactions. Use the A–E invented fixture and expected outputs from `05-views.md` in tests with `source_scope="test_fixture"` injected through a test loader, never an end-user configuration option. Extend that fixture in the test loader with the reconciled filter fields and suitable narratives; preserve the original numerical fields.

| Check | Expected result |
|---|---|
| Example TOML, fresh session, fixture loader | Year 2025; both multiselects empty, query blank; five views visible; headline 120 estimated visits, 5 records, 41.7% severe. Actual production values must come from the real prepared cohort, not these constants. |
| View placement | Three metrics first; mechanism bar left then scatter right; diagnosis composition next; summary table last. Registered IDs each rendered once; no tabs or chart picker. |
| Mechanism Fall selected | Every view uses only A/B; headline 40, 2, 25%; scatter has the single Fall point; table and diagnosis stack agree with `05`'s Fall expectations. |
| Severe selected | All views use A/C/E; headline 50, 3, 100%; visible selection note explains the changed denominator. |
| Search `belt`, with narratives A=`FELL from treadmill belt`, B=`Tripped beside treadmill`, C=`Hand caught in BELT`, D/E=null | A/C remain; headline 30, 2, 100%; context states search `belt`. Other numerical view behavior remains owned by `05`. |
| Search with no matches, then reset | Empty-state message, 0/0/N/A, no old marks/rows; options remain available; reset restores all five records and 120/5/41.7%. |
| Instrument loader, change filters repeatedly | One successful underlying load for unchanged artifacts; filtering/views rerun each time with one shared snapshot. Updating the prepared file fingerprint triggers a new load. |
| Missing config; year as string; unknown key; repeated/unknown/missing view ID; reordered views; nonempty defaults | Each reports its config problem and stops before loader execution. No silent coercion or fallback. |
| Missing file, sample or missing provenance, wrong year, inconsistent derived labels/flags | Actionable failure, no national estimates and no stale results from a previous run. |
| Empty but valid prepared cohort | Distinct no-prepared-cases message, zero headline counts and N/A severity; reset remains available. |

Before handoff, run `05`'s arithmetic and edge-case checks independently, then these wiring checks using test doubles, and finally open the real 2025 application locally to verify the initial screen and one filter/reset cycle. No implementation or live performance claim follows from these specification-level checks.

## Unresolved integration issues / rubric review

- **Required reconciliation:** `04` uses `Injury_Mechanism`, `Severity`, and `Unknown / unclear`; `05` uses `injury_mechanism`, `is_severe`, and an example `Unknown/Unclassified`. Agree one upstream schema or explicitly document compatible additional columns. Setup does not choose a taxonomy or translate it.
- **Missing pieces:** `02` and `03` are empty. Confirm the proposed CSV/provenance artifacts and loader interface, source-completeness validation, preparation command, and duplicate-source handling. These are whole-prompt completeness blockers, not reasons to fabricate preparation inside setup.
- **Stale note in `05`:** it says `04` is empty, but `04` now specifies narrative search. This setup wires that existing control and includes it in context; it does not add search matching logic or edit `05`.
- **Team confirmation retained from `05`:** primary-diagnosis-only composition and all-visit weighted severity denominator still need signoff when combining pieces; setup uses those contracts unchanged.
- **Rubric self-review:** stakeholder/decision and opening workflow are explicit (1–2); boundaries precede details, with shared rules referenced rather than repeated (3–4); component calls and cache ownership are separated (5); prepared data, local dependencies, rerun strategy, and cloud path are defined (6); source provenance and failure handling are explicit (7); build order and concrete checks are present (8). A level-3 score for the combined prompt remains contingent on resolving the integration blockers above.
