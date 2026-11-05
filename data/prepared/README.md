# Prepared treadmill cohort

One row is one ED visit. The original 25 fields and narratives are retained.
`adult_65_plus`: age integer years 65–120 (not age 0 or infant-month codes).
`has_product_3277`: code 3277 in any of Product_1/2/3.
`mentions_treadmill`: case-insensitive literal TREADMILL in Narrative_1.
All three flags must be true. `treatment_year` comes from Treatment_Date.
`is_severe`: disposition 2/4/5/8, false for other or missing outcomes.
`injury_mechanism`: human-reviewed, mutually exclusive Version: 1.1 codebook label.
Unknown/Unclassified is a reviewed unclear mechanism, never unfinished review.
Primary Diagnosis alone is used in composition. Secondary blanks are retained.
XLSX dates use the explicit NEISS_year sheet; annual TSV dates are MM/DD/YYYY;
sample dates are ISO. CSV outputs use ISO dates and explicit true/false flags.

Candidate, blank review, source evidence and quality files are audit artifacts,
ignored by git and never read by the dashboard. Preserve them locally. Candidate
SHA-256 binds finalization to the export. Final CSV/provenance bind the runtime
cohort. No estimates may be published until every candidate is human-reviewed.
The complete lookup is copied unchanged to ../reference/ and comes from the
dataset repository's complete 2025 four-column reference, not a sampled lookup.

Version 1.1 adds Non-use equipment/cord-related falls and covers unpowered supporting-surface Fall. See ../../docs/MECHANISM_CHANGELOG.md. Missing use context does not establish non-use; four current mappings remain pending and no runtime pair is finalized.
