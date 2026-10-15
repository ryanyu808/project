# 03-loader.md — Loader

You are responsible for implementing the data-loading layer for the NEISS
treadmill-injury dashboard.

The dashboard is designed for a CPSC epidemiology analyst reviewing
treadmill-related emergency-department visits among adults age 65 and older.

Your component sits between the raw/cleaned NEISS source files and the
interactive filtering and visualization components.

Do not redesign the dashboard or invent new analytical definitions.
Implement the loading behavior described below.

## Job

The loader must:

1. prepare the three annual NEISS files for efficient use by the app;
2. identify the records eligible for this treadmill-injury analysis;
3. create and load a compact app-ready case-level dataset;
4. precompute the metadata and counts needed by downstream components;
5. verify the data facts that the rest of the application relies on.

The Streamlit app must not reread and scan all three raw Excel workbooks
after every user interaction.

## Source data

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

## Prepare the app-ready rows

For each annual file:

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

## Columns returned

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

Also preserve any downstream-created field that the filters require,
especially the narrative-coded `mechanism` field once it has been created
by the mechanism-classification component.

Do not silently discard columns required by downstream components.

## Precompute once

Do not repeatedly scan the three raw Excel workbooks during interactive
use.

Create a compact prepared dataset that contains only the cases required
for this project.

Also precompute or expose the metadata downstream controls need:

- minimum and maximum eligible age;
- available treatment years;
- number of prepared cases by treatment year;
- number of prepared cases by mechanism, once mechanism labels exist;
- whether the loader is using the full annual NEISS data or only a sample.

These values should be derived from the prepared data rather than
hard-coded.

## Runtime loading behavior

When the application starts:

1. Load the prepared case-level dataset.
2. Do not reload the original annual Excel files unless the prepared
   artifact does not exist and preparation is explicitly being run.
3. Return a pandas DataFrame suitable for the filtering component.
4. Preserve numeric types for `Age`, `Disposition`, product codes, and
   `Weight`.
5. Preserve `Treatment_Date` as a date/datetime value and
   `treatment_year` as an integer.

The filtering component, not the loader, is responsible for responding
to ordinary sidebar changes such as age range, year range, or selected
mechanisms.

## Data checks

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

## Full-data versus sample behavior

Expose a simple indicator such as `data_mode` with values like:

- `full`
- `sample`

Weighted national visit estimates are valid for the dashboard only when
the project is running on the intended full NEISS annual files.

If only a project sample is available, the loader must make that state
available to downstream components so the views can clearly label results
as sample-only and avoid presenting the sum of `Weight` as a national
estimate.

## Interface to downstream pieces

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

## Acceptance checks

The loader is complete when:

- the app can start without rereading more than one million raw NEISS rows
  on every run;
- the prepared dataset contains only the intended age-65+ treadmill cases;
- all required downstream columns and metadata are available;
- the full-data/sample state is unambiguous;
- all validation checks pass;
- filters and views can consume the returned data without reopening the
  raw workbooks.