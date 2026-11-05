# MVP validation

Evidence draft, 2026-11-05. Human review, real-data numbers and public-app evidence are pending. This document accurately reports completed software/fixture checks; it is not a claim that the real-data MVP or validation is complete.

This app helps a CPSC epidemiology analyst decide which treadmill injury mechanisms among adults 65-120 deserve closer investigation. It combines estimated emergency-department (ED) visits, recorded severe outcomes, primary diagnoses and supporting narratives. The full 2025 source passed 410,201-row, 25-column and calendar-year checks and produced 188 screening candidates. No finalized injury cohort exists. There are 171 recorded approvals transcribed from blanket chat endorsement; informed case-level review cannot be established from the available evidence. Those values are preserved, not treated as verified human decisions. Seventeen further cases have no approval. The proposed policy recommends 108 Include, 72 Exclude and 8 Unresolved; these are AI review-progress counts, not final injury findings.

## 1. Design

The CPSC [NEISS FAQ](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Neiss-Frequently-Asked-Questions) describes surveillance estimates and follow-back investigation, and distinguishes product association from causation. This supports an investigation-screening use case. Our particular interface, role scenarios and prioritization workflow are design hypotheses; no interview, usability study or observed analyst adoption is claimed. PENDING: team/user corroboration of decision constraints, workflow and usefulness.

The intended decision is where to spend limited follow-up attention, rather than whether a product is defective. Burden and severe share answer different questions: estimated volume versus recorded outcomes among visits. Diagnosis and narratives add context; visible evidence and missing outcomes help prevent overreading a high percentage supported by few records. The following eight changes extend the professor's starting build and remain protected by automated tests.

| Change request | Implemented behavior and decision rationale |
| --- | --- |
| CR-01 | Selected severe burden alongside all-outcome severe share, retaining mechanism/search. Prevents a severe-only filter from flattening every nonempty percentage to 100%. |
| CR-02 | Visible mechanism record counts and unknown-disposition counts/weights. Makes evidence volume and missingness inspectable without inventing precision thresholds. |
| CR-03 | Primary-diagnosis baseline beside selected composition under severity filtering. Keeps clinical context from being silently redefined. |
| CR-04 | Matching IDs and original narratives after all active filters. Enables users to examine what a literal search actually selected. |
| CR-05 | Reset and session-specific Undo reset. Restores the complete prior mechanism/severity/search selection for comparison. |
| CR-06 | Unknown share and none/all-unknown-severe endpoints. Shows the decision impact of missing outcomes without imputing values. |
| CR-07 | In-app mechanism definitions, version and initiating-event precedence. Makes taxonomy interpretation visible. |
| CR-08 | Full-precision contribution reconciliation and CSV with filter/period/data hash. Explains display rounding and supports independent audit. |

The team deliberately did not build exposure-adjusted risk, geographic/brand attribution, prediction, causal defect detection, significance claims or automatic investigation recommendations. The data and design do not support them. Source period is fixed to 2025; year-range controls and trends would require additional agreed artifacts and sampling interpretation. Counts are not confidence intervals, and no design-based uncertainty is estimated.

Meaningful alternatives are the official [NEISS query builder](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Instructions-for-Using-the-NEISS-Estimates-Query-Builder), an independent spreadsheet/script, and CPSC follow-back investigation. The official query provides selectable confidence intervals/CV and downloadable records; it does not automatically reproduce our narrative-screened, manually classified cohort. A separate analysis can explore broader fall-involving definitions but takes reconciliation work. Follow-back can supply circumstances absent from short narratives; this dashboard cannot replace it. A database or automated classifier would not resolve the present evidence/approval gap. Small, precomputed flat files keep interactions in memory and avoid exposing preparation inputs.

Preparation, loading, filtering, aggregation and UI wiring remain separate. Source and candidate fingerprints bind a completed review to its exact export; the loader rejects missing, edited, incomplete or sample artifacts instead of silently displaying national estimates. The injury-focused policy narrows the original broader involvement contract. Workbook acceptance cells record chat endorsement, while the fingerprinted policy document still says AI recommendation. The team must resolve that scope/approval inconsistency explicitly; no policy or codebook was silently changed. All records and taxonomy boundaries require real human verification; AI agreement does not satisfy that gate.

PENDING LIVE EVIDENCE: initial public screenshot with period, labels and selections; user/team assessment of whether these features support the intended decision. The code and tests are evidence of implemented behavior, not of actual user benefit.

## 2. Cases

These are illustrative role scenarios, not actual people or completed user research. The official surveillance/follow-back context supports the general tasks; individual priorities and decision constraints are assumptions the team must verify. For each case, capture the public app with active controls and record the actual interpretation, alternatives and limitations. No production result or screenshot is invented.

| Scenario and decision context | Interaction and interpretation to verify |
| --- | --- |
| Surveillance analyst allocating follow-up attention across mechanisms | Start with all 2025 records. Compare burden and severe share, supporting counts and primary diagnoses. PENDING: actual ranked mechanism, weights, evidence counts and screenshot. More weighted ED visits supports a volume question, not higher risk per user-hour. Consider activity exposure, healthcare access and review exclusions before prioritizing. |
| Incident reviewer checking a suspected belt-involved severe-fall pattern | Select Fall, Severe and literal belt search. Read matching narratives and compare with the same-search all-outcome baseline. PENDING: actual membership, values, narrative interpretation and screenshot. Belt may be a landing surface; a match does not prove belt initiation, defect or causation. An empty result is a valid result. |
| Evidence-quality lead deciding whether the severe share supports a defensible comparison | Inspect record count, unknown outcomes and conditional endpoints; compare primary-diagnosis mix. PENDING: actual unknown weight/share, endpoints and screenshot. Consider non-ED injuries left out, small supporting samples and missing clinical context. The endpoints are conditional assumptions, not probability intervals. |
| Analyst comparing a narrow subset with the starting population | Exercise Reset, Undo and a no-match phrase. PENDING: live controls, restored selection and screenshots. Confirm that comparisons retain the intended population and that empty results show unavailable percentages rather than misleading zeros. |

Ryan's claimed individual HW11 case is preserved in `cases/ryan-treadmill-falls.md`; the cleaner memo is `cases/ryan-treadmill-falls-final.md`, and its source/claim audit is `cases/ryan-treadmill-falls-evidence.md`. Alex, a fictional CPSC epidemiology analyst, must decide whether older-adult treadmill falls deserve priority. The planned public selections are: all mechanisms/outcomes and blank search; Fall with all outcomes; then Fall + Severe + literal belt. No live observations or personal verdict are supplied. Codebook 1.0 classifies initiating mechanisms, so entering/exiting and belt-initiated falls can lie outside Fall. Alex must decide whether that definition answers the priority question before relying on a rank. Neither the separate HW11 PDF nor a teammate's verdict was fabricated.

The [CPSC estimates explanation](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Explanation-Of-NEISS-Estimates-Obtained-Through-The-CPSC-Website) describes unequal weights and survey uncertainty. Sample counts do not replace design-based uncertainty or an exposure denominator. An apparent severe-share difference would not by itself settle investigation priority, especially when missing outcomes, diagnostic mix or medical triggers differ. The team must support each final case conclusion using actual observations and external context. No actual user interview or completed teammate case was found in the repository.

Scope-sensitive review cases are handled offline before these uses: medical-only visits versus medically triggered injury, mixed workouts versus unlinked history, direct equipment/cord contact versus unrelated hazards, and injury evidence versus isolated pain. Eight inclusion decisions remain indeterminate. Ten records have a taxonomy flag, including one of those eight; nine proposed inclusions need explicit human mapping resolution under the unchanged codebook. Do not turn a known uncovered event into a reviewed Unknown to satisfy software.

PENDING CASE CONCLUSIONS: after genuine review and deployment, state for each scenario whether the analyst is better off, which verified observation supports that conclusion, what outside evidence is still needed and when the app should not be used. Until then, usefulness is plausible rather than demonstrated. This prevents software tests from being described as user validation.

## 3. Numbers

One row represents one ED visit. Let T be selected survey-weight sum; S the weight for dispositions 2/4/5/8; U the weight for disposition 9, missing or unrecognized. Codes 0/1/6 are other known outcomes. We retain unknown weight in the severe-share denominator, do not rescale weights after exclusion, and use primary Diagnosis only. These are team conventions, not a clinical severity scale.

| Metric | Correct definition and independent check |
| --- | --- |
| Included records and weighted ED visits | Unique selected visit count and T. Compare independent ID membership/count and Decimal weight sum with actual filters/headline. |
| Severe count and weighted severe share | Count of disposition 2/4/5/8 records and 100*S/T. Verify severe-filter membership and weighted sums separately. Empty denominator is unavailable. |
| Mechanism totals | Sum original selected weights within each reviewed label; contributions must reconcile with T. Exclusions and unresolved records never enter the cohort. |
| Diagnosis composition | Primary-diagnosis weight divided by that mechanism's selected weight. Preserve missing and unmapped buckets; compare bucket sets/weights/shares and no duplicate contributions. |
| Unknown outcomes and sensitivity | Count and U; 100*U/T; conditional endpoints 100*S/T and 100*(S+U)/T. No missing value is recoded or imputed. |
| Baselines and exported precision | Baseline retains mechanism/search and removes severity only. Compare baseline severe share and selected severe burden independently. Downloaded CSV contributions must match independent unrounded numbers; final Weight must equal its original candidate value as Decimal. |

`validation/independent_numbers.py` uses csv, Decimal and loops without importing dashboard aggregations. `validation/verify_dashboard.py` extends the independent checks, then compares them with actual production filter/view builders and reconciliation exports. It covers all records, each available mechanism, Severe/Other known/Unknown, literal belt/metacharacter searches, combined Fall/Severe/belt and empty selections. Counts, IDs and bucket sets are exact; numerical comparison tolerance is max(1e-8 absolute, 1e-12 relative). Native public-browser presentation remains a separate check.

The reproducible fixture report is `validation/results/dashboard_fixture_results.json`. Records A-E and the historical toy label Contact are INVENTED, not production NEISS categories/findings. Actual fixture results and hand arithmetic agree:

| Invented fixture check | Independently verified result |
| --- | --- |
| Count and total | 5 records; 10+30+20+40+20 = 120 weight |
| Recorded severe | 3 records; 10+20+20 = 50 weight; 100*50/120 = 41.666666...% |
| Mechanism weights | Fall 40; toy Contact 60; Unknown/Unclassified 20 |
| Primary diagnosis within Fall | 57: 10/40 = 25%; 53: 30/40 = 75% |
| Primary diagnosis within toy Contact | 57: 20/60 = 33.333333...%; missing: 40/60 = 66.666666...% |
| Unknown outcomes | 1 record; 40 weight; 100*40/120 = 33.333333...% |
| Conditional endpoints | 41.666666...% if none unknown severe; 100*(50+40)/120 = 75% if all unknown severe |
| Display rounding | Three 10.4 contributions sum to 31.2. Rounded headline 31 can differ from separately rounded contributions summing to 30; exported contributions remain unrounded. |

During implementation the extended checker caught noncanonical diagnosis strings (53.0 versus 53) and incorrectly typed string weights in the new fixture runner. Canonical integer-code parsing and production-type normalization fixed the validation inputs; no metric definition or application aggregation was changed to force agreement. A regression test also injects an incorrect export value and confirms rejection. No unexplained fixture discrepancy remains.

PENDING REAL DATA: retained count, T, severe count/S/T, mechanism/diagnosis totals, U and both endpoints, final SHA-256, actual public outputs and CSV precision. No actual production cohort exists because genuine human verification, scope ownership and 17 priority decisions remain unresolved. Source/candidate/policy fingerprints match their preserved evidence; this verifies file identity, not human judgment. Candidate/AI counts and annual-source totals do not substitute for this evidence. The guarded finalization workflow will run these checks automatically after actual review; `validation/README.md` gives the separate executable command. The team must verify and defend the definitions and resulting interpretations.

## 4. Tests

The full repository suite passed **163 tests**, **0 failures**, **0 errors** and **0 skipped** on Windows/Python 3.13.15 on 2026-11-05; JUnit elapsed time 35.606 seconds. A fresh initial run in this session passed 155 tests. Eight additional tests protect private prepared-file packaging and honest approval-provenance reporting. Evidence and module counts are saved in `validation/results/test_summary.json`. Command: python -B -m pytest -q -p no:cacheprovider, with JUnit and temporary files outside the repository. No success is inferred from a previous run.

Existing tests cover preparation eligibility and annual source baselines, preserved fields/fingerprints, incomplete-review rejection, loader/provenance failures, empty/sample behavior, all five views, filters, cache invalidation and session isolation. `tests/test_mvp_changes.py` protects all eight change requests; `tests/test_independent_numbers.py` compares independent arithmetic with chart/table data. Original request descriptions and implementation commits in change-requests.md are preserved.

The review-transfer tests reject absent/deferred approvals, missing reviewer/explicit human verification, conflicting decisions, missing/foreign/duplicate IDs, changed narratives, invalid mechanism labels, unresolved recommendations, missing exclusion/resolution notes, stale candidate/policy identities and formula-based attestations. The new workflow tests reject a taxonomy gap without human resolution and an independent numerical discrepancy before publication. Invented-only end-to-end tests exercise review export, the unchanged finalizer, provenance loading, precise arithmetic and preserved inputs; production validators expose no fixture-bypass CLI.

The focused Human review form places the eight unresolved inclusion cases and nine included mechanism mappings first, while retaining all 188 records and the original audit/source sheets. Six additional invented-record tests verify that the reader uses explicit entries from this form and rejects ID/narrative mismatches, changed AI proposals, altered adjudication flags and conflicting legacy human inputs. Progress formulas report entries present, not approval. The form reader does not generate source values, reviewer identities or approvals. Existing workbook entries were assistant-transcribed earlier; this session preserved them and flagged their unestablished informed-review basis.

Release-path tests reject environments, raw downloads, nested datasets, candidate/review CSVs, workbooks, audit reports and secrets. The prepared directory now has a strict publication allowlist: only the 2025 runtime CSV/provenance, codebook and public preparation README. This closes a gap where a differently named policy or approval report could otherwise enter an archive. The read-only provenance audit flags assistant-transcribed attestations without changing them or treating populated Boolean cells as proof of review. The committed-HEAD audit found no private paths or candidate secret patterns, but blocked release for missing reviewed runtime data, pending links and uncommitted work. This is a limited pattern/path audit, not proof that no secret exists anywhere in history. The final staged diff and ZIP still require inspection.

Dependency checks passed: all 45 installed packages compatible and the lockfile consistent with the declared manifest. Local Streamlit health and root responded HTTP 200; AppTest raised zero exceptions and displayed the expected unavailable-data message. This verifies honest missing-data behavior, not a working public real-data release. Runtime application code, dependencies, tests for the eight CRs and one-shot-prompt.md were not changed by this session. The two already committed Colby property tests also passed: record-order invariance and unchanged shares/counts under uniform weight scaling.

PENDING RELEASE EVIDENCE: all 188 actual human decisions, semantic mechanism/policy acceptance, independently checked real-data outputs, Linux/cloud behavior, public/incognito access, live screenshots, realistic user interpretation and the recorded demo. Automated success cannot establish truthful human review, public availability or practical decision value. The professor's 03-mvp.pdf requires those remaining items; this PDF stays an evidence draft until they are completed.
