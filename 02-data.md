data cleaning instructions
# Data Cleaning Instructions

## Goal

Create reproducible, analysis-ready NEISS tables for screening possible
treadmill injury mechanisms among adults age 65 and older. Preserve all raw
files unchanged. The cleaned data supports screening and narrative review; it
must not be used to claim that a treadmill caused an injury.

## Inputs

Use these files:

- `neiss_all_products_2025_sample.csv`
- `neiss_sports_2023_2025_sample.csv`
- `neiss_code_lookup_2025.csv`
- `sports_product_codes.csv`

The two NEISS case files are samples for development only. Do not report their
counts, percentages, or summed weights as national estimates.

## Required cleaning steps

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

## Validation checks

Before sharing outputs, verify that:

- no raw rows were overwritten;
- case IDs remain unique;
- all treatment dates parse correctly or appear in an exceptions report;
- all adult-65+ records have ages from 65 through 120;
- product-code flags check all three product columns;
- narrative-rule results can be traced to the original narrative;
- joins do not unexpectedly multiply case rows;
- raw sample totals are never described as U.S. national totals.

## AI use rule

AI may suggest cleaning code, regular expressions, and candidate narrative
rules. A human must inspect the resulting rows, especially all treadmill and
mechanism classifications, verify output counts, and document each decision.