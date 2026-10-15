# 05 — Dashboard views

## Purpose and boundaries

Help a CPSC epidemiology staff member identify treadmill injury mechanisms among adults ages 65–120 that deserve further investigation by comparing estimated ED burden, severe outcomes, and diagnosis composition. These are descriptive comparisons of ED visits, not evidence of causation, exposure-adjusted risk, or a treadmill design defect.

Follow `01-design.md`: `02-data.md` prepares and classifies records once; `03-loader.md` loads and validates them; `04-filters.md` supplies a filtered pandas DataFrame; this component aggregates and renders the five views below. It never reads raw annual files, identifies treadmills, classifies narratives, applies dashboard selections, or mutates its input. `06-setup.md` owns layout, chart availability, UI configuration, defaults, and application wiring. No additional dashboard controls are introduced here.

Compute small summaries in pandas from the already prepared cohort on each filter change. Reuse the same mechanism summary across three views so their numbers agree. Do not reuse startup aggregates that ignore current filters. Separate aggregation from rendering so invented DataFrames can test each view without starting the UI. Chart library and styling remain implementation choices within setup's configuration.

## Filtering-to-views contract

Proposed interface (the adjacent component specifications are currently empty):

```python
build_view_data(filtered_df: pd.DataFrame, *, context: dict,
                diagnosis_lookup: pd.DataFrame) -> dict
```

`filtered_df` contains one row per eligible ED visit, after all active selections. Every view receives this same snapshot. Upstream components own eligibility, deduplication, numeric/date normalization, and severe-flag creation/validation. Do not explode product or diagnosis columns into extra visits.

| Required field | Origin and contract |
|---|---|
| `CPSC_Case_Number` | Original NEISS identifier; nonmissing and unique in the supplied cohort. Counts represent visits, not distinct people. |
| `Treatment_Date` | Original NEISS column, normalized upstream to a nonmissing date; use this for year, never the case-number prefix. |
| `Weight` | Original NEISS column, finite positive numeric value; each row's national ED visit contribution. |
| `Disposition` | Original NEISS code, normalized upstream to nullable integer. |
| `Diagnosis` | Original NEISS primary diagnosis code, normalized upstream to nullable integer. |
| `injury_mechanism` | **Derived**, not a NEISS column: one nonblank classification label per visit, assigned by data preparation. Unclassifiable cases must have an explicit upstream category such as `Unknown/Unclassified`. Views accept the supplied taxonomy without keyword matching or recoding. |
| `is_severe` | **Derived**, not a NEISS column: nonnull Boolean, validated upstream against `Disposition` membership in `{2, 4, 5, 8}`. |

Original eligibility fields are `Age`, `Product_1`, `Product_2`, `Product_3`, and `Narrative_1`; their rules belong exclusively to data preparation. They need not be passed to views. `Diagnosis_2`, `Other_Diagnosis`, and `Other_Diagnosis_2` are original columns but are not used in this component's diagnosis composition.

`context` must contain:

- `analysis_years`: sorted, nonempty list of the complete annual source years represented by the selected analysis period, even when filters leave no records.
- `source_scope`: `full_annual` for production; `test_fixture` only in tests; `sample` for an explicitly nonnational preview.
- `filter_description`: human-readable active mechanism and severity selections, including “all” selections. Setup supplies defaults through filtering; views do not choose them.

Production estimates require the complete annual files upstream, then the agreed cohort restriction and dashboard filters. Summing `Weight` from either supplied sample CSV does not produce national estimates. For `source_scope=sample`, return an unavailable state for these five production views with a request to load full annual data; do not display sample sums as national figures.

Check required columns and context before aggregation. Missing columns, invalid weights, duplicate/missing IDs, invalid dates, missing mechanism labels, or missing/inconsistent severe flags return `status="invalid_input"`, an actionable message identifying the upstream contract failure, and no numeric outputs. Do not silently drop rows, replace weights, deduplicate, or repair classifications in views. Check that record years are contained in `analysis_years`.

### Lookup contract and missing outcomes

Use the complete `sample/neiss_code_lookup_2025.csv` (also available as annual workbook sheet `NEISS_FMT`). Its actual columns are `Format name`, `Starting value for format`, `Ending value for format`, and `Format value label`. Restrict diagnosis lookup rows to `Format name == "DIAG"`; strip padded code strings and convert them to integer keys before a many-to-one join to `Diagnosis`. Require unique keys; prevent join multiplication. `DISP` rows document the severity codes:

| `Disposition` | Lookup meaning | `is_severe` |
|---|---|---|
| 2 | Treated and transferred | true |
| 4 | Treated and admitted/hospitalized | true |
| 5 | Held for observation | true |
| 8 | Fatality including DOA / died in ER | true |
| 0, 1, 6 | No injury; treated/examined and released; left without being seen | false |
| 9, missing, or unrecognized code | Unknown/not stated or unavailable | false, meaning **not recorded as severe**, not confirmed nonsevere |

Severity denominator is **all filtered visit weight**, including unknown disposition. This is a recorded severe-outcome percentage, not the percentage among known dispositions. Preserve unknowns in totals and report their record count and weight in supporting metadata/notes. This denominator convention needs team review before combination with the neighboring specs.

Keep each valid primary diagnosis code separate, using the lookup's code-prefixed label (e.g. `57 - FRACTURE`, `71 - OTHER`). Do not infer specific conditions from code 71 or its free text. Missing `Diagnosis` becomes `Missing diagnosis`; an unmapped code becomes `Unmapped diagnosis (<code>)`. Both remain in the composition denominator. Missing lookup columns or duplicate DIAG keys are invalid input; an individual unmapped diagnosis is not.

## Shared calculations and output contract

For any supplied subset S, with no intermediate rounding:

```text
weighted_ed_visits(S) = sum(Weight)
record_count(S) = number of rows
severe_weight(S) = sum(Weight where is_severe is true)
severe_outcome_pct(S) = 100 * severe_weight(S) / weighted_ed_visits(S)
```

Never average row percentages, mechanism percentages, or unweighted severe flags to get an overall percentage. All output names below are **derived** summary fields. Preserve numeric precision in returned data; display visit estimates rounded to whole visits, record counts as integers, and percentages to one decimal. Sort using unrounded values. Separately rounded cells need not sum to the rounded total.

Return a dictionary with `status` (`ok`, `empty`, `invalid_input`, or `unavailable`), `messages` (list of strings), unchanged `context`, `headline` (dictionary), `mechanism_summary` (DataFrame), `diagnosis_composition` (DataFrame), and `quality` (dictionary). The headline and table schemas are listed below. `quality` has keys `unknown_disposition_record_count` (integer) and `unknown_disposition_weight` (float), counting rows whose `Disposition` is missing, 9, or outside `{0, 1, 2, 4, 5, 6, 8, 9}`. Summary counts are integers, weights/percentages are numeric, and missing percentages use a nullable numeric value. For `invalid_input` or `unavailable`, set `headline` and `quality` to null and return empty tables with their declared columns; render messages only. Renderers consume these outputs and return their chart/table objects for setup to place; no hidden global filter state.

For a valid empty selection: `status="empty"`, headline visits/count = 0, severe percentage = null, both quality values = 0, and empty summary/composition tables with their declared columns. Show “No records match the current filters”; display severity as N/A and no fabricated zero bars or points. An internal zero denominator likewise yields null, never infinity or 0%.

Every view updates from the filtered rows on every selection change. A severity-only selection changes both numerator and denominator: selecting only severe records produces 100% for every nonempty mechanism. Show active filters and explain that the percentage describes the current selection. No view silently restores the unfiltered denominator or initiates chart-driven cross-filtering.

Each view must identify its analysis period. A single year is an annual estimate. If setup/filtering allows multiple years, label sums “Estimated ED visits over selected years (combined total; not annual)” and compute a ratio of summed weights for severity. Show a sampling-change caution whenever the selection includes 2023 and a year from 2024 onward. Do not add year-over-year deltas, trend lines, growth rankings, or claims of changing injury incidence across that break.

## View specifications

### 1. Headline metrics

**Purpose:** establish the selected burden, supporting sample size, and recorded severity before comparing mechanisms.

**Inputs:** all filtered rows' `Weight` and `is_severe`; shared context and quality notes. **Output:** `headline` with `weighted_ed_visits`, `record_count`, `severe_outcome_pct`. Use the shared formulas over the entire snapshot. No axes or sorting. Display the three distinct measures with units; raw NEISS records must never be labeled national visits. Missing and empty behavior follows the shared contract. All filters change all three metrics.

### 2. Horizontal mechanism bar chart

**Purpose:** rank mechanisms by estimated national ED burden to find frequent mechanisms worth reviewing.

**Inputs:** `injury_mechanism`, `Weight`, `is_severe` from filtered rows. **Output:** one `mechanism_summary` row per present mechanism with `injury_mechanism`, `weighted_ed_visits`, `record_count`, `severe_outcome_pct` using the shared formulas within each mechanism.

**Axes:** x = weighted ED visits, linear starting at zero; y = mechanism. Sort top to bottom by weighted ED visits descending, ties by mechanism label ascending. Include all present mechanisms, including the upstream unknown category; no top-N truncation or empty categories. Tooltip includes all four summary fields. Missing/invalid inputs follow the shared rules. Rebuild from the current selection after either filter changes.

### 3. Frequency–severity scatter plot

**Purpose:** compare burden and recorded severity together; support investigation priorities without inventing a combined risk score.

**Input/output:** use `mechanism_summary` unchanged; one labeled point per mechanism. **Axes:** x = weighted ED visits (linear, starting at zero); y = weighted severe-outcome percentage (0–100%). Label every point with its mechanism and expose all summary fields in the tooltip. Use uniform marker size; record count remains available in the tooltip. Draw in the summary's deterministic order; spatial position is determined by values, not ranking. Offset labels as needed without changing coordinates; coincident mechanisms must retain separate labels/tooltips. A null percentage has no plottable y-value: omit that point and state why. Empty selections have no points. All filtering and unknown-category behavior matches the summary/bar chart.

### 4. Weighted diagnosis composition by mechanism

**Purpose:** show whether mechanisms have different mixes of primary diagnoses, providing clinical context for further investigation.

**Inputs:** filtered `injury_mechanism`, `Diagnosis`, `Weight`, DIAG lookup, and mechanism summary order. Use **only primary `Diagnosis`**, one diagnosis bucket per visit, to avoid counting visits twice.

**Output:** long-form `diagnosis_composition` with `injury_mechanism`, `diagnosis_code` (nullable), `diagnosis_label`, `diagnosis_weighted_ed_visits`, and `diagnosis_pct`:

```text
diagnosis_weighted_ed_visits(m,d) = sum(Weight in mechanism m and diagnosis bucket d)
diagnosis_pct(m,d) = 100 * diagnosis_weighted_ed_visits(m,d)
                   / weighted_ed_visits(m)
```

**Axes:** horizontal 100% stacked bars, x = percentage of mechanism's weighted ED visits (0–100%); y = mechanism in the burden bar chart's order. Stack known diagnosis codes ascending, then unmapped codes ascending, then missing diagnosis. Use consistent diagnosis colors and legend across mechanisms within a snapshot. Include all buckets, without merging into an additional “Other” group. Return observed mechanism/bucket pairs; absent pairs render as zero-width segments. Tooltip includes mechanism, diagnosis code/label, weighted visits, and share. Each nonempty mechanism sums to 100% before rounding. Unknown/missing diagnosis is retained as specified above. All dashboard filters recalculate both cell weights and within-mechanism denominators.

### 5. Summary table

**Purpose:** give exact supporting values for the same mechanism comparisons.

**Input/output:** render `mechanism_summary` with columns in this order: mechanism, estimated weighted ED visits, NEISS record count, weighted severe-outcome percentage. No chart axes. Default row order and missing/filter behavior match the burden chart. Show all mechanisms; do not add a total row that averages severity. The headline already supplies the correctly weighted total. Preserve numeric types for formatting and any table sorting.

## Independent acceptance checks (invented data only)

Build aggregation first, then test each renderer against these outputs, then wire into setup. Tests need no raw files or narrative classifier. These labels are fixture labels, not a proposed production taxonomy. All dates below are `2025-01-01`; IDs A–E are unique test identifiers; context is `analysis_years=[2025]`, `source_scope="test_fixture"`, filters “all”. Supply the real DIAG lookup.

| `CPSC_Case_Number` | `injury_mechanism` | `Weight` | `Disposition` | `is_severe` | `Diagnosis` |
|---|---|---:|---:|---|---:|
| A | Fall | 10 | 4 | true | 57 |
| B | Fall | 30 | 1 | false | 53 |
| C | Contact | 20 | 2 | true | 57 |
| D | Contact | 40 | 9 | false | missing |
| E | Unknown/Unclassified | 20 | 5 | true | 71 |

1. **Headline alone:** weight = 120; records = 5; severe weight = 50; percentage = `100*50/120 = 41.666666…%` (display 41.7%). Quality reports 1 unknown-disposition record, weight 40. This catches an unweighted 60% calculation and exclusion of unknown disposition.
2. **Burden bar alone:** rows in order Contact (60, 2, 33.333333…%), Fall (40, 2, 25%), Unknown/Unclassified (20, 1, 100%). Bar lengths are 60, 40, 20; all labels present. Their weights/counts reconcile to the headline.
3. **Scatter alone:** labeled coordinates Contact `(60, 33.333333…)`, Fall `(40, 25)`, Unknown/Unclassified `(20, 100)`. Exactly three equal-size points; record counts 2, 2, 1 in tooltips.
4. **Diagnosis stack alone:** Contact: fracture weight 20 / 33.333333…%, missing weight 40 / 66.666666…%; Fall: contusions/abrasions (53) weight 30 / 75%, fracture (57) weight 10 / 25%; Unknown/Unclassified: code 71 weight 20 / 100%. Each bar totals 100%, and diagnosis weights sum to the corresponding mechanism's visits. Adding `Diagnosis_2=57` to every fixture row must leave outputs unchanged.
5. **Table alone:** exactly the three rows and four fields in check 2, with the specified default ordering and display rounding. No omitted unknown mechanism or extra total row.
6. **Filter response:** filtering upstream to Fall only yields headline (40, 2, 25%), one bar, one scatter point `(40,25)`, one table row, and the Fall diagnosis shares above. Filtering upstream to severe records A/C/E yields (50, 3, 100%); mechanism order Contact, Unknown/Unclassified, Fall (20/20/10 visits, alphabetical tie break); each severity is 100%. Contact and Fall are 100% fracture, unknown mechanism is 100% code 71. All five views must agree.
7. **Empty and invalid:** an empty frame retaining the required schema returns the declared empty state. Null/negative/infinite `Weight`, duplicate IDs, blank mechanism, missing required column, or A's severe flag changed to false must each fail explicitly with no partial totals. Set A's disposition to 8, retaining true: headline remains unchanged (death counts as severe). Set D's disposition to missing, retaining false: totals remain unchanged and unknown quality weight remains 40.
8. **Diagnosis fallback:** replace D's missing diagnosis with invented code 999; its 40 weight / 66.666666…% becomes `Unmapped diagnosis (999)`, with no change to any other view. Duplicate a DIAG lookup key: fail rather than multiply weight.
9. **Provenance and period:** `source_scope="sample"` returns unavailable national views. For a period-label test only, copy the fixture to 2023 with distinct IDs and combine it with the 2025 fixture: totals = 240 visits, 10 records, 41.666666…%; labels say combined 2023 and 2025 total, and show the sampling-change caution. Do not label 240 an annual estimate or compute a growth percentage.

Compare unrounded numerical results within `1e-8`. Render checks verify units, category order, labels, filter/period context, and empty states, not pixel styling. No inferential significance, reliability threshold, or confidence interval is invented here; expose record counts alongside estimates and describe the dashboard as an investigation aid.

## Integration decisions to review

- `02-data.md`, `03-loader.md`, `04-filters.md`, and `06-setup.md` are empty at drafting time. Confirm the proposed derived names, payload/context fields, single-label mechanism taxonomy, validation ownership, and denominator convention when combining pieces.
- The vision does not specify an analysis period. Setup must choose the initial year/period and default filters; views support explicit period metadata without assuming a new year control. Prefer within-year mechanism comparisons; multi-year sums require the labels/caution above.
- Confirm primary-diagnosis-only composition and the treatment of unknown disposition as not recorded severe in an all-visit denominator. These are explicit proposed conventions, not previously documented team decisions.
- Basis inspected: `00-vision.md`, `01-design.md`, `08-architect/one-shot-prompt-specs.md`, Module 8 README/orientation, dataset README/overview, actual sample headers, and complete DIAG/DISP lookup rows. No separate Module 8 handout was found locally. The copied lookup in this team repository matches the sibling dataset repository.
