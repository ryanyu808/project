# MVP validation — draft, not submission-ready

This dashboard is for a CPSC epidemiology analyst deciding which treadmill injury
mechanisms among adults ages 65–120 warrant deeper investigation. It brings
weighted ED burden, recorded severity, primary diagnoses and narrative evidence
together. The local 2025 annual export screened 410,201 records into 188 candidates;
none is yet represented as a human-approved production cohort. There is no live
app link or real-data numeric validation yet. All numerical examples below are
invented test fixtures. The team must verify the metrics, cases and conclusions.

## 1. Design

CPSC describes NEISS as supporting priorities for further study and distinguishes
product association from causation ([NEISS FAQ](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Neiss-Frequently-Asked-Questions)).
That supports an investigation-screening workflow; it does not prove a particular
analyst would use our interface. **PENDING HUMAN RESEARCH:** corroborate the actual
analyst workflow, decision constraints and relevant personas with stakeholder or
published workflow evidence. No interview or usability study is claimed.

Burden and severe share answer different questions: volume of ED visits versus
recorded severe outcomes within those visits. Diagnosis composition adds clinical
context. Search and matching narratives let an analyst inspect what supports a
count. Visible counts/unknown outcomes reduce the chance of interpreting a small
record group as precise. The codebook makes classification rules inspectable.

CR-01 adds an all-outcome severity baseline, CR-02 visible supporting evidence,
CR-03 a diagnosis baseline, CR-04 matching records, CR-05 Undo reset, CR-06 missing
outcome sensitivity, CR-07 definitions and CR-08 unrounded reconciliation/export.
Baselines preserve mechanism and narrative selections and remove only severity;
they are not automatically the whole cohort. Selected headlines remain unchanged.
The independent comparison populations are labeled rather than silently mixed.

We deliberately exclude geographic filtering, brand attribution, causal claims,
exposure-adjusted risk and automated safety recommendations because those inputs
or causal evidence are not available here. We do not show year-over-year trends
across the sampling change or add an unsupported risk score. Survey uncertainty
would require design-aware methods; record counts alone are not precision
estimates ([CPSC estimate explanation](https://www.cpsc.gov/cgibin/NEISSQuery/WebEstimates.html)).
Sensitivity endpoints are conditional missing-outcome calculations, not confidence
intervals. **PENDING:** team approval of medical-only and stationary-equipment
eligibility policies; genuine human review of every candidate.

## 2. Cases

The following are proposed scenarios, not observed users or validated research.
**PENDING:** source each persona's real context and constraints, run these cases
on the deployed reviewed-data app, capture screenshots with visible selections,
record actual outputs and have a human defend the interpretation.

| Proposed analyst situation | Actions | Decision and limits to evaluate |
|---|---|---|
| Hazard-screening analyst allocating investigation attention | Start unfiltered; compare burden and severity; inspect diagnosis and supporting counts | Which mechanism deserves narrative/incident follow-up? More weighted visits does not imply higher risk per user-hour. |
| Analyst evaluating a suspected belt-related severe event pattern | Select Fall, Severe, search belt; inspect exact narratives and all-outcome baselines | Does the text support the hypothesis, or is belt only a landing surface? Search may return few/no cases and is not a classifier. |
| Analyst faced with a high severe share and sparse records | Inspect evidence counts, unknown outcomes and conditional endpoints | Is evidence too limited for a priority recommendation? Neither count nor 100% implies statistical certainty. |
| Reviewer confronting medical-only, multi-episode or stationary-equipment narratives | Use the consolidated offline workbook and approved scope policy before finalizing | Is this an eligible injury visit? Do not automatically turn treadmill presence into causation or approval. |
| Analyst comparing a narrow subset with the full cohort | Reset and Undo reset; test a no-match literal phrase | Does comparison preserve the intended selection and show honest empty results? No matches does not establish absence of a real hazard. |

NEISS covers ED-treated visits from its probability sample, not all injuries or
participants. Short narratives and the treadmill-text restriction can miss or
misdescribe events. Exposure, population activity, medical triggers, reporting and
classification decisions can affect interpretation. **PENDING:** case-specific
limitations with sources, actual numerical evidence, outside factors and a clear
conclusion about whether the analyst is better off. No production findings or
live screenshots have been invented.

## 3. Numbers

The team must own these definitions. Let T be the sum of selected visit weights,
S the sum for dispositions 2/4/5/8, and U the sum for unknown dispositions (9,
missing or unrecognized). Codes 0/1/6 are other known outcomes. False is not proof
of a mild injury. One record is one ED visit, not one distinct person.

| Metric | Exact definition and population |
|---|---|
| Estimated ED visits | T, sum of original weights after active filters; no rescaling after exclusions |
| NEISS records | Number of selected unique case IDs |
| Severe share | 100*S/T; unknown outcomes remain in denominator; empty denominator is unavailable |
| Mechanism burden | Sum of selected weights for each reviewed mechanism; contributions reconcile with T |
| Diagnosis composition | Primary Diagnosis weight / mechanism's selected weight; missing and unmapped buckets retained; no secondary double-counting |
| Severity baseline | Same mechanism/search population with severity removed; baseline S/T compared with selected severe weight |
| Completeness | 100*U/T; conditional endpoints 100*S/T and 100*(S+U)/T, all on the selected population |

CPSC distinguishes weighted national estimates from sample case counts and
design-based uncertainty ([estimate explanation](https://www.cpsc.gov/cgibin/NEISSQuery/WebEstimates.html)).
The severe composite and mechanism rules are team conventions in the unchanged
one-shot prompt and codebook, not CPSC clinical-severity thresholds.

Independent calculator: validation/independent_numbers.py uses csv, Decimal and
loops without importing dashboard aggregations. Its fixture/results files are
under validation/fixtures and validation/results. An integration test compares
its independently calculated values with all dashboard aggregates.

| Invented check | Hand result |
|---|---|
| A–E total/count | 10+30+20+40+20 = 120; 5 records |
| Severe weight/share | 10+20+20 = 50; 50/120*100 = 41.666666…% |
| Mechanism weights | Contact 60, Fall 40, Unknown 20; Contact is a toy fixture label only |
| Fall diagnoses | Code 57: 10/40=25%; code 53: 30/40=75% |
| Contact diagnoses | Code 57: 20/60=33.333…%; missing: 40/60=66.666…% |
| Severe-filter baseline | Selected severe weight 50; baseline Fall severe share remains 25% |
| Unknown sensitivity | U=40; U/T=33.333…%; endpoints 41.666…% and 75% |
| Rounding | Three 10.4 contributions sum to 31.2, headline rounds to 31, separate displayed integers sum to 30 |

There is no unresolved numerical difference in these fixture checks. **PENDING
REAL DATA:** run the independent calculator on the final matching CSV/provenance;
check all important initial/filtered values against the live app, reconcile
rounding/exclusions and record the cohort SHA-256. Candidate counts, AI labels,
simulations and annual-source row counts are not reviewed injury findings.

## 4. Tests

Starting baseline in this session: 90 tests passed on Windows/Python 3.13.15.
This includes the professor's original 87 plus the pre-existing three Ryan Module
10 cases; the latter were untracked at handoff and were preserved unchanged.
The original tests cover review gates, eligibility, fingerprints, loader failures,
filter semantics, missing values, arithmetic, empty/sample states, widgets and cache.

New tests in tests/test_mvp_changes.py protect the eight change requests: selected
versus baseline populations, zero-selected/nonempty-baseline results, search and
mechanism restrictions, unknown counts, literal record matching, definition text,
diagnosis baseline, Reset/Undo session isolation, sensitivity endpoints, rounding,
download metadata and empty behavior. tests/test_independent_numbers.py adds a
separate Decimal cross-check for all five requested numerical families and guards
duplicate IDs/bad weights. These protect the decisions users could otherwise
misread, rather than merely checking that a page opens.

Unchanged invariants: positive finite weights, unique IDs, no join multiplication,
full-source provenance, complete human-review gate, preserved narratives, diagnosis
shares summing to 100% within a nonempty mechanism, and no national outputs from
development samples. Approximate floating comparisons use 1e-8 where appropriate;
IDs, selected membership and counts are exact. The reconciliation download also
checks internal sum agreement before export.

**PENDING RELEASE EVIDENCE:** final run record is in MVP_WORK_REPORT.md. Native
Linux/cloud behavior, multi-user performance, live screenshots, actual user
interpretation and independently recalculated real-data totals remain unverified.
Fixture UI tests are not live-app screenshots or evidence of completed human review.
