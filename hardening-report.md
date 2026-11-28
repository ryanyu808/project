# Final hardening report

Executed November 27, 2026 Pacific on the integrated production cohort. Local AppTest evidence is not represented as live-browser screenshots. This is one scripted hardening pass, not a claim that several independent review rounds or a user study occurred.

Run `uv run --locked python validation/final_hardening.py`. Complete observations, selected metrics, warnings and empty messages are in `validation/results/final_20261127/hardening.json`.

| Kind | Tried and expected behavior | Actual finding and action |
| --- | --- | --- |
| Heavy everyday use | Five Fall + Severe + belt cycles; Reset twice; Undo; Reset. Controls must restore all selections and clear them on Reset. | All five cycles passed. Empty 0 / 0 / N/A was explicitly explained; actionable Clear guidance was visible. Parth's repeated-Reset fix retained the meaningful snapshot; no additional control defect found. |
| Unusual selections | Literal [.*], huge numeric text, absent name, whitespace, senior, button and wrong searches. No traceback or misleading substantive empty answer; identify what to change. | All checks passed. Empty selections gave recovery guidance. Whitespace restored the full population. Numeric text is narrative text, not an unsupported numeric input. The app has no editable age/date/ID controls; incompatible dates cannot be submitted. |
| Tiny groups | senior, button, wrong and Entering/exiting. Expect visible CPSC headline warnings. | All warned. Entering/exiting showed 255 / 4 / 0.0% with warning. James's warning checks current filtered headline, including severity. Survey CV remains uncomputed, explicitly disclosed; four records cannot establish safety or intervention effectiveness. |
| Data problems | Inspect runtime duplicate IDs, age bounds, positive weights, missing/variant mechanism labels; rescan publisher workbook and reviewed IDs. Regression suite also injects malformed/missing/source-mismatched bundles. | No duplicate runtime IDs, invalid ages, nonpositive weights or blank/variant labels. Source audit reproduced 188 screened / 109 included / 79 excluded. Missing outcomes are handled by explicit denominator/sensitivity logic. Fixed calendar 2025 is the only period, verified across original annual dates. Brief narratives, classification boundaries and absent exposure remain inherent data limits. |
| Consistency | Independently compare membership, totals, severity/diagnosis baselines and CSV across 14 selections; publisher-versus-app comparison; seven controlled calculation errors. | All 14 dashboard/export scenarios passed; all eight main values reconciled; all seven mutants failed as intended and views.py remained unchanged. Floating-point differences are explained in Part 3. Final video and final live screenshots still require separate verification. |

Commands and full raw outputs are in `validation/results/final_20261127/commands.json` and adjacent text files. The pinned Streamlit 1.45.1 suite passed 204 tests in 56.16s. A second run with the existing Streamlit 1.66.0 environment also passed 204 tests in 81.08s. Production AppTest and dashboard/export checks passed. No automated test was deleted or weakened during integration. R1 adds its caption regression, R4 adds empty-guidance and Undo regressions, and the existing main-result tests protect numerical behavior. Layout-only screenshot defects are checked visually.

The initial network-restricted Git fetch failed; the authorized network fetch succeeded. The public app was asleep, then woke without sign-in. Initially it lacked the unmerged R1 captions; R1 was merged after tests and successful CI. The old PDF builder loaded a stale historical PDF; it was replaced by current-source rendering to preserve Richard's new comparison and wording corrections. The original workbook's historical download date was not recorded; no date was invented.

The original recording gate was closed by the inspected final MP4. Current-source PDFs and clean extraction checks are verified separately; see validation.md and the final video evidence.


### Clean extraction and link checks (November 27)

A git-archive extraction of integration commit 89af745 installed from README with `uv sync --locked --python 3.13` and started with the README Streamlit command. Its health endpoint returned HTTP 200 / ok. The first elevated pytest process reported 126 passed / 78 setup errors because it could not access Windows pytest's existing temporary directory. Running that installed environment normally, without changing code or tests, completed successfully: `204 passed in 61.52s (0:01:01)`. The full command and diagnosis are recorded in `validation/results/final_20261127/clean_extraction.json`. This is an environment permission issue, not an application calculation failure; the earlier pinned full regression output remains reproduced above.

The link audit checked 21 extracted URLs. CDC/CPSC automated HEAD requests returned HTTP 403; those checks cannot establish that the source pages are inaccessible to a person. The public Streamlit link loops under a bare HTTP client but was successfully opened and exercised in the browser without sign-in. The scanner also captured one sentence-ending `/.` variant, which is not a separate published link. See `validation/results/final_20261127/url_checks.json`. Original workbook acquisition date remains undocumented. Final encoded-video review is now recorded in validation/results/final_demo_20261127/video-verification.json.


## Final recorded demo - November 27, 2026 Pacific

The required final recording is root [demo.mp4](demo.mp4): 322.700 seconds, 1920x1080 H.264 video at 12/1 fps, AAC audio with synthetic Microsoft Zira Desktop narration, 7,407,910 bytes. It shows the actual deployed dashboard in an isolated Chrome window with its real address bar. The file was fully decoded without errors and inspected through decoded frames for every narrated scene and the required interactions. No full-black interval of half a second or more was detected. Static reading intervals are deliberate; the actual filter/search/reset actions are continuously captured. No outside-team audience comprehension test is claimed.

- R5.2a: PASS. Every described control action is performed in the actual deployed app. The getting search is typed/applied during 04:06-04:09, with its result shown at 04:09-04:22; got off is typed/applied during 04:22-04:30, with its result at 04:30-04:45. The video also performs mechanism/severity filtering, narrative expansion, the empty intersection, two Resets and Undo. See root demo.mp4 and submission/FINAL_DEMO_TRANSCRIPT.md.
- R5.2b: PASS. Spoken opening results remain readable at 00:24-00:50; both mechanisms' totals, supporting counts and severe percentages remain in the summary table at 00:52-01:16. The selected severe Fall headline is shown at 02:09-02:26; search counts remain on screen during both search explanations. The final recorded narrative focuses on the analyst workflow and does not discuss a fracture-bar value or off-screen full-precision total. Decoded final-MP4 frames and timing evidence: submission/video-evidence and validation/results/final_demo_20261127/video-verification.json.
- R5.2c: PASS. The actual Chrome address bar displays treadmill-injury-dashboard.streamlit.app during the opening 00:02-00:23 and remains in the native window capture. This is the deployed URL in README, not a typed slide or simulated browser bar. See submission/video-evidence/opening.jpg and root demo.mp4.

The final workflow ends with Fall plus Severe as the initial follow-up shortlist and states the next investigation steps and limits. Exact narration and timestamps are in submission/FINAL_DEMO_TRANSCRIPT.md; machine metadata and hashes are in validation/results/final_demo_20261127/video-verification.json. Video production inputs remain outside the team repository.


### Final demo archive regression verification

The clean extraction of video release commit a9d97c3 installed with `uv sync --locked --python 3.13`. Running the extracted project's installed Python with `-m pytest -q -p no:cacheprovider` produced the complete actual output below. The production AppTest also passed. Raw commands/output and production-data fingerprint are in `validation/results/final_demo_20261127/extracted-checks.json`, `extracted-tests.txt`, `extracted-apptest.txt` and `extracted-app.json`. No application or test changes followed this check; subsequent final documentation and evidence additions do not change the tested runtime.

```text
........................................................................ [ 35%]
........................................................................ [ 70%]
............................................................             [100%]
204 passed in 22.61s
```
