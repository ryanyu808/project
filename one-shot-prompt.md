**Team Project Repository:** https://github.com/ryanyu808/project

# CPSC Treadmill Injury Dashboard — One-shot Build Prompt

Build the local dashboard described here from this Markdown file, the [NEISS dataset repository](https://github.com/USC-DSO-576-PS/dataset_neiss-sports-injuries), and public documentation. Numbered file references below identify sections of this prompt; no other team files are build dependencies.

## Design principles

- **Separate five responsibilities:** preparation defines eligible visits and reviewed classifications; loading validates saved artifacts; filtering selects rows; views aggregate; setup connects and places components. This lets each piece be built and checked independently.
- **Pass explicit data:** use pandas DataFrames and the contracts below without hidden global filter state, so every view describes the same selected visits.
- **Prepare once, interact in memory:** keep annual source files unchanged on disk, save the small prepared cohort, cache loading, and recompute only selected summaries. This avoids scanning roughly 1.11 million annual records on widget changes.
- **Make estimates auditable:** preserve source provenance, record counts, unknown outcomes, and narrative-review decisions. Weighted burden and recorded severity help prioritize investigation; they do not establish causation or defects.

## Unresolved integration issues

Do not silently resolve conflicting requirements. Report the affected integration before implementing it; unaffected pieces can be built and checked independently.

- Preparation specifies sample CSVs for development; loader, views, and setup require full annual files for national estimates. The production preparation command remains unspecified.
- Loader expects three years in the full prepared dataset and mentions age/year filters; filters define mechanism, severity, and narrative controls; setup specifies a single configured year, initially 2025. Agree artifact coverage and period selection without inventing controls.
- Loader-to-setup interface resolved: Both components use the four-key dictionary defined in Section 03 (`data`, `diagnosis_lookup`, `provenance`, and `metadata`). Preparation artifact creation, provenance verification, and source-completeness validation still require team confirmation.
- Vision bounds age at 65–120; loader says 65+ without an explicit upper bound. Preparation requires manual narrative/mechanism review, whose production workflow must be documented. Views retain team-review questions about primary-diagnosis composition and the all-visit severity denominator.

## 00 — Vision and analyst workflow

A CPSC epidemiology staff member must decide which treadmill injury mechanisms among adults ages 65–120 deserve further investigation. Reading raw narratives and manually reconciling weights and dispositions makes it difficult to compare mechanisms consistently. This dashboard puts estimated national ED burden, recorded severe-outcome percentage, and diagnosis composition together, with the supporting NEISS record count.

On opening, the analyst sees all 2025 mechanisms across the five coordinated views:
- **Use case 1 — Prioritizing high-burden vs. high-severity mechanisms:** From the initial full-year view (all mechanisms and severities), the analyst **sees** the horizontal burden bar chart alongside the frequency–severity scatter plot and **decides** whether a high-volume mechanism (e.g., `Fall`) or a lower-volume mechanism with a high severe-outcome share (e.g., `Belt contact`) warrants priority clinical review, using the primary-diagnosis stacked bar chart to check whether severe cases are driven by fractures (`57 - FRACTURE`) or other diagnoses.
- **Use case 2 — Verifying severe narrative patterns:** The analyst **selects** a candidate mechanism (e.g., `Fall`), **selects** `Severe` in the severity filter, and enters `belt` in the narrative search box. All five views update to that exact subset; the analyst **sees** the filtered national ED visit estimate, supporting NEISS record count, and diagnosis mix, then **decides** whether to pull full CPSC incident investigation reports for belt-involved falls. A high percentage based on few records is treated as a screening signal, not proof of elevated exposure-adjusted risk.

The agreed cohort requires age 65–120, product code `3277` in any of the three product columns, and a treadmill mention in `Narrative_1`, with manual review as specified in section 02. No geographic filter, exposure denominator, brand/model attribution, causal conclusion, or claim of a treadmill design defect is supported.

## 01 — Components and integration

| Component / future module | Receives | Returns / passes onward | Runs |
|---|---|---|---|
| Preparation / `prepare_data.py` | One complete annual source (or a development sample), complete code lookup, and human review | Per-year prepared CSV, provenance JSON, quality report, and derived-field/rule documentation | Offline; never during UI interactions |
| Loader / `loader.py` | Prepared/provenance/lookup paths and configured year | `LoadedData` dictionary containing validated `data`, `diagnosis_lookup`, `provenance`, and `metadata` | Startup/cache miss |
| Filters / `filters.py` | `LoadedData["data"]` and `FilterSelection` | Matching rows with original columns, values, index, and order | Every widget rerun |
| Views / `views.py` | One filtered snapshot, context, and lookup | `build_view_data` result plus independently callable view renderers | Every selection change |
| Setup / `app.py` | TOML configuration and the component results | One Streamlit page and session-specific controls | Every rerun; reuses cached loading |

Period reconciliation: prepare 2023, 2024, and 2025 **independently when available**, with one artifact per year. Each dashboard run loads only the configured year, initially 2025. The artifact need not contain records from all three years. Available years come from validated artifacts; an empty eligible cohort does not imply that its annual source was incomplete. There are no interactive age/year range controls in this MVP.

Use the exact shared fields and interfaces below. Do not create alternative mechanism/severity aliases. Preparation creates derived fields, the loader validates and preserves them, filters apply selections, views aggregate, and setup wires the results.

### Approved mechanism codebook and analytical conventions

1. **Approved mechanism codebook (`Version: 1.0`):** Preparation writes or validates `data/prepared/mechanism-codebook.md` using `Version: 1.0` and the mutually exclusive categories below. During candidate export, preparation may propose an initial label in a separate audit column using the priority order below; human review confirms or overrides `injury_mechanism` in `treadmill_<year>.reviews.csv` before `finalize`. When a narrative describes a chain of events, assign the earliest initiating treadmill mechanism (using priority order 1 → 6 as the tie-breaker):

| Priority | `injury_mechanism` | `definition` | `overlap_rule` |
|---:|---|---|---|
| 1 | `Repair/moving` | Injury while lifting, folding, assembling, cleaning, or servicing an unmounted treadmill. | Takes precedence over `Struck by equipment` or `Fall` if the patient was not using the treadmill for exercise. |
| 2 | `Entering/exiting` | Slip, trip, or loss of balance while mounting, stepping onto, or stepping off the treadmill. | Takes precedence over general `Fall` when the narrative specifies getting on or off. |
| 3 | `Belt contact` | Friction burn, pinch, entrapment, or direct pull from the moving belt (or belt sudden stop/surge) as the initiating event. | Takes precedence over `Fall` when belt contact/slip initiated the fall; if a general fall merely lands on the belt, code as `Fall`. |
| 4 | `Struck by equipment` | Hit by a falling, folding, or tipping treadmill frame/console, or thrown into part of the machine without a preceding fall. | Excludes impacts that occur solely as the landing of a `Fall` or during `Repair/moving`. |
| 5 | `Fall` | Loss of balance, trip, dizziness, or fall on/from the treadmill during use without a more specific initiating mechanism above. | Default category for exercise-use falls not initiated by mounting/dismounting or belt malfunction/entrapment. |
| 6 | `Unknown/Unclassified` | Reviewed treadmill-involved visit where the narrative lacks sufficient detail to determine how the injury occurred. | Reserved for reviewed unclear narratives; never used to bypass unfinished candidate review. |

2. **Confirmed analytical conventions:** Primary-`Diagnosis`-only composition (one bucket per visit, preventing double-counting) and the all-filtered-visit-weight severity denominator (including unknown dispositions) specified in section 05 are confirmed team conventions.

**Production-data gate:** After candidate export, a human must review every candidate narrative using the codebook above (`reviewed=true` in `treadmill_<year>.reviews.csv`) before `finalize` publishes production data. Build and test components with the invented fixtures below while production narrative review is pending; `Unknown/Unclassified` represents a reviewed unclear narrative and must not hide unfinished review.

## 02 — Data preparation

### Sources, granularity, and acquisition

One source row is one ED visit, not one unique person. Preserve the original 25 NEISS columns in prepared rows:

```text
CPSC_Case_Number, Treatment_Date, Age, Sex, Race, Other_Race, Hispanic,
Body_Part, Diagnosis, Other_Diagnosis, Body_Part_2, Diagnosis_2,
Other_Diagnosis_2, Disposition, Location, Fire_Involvement,
Product_1, Product_2, Product_3, Alcohol, Drug, Narrative_1, Stratum, PSU, Weight
```

Place the dataset repository at `dataset_neiss-sports-injuries/` beside `app.py`, or update configured paths. Its README and overview section 4 describe browser acquisition from the [CPSC NEISS query/download page](https://www.cpsc.gov/cgibin/NEISSQuery/home.aspx): select affiliation, Archived Annual NEISS Data, year, Excel or Tab Delimited Text, Find Data, and save the full file in the dataset repository's `data/` folder. Do not add a dashboard download loop or assume a nonexistent download script. If access is blocked, show the browser instructions rather than retry automatically.

The repository documents these full-source baselines; verify before cohort restriction:

| Year | Workbook / case sheet | Original rows | Original columns |
|---|---|---:|---:|
| 2023 | `neiss2023.xlsx` / `NEISS_2023` | 338,262 | 25 |
| 2024 | `neiss2024.xlsx` / `NEISS_2024` | 361,672 | 25 |
| 2025 | `neiss2025.xlsx` / `NEISS_2025` | 410,201 | 25 |

Read one year at a time with pandas; use `openpyxl` and an explicit case-sheet name for XLSX. `NEISS_FMT` is the other sheet, not case data. The 2025 workbook is about 54 MB; its optional `neiss2025.tsv` twin is about 86 MB and loads faster via `pd.read_csv(..., sep="\t")`; parse its dates with `format="%m/%d/%Y"`. Use **one** source representation per year, never concatenate XLSX and TSV twins. Date coverage should be January 1–December 31 of the source year. If source schema/count/coverage differs, report the discrepancy and require confirmation of an official source revision; do not silently bless it as complete.

Development files `sample/neiss_all_products_2025_sample.csv` (15,000 rows) and `sample/neiss_sports_2023_2025_sample.csv` (20,000 rows across years) are alternative fixtures, not additive annual sources. Their counts, shares, rankings, and summed weights must never be reported as national findings. Run them separately in development, validate the documented sample shape instead of the full-year baseline, then select the requested treatment year and mark provenance `sample`. Source evidence describes the whole input sample; prepared rows still belong only to the requested year.

Both `sample/neiss_code_lookup_2025.csv` (1,250 rows, four columns) and `sample/sports_product_codes.csv` (126 codes) are complete reference tables despite their directory name. Keep the sports-product list unchanged; it is not an additional restriction on this treadmill cohort. Verify relevant codes against each source year's `NEISS_FMT`; record discrepancies rather than guessing a cross-year mapping.

### Preparation rules and human review

1. Leave source files unchanged. Record source row count, columns, date coverage, missingness, and duplicate IDs before transforming. Normalize types in the cleaned copy; retain original narratives/code values and keep exceptions traceable to their source. For eligible records, candidate and prepared CSVs retain the normalized original 25 fields. A cleaned source table can remain in preparation memory; the saved raw source, candidates, final cohort, and quality report preserve the audit trail without loading a full cleaned annual table into the dashboard.
2. Interpret `Age` 0 as unrecorded and 201–223 as infant months. Eligible ages are integer years 65–120 inclusive; exclude unknown ages and month codes. Create `adult_65_plus` accordingly.
3. Create separate derived flags `has_product_3277` (any of `Product_1`, `Product_2`, `Product_3` equals 3277) and `mentions_treadmill` (trimmed, case-insensitive, literal `TREADMILL` occurs in `Narrative_1`). Require **both flags and eligible age**. Null narrative is empty for this match only. Keep product 0 as “no additional product”; a product match alone does not establish treadmill involvement.
4. Export every candidate's ID, original `Narrative_1`, and proposed mechanism/rule for human review. A human must inspect every candidate, confirm treadmill involvement, and assign one reviewed `injury_mechanism` under the approved codebook. Preserve review decisions, reasons, and rule/codebook version separately from original columns. Excluded false mentions require a recorded reason. Reviewed unclear mechanisms use exactly `Unknown/Unclassified`; no automatic category may be passed off as fact.
5. Create nonnull Boolean `is_severe` using the shared disposition mapping in section 03, and integer `treatment_year` from `Treatment_Date`, never the case-number prefix. Do not infer missing disposition from diagnosis or narrative.
6. Retain missing secondary diagnosis/body-part values: blank means a second injury was not recorded; do not impute one. Retain `Other_Diagnosis` text for audit, but do not infer primary chart categories from it. Preserve all source columns in eligible rows, plus the documented derived fields.
7. Clean lookup keys by trimming format/code strings and using error-safe numeric conversion. `.` in `HISP`/`ALC_DRUG` becomes missing; `AGELTTWO` 2–120 is a range and must not use an equality join. Code-label joins must be many-to-one, keyed by format plus code; section 05 defines diagnosis buckets.
8. Report invalid dates/IDs/weights, duplicate visits, and review exceptions. Do not silently drop, deduplicate, repair weights, or rescale for exclusions. Stop on structural failures, preserving the exception report, rather than assuming malformed rows are ineligible. Do not finalize production with unresolved structural failures or unfinished candidate reviews. Quality-report counts must reconcile source → age/product/text candidates → reviewed exclusions + retained visits.

### Offline commands and artifacts to implement

The future agent implements the following two phases in the preparation component; these commands are a build contract, not existing runnable scripts. Resolve CLI paths relative to the repository root.

```powershell
python prepare_data.py candidates --source dataset_neiss-sports-injuries/data/neiss2025.xlsx --year 2025 --source-scope full_annual --output-dir data/prepared
python prepare_data.py finalize --candidates data/prepared/treadmill_2025.candidates.csv --reviews data/prepared/treadmill_2025.reviews.csv --codebook data/prepared/mechanism-codebook.md --output-dir data/prepared
```

The candidates phase writes `treadmill_<year>.candidates.csv`, a blank `treadmill_<year>.reviews.csv` template, `treadmill_<year>.source.json`, and the quality report. The source JSON records the year/scope, raw-source evidence below, and candidate-file SHA-256 so finalize can detect edited candidate rows. It does not publish the final prepared artifact. Finalize discovers the source JSON beside the candidates file, verifies the source/candidate evidence and completed reviews, then writes the artifact bundle below. Human candidate review is the production-data gate in section 01, not an extra software component. For XLSX, use its `NEISS_FMT` lookup; for TSV/sample inputs, the candidates command accepts `--lookup <path>` (default `dataset_neiss-sports-injuries/sample/neiss_code_lookup_2025.csv`). Sample dates are ISO dates; unlike the TSV, parse them as such.

The review CSV has exactly one row per candidate, keyed by `CPSC_Case_Number`, with `treadmill_confirmed` (Boolean), `injury_mechanism` (required when retained), `reviewed` (Boolean), and `review_note` (required for exclusion). Finalize requires identical candidate/review ID sets, all reviewed=true, and no duplicate IDs; it rejects labels absent from the approved codebook. The codebook file starts with Version: 1.0 and the Markdown table with injury_mechanism, definition, and overlap_rule columns defined in section 01, including the reserved Unknown/Unclassified label. Candidate export preserves source fields and the candidate flags. Store proposed labels/rules in separate audit fields if AI is used. Every output README documents its derived columns and matching/review rules.

| Per-year artifact | Contents |
|---|---|
| `treadmill_<year>.csv` | Final eligible, reviewed cohort; UTF-8 CSV without index; all original columns and shared derived fields |
| `treadmill_<year>.provenance.json` | Source/completeness, output, and review evidence defined below |
| `treadmill_<year>.quality.json` | Counts at each stage, missing/invalid/duplicate counts, review exclusions, and traceable exceptions |
| `README.md` | Derived-field definitions, source/date parsing, classification rules, and codebook version |
| Candidate/review/source-evidence files | Audit trail retained separately; never loaded into the dashboard |

Provenance JSON has these required keys (values below are definitions, not invented results):

| Key | Required value |
|---|---|
| `schema_version` | Integer 1 for this contract |
| `analysis_years` | One-element integer list, e.g. `[2025]` |
| `source_scope` | `full_annual` or `sample`; `test_fixture` is test injection only |
| `source_files` | List of exactly one object with `path`, `sha256`, `row_count`, `column_count`, `min_date`, `max_date`; dates are ISO strings, counts are integers |
| `source_checks_passed` | Boolean recording successful raw-source schema/count/date checks above; a filename alone is insufficient |
| `prepared_sha256`, `prepared_row_count` | Digest of the final CSV bytes and its number of rows |
| `review_complete`, `reviewed_candidate_count` | True and the count of reviewed candidates, including documented exclusions |
| `codebook_version`, `review_sha256`, `codebook_sha256` | Nonblank version and fingerprints of the review/codebook used |

Source hashes identify the input checked offline; they are not proof of authenticity or an excuse to relabel samples. The loader must validate this recorded evidence and the prepared output; it must not reread annual files on interactions. A zero-row prepared cohort is valid only when source and review checks succeeded; write the full CSV header and zero review counts where appropriate. On failure, preserve diagnostics and avoid publishing a mismatched CSV/provenance pair.

### Preparation completion checks

Test independently with invented records: age 0, 205, 64, or 121 is excluded; 65 and 120 are eligible. For otherwise eligible records, code 3277 in only `Product_2` or `Product_3` qualifies just as in `Product_1`; product-only or text-only evidence does not. `tReAdMiLl` matches case-insensitively; null text does not. Duplicate/missing IDs, missing or inconsistent reviews, and join multiplication fail with diagnostics. The severity mapping cases are in section 03. Final retained + reviewed-excluded candidates must equal candidate count, and no raw file may change.

Check the export/finalize boundary without annual downloads: use three invented eligible candidate IDs P/Q/R with weights 10/20/30. Provide reviewed=true for all, retain P/Q with labels from a test-only codebook, and exclude R with a reason. Finalize must write exactly P/Q, `prepared_row_count=2`, `reviewed_candidate_count=3`, and a digest matching the written CSV; loaded weights remain 10/20. Missing Q's review, adding a foreign review ID, changing candidate bytes, or leaving reviewed=false must prevent finalization. This is an isolated test fixture, not full-annual source evidence or a production taxonomy.

## 03 — Loader and shared case contract

Implement `load_dashboard_data(prepared_path, provenance_path, diagnosis_lookup_path, analysis_year) -> dict` in `loader.py`. It loads the prepared CSV and complete lookup, validates them, and returns:

| Dictionary key | Value |
|---|---|
| `data` | Case-level pandas DataFrame for exactly the configured year, preserving all source/derived columns; never aggregated |
| `diagnosis_lookup` | Complete four-column lookup DataFrame, with valid unique DIAG keys as in section 05 |
| `provenance` | Validated dictionary from section 02, unchanged |
| `metadata` | `available_treatment_years` (list), `age_min`/`age_max` (nullable integers), `prepared_record_count` (integer), `record_counts_by_year` and `record_counts_by_mechanism` (dictionaries of integers) |

Metadata is derived from validated loaded rows, except available source years come from provenance even for an empty cohort. Return null age bounds and empty mechanism counts for an empty cohort; year count remains `{analysis_year: 0}`. Do not require other years to be present. Use `provenance["source_scope"]` throughout, with no separate `data_mode` or `full` alias.

### Shared field schema and disposition mapping

| Field | Origin and runtime representation |
|---|---|
| `CPSC_Case_Number` | Original; nonmissing unique identifier, normalized to string without altering identity; visits are not unique people |
| `Treatment_Date` | Original; normalized nonmissing pandas datetime, within the configured calendar year; CSV serialized as ISO date |
| `Age`, `Product_1`, `Product_2`, `Product_3` | Original; integer codes; eligible age/product rules in section 02 |
| `Disposition`, `Diagnosis` | Original; nullable integers; missing/unknown disposition remains visible through the mapping below; unmapped diagnosis remains a chart bucket |
| `Narrative_1` | Original text, possibly null; preserve verbatim |
| `Weight` | Original; finite, positive numeric survey weight |
| `Stratum`, `PSU` | Original survey-design fields; preserve for possible later uncertainty analysis; never interpret PSU as geography |
| `adult_65_plus`, `treatment_year` | Derived by preparation; true for every retained row and integer year matching the date |
| `injury_mechanism` | Derived by preparation; one nonblank reviewed label; exactly `Unknown/Unclassified` for reviewed unknown mechanisms |
| `is_severe` | Derived by preparation; nonnull Boolean according to the table below |

| `Disposition` | Lookup meaning | `is_severe` | Filter display category |
|---|---|---|---|
| 2 | Treated and transferred | true | Severe |
| 4 | Treated and admitted/hospitalized | true | Severe |
| 5 | Held for observation | true | Severe |
| 8 | Fatality including DOA / died in ER | true | Severe |
| 0, 1, 6 | No injury; treated/examined and released; left without being seen | false | Other known disposition |
| 9, missing, or unrecognized code | Unknown/not stated or unavailable | false | Unknown |

False means “not recorded severe,” not confirmed nonsevere. Preparation creates the flag; the loader validates it; filters derive the display category locally from original `Disposition`, since the Boolean alone cannot distinguish unknown outcomes. Do not add `Severity` or alternative mechanism columns. Parse saved Booleans explicitly as true/false (case-insensitive); never use truthiness of CSV strings such as `"False"`.

### Validation, failures, and completion checks

Before returning, verify required source/derived columns, unique/nonmissing IDs, finite positive weights, normalized types/dates, cohort age/product/text conditions, and consistent derived fields. Do not classify narratives or redo manual review. Validate provenance schema, configured-year equality, source-scope enum, prepared byte digest/count, successful source checks, and completed review/version evidence. For `full_annual`, raw-source evidence must match section 02's baseline. Missing/partial/unverified source evidence is an error, not automatic sample fallback. For explicitly declared `sample`, preserve that scope so views return unavailable national results.

Raise `ValueError` with the file, field/check, and remedy for invalid artifacts; preserve ordinary file-not-found errors with the missing path. Never silently deduplicate, repair flags/weights, discard required columns, or load raw files when prepared data is absent. Lookup joins must not multiply visits.

Independent checks: use tiny prepared CSV/provenance fixtures in a temporary test directory with an explicit test-only source validator (never a production flag accepting toy raw counts). Reject a changed CSV digest, mismatched year, missing required field, duplicate ID, invalid Boolean, inconsistent severity, blank mechanism, invalid weight, or failed/incomplete source/review evidence. Exercise codes 2/4/5/8 (true), 0/1/6/9 (false), and missing/unrecognized disposition (false); confirm counts and metadata, including an empty but valid cohort. A successful load must let filters/views operate without reopening source workbooks.
Mechanism classification is done when every prepared case has exactly one valid `injury_mechanism`, a small hand-checked set produces the expected classifications, and `Unknown/Unclassified` cases are reported separately for review.

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

Implement `load_dashboard_data(prepared_path, provenance_path, diagnosis_lookup_path, analysis_year)` and return a dictionary with exactly these top-level keys:

- `data`: the validated prepared pandas DataFrame, preserving all required columns and rows.
- `diagnosis_lookup`: the complete diagnosis lookup pandas DataFrame used by views.
- `provenance`: a dictionary containing `analysis_years`, `source_scope`, and `source_files`, validated against the prepared artifact and configured year.
- `metadata`: a dictionary containing `age_min`, `age_max`, `available_years`, `case_counts_by_year`, and `case_counts_by_mechanism`, calculated from the prepared data.

Raise an actionable validation error when a required file, key, field, or data type is missing or inconsistent. Do not silently create replacement values. The filters receive `result["data"]`; views receive the filtered DataFrame, `result["diagnosis_lookup"]`, and context built from `result["provenance"]`. Setup owns this wiring, not the loader.

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

Narrow the loaded cohort by mechanism, severity, and narrative text. Return one selected snapshot for all views; retain the preparation/loading ownership boundaries in section 01. This component owns its sidebar controls and pure selection function, not the page layout.

### Input and output contract

Required input columns: `injury_mechanism`, `is_severe`, `Disposition`, and `Narrative_1`, using section 03's representations. Other loaded columns pass through unchanged for views; standalone filter fixtures need only these four fields. Loader owns whole-artifact validation.

Derive a local severity display Series from `Disposition` using section 03's table. Use it for severity selections only; never add a `Severity` column, overwrite `is_severe`, or mutate the input. `Other known disposition` is not a claim that those injuries were mild. Missing/unrecognized outcomes belong to `Unknown`, not `Other known disposition`.

Return matching rows with their original columns, values, index, and order, including `Weight`, `Stratum`, and `PSU`. Do not aggregate, deduplicate, or rescale. Missing required columns or invalid selection labels raise an actionable `ValueError` naming the column/value.

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
every view. Setup displays the unweighted selected/loaded counts (section 06).

When no rows match, retain controls/options and return an empty DataFrame with the original schema. Setup displays the empty-result state from section 05; for an empty loaded cohort, it also identifies the absence of prepared cases. Reset remains available and a single matching row must render. An empty multiselect remains unrestricted, as specified above; it does not mean no matching rows.

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

Aggregate the filtered snapshot into the five descriptive views below. Follow section 01's ownership boundaries; do not read raw files, classify narratives, apply selections, or mutate input. Reuse one mechanism summary for the burden chart, scatter, and table. Separate pandas aggregation from Plotly rendering so each can be checked without starting Streamlit; do not reuse startup summaries that ignore current filters. Setup owns placement and controls; decorative styling remains an implementation choice.

### Filtering-to-views contract

Implement this aggregation interface independently of Streamlit:

```python
build_view_data(filtered_df: pd.DataFrame, *, context: dict,
                diagnosis_lookup: pd.DataFrame) -> dict
```

`filtered_df` contains one row per eligible ED visit, after all active selections. Every view receives this same snapshot. Upstream components own eligibility, deduplication, numeric/date normalization, and severe-flag creation/validation. Do not explode product or diagnosis columns into extra visits.

Required inputs: `CPSC_Case_Number`, `Treatment_Date`, `Weight`, `Disposition`, `Diagnosis`, `injury_mechanism`, and `is_severe`, with the exact representations in section 03. All output summary names below are derived, not original NEISS columns. Views neither identify treadmills nor reclassify mechanisms.

`Diagnosis_2`, `Other_Diagnosis`, and `Other_Diagnosis_2` remain available for audit but are not used in primary-diagnosis composition.

`context` must contain:

- `analysis_years`: sorted, nonempty list of the complete annual source years represented by the selected analysis period, even when filters leave no records.
- `source_scope`: `full_annual` for production; `test_fixture` only in tests; `sample` for an explicitly nonnational preview.
- `filter_description`: human-readable mechanism, severity, and narrative-search selections, including “all” for unrestricted selections. Setup constructs it from the filter state.

For `source_scope=sample`, return `status="unavailable"` for these five production views with a request to load full annual data. Never label sample sums as national estimates. `test_fixture` is accepted only in isolated tests; an unrecognized scope is invalid input.

Check required columns and context before aggregation. Missing columns, invalid weights, duplicate/missing IDs, invalid dates, missing mechanism labels, or missing/inconsistent severe flags return `status="invalid_input"`, an actionable message identifying the upstream contract failure, and no numeric outputs. Do not silently drop rows, replace weights, deduplicate, or repair classifications in views. Check that record years are contained in `analysis_years`.

#### Lookup contract and missing outcomes

Use the complete `sample/neiss_code_lookup_2025.csv` (also available as annual workbook sheet `NEISS_FMT`). Its actual columns are `Format name`, `Starting value for format`, `Ending value for format`, and `Format value label`. The loader normalizes padded format/code strings and validates unique integer DIAG keys once at load; views restrict to `Format name == "DIAG"` and perform a many-to-one join to `Diagnosis` without multiplying visits. When views are tested directly with the raw complete lookup, normalize/validate it through the same helper used by the loader. The disposition definition and unknown-outcome treatment are in section 03.

Severity denominator is **all filtered visit weight**, including unknown disposition. This is a recorded severe-outcome percentage, not the percentage among known dispositions. Preserve unknowns in totals and report their record count and weight in supporting metadata/notes. The team-confirmation gate is recorded once in section 01.

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

For valid nonempty input return `status="ok"`; `messages` carries applicable data/period notes. For a valid empty selection: `status="empty"`, headline visits/count = 0, severe percentage = null, both quality values = 0, and empty summary/composition tables with their declared columns. Show “No records match the current filters”; display severity as N/A and no fabricated zero bars or points. An internal zero denominator likewise yields null, never infinity or 0%.

Every view updates from the filtered rows on every selection change. A severity-only selection changes both numerator and denominator: selecting only severe records produces 100% for every nonempty mechanism. Show active filters and explain that the percentage describes the current selection. No view silently restores the unfiltered denominator or initiates chart-driven cross-filtering.

Each view must identify its analysis period. A single year is an annual estimate. If setup/filtering allows multiple years, label sums “Estimated ED visits over selected years (combined total; not annual)” and compute a ratio of summed weights for severity. Show a sampling-change caution whenever the selection includes 2023 and a year from 2024 onward. Do not add year-over-year deltas, trend lines, growth rankings, or claims of changing injury incidence across that break.

### View specifications

#### 1. Headline metrics

**Purpose:** establish the selected burden, supporting sample size, and recorded severity before comparing mechanisms.

**Inputs:** all filtered rows' `Weight` and `is_severe`; shared context and quality notes. **Output:** `headline` with `weighted_ed_visits`, `record_count`, `severe_outcome_pct`. Use the shared formulas over the entire snapshot. No axes or sorting. Display the three distinct measures with units; raw NEISS records must never be labeled national visits. Missing and empty behavior follows the shared contract. All filters change all three metrics.

#### 2. Horizontal mechanism bar chart

**Purpose:** rank mechanisms by estimated national ED burden to find frequent mechanisms worth reviewing.

**Inputs:** `injury_mechanism`, `Weight`, `is_severe` from filtered rows. **Output:** one `mechanism_summary` row per present mechanism with `injury_mechanism`, `weighted_ed_visits`, `record_count`, `severe_outcome_pct` using the shared formulas within each mechanism.

**Axes:** x = weighted ED visits, linear starting at zero; y = mechanism. Sort top to bottom by weighted ED visits descending, ties by mechanism label ascending. Include all present mechanisms, including the upstream unknown category; no top-N truncation or empty categories. Tooltip includes all four summary fields. Missing/invalid inputs follow the shared rules. Rebuild from the current selection after any filter changes.

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
7. **Empty and invalid:** an empty frame retaining the required schema returns the declared empty state. Null/zero/negative/infinite `Weight`, duplicate IDs, blank mechanism, missing required column, or A's severe flag changed to false must each fail explicitly with no partial totals. Set A's disposition to 8, retaining true: headline remains unchanged (death counts as severe). Set D's disposition to missing, retaining false: totals remain unchanged and unknown quality weight remains 40.
8. **Diagnosis fallback:** replace D's missing diagnosis with invented code 999; its 40 weight / 66.666666…% becomes `Unmapped diagnosis (999)`, with no change to any other view. Duplicate a DIAG lookup key: fail rather than multiply weight.
9. **Provenance and period:** `source_scope="sample"` returns unavailable national views. For a period-label test only, copy the fixture to 2023 with distinct IDs and combine it with the 2025 fixture: totals = 240 visits, 10 records, 41.666666…%; labels say combined 2023 and 2025 total, and show the sampling-change caution. Do not label 240 an annual estimate or compute a growth percentage.

Compare unrounded numerical results within `1e-8`. Render checks verify units, category order, labels, filter/period context, and empty states, not pixel styling.

### Boundaries for interpretation

Use the primary-diagnosis composition and weighted severity definition above without inventing significance tests, reliability thresholds, or a combined risk score. Record counts aid interpretation but do not measure precision; uncertainty estimates require a survey design using `Stratum` and `PSU` and are outside this MVP. See section 01 for the confirmed analytical conventions.

## 06 — Setup, configuration, and application wiring

### Purpose and design

Connect the five components on one Streamlit page. Put burden and severity together before diagnosis detail to support the workflow in section 00. Setup owns configuration, initial state, layout/navigation, and calls to the other components; their business logic remains outside setup.

### Initial state and layout

Default to the complete 2025 calendar year, all mechanisms, all severity groups, and blank narrative search. Headline values are computed from that year's validated prepared cohort using section 05, never hard-coded from the raw-source row counts. If the artifact is missing, report it without falling back to another year or sample.

Use one scrolling page, wide layout, with no tabs or separate pages. Configure the page before rendering content. Display:

1. Title: `CPSC Treadmill Injury Dashboard`; subtitle: adults ages 65–120, selected calendar year, descriptive investigation aid.
2. Sidebar: fixed analysis-year text from configuration, then call `filters.render_sidebar(data)` for mechanism and severity multiselects, narrative search, and reset in the order specified in `04-filters.md`. The analysis year is configured, not another interactive filter. Empty multiselects mean all; blank search means no restriction.
3. Above results: active-filter description and `Showing X of Y prepared cases`, where X is filtered row count and Y is the loaded cohort count for the configured year. Setup owns this single count caption; the sidebar renderer owns only controls.
4. Three headline metrics in one row: estimated national ED visits, NEISS record count, weighted severe-outcome percentage, using `headline` from `05-views.md` without recomputation.
5. Next row: horizontal burden bar chart on the left; frequency–severity scatter plot on the right. On narrow screens they may stack in that order.
6. Full-width weighted primary-diagnosis composition stacked chart.
7. Full-width mechanism summary table.

Use the five views' axes, sorting, tooltips, labels, rounding, and missing-value rules exactly as specified in `05-views.md`. They are all visible initially; there is no chart picker or chart-driven filtering. Show the period and active selections alongside results. Below the headlines, show a brief severity-denominator note and the returned unknown-disposition count/weight, including zero. Explain that percentages describe the selected cases when severity is restricted. Leave decorative styling to the coding agent.

### Configuration contract

The future implementation reads `config.toml` beside `app.py` using Python 3.11+ `tomllib`. Resolve relative paths against that directory, not the shell's working directory. These paths implement the artifact contract in section 02; setup must not generate prepared data.

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

Use the component boundaries in section 01, the preparation artifacts in section 02, and the exact loader dictionary in section 03. After validating TOML and calling `st.set_page_config`, resolve artifact paths, load/cache the selected year, and execute this sequence:
The following loader boundary and artifact locations are **proposed integration contracts** requiring reconciliation with sections 02 and 03, not claims that these functions already exist. Reconcile them before the build; a coding agent must report incompatible contracts rather than quietly rename fields or implement preparation inside setup.

| Component | Receives | Returns / responsibility | When |
|---|---|---|---|
| Preparation (`02`) | Full annual NEISS source and its code documentation | Prepared cohort and provenance artifact | Separate offline step, never on dashboard reruns |
| Loader (`03`), proposed `load_dashboard_data(prepared_path, provenance_path, diagnosis_lookup_path, analysis_year)` | Resolved paths and configured year | Returns a validated dictionary with exactly four keys: `data`, `diagnosis_lookup`, `provenance`, and `metadata`, following the Section 03 loader contract. Raises an actionable error for missing or inconsistent values. | First successful load; cache thereafter |
| Filters (`04`) | `data` | `render_sidebar(data) -> FilterSelection`, then `apply_filters(data, selection) -> pd.DataFrame`, preserving rows' columns and values | Initial run and each widget rerun |
| Views (`05`) | The single filtered DataFrame, context, lookup | `build_view_data(filtered_df, *, context, diagnosis_lookup) -> dict`, exactly as specified in `05-views.md` | Initial run and every filter change |
| Setup (`06`) | Validated config and component results | Streamlit page, state messages, and placement of view renderers; no numerical aggregations | Every Streamlit rerun, reusing cached loading |

### Loader-to-setup interface validation

Before rendering dashboard results, setup must verify that the loader returns a dictionary containing all four required keys.

- `data` and `diagnosis_lookup` must be pandas DataFrames.
- `provenance` and `metadata` must be dictionaries.
- `provenance["analysis_years"]` must match the configured year.
- `metadata["case_counts_by_year"]` must agree with the loaded DataFrame.
- Missing or inconsistent values must produce an actionable validation error, not partial dashboard results.

Test this contract using a small invented DataFrame. Confirm that valid loader output reaches filters and views, while missing keys, incorrect types, or inconsistent metadata prevent rendering.

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

Build `filter_description` from `FilterSelection.mechanisms`, `.severities`, and `.narrative_query`: say “all” for empty tuples, list selected labels otherwise, and quote the trimmed search phrase or say “none”. This presents filter state without reimplementing matching. Escape user text through normal Streamlit text APIs.

Use a views registry with exactly the five IDs in `available_views`. Each renderer receives `(result, context)` and reads only the relevant fields: `headline` for metrics; `mechanism_summary` for the burden chart, scatter, and table; `diagnosis_composition` for the stack. Return a Plotly Figure for each chart, a DataFrame for the table, or the headline dictionary for setup's three metric slots. Setup reads dictionary keys such as `result["headline"]`, renders with `st.plotly_chart`/`st.dataframe`/`st.metric`, and owns page annotations from `quality`/`messages`. It never recomputes analytical quantities.

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
| Views `empty` | Keep filters and reset; show the empty-state message, 0 estimated visits, 0 records, N/A severity, and no chart marks or table rows per `05`. Sample scope still returns `unavailable`, even if its filtered rows are empty. |
| Valid loaded cohort itself empty | Also show `No prepared treadmill cases are available.` This is distinct from a selection excluding otherwise available cases. |

No raw traceback is necessary in the user interface; retain technical details in local logs. On each rerun render only the current result so an error or empty selection cannot leave old numbers visible. Unknown diagnosis/disposition handling remains with loader/views as documented; it is not a setup error unless a component reports a contract violation.

### Local execution and future deployment

Future application entry point: repository-root `app.py`, with `config.toml` beside it. Use Python 3.11+; pandas reads/normalizes files, selects rows, and aggregates; Plotly creates figures; Streamlit renders the page, session controls, and cached loading. TOML, JSON, hashing, and CLI parsing use the standard library. No database or external AI service is required at runtime. Declare dependencies in the project environment and lock the resolved compatible versions; `openpyxl` is needed for offline XLSX preparation only. The coding agent implements the modules/commands specified here; this editing task creates no application code.

Before setup, verify that `python --version` resolves to Python 3.11 or later. On Windows, a Store-alias message is not an installed interpreter: install or locate a supported Python and use its executable consistently to create the virtual environment. From the team repository, the future local launch is:

```powershell
python -m pip install streamlit pandas plotly openpyxl
python -m streamlit run app.py
```

From a fresh build: create/activate a virtual environment (`python -m venv .venv`, then on PowerShell `.\.venv\Scripts\Activate.ps1`), install dependencies above, obtain the annual source and complete lookup as in section 02, run the candidates phase, complete human review, run finalize, then launch `python -m streamlit run app.py`. The launch does not bypass review or create missing artifacts. `config.toml` is supplied by the future implementation from the example above; completed candidate reviews are the required human step before finalizing production data.

For later Streamlit hosting, deploy the same entry point and locked dependencies, prepare the cohort once outside the web process, and stage versioned prepared/provenance/lookup artifacts in deployment storage. Configure their paths there; avoid downloading the annual workbooks during requests. Verify memory limits and the same acceptance checks on the host, keep widget state session-specific, and invalidate caches when artifact versions change. No cloud deployment is part of this task.

### Build order and acceptance checks

Build in order: config validation/page skeleton; preparation export/finalize and its standalone checks; loader and its artifact checks; pure filtering then sidebar; view aggregations then renderers; setup wiring and UI checks. Component tests may use fixtures while team review is pending. Use the A–E invented fixture and expected outputs from `05-views.md` in tests with `source_scope="test_fixture"` injected through a test loader, never an end-user configuration option. Extend that fixture in the test loader with suitable `Narrative_1` values; it already contains the shared derived fields. Preserve its original numerical fields.

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

Before implementation handoff, give only this prompt and the dataset repository to a fresh agent for a readiness review; record every question, guess, and unavailable dependency, and resolve supported gaps. This review does not require implementing the dashboard. When the next deliverable builds the application, run `05`'s arithmetic and edge-case checks independently, then these wiring checks using test doubles, and finally open the real 2025 application locally to verify the initial screen and one filter/reset cycle. Do not describe a readiness review as an independent build test or claim a run that did not occur.


