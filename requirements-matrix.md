# Final feedback requirements matrix

November 27, 2026 Pacific. Based on all pages of the official T9 MVP Feedback Report. PASS locally does not imply the final live deployment or video has been verified. The report has 11 numbered required points; lettered checks are split below for traceability.

| Check | Owner | Acceptance criterion | Implementation/evidence | Status |
|---|---|---|---|---|
| R1.1a | Colby | Headline states reviewed subset of 2025 visits at 65+, treadmill mention and some screened visits set aside. | app.py; tests/test_app.py | PASS locally and public captures available |
| R1.1b | Colby | Severe outcomes explained in words beside headline. | app.py: transfers, admissions, observation and ED fatalities | PASS locally and public captures available |
| R2.1 | James | Headline warns next to totals below 1,200 weighted visits or 20 records, using current severity selection. | app.py; tests/test_mvp_changes.py; final_20261127/hardening.json | PASS locally and public captures available |
| R3.1 | Ryan integration | Each final live-app case screenshot shows its selections; no dropdown obscures Severity/search. | Cases in validation.md | PASS: final case supplement with controls visible |
| R4.1 | Parth | Empty intersection identifies filters or combinations to change. | filters.py; tests/test_r4_recovery.py | PASS locally |
| R4.2 | Parth | Two consecutive Resets retain last meaningful selection for Undo. | filters.py; tests/test_r4_recovery.py; five repeated production cycles | PASS locally |
| R5.1 | Richard | Design reports actual nearest CPSC query result and selection limits. | validation.md Design; cases/screenshots/cpsc-query-2025-result.png | PASS: teammate capture gives 24,577 / 509 for exercise equipment |
| R5.2a | Ryan integration | Every narrated step performed on screen in final live app. | submission/FINAL_DEMO_PLAN.md | PENDING authentic final recording |
| R5.2b | Ryan integration | Every spoken number remains readable during narration. | submission/FINAL_DEMO_PLAN.md | PENDING recording review |
| R5.2c | Ryan integration | Browser address bar shows README live link at least once. | submission/FINAL_DEMO_PLAN.md | PENDING recording |
| R6.1 | Richard | Case 3 no longer calls 3277 treadmill-specific. | cases/case-sarah-treadmill-orientation.md; validation.md | PASS in current source; rendered from current Markdown |
| R7.1a | Ryan | Standalone original-2025-publisher check imports no app; documents source location. | validation/publisher_numbers.py; original workbook SHA in Part 3 | PASS: original workbook rerun, 410,201 rows |
| R7.1b | Ryan | Each main result beside app value, all discrepancies explained. | validation/compare_publisher.py; Part 3; final_20261127/publisher.json | PASS: eight values agree within stated floating-point tolerance |
| R8.1 | Ryan | Tests demonstrably fail for every required main calculation except overall count. | tests/test_publisher_results.py; validation/results/r8/*.txt; Part 4 | PASS: seven authentic failed runs, correct source hash unchanged |
| R9.1 | Ryan integration | Part 4 covers all five kinds: tried, found, changed or inherent limits. | validation/final_hardening.py; hardening-report.md; final_20261127/hardening.json | PASS: local five-category report and public workflow captures |
