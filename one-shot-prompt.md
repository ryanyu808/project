# CPSC Treadmill Injury Dashboard — One-shot Build Prompt

Build the dashboard specified below using this prompt and the NEISS dataset repository. Sections preserve the team's decisions in source-file order. References to numbered Markdown files refer to the corresponding sections here, not additional build dependencies.

## Unresolved integration issues

Do not silently resolve conflicting requirements. Report the affected integration before implementing it; unaffected pieces can be built and checked independently.

- Preparation specifies sample CSVs for development; loader, views, and setup require full annual files for national estimates. The production preparation command remains unspecified.
- Loader expects three years in the full prepared dataset and mentions age/year filters; filters define mechanism, severity, and narrative controls; setup specifies a single configured year, initially 2025. Agree artifact coverage and period selection without inventing controls.
- Loader specifies a DataFrame plus metadata and `full`/`sample` mode; setup proposes a dictionary, CSV/provenance artifacts, and `full_annual`/`sample` provenance. Confirm the exact interface and source-completeness validation.
- Vision bounds age at 65–120; loader says 65+ without an explicit upper bound. Preparation requires manual narrative/mechanism review, whose production workflow must be documented. Views retain team-review questions about primary-diagnosis composition and the all-visit severity denominator.

The remaining issues above are unresolved. The shared derived-field contract is settled: preparation creates `injury_mechanism` and `is_severe`; the loader preserves and validates them; filters apply selections using local severity display categories derived from `Disposition`; views aggregate; setup connects the components. Unknown mechanisms use `Unknown/Unclassified`. All invented fixtures below are test data, not national findings.

## 00 — Vision — CPSC Treadmill Injury Dashboard

Our stakeholder is a member of the CPSC epidemiology team who needs to decide which types of treadmill injuries among adults aged 65 and older deserve further investigation. The dashboard will provide a quick way to compare injury mechanisms based on estimated national emergency department (ED) visits and how frequently they result in severe outcomes.

For this prototype, we are focusing only on treadmill injuries among adults ages 65–120 rather than the entire sports injury dataset. A case must have product code `3277` in at least one of the three product columns and mention a treadmill in `Narrative_1`. We will use `Weight` to estimate national ED visits and define a severe outcome as a case involving transfer, hospital admission, observation, or death.

The dashboard will help the epidemiology team identify injury mechanisms that may warrant closer investigation by comparing their estimated frequency and severity in one place.

## 01 — Architecture and design

### Architecture diagram

```text
                  RAW CPSC INJURY DATA
                           |
                           v
          +--------------------------------+
          | 02-data.md (Richard)                    |
          | DATA PREPARATION               |
          |                                |
          | - Filter ages 65–120           |
          | - Product code 3277            |
          | - Check Narrative_1            |
          | - Classify injury mechanisms   |
          | - Clean and validate records   |
          |                                |
          | Runs: Once ahead of time       |
          +--------------------------------+
                           |
                    Cleaned DataFrame
                           |
                           v
          +--------------------------------+
          | 03-loader.md (James)                  |
          | DATA LOADING & VALIDATION      |
          |                                |
          | - Load prepared data           |
          | - Validate required columns    |
          | - Check Weight and severity    |
          | - Precompute summary metrics   |
          |                                |
          | Runs: Ahead of time / startup  |
          +--------------------------------+
                           |
                   Loaded DataFrame
                           |
                           v
          +--------------------------------+
          | 04-filters.md (Parth)                 |
          | FILTERS                        |
          |                                |
          | - Filter by injury mechanism   |
          | - Filter by severity           |
          | - Apply user selections        |
          |                                |
          | Runs: On each filter change    |
          +--------------------------------+
                           |
                  Filtered DataFrame
                           |
                           v
          +--------------------------------+
          | 05-views.md (Ryan)                   |
          | DASHBOARD VISUALIZATIONS       |
          |                                |
          | - Estimated national ED visits |
          | - Severe outcome comparisons   |
          | - Injury mechanism charts      |
          | - Summary tables               |
          |                                |
          | Runs: On each interaction      |
          +--------------------------------+
                           ^
                           |
                    Dashboard settings
                           |
          +--------------------------------+
          | 06-setup.md (Colby)                   |
          | SETUP & CONFIGURATION          |
          |                                |
          | - Dashboard layout             |
          | - Default filter settings      |
          | - Available charts and views   |
          | - User interface configuration |
          |                                |
          | Runs: When dashboard starts    |
          +--------------------------------+
```

### Design decisions

**1. Clear Pieces:** We will divide the dashboard into five components so that data preparation, loading, filtering, visualization, and setup can be developed and tested independently.

**2. Simple Connections:** Components will exchange pandas DataFrames with clearly defined inputs and outputs. Each component will focus on its own responsibility without modifying unrelated components.

**3. Local Changes:** We will keep data preparation rules, filtering logic, visualizations, and dashboard settings separate. This allows us to update injury classifications or dashboard features without rewriting the entire application.

**4. Real-World Operation:** We will clean and classify the injury data once ahead of time, then load the prepared data when the dashboard starts. We will cache reusable calculations to avoid unnecessary processing during user interactions.

## 02 — Data Cleaning Instructions

### Goal

Create reproducible, analysis-ready NEISS tables for screening possible
treadmill injury mechanisms among adults age 65 and older. Preserve all raw
files unchanged. The cleaned data supports screening and narrative review; it
must not be used to claim that a treadmill caused an injury.

### Inputs

Use these files:

- `neiss_all_products_2025_sample.csv`
- `neiss_sports_2023_2025_sample.csv`
- `neiss_code_lookup_2025.csv`
- `sports_product_codes.csv`

The two NEISS case files are samples for development only. Do not report their
counts, percentages, or summed weights as national estimates.

### Required cleaning steps

1. Read each CSV with pandas and confirm its row count, column names, and
   duplicate-case count before transforming it.

2. Keep raw columns unchanged. Create new cleaned or derived columns rather
   than replacing `Age`, `Treatment_Date`, product codes, or narratives.

3. Convert `Treatment_Date` to a datetime column. Record rows with invalid or
   missing dates rather than silently dropping them.

4. Handle age correctly:
   - `Age == 0` means age is not recorded.
   - `Age` values `201` through `223` represent age in months, not years.
   - Create an `adult_65_plus` flag only when age is from 65 through 120 years.
   - Do not treat infant month codes as adults.

5. Preserve `Product_2 == 0` and `Product_3 == 0` as “no additional product,”
   rather than treating them as missing product codes.

6. Standardize `Narrative_1` only in a derived text column:
   - convert to string safely;
   - trim leading/trailing whitespace;
   - create an uppercase or lowercase version for matching;
   - preserve the original narrative for review.

7. Create transparent candidate flags for treadmill review:
   - an exercise-equipment flag when `Product_1`, `Product_2`, or `Product_3`
     equals `3277`;
   - a narrative treadmill flag when the cleaned narrative contains
     `TREADMILL`;
   - a candidate flag requiring both adult age 65+ and treadmill evidence.
   Keep the separate flags so analysts can inspect disagreements.

8. Do not automatically label an injury mechanism as fact. If AI proposes
   narrative categories such as fall, belt-related fall, entering/exiting,
   struck by equipment, repair/moving, or unclear, save the rule and label in
   separate columns and require manual review of every candidate narrative.
   Preparation creates `injury_mechanism` as one nonblank reviewed label per visit;
   missing or unclassifiable mechanisms use exactly `Unknown/Unclassified`.
   Preparation also creates `is_severe`, a nonnull Boolean: true exactly when
   `Disposition` is 2, 4, 5, or 8; false otherwise, including code 9, missing,
   or unrecognized codes (not recorded severe, not confirmed nonsevere).
   These are derived columns, not original NEISS columns. Preserve `Disposition`.

9. Clean the code lookup table before joining:
   - trim whitespace from code fields;
   - convert code values to numeric using an error-safe conversion;
   - treat the `.` values in `HISP` and `ALC_DRUG` as missing;
   - join labels using both the relevant format name and code.
   Do not use an equality join for the `AGELTTWO` 2-to-120 range.

10. Keep the sports-product lookup unchanged. Use it only to identify sports
    codes and subgroup labels, recognizing that a visit may have up to three
    product codes.

11. Retain missing secondary diagnosis and body-part fields. A blank secondary
    field means a second injury was not recorded; it is not an error to fill
    with a diagnosis label.

12. Save outputs separately from raw data:
    - a cleaned case table;
    - a treadmill-candidate table;
    - a data-quality report with row counts, missingness, duplicates, and
      counts at each filtering step;
    - a README describing every derived column and rule.

### Validation checks

Before sharing outputs, verify that:

- no raw rows were overwritten;
- case IDs remain unique;
- all treatment dates parse correctly or appear in an exceptions report;
- all adult-65+ records have ages from 65 through 120;
- product-code flags check all three product columns;
- narrative-rule results can be traced to the original narrative;
- joins do not unexpectedly multiply case rows;
- raw sample totals are never described as U.S. national totals.

### AI use rule

AI may suggest cleaning code, regular expressions, and candidate narrative
rules. A human must inspect the resulting rows, especially all treadmill and
mechanism classifications, verify output counts, and document each decision.

## 03 — Loader

You are responsible for implementing the data-loading layer for the NEISS
treadmill-injury dashboard.

The dashboard is designed for a CPSC epidemiology analyst reviewing
treadmill-related emergency-department visits among adults age 65 and older.

Your component sits between the prepared NEISS case-level artifact and the
interactive filtering and visualization components.

Do not redesign the dashboard or invent new analytical definitions.
Implement the loading behavior described below.

### Job

The loader must:

1. load the compact case-level dataset created by data preparation;
2. validate its eligibility and derived fields without reclassifying records;
3. preserve the prepared rows and columns needed by downstream components;
4. precompute the metadata and counts needed by downstream components;
5. verify the data facts that the rest of the application relies on.

The Streamlit app must not reread and scan all three raw Excel workbooks
after every user interaction.

### Source data

Use the full annual NEISS files for 2023, 2024, and 2025 when available.

Expected files:

- neiss2023.xlsx
- neiss2024.xlsx
- neiss2025.xlsx

Each workbook contains a main annual NEISS sheet and an `NEISS_FMT`
lookup sheet.

The annual case files contain these fields:

- CPSC_Case_Number
- Treatment_Date
- Age
- Sex
- Race
- Other_Race
- Hispanic
- Body_Part
- Diagnosis
- Other_Diagnosis
- Body_Part_2
- Diagnosis_2
- Other_Diagnosis_2
- Disposition
- Location
- Fire_Involvement
- Product_1
- Product_2
- Product_3
- Alcohol
- Drug
- Narrative_1
- Stratum
- PSU
- Weight

Do not modify the source workbooks.

### Validate the prepared rows

Data preparation owns the following annual-file steps, including creation of
`treatment_year`; the loader validates their results rather than repeating them:

1. Read the main NEISS case sheet.
2. Keep adults age 65 and older.
3. Do not treat Age values 201–223 as adult ages. Those values represent
   ages expressed in months.
4. Keep candidate records when at least one of `Product_1`, `Product_2`,
   or `Product_3` equals 3277.
5. From those candidate records, retain only cases whose `Narrative_1`
   explicitly supports treadmill involvement.
6. Add a `treatment_year` field derived from `Treatment_Date`.

The treadmill narrative rule must be transparent and conservative.
Do not infer treadmill involvement merely because product code 3277 is
present: 3277 represents exercise equipment more broadly.

If the project already defines the exact treadmill-text matching rule
elsewhere, use that rule rather than inventing a new one.

### Columns returned

The app-ready case-level data must preserve at least:

- CPSC_Case_Number
- Treatment_Date
- treatment_year
- Age
- Disposition
- Product_1
- Product_2
- Product_3
- Weight
- Narrative_1

Also preserve preparation-created `injury_mechanism` and `is_severe`.
Validate that `injury_mechanism` is nonblank, using `Unknown/Unclassified`
for unknown mechanisms, and `is_severe` is a nonnull Boolean equal to
`Disposition` membership in {2, 4, 5, 8}, with missing disposition yielding false.
Reject invalid or inconsistent fields; do not create aliases, repair flags,
or reclassify mechanisms in the loader.

Do not silently discard columns required by downstream components.

### Precompute once

Do not repeatedly scan the three raw Excel workbooks during interactive
use.

Load the compact dataset created by preparation, containing only the cases
required for this project.

Also precompute or expose the metadata downstream controls need:

- minimum and maximum eligible age;
- available treatment years;
- number of prepared cases by treatment year;
- number of prepared cases by mechanism, once mechanism labels exist;
- whether the loader is using the full annual NEISS data or only a sample.

These values should be derived from the prepared data rather than
hard-coded.

### Runtime loading behavior

When the application starts:

1. Load the prepared case-level dataset.
2. Do not reload the original annual Excel files. If the prepared artifact
   is missing, report it; preparation runs separately through section 02.
3. Return a pandas DataFrame suitable for the filtering component.
4. Preserve numeric types for `Age`, `Disposition`, product codes, and
   `Weight`.
5. Preserve `Treatment_Date` as a date/datetime value and
   `treatment_year` as an integer.

The filtering component, not the loader, is responsible for responding
to ordinary sidebar changes such as age range, year range, or selected
mechanisms.

### Data checks

Before making the prepared data available to the rest of the app, verify:

- all required columns are present;
- all three intended treatment years, 2023, 2024, and 2025, are represented
  when full data are being used;
- every retained record has Age >= 65 using the NEISS age convention;
- no Age value from 201 through 223 has been interpreted as an adult age;
- every retained record has product code 3277 in at least one of
  `Product_1`, `Product_2`, or `Product_3`;
- every retained record satisfies the project's treadmill narrative rule;
- `CPSC_Case_Number` is not accidentally duplicated during annual-file
  concatenation;
- `Weight` is numeric for records used in weighted estimates;
- `Disposition` remains in its original NEISS code form;
- no preparation step changes the original source files.

If a required structural assumption fails, raise a clear error that says
which file, field, or check failed. Do not silently continue with corrupted
or incompatible data.

### Full-data versus sample behavior

Expose a simple indicator such as `data_mode` with values like:

- `full`
- `sample`

Weighted national visit estimates are valid for the dashboard only when
the project is running on the intended full NEISS annual files.

If only a project sample is available, the loader must make that state
available to downstream components so the views can clearly label results
as sample-only and avoid presenting the sum of `Weight` as a national
estimate.

### Interface to downstream pieces

Return or make available:

1. the prepared case-level pandas DataFrame;
2. the available age bounds;
3. the available treatment years;
4. precomputed row counts needed for setup or display;
5. the full-data/sample indicator.

The filters component will use this case-level data to apply the analyst's
age-range, treatment-year, and mechanism selections.

The views component will use the filtered rows to calculate or display
case counts, weighted burden, serious-disposition measures, tables, and
plots.

Do not implement the Streamlit page layout in this component.

### Acceptance checks

The loader is complete when:

- the app can start without rereading more than one million raw NEISS rows
  on every run;
- the prepared dataset contains only the intended age-65+ treadmill cases;
- all required downstream columns and metadata are available;
- the full-data/sample state is unambiguous;
- all validation checks pass;
- filters and views can consume the returned data without reopening the
  raw workbooks.

## 04 — Sidebar Filters and Narrative Search

### Purpose and boundaries

Let the CPSC epidemiology user narrow the prepared treadmill injury cases by
injury mechanism, severity, and narrative text. All charts and tables must use
the same filtered DataFrame so the user can compare the selected cases consistently.

This component receives the loaded DataFrame from `03-loader.md` and passes a
filtered DataFrame to `05-views.md`. It runs on each filter change. Data preparation
owns the ages 65–120, product-code 3277, and treadmill-confirmation rules; filters
must not reload raw files or reclassify mechanisms. `06-setup.md` owns page layout
and calls the sidebar renderer. There is no job-title field in this dashboard;
the text-search control searches injury narratives instead.

### Input and output contract

The loader must provide these columns. Preparation creates the two derived
fields; the loader preserves and validates them.

| Column | Required representation |
|---|---|
| `injury_mechanism` | Derived: one nonblank reviewed label per visit; unknown mechanisms use `Unknown/Unclassified`. |
| `is_severe` | Derived: nonnull Boolean, true exactly for `Disposition` codes 2, 4, 5, 8; false otherwise. |
| `Disposition` | Original NEISS code, normalized upstream to nullable integer; preserved unchanged by filtering. |
| `Narrative_1` | Narrative text, possibly null. Treat null as empty text for search only. |

Derive a local severity display Series from `Disposition`: 2, 4, 5, 8 map to
`Severe`; 0, 1, 6 to `Other known disposition`; 9, missing, or unrecognized
codes to `Unknown`. Use it for severity selections only; never add a `Severity`
column, overwrite `is_severe`, or otherwise mutate the input DataFrame.
Do not derive categories from the Boolean alone: false includes unknown outcomes.

`Other known disposition` is a grouping of the remaining recognized disposition
codes, not a claim that those injuries were mild. Confirm the disposition mapping
against each source year's codebook during preparation. The 2025 lookup in the
dataset repository supports the codes above.

Return matching rows with their original columns, values, index, and order,
including `Weight`, `Stratum`, and `PSU`. Do not aggregate, deduplicate, rescale
weights, or mutate the input. Missing required columns or invalid selection
labels must produce an actionable validation error naming the column or value.

Implement in `filters.py` with these public interfaces:

```python
from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class FilterSelection:
    mechanisms: tuple[str, ...] = ()
    severities: tuple[str, ...] = ()
    narrative_query: str = ""

def render_sidebar(data: pd.DataFrame) -> FilterSelection:
    """Render Streamlit controls and return the current selection."""

def apply_filters(data: pd.DataFrame, selection: FilterSelection) -> pd.DataFrame:
    """Apply selections without Streamlit calls, file access, or hidden state."""
```

Keep the filtering function independent of the UI so it can be checked with a
small DataFrame and reused if the sidebar changes.

### Controls and matching rules

| Sidebar control | Options and behavior | Initial value |
|---|---|---|
| Injury mechanism | Multiselect, using sorted distinct labels from the full loaded cohort, including `Unknown/Unclassified` when present. | Empty selection: all mechanisms. |
| Severity | Multiselect: `Severe`, `Other known disposition`, `Unknown`. | Empty selection: all severities. |
| Search injury narratives | Text input with a hint such as `Enter one word or phrase, e.g., belt`. Match the entire trimmed query as one case-insensitive, literal substring of `Narrative_1`. | Empty text: no text restriction. |
| Reset filters | Clear both multiselects and search text using a Streamlit callback before widgets render again. | Available on first load. |

Within each multiselect, selected values are combined with OR. Combine the two
multiselects and narrative search with AND. Whitespace-only queries match all
rows. Punctuation is literal: `fall.*` searches for those exact characters, with
no regex, wildcard, or keyword-OR behavior. Null narratives remain eligible when
the query is blank and cannot match a nonblank query.

Use stable widget keys. Build options from the full loaded cohort on every rerun,
not from the filtered result, so choices do not disappear after a zero-match search.
Apply a vectorized pandas Boolean mask (`isin` and `str.contains` with
`case=False, regex=False, na=False`); reuse the loader's cached data rather than
reading files on each interaction. The application passes this one result to
every view. Show `Showing X of Y prepared cases` using unweighted row counts.

If no rows match, preserve the controls and show `No cases match these filters.
Try clearing a selection or changing the search text.` Views must skip empty
charts and show unavailable percentages as `N/A`, rather than dividing by zero.
If the loaded cohort itself is empty, show `No prepared treadmill cases are
available.` Keep reset available. A single matching case must still render.

### Build order and completion checks

Implement `apply_filters` first, then the sidebar renderer, then connect its
result to the views. Check behavior using this invented prepared fixture:

| Case | injury_mechanism | Disposition | is_severe | Narrative_1 | Weight |
|---|---|---:|---|---|---:|
| A | Fall | 4 | true | FELL from treadmill belt | 10 |
| B | Fall | 1 | false | Tripped beside treadmill | 20 |
| C | Belt contact | 2 | true | Hand caught in BELT | 30 |
| D | Unknown/Unclassified | 9 | false | null | 40 |

| Selection or interaction | Expected result |
|---|---|
| First load; or reset after changing every control | A, B, C, D, unchanged weights; count `4 of 4`. |
| Mechanisms `Fall` and `Belt contact` | A, B, C. |
| Mechanism `Fall`, severity `Severe` | A only. |
| Severities `Severe` and `Unknown` | A, C, D. |
| Search `  belt  ` | A and C; trimming and case-insensitive matching work. |
| Mechanism `Fall`, severity `Severe`, search `belt` | A only: all three restrictions apply together. |
| Search containing only spaces | A, B, C, D, including the null narrative. |
| Search `fall.*` | No rows; literal punctuation and the empty-state message work. |
| Severity `Unknown` | D only; missing severity is not silently treated as non-severe. |
| Search producing zero matches, then clear search | All rows return and mechanism options remain available. |

Also verify that filtering leaves the source DataFrame unchanged (including its
column list and `is_severe` values), creates no `Severity` column, and maps D
to the `Unknown` display category even though its Boolean flag is false.
Replacing D's disposition with missing or an unrecognized code must retain that
category; codes 2, 4, 5, and 8 must each map to `Severe`. Verify that every view
receives the same selected cases, and that missing required columns fail clearly.
Use this fixture for filter checks only; national estimates require the full
prepared dataset and belong to the views component.

## 05 — Dashboard views

### Purpose and boundaries

Help a CPSC epidemiology staff member identify treadmill injury mechanisms among adults ages 65–120 that deserve further investigation by comparing estimated ED burden, severe outcomes, and diagnosis composition. These are descriptive comparisons of ED visits, not evidence of causation, exposure-adjusted risk, or a treadmill design defect.

Follow `01-design.md`: `02-data.md` prepares and classifies records once; `03-loader.md` loads and validates them; `04-filters.md` supplies a filtered pandas DataFrame; this component aggregates and renders the five views below. It never reads raw annual files, identifies treadmills, classifies narratives, applies dashboard selections, or mutates its input. `06-setup.md` owns layout, chart availability, UI configuration, defaults, and application wiring. No additional dashboard controls are introduced here.

Compute small summaries in pandas from the already prepared cohort on each filter change. Reuse the same mechanism summary across three views so their numbers agree. Do not reuse startup aggregates that ignore current filters. Separate aggregation from rendering so invented DataFrames can test each view without starting the UI. Chart library and styling remain implementation choices within setup's configuration.

### Filtering-to-views contract

Proposed interface (adjacent contracts require reconciliation as noted above):

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
| `injury_mechanism` | **Derived**, not a NEISS column: one nonblank classification label per visit, assigned by data preparation. Unclassifiable cases must use exactly `Unknown/Unclassified`. Views accept the supplied taxonomy without keyword matching or recoding. |
| `is_severe` | **Derived**, not a NEISS column: nonnull Boolean, created by preparation and validated by the loader against `Disposition` membership in `{2, 4, 5, 8}`; false otherwise, including missing disposition. |

Original eligibility fields are `Age`, `Product_1`, `Product_2`, `Product_3`, and `Narrative_1`; their rules belong exclusively to data preparation. They need not be passed to views. `Diagnosis_2`, `Other_Diagnosis`, and `Other_Diagnosis_2` are original columns but are not used in this component's diagnosis composition.

`context` must contain:

- `analysis_years`: sorted, nonempty list of the complete annual source years represented by the selected analysis period, even when filters leave no records.
- `source_scope`: `full_annual` for production; `test_fixture` only in tests; `sample` for an explicitly nonnational preview.
- `filter_description`: human-readable active mechanism and severity selections, including “all” selections. Setup supplies defaults through filtering; views do not choose them.

Production estimates require the complete annual files upstream, then the agreed cohort restriction and dashboard filters. Summing `Weight` from either supplied sample CSV does not produce national estimates. For `source_scope=sample`, return an unavailable state for these five production views with a request to load full annual data; do not display sample sums as national figures.

Check required columns and context before aggregation. Missing columns, invalid weights, duplicate/missing IDs, invalid dates, missing mechanism labels, or missing/inconsistent severe flags return `status="invalid_input"`, an actionable message identifying the upstream contract failure, and no numeric outputs. Do not silently drop rows, replace weights, deduplicate, or repair classifications in views. Check that record years are contained in `analysis_years`.

#### Lookup contract and missing outcomes

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

### Shared calculations and output contract

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

### View specifications

#### 1. Headline metrics

**Purpose:** establish the selected burden, supporting sample size, and recorded severity before comparing mechanisms.

**Inputs:** all filtered rows' `Weight` and `is_severe`; shared context and quality notes. **Output:** `headline` with `weighted_ed_visits`, `record_count`, `severe_outcome_pct`. Use the shared formulas over the entire snapshot. No axes or sorting. Display the three distinct measures with units; raw NEISS records must never be labeled national visits. Missing and empty behavior follows the shared contract. All filters change all three metrics.

#### 2. Horizontal mechanism bar chart

**Purpose:** rank mechanisms by estimated national ED burden to find frequent mechanisms worth reviewing.

**Inputs:** `injury_mechanism`, `Weight`, `is_severe` from filtered rows. **Output:** one `mechanism_summary` row per present mechanism with `injury_mechanism`, `weighted_ed_visits`, `record_count`, `severe_outcome_pct` using the shared formulas within each mechanism.

**Axes:** x = weighted ED visits, linear starting at zero; y = mechanism. Sort top to bottom by weighted ED visits descending, ties by mechanism label ascending. Include all present mechanisms, including the upstream unknown category; no top-N truncation or empty categories. Tooltip includes all four summary fields. Missing/invalid inputs follow the shared rules. Rebuild from the current selection after either filter changes.

#### 3. Frequency–severity scatter plot

**Purpose:** compare burden and recorded severity together; support investigation priorities without inventing a combined risk score.

**Input/output:** use `mechanism_summary` unchanged; one labeled point per mechanism. **Axes:** x = weighted ED visits (linear, starting at zero); y = weighted severe-outcome percentage (0–100%). Label every point with its mechanism and expose all summary fields in the tooltip. Use uniform marker size; record count remains available in the tooltip. Draw in the summary's deterministic order; spatial position is determined by values, not ranking. Offset labels as needed without changing coordinates; coincident mechanisms must retain separate labels/tooltips. A null percentage has no plottable y-value: omit that point and state why. Empty selections have no points. All filtering and unknown-category behavior matches the summary/bar chart.

#### 4. Weighted diagnosis composition by mechanism

**Purpose:** show whether mechanisms have different mixes of primary diagnoses, providing clinical context for further investigation.

**Inputs:** filtered `injury_mechanism`, `Diagnosis`, `Weight`, DIAG lookup, and mechanism summary order. Use **only primary `Diagnosis`**, one diagnosis bucket per visit, to avoid counting visits twice.

**Output:** long-form `diagnosis_composition` with `injury_mechanism`, `diagnosis_code` (nullable), `diagnosis_label`, `diagnosis_weighted_ed_visits`, and `diagnosis_pct`:

```text
diagnosis_weighted_ed_visits(m,d) = sum(Weight in mechanism m and diagnosis bucket d)
diagnosis_pct(m,d) = 100 * diagnosis_weighted_ed_visits(m,d)
                   / weighted_ed_visits(m)
```

**Axes:** horizontal 100% stacked bars, x = percentage of mechanism's weighted ED visits (0–100%); y = mechanism in the burden bar chart's order. Stack known diagnosis codes ascending, then unmapped codes ascending, then missing diagnosis. Use consistent diagnosis colors and legend across mechanisms within a snapshot. Include all buckets, without merging into an additional “Other” group. Return observed mechanism/bucket pairs; absent pairs render as zero-width segments. Tooltip includes mechanism, diagnosis code/label, weighted visits, and share. Each nonempty mechanism sums to 100% before rounding. Unknown/missing diagnosis is retained as specified above. All dashboard filters recalculate both cell weights and within-mechanism denominators.

#### 5. Summary table

**Purpose:** give exact supporting values for the same mechanism comparisons.

**Input/output:** render `mechanism_summary` with columns in this order: mechanism, estimated weighted ED visits, NEISS record count, weighted severe-outcome percentage. No chart axes. Default row order and missing/filter behavior match the burden chart. Show all mechanisms; do not add a total row that averages severity. The headline already supplies the correctly weighted total. Preserve numeric types for formatting and any table sorting.

### Independent acceptance checks (invented data only)

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

### Integration decisions to review

- The adjacent pieces are included in this combined prompt. Derived names and validation ownership follow the shared contract above. Confirm payload/context fields, the remaining single-label mechanism taxonomy, and denominator convention when combining pieces.
- The vision does not specify an analysis period. Setup must choose the initial year/period and default filters; views support explicit period metadata without assuming a new year control. Prefer within-year mechanism comparisons; multi-year sums require the labels/caution above.
- Confirm primary-diagnosis-only composition and the treatment of unknown disposition as not recorded severe in an all-visit denominator. These are explicit proposed conventions, not previously documented team decisions.
- Basis inspected: `00-vision.md`, `01-design.md`, `08-architect/one-shot-prompt-specs.md`, Module 8 README/orientation, dataset README/overview, actual sample headers, and complete DIAG/DISP lookup rows. No separate Module 8 handout was found locally. The copied lookup in this team repository matches the sibling dataset repository.

## 06 — Setup, configuration, and application wiring

### Purpose and design

Provide a single-page Streamlit dashboard where a CPSC epidemiology staff member can compare treadmill injury mechanisms among adults ages 65–120 and choose candidates for further investigation. Put burden and severity together before diagnosis detail so this decision requires less manual comparison. The dashboard describes ED visits; it does not establish causation, exposure-adjusted risk, or a treadmill design defect.

Setup owns configuration, initial state, page layout, navigation, and component calls. Data preparation owns cohort eligibility and classification; loading owns reading and validating prepared data; filtering owns selections and matching; views own calculations and chart construction. Keep their logic in those components. All views consume one filtered snapshot to prevent contradictory totals.

### Initial state and layout

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

### Configuration contract

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

### Component integration and contracts

The following loader boundary and artifact locations are **proposed integration contracts** requiring reconciliation with sections 02 and 03, not claims that these functions already exist. Reconcile them before the build; a coding agent must report incompatible contracts rather than quietly rename fields or implement preparation inside setup.

| Component | Receives | Returns / responsibility | When |
|---|---|---|---|
| Preparation (`02`) | Full annual NEISS source and its code documentation | Prepared cohort and provenance artifact | Separate offline step, never on dashboard reruns |
| Loader (`03`), proposed `load_dashboard_data(prepared_path, provenance_path, diagnosis_lookup_path, analysis_year)` | Resolved paths and configured year | Dictionary with `data` (validated pandas DataFrame), `diagnosis_lookup` (complete lookup DataFrame), and `provenance` (dictionary below); raises an actionable load/validation error on failure | First successful load; cache thereafter |
| Filters (`04`) | `data` | `render_sidebar(data) -> FilterSelection`, then `apply_filters(data, selection) -> pd.DataFrame`, preserving rows' columns and values | Initial run and each widget rerun |
| Views (`05`) | The single filtered DataFrame, context, lookup | `build_view_data(filtered_df, *, context, diagnosis_lookup) -> dict`, exactly as specified in `05-views.md` | Initial run and every filter change |
| Setup (`06`) | Validated config and component results | Streamlit page, state messages, and placement of view renderers; no numerical aggregations | Every Streamlit rerun, reusing cached loading |

The loader must supply the union of required columns from `04` and `05`, preserving original `CPSC_Case_Number`, `Treatment_Date`, `Weight`, `Disposition`, `Diagnosis`, `Narrative_1`, `Stratum`, and `PSU`, plus preparation-created `injury_mechanism` and `is_severe`. The loader validates those derived fields; filters preserve them and derive severity display categories locally from `Disposition` without adding columns. Views aggregate the filtered rows. Setup only connects these components: it must not create aliases, derive flags, or recode mechanism labels. Unknown mechanisms use exactly `Unknown/Unclassified`.

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

### Performance and state handling

Keep raw annual files on disk and preparation offline. Read only the prepared cohort and complete lookup at startup; pandas in memory is sufficient for this restricted cohort, with no SQL server needed. Use `st.cache_data` around the loader boundary, keyed by resolved paths, file modification times/sizes (including provenance/lookup), configured year, and loader/schema version. Changed artifacts must invalidate the cache. Never cache a failed load as a successful result or substitute a stale successful result after a failed refresh.

The cached loader may provide optional startup summaries per `01-design.md`; setup must not use them as filtered results. Recompute filtering and `build_view_data` for the current snapshot on each interaction, then rerender all five views. Do not cache filtered results in a shared global variable. Read/validate the small TOML each rerun; its defaults are initialized only when a session starts. After editing configuration, restart the application to establish a fresh session. Instrument loader call counts in tests instead of requiring raw workbook timing on every interaction.

### Errors and empty states

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

### Local execution and future deployment

Future application entry point: repository-root `app.py`, with `config.toml` beside it. Use Python 3.11+, `streamlit`, `pandas`, and `plotly` for the chart implementation; TOML parsing uses the standard library. The future agent must declare dependencies in the project's environment and lock resolved compatible versions. `openpyxl` is needed only by offline preparation if it reads XLSX; CSV loading in the dashboard does not require it. No application code or dependency files are created by this specification.

From the team repository, the future local launch is:

```powershell
python -m pip install streamlit pandas plotly
python -m streamlit run app.py
```

Before launching, obtain full annual data using section 4 of the dataset overview (browser download where required), complete preparation according to `02`, and place the validated prepared/provenance artifacts at the configured locations. The complete lookup under `sample/` is valid reference data; the injury sample CSVs are not valid production inputs. The precise preparation command remains blocked on `02` and must be included in the combined prompt before handoff.

For later Streamlit hosting, deploy the same entry point and locked dependencies, prepare the cohort once outside the web process, and stage versioned prepared/provenance/lookup artifacts in deployment storage. Configure their paths there; avoid downloading the annual workbooks during requests. Verify memory limits and the same acceptance checks on the host, keep widget state session-specific, and invalidate caches when artifact versions change. No cloud deployment is part of this task.

### Build order and acceptance checks

Build configuration validation and page skeleton first; integrate the validated loader next; connect `04` and `05` through the shared `injury_mechanism`/`is_severe` contract; then verify layout and interactions. Use the A–E invented fixture and expected outputs from `05-views.md` in tests with `source_scope="test_fixture"` injected through a test loader, never an end-user configuration option. Extend that fixture in the test loader with suitable `Narrative_1` values; it already contains the shared derived fields. Preserve its original numerical fields.

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

### Unresolved integration issues / rubric review

- **Shared contract resolved:** Preparation creates `injury_mechanism` and `is_severe`; loader validates and preserves them; filters derive severity display categories locally from `Disposition` and apply selections without mutation; views aggregate; setup wires the components. Unknown mechanisms use `Unknown/Unclassified`.
- **Preparation/loader integration:** Sections `02` and `03` are now included. Confirm the proposed CSV/provenance artifacts and loader interface, source-completeness validation, preparation command, and duplicate-source handling. These are whole-prompt completeness blockers, not reasons to fabricate preparation inside setup.
- **Narrative-search integration:** Section `04` specifies narrative search. Setup wires that control and includes it in context without adding search matching logic.
- **Team confirmation retained from `05`:** primary-diagnosis-only composition and all-visit weighted severity denominator still need signoff when combining pieces; setup uses those contracts unchanged.
- **Rubric self-review:** stakeholder/decision and opening workflow are explicit (1–2); boundaries precede details, with shared rules referenced rather than repeated (3–4); component calls and cache ownership are separated (5); prepared data, local dependencies, rerun strategy, and cloud path are defined (6); source provenance and failure handling are explicit (7); build order and concrete checks are present (8). A level-3 score for the combined prompt remains contingent on resolving the integration blockers above.
