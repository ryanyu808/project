# Independent numerical validation

Run `uv run python validation/independent_numbers.py` from the application root.
The default five visits are invented, hand-computable test fixtures. Contact is
a historical toy label, not an additional production mechanism. No national
findings may be inferred from these records.

The calculator uses Python csv, Decimal and explicit loops, without importing
pandas, views, filters, loader or preparation. Results include total weight,
record count, recorded severe share, mechanism weights and primary diagnosis
shares, plus Fall, Severe, literal belt search and empty selections.

Hand arithmetic: total=10+30+20+40+20=120; severe=10+20+20=50;
severe%=100*50/120=41.666666... . Fall=40, Contact=60, Unknown=20.
Fall diagnoses: 57=10/40=25%, 53=30/40=75%. Contact diagnoses:
57=20/60=33.333333...%, missing=40/60=66.666666...%.

The integration cross-check in tests/test_independent_numbers.py compares all
these independent results with the dashboard outputs. It does not turn fixture
agreement into real-data validation. Review and compare the saved results with
the live app after the real cohort has been genuinely reviewed and finalized.

For a later real-data calculation, pass `--cohort data/prepared/treadmill_2025.csv
--provenance data/prepared/treadmill_2025.provenance.json --output
validation/results/real_2025_results.json` on a single command line. This verifies
the matching reviewed/full-annual metadata and hash, but is not an independent
verification that a human actually reviewed narratives. No real-data calculation
was performed in this session because no finalized production bundle exists.
