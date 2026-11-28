# Team T9 response to MVP feedback

Final integration draft, November 27, 2026 Pacific. Technical checks below are executed evidence; pending items are explicitly identified. Attribution follows the assigned division and Git history.

## R1.1a

Requirement: Headline states reviewed subset of 2025 visits at 65+, treadmill mention and some screened visits set aside.

Response (Colby): PASS locally and public captures available. Evidence: app.py; tests/test_app.py. See `requirements-matrix.md` and the current validation PDF for context.

## R1.1b

Requirement: Severe outcomes explained in words beside headline.

Response (Colby): PASS locally and public captures available. Evidence: app.py: transfers, admissions, observation and ED fatalities. See `requirements-matrix.md` and the current validation PDF for context.

## R2.1

Requirement: Headline warns next to totals below 1,200 weighted visits or 20 records, using current severity selection.

Response (James): PASS locally and public captures available. Evidence: app.py; tests/test_mvp_changes.py; final_20261127/hardening.json. See `requirements-matrix.md` and the current validation PDF for context.

## R3.1

Requirement: Each final live-app case screenshot shows its selections; no dropdown obscures Severity/search.

Response (Ryan integration): PASS: final case supplement with controls visible. Evidence: Cases in validation.md. See `requirements-matrix.md` and the current validation PDF for context.

## R4.1

Requirement: Empty intersection identifies filters or combinations to change.

Response (Parth): PASS locally. Evidence: filters.py; tests/test_r4_recovery.py. See `requirements-matrix.md` and the current validation PDF for context.

## R4.2

Requirement: Two consecutive Resets retain last meaningful selection for Undo.

Response (Parth): PASS locally. Evidence: filters.py; tests/test_r4_recovery.py; five repeated production cycles. See `requirements-matrix.md` and the current validation PDF for context.

## R5.1

Requirement: Design reports actual nearest CPSC query result and selection limits.

Response (Richard): PASS: teammate capture gives 24,577 / 509 for exercise equipment. Evidence: validation.md Design; cases/screenshots/cpsc-query-2025-result.png. See `requirements-matrix.md` and the current validation PDF for context.

## R5.2a

Requirement: Every narrated step performed on screen in final live app.

Response (Ryan integration): PENDING authentic final recording. Evidence: submission/FINAL_DEMO_PLAN.md. See `requirements-matrix.md` and the current validation PDF for context.

## R5.2b

Requirement: Every spoken number remains readable during narration.

Response (Ryan integration): PENDING recording review. Evidence: submission/FINAL_DEMO_PLAN.md. See `requirements-matrix.md` and the current validation PDF for context.

## R5.2c

Requirement: Browser address bar shows README live link at least once.

Response (Ryan integration): PENDING recording. Evidence: submission/FINAL_DEMO_PLAN.md. See `requirements-matrix.md` and the current validation PDF for context.

## R6.1

Requirement: Case 3 no longer calls 3277 treadmill-specific.

Response (Richard): PASS in current source; rendered from current Markdown. Evidence: cases/case-sarah-treadmill-orientation.md; validation.md. See `requirements-matrix.md` and the current validation PDF for context.

## R7.1a

Requirement: Standalone original-2025-publisher check imports no app; documents source location.

Response (Ryan): PASS: original workbook rerun, 410,201 rows. Evidence: validation/publisher_numbers.py; original workbook SHA in Part 3. See `requirements-matrix.md` and the current validation PDF for context.

## R7.1b

Requirement: Each main result beside app value, all discrepancies explained.

Response (Ryan): PASS: eight values agree within stated floating-point tolerance. Evidence: validation/compare_publisher.py; Part 3; final_20261127/publisher.json. See `requirements-matrix.md` and the current validation PDF for context.

## R8.1

Requirement: Tests demonstrably fail for every required main calculation except overall count.

Response (Ryan): PASS: seven authentic failed runs, correct source hash unchanged. Evidence: tests/test_publisher_results.py; validation/results/r8/*.txt; Part 4. See `requirements-matrix.md` and the current validation PDF for context.

## R9.1

Requirement: Part 4 covers all five kinds: tried, found, changed or inherent limits.

Response (Ryan integration): PASS: local five-category report and public workflow captures. Evidence: validation/final_hardening.py; hardening-report.md; final_20261127/hardening.json. See `requirements-matrix.md` and the current validation PDF for context.

## Optional items

### O1

Deferred: chart color and scatter-label redesign were outside the required integration fixes. Existing hover/table labels remain available; no claim that the visual suggestion was implemented.

### O2

Deferred: age standardization, medical-event sensitivity and second-diagnosis sensitivity were not added to this release. Existing cases retain their descriptive limits; no adjusted risk or causal interpretation is claimed.

### O3

Deferred: no new classification decisions, alternative spellings cohort or severe-share export fields were introduced. Existing reviewed labels are preserved; these extensions require separate cohort/definition review.

### O4

Deferred: broader product comparisons and a validated survey estimator were not added. CV is explicitly uncomputed; raw hospital counts would not substitute for a validated estimator.

### O5

Deferred: excluded-reason aggregation was not published. The allowed reviewed-ID list preserves genuine decisions without publishing private review notes.

### O6

Deferred: selected-record field/download expansion is not implemented. Existing narrative IDs support follow-up, with the original source still needed for other fields.

### O7

Not implemented in this integration: the existing literal-metacharacter fixture weakness remains a test-coverage limitation, although production literal matching uses regex=False. No claim of protection against all filter mutations is made.

### O8

Deferred: zero-valued severe charts and the severity-filter wording were retained. They do not change calculations; this report does not claim those displays were redesigned.

