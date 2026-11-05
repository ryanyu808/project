# MVP completion status - November 5, 2026

Not submission-ready. This report distinguishes verified preparation from the missing reviewed-data/public release. The professor's source is ../11-prove-tt/mvp.md, the Markdown equivalent of 03-mvp.pdf. One teammate submits one repository ZIP below 2 GB before Quiz 11. The actual deadline is the course /hw calendar; the local Tue/Thu handout states November 10 at 9:30 am, but the team's section and official deadline must be confirmed. Keep the public app running through December 16.

The original Downloads/03-mvp.pdf is no longer present at its previously supplied path. The complete course mvp.md explicitly states it contains the same instructions; it was used as the current rubric source. No replacement rubric or deadline was invented.

## Completed and preserved

- Fresh initial suite: 155 passed. After eight meaningful release/provenance tests: **163 passed, 0 failed, 0 errors, 0 skipped**, Python 3.13.15, JUnit 35.606 seconds. See validation/results/test_summary.json. All eight CRs are implemented and tested; their request descriptions, built statuses and actual cf21acc implementation reference remain unchanged.
- Source identity, 188 unique candidate IDs/narratives, permitted mechanisms and source/policy fingerprints checked. Original review CSV still has all 188 reviewed=False. No approvals, candidate/source values, weights, codebook or one-shot prompt changed.
- Read-only approval audit now distinguishes entry validation from human-review provenance. All 171 recorded approvals remain preserved and flagged for unestablished informed review, including 59 adjudication-flagged entries. Seventeen priority decisions are still blank: eight inclusion and nine included mechanism mappings. AI proposals remain 108 Include / 72 Exclude / 8 Unresolved.
- One consolidated private 17-case decision table with original narratives and conditional recommendations: data/prepared/treadmill_2025.mvp_decision_report.md. No new workbook. Unavailable facts were not replaced by guesses; known taxonomy gaps remain visible.
- Guarded finalizer rejected case 250168690 for missing approval (exit 2), without --execute or output. Production CSV/provenance are absent. No unverified production data, fixture findings or AI approvals were published.
- Independent csv/Decimal fixture and actual dashboard-builder/export comparison both passed. Fixtures are explicitly invented. Unexplained fixture discrepancies: none. Real-data numerical validation is pending a genuinely finalized cohort.
- Locked manifest and requirements pins match; all 45 installed packages compatible. Isolated 14-file Windows runtime started from unrelated cwd; AppTest had zero exceptions and correctly no metrics/charts. Actual health and root HTTP 200; temporary server stopped. Native Linux/cloud/public behavior remains unverified.
- Packaging checks now allow only explicit public runtime files within data/prepared. Private policy, reviewer evidence and differently named prepared reports cannot pass the path audit. The final archive must still be inspected for contents and size.
- Root validation.md/PDF preserve substantial work, include the HW11 case and evidence limitations, and retain exactly Design, Cases, Numbers, Tests after the introduction. They are evidence drafts, not finished validation.
- Ryan's HW11 claim, research, final-memo draft and fixture report are preserved. No personal verdict, live values or screenshot was invented. No individual HW11 PDF is claimed.

## Rubric acceptance map

| Criterion | Evidence completed | Still required |
| --- | --- | --- |
| 1 Clear video | Five-minute narration and exact recording sequence | Actual recording, upload, signed-out access |
| 2 Compelling video | Specific analyst decision and interpretation prompts | Supported live conclusion; show why the user benefits |
| 3 Functional app | Local isolated startup; complete automated suite | Reviewed runtime cohort and public interactive checks |
| 4 Features | CR-01 through CR-08 implemented/tested | Confirm those features on the deployed release |
| 5 Design | Source-backed role, feature rationale, alternatives and deliberate exclusions | Team ownership and defensible user/workflow assumptions |
| 6 Cases | Ryan's specific case plus planned difficult scenarios | Several team-owned realistic public-app cases/screenshots |
| 7 Interpretation | Metric/scope/missingness/taxonomy limitations tied to decisions | Actual observations and human conclusions/verdicts |
| 8 Numbers | Independent checker, hand examples, precision/export guards | Actual finalized real-data and live reconciliation |
| 9 Tests | 163 passing tests with protected properties and regression examples | Recheck if later policy/taxonomy/runtime changes |
| 10 Overall | Guarded release and reproducible packaging preparation | End-to-end reviewed real-data MVP, links and final evidence |

## Remaining actions, in dependency order

1. **Team review:** establish the actual informed-review basis for the 171 transcribed approvals. Read/check each narrative and recommendation; resolve flagged reasoning case by case. Preserve existing entries and record truthful corrections or evidence. A new blanket automation confirmation is insufficient.
2. **Team decisions:** use the one private table to resolve eight inclusion cases and nine mechanisms. Explicitly own the injury-focused scope versus the original broader involvement definition. Reconcile the policy approval record and exact document fingerprint. A taxonomy revision requires consistent versioned contracts/tests and renewed affected-case review, not a note that contradicts the codebook.
3. **Data release:** run the validation-only command in review_tools/README.md. Only after genuine review and success, add --execute. Run validation/verify_dashboard.py and independent_numbers.py on the resulting matching runtime pair. Review counts, full-precision weights, exclusions, mechanisms, diagnoses, unknowns, endpoints, filters/baselines and exports. Publish only the small CSV/provenance.
4. **Hosting access:** browser inventory here returns The browser access host is unavailable. At share.streamlit.io select Create app > Yup, I have an app > repository ryanyu808/project > main > app.py > Advanced settings Python 3.13 > Deploy. No secrets. Sharing > This app is public and searchable. Keep GitHub private. This setup may be done earlier with an honest unavailable-data screen, but that is not MVP evidence. Verify the actual URL signed out; follow DEPLOYMENT.md.
5. **Evidence and evaluation:** compare the live app with independent real-data results, exercise Fall/Severe/belt, Reset/Undo and empty results, download CSV, and capture genuine public screenshots with visible controls. Finish Ryan's and teammates' interpretations/verdicts. Then update validation.md, generate/inspect final validation.pdf, and export the separate individual HW11 PDF. Do not submit the current draft as final.
6. **Video:** rehearse submission/DEMO_SCRIPT.md, record/upload the actual demonstration as Unlisted, and verify without login. Add only verified app/video links to README.
7. **Submit:** safely integrate teammate commits, inspect/stage/commit/push only the completed safe release artifacts, run submission/check_release.py, then --create-zip team-repo.zip. Inspect ZIP root files, runtime pair, exclusions and size. Upload the team ZIP and separate HW11 PDF to the correct Brightspace assignments by the confirmed deadline.

Git integration/push details and the final HEAD archive audit are recorded in the session completion report. No final submission ZIP is created while required gates remain open. The packaging workflow is ready; an unavailable-data framework package is not a submission-ready repository.
