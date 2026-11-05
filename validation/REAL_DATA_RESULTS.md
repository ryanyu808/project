# Reviewed 2025 production results

Verified local production evidence, November 5, 2026.

The guarded production workflow passed with **188 completed genuine reviews, 109 Include / 79 Exclude**, zero held cases and exactly 109 retained IDs. All retained weights match the original candidates as Decimal values. The full annual source has 410,201 records / 25 columns and dates January 1-December 31, 2025. Production CSV SHA-256: `c97b9ef421000d5a6e476a5e1598e16d6c8fde9ad20b5cd32d83c626480e985f`. Codebook version **1.2**. No candidate count is presented as an injury estimate.

Total T = **5119.6280 weighted ED visits**, 109 sampled visits. Severe dispositions 2/4/5/8 contribute **1141.8206** weight from **24** visits. S/T x 100 = **22.30280403185543949677593763%** (headline 22.3%). Unknown disposition U = **0**, zero records. Both conditional sensitivity endpoints therefore equal 22.30280403185543949677593763%; these are not confidence intervals.

| Mechanism | Records | Weighted ED visits | Severe records | Severe weight | Severe % |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fall | 65 | 3114.4453 | 18 | 882.6389 | 28.340164 |
| Unknown/Unclassified | 15 | 697.4813 | 3 | 102.9095 | 14.754446 |
| Equipment/cord obstacle or landing falls | 8 | 444.8651 | 1 | 51.8171 | 11.647823 |
| Belt contact | 9 | 330.4278 | 2 | 104.4551 | 31.612080 |
| Repair/moving | 8 | 277.7898 | 0 | 0 | 0.000000 |
| Entering/exiting | 4 | 254.6187 | 0 | 0 | 0.000000 |
| Struck by equipment | 0 | 0 | 0 | 0 | N/A |

All groups use all selected visit weight as the severe denominator. The codebook's Struck category is valid but absent in this cohort; the UI presents only observed mechanisms. Fall is not all fall-involving events: mounting, belt-initiated and equipment obstacle/landing mechanisms are distinct.

Primary diagnosis shares use one `Diagnosis` bucket per visit, divided by all weight in that mechanism; missing/unmapped buckets are preserved. In Fall, fractures (code 57) contribute **1092.5582 / 3114.4453 = 35.08034641032224903741285808%**. The independent report enumerates every diagnosis bucket, not just this example.

All 14 independent scenarios pass: all, six observed mechanisms, each severity, literal belt, literal metacharacters, deliberate empty and Fall + Severe + belt. Unrestricted belt = 3 records / 123.7879 weight / zero severe. Fall + Severe + belt = zero records / zero weight / N/A, not evidence that belt injuries never occur. Severe-only all-cohort = 24 records / 1141.8206 weight / 100%; the comparison baseline remains 109 / 5119.6280 / 22.302804%, retaining other selections. Fall severe baseline remains 65 / 3114.4453 / 28.340164% versus 18 selected severe records / 882.6389 weight.

The independent csv/Decimal method shares no pandas aggregation with the application. It checks exact ID sets, counts, mechanism and diagnosis buckets; weights/percentages use max(1e-8 absolute, 1e-12 relative) tolerance for floating-point dashboard values. CSV contributions reconcile unrounded; the separate selected_total row is not another contribution. Mechanism values rounded separately sum to 5119, while the rounded total is 5120. This one-visit display difference is explained by rounding; no weights were changed. No unexplained discrepancy remains.

Evidence: validation/results/real_2025_results.json, real_2025_dashboard_check.json and real_2025_app_check.json. These establish reviewed-data, builder/export and actual configured local-app agreement, **not public-browser evidence**. Public CSV download and visible screens must still be compared with this same hash.
