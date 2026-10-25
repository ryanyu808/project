# Build report

Status: complete

- Builder model(s): Codex GPT-6.1 (gpt-6.1-sol), medium reasoning; one same-model readiness-review agent, as explicitly requested in the prompt. No implementation delegation.
- Dates and sessions: 2026-10-20, one build session.
- App repo: USC-DSO-576-PS/project-prof-build-T9
- Run command (from a fresh clone): Python 3.11–3.13; create/activate `.venv`, `python -m pip install -r requirements.txt`, then `python -m streamlit run app.py`. Exact macOS and Windows PowerShell commands are in README.md.

## Outcome

Implemented the specified five-component Streamlit application, offline candidate export/finalize CLI, strict configuration, validated cached loader, pure filters, five coordinated views, and automated component/UI checks. Downloaded all three complete annual sources and independently exported 122/148/188 candidates for 2023/2024/2025. Production remains blocked by the explicit human narrative-review gate: no person is available to review those candidates. The default app runs and displays the prescribed actionable missing-artifact state, without numeric estimates or fallback. All five views and both workflows run with isolated invented fixtures. No production classifications, estimates, or completed reviews were invented. The real production initial/filter/reset cycle cannot be completed until human review and finalization occur.

## Asked or guessed

No questions were asked; the user said no one would answer. The readiness review identified the human-review dependency, path mismatch, fixture taxonomy and historical editing language before substantive implementation.

| # | Prompt text (quote, with section) | What the builder did | Effect on the app | Cause (PROMPT / BUILD / UNSURE) |
|---|---|---|---|---|
| 1 | §01: “a human must review every candidate narrative” and “Build and test components with the invented fixtures ... while production narrative review is pending” | Left every real review pending; tested fixtures through explicit test-only injection. Finalizer rejects the real review template. | Production views unavailable; no fabricated classifications or estimates. | PROMPT |
| 2 | §02: “Place the dataset repository ... beside app.py, or update configured paths.” | Copied the complete 1,250-row lookup unchanged from the provided sibling into data/reference; configured that path. | Fresh clones do not depend on sibling paths. | BUILD (coordinator retag: caused by the build setup's sibling dataset location, which the prompt allows to be handled by updating paths) |
| 3 | §02: “prepare 2023, 2024, and 2025 independently when available” | Acquired official 2023/2024 XLSX and 2025 TSV; exported each independently, without combining years. | Fixed 2025 UI; older exports remain offline, unreviewed. | PROMPT |
| 4 | §02: “Use one source representation per year” and “Verify relevant codes against each source year's NEISS_FMT” | Used only TSV case records for 2025; separately downloaded its XLSX for NEISS_FMT verification only. Compared DIAG, DISP and product 3277 against all three annual format sheets; no discrepancies. | No double-counted twin sources; unchanged runtime lookup validated. | PROMPT |
| 5 | §06: “These labels are fixture labels, not a proposed production taxonomy.” | Tests accept Contact and toy P/Q/R labels only through private test injection; production loader/finalizer use the six approved labels. | No additional production mechanism aliases. | PROMPT |
| 6 | §06: “this editing task creates no application code” / “future implementation” | Treated these historical phrases as superseded by the user's explicit instruction to build. | Implemented the application and commands. | PROMPT |
| 7 | §06: “Leave decorative styling to the coding agent.” | Used Streamlit's native layout with restrained Plotly styling, preserving exact view order and controls. | One wide scrolling page, no tabs, chart picker or new filters. | PROMPT |
| 8 | §02: “Candidate/review/source-evidence files ... Audit trail retained separately; never loaded” and user: “only the condensed data files the app reads” | Kept raw files and generated candidate/review/source/quality evidence locally, git-ignored. Committed runtime lookup and documentation; no unfinished production CSV. | Small repository; audit exports regenerate offline. | BUILD (coordinator retag: commit scope comes from the build protocol/user rule, not the prompt) |
| 9 | §02: “Stop on structural failures ... rather than assuming malformed rows are ineligible.” | Validate IDs/dates/weights across entire source before eligibility and preserve traceable exception rows. Refuse to overwrite existing candidate/review work. | Bad upstream records cannot disappear through cohort exclusion; repeat exports use a new directory. | PROMPT |
| 10 | §06: “lock the resolved compatible versions” / “Python 3.11+” | Locked a Python 3.11–3.13-compatible dependency set and tested on Python 3.12.13 and fresh-clone Python 3.11.15; README recommends 3.12. Environment's python command was absent and system python3 was 3.14, so used uv to create 3.12 environment. | Portable standard-library app/tests; no Linux-only imports or symlinks. Native macOS/Windows execution not available here. | BUILD |
| 11 | §06: “Before implementation handoff ... fresh agent ... readiness review” | Ran a prompt-and-dataset readiness review with a separate agent. Recorded findings above. | Human review identified as an external prerequisite; readiness was not counted as build validation. | PROMPT |
| 12 | §06: “open the real 2025 application locally ... initial screen and one filter/reset cycle” | Opened default app in headless Chrome; verified unavailable state. Separately opened fixture app and exercised search/reset. | Real numeric initial/filter/reset acceptance explicitly remains blocked, not passed. | PROMPT |
| 13 | §02.4: “Export every candidate's ID, original Narrative_1, and proposed mechanism/rule for human review” vs §01 “preparation may propose an initial label” (row added by coordinator) | Candidate CSV has the 25 source fields plus flags; no proposed-label/rule audit column. | Human reviewer gets no starting proposal for 188/148/122 narratives; does not affect published data. | PROMPT (coordinator: §01 says “may”, §02 says “export”; inconsistent wording) |

## Use cases

| # | Use case | Result (works / partly / fails) | Cause (PROMPT / BUILD / UNSURE / —) | Evidence |
|---|---|---|---|---|
| 1 | Prioritize high burden versus recorded severity; check primary diagnoses | partly | PROMPT | Fixture UI shows 120 estimated visits, 5 records, 41.7%; bars/scatter/table reconcile to Contact 60, Fall 40, unknown 20. Diagnosis shares pass independent arithmetic/render tests. Real mechanism comparisons await human review. |
| 2 | Select Fall, Severe, search belt; inspect all five views | partly | PROMPT | Streamlit UI tests produce fixture A only: 10 visits, 1 record, 100%; belt alone selects A/C (30, 2, 100%). Headless-browser belt search and reset restore 120/5/41.7%. Real narrative investigation remains blocked by review gate. |

## The prompt's "done when" checks

Final suite: **87 passed**, 6.03 s on Python 3.12.13; **87 passed**, 10.68 s in a separate fresh clone on Python 3.11.15.

| Check | Result | Note |
|---|---|---|
| Readiness review using prompt/dataset only | PASS | Separate agent; no implementation delegation or external private dependencies. |
| Config validation/page skeleton first, then preparation, loader, filtering, aggregation/rendering, setup | PASS | Implemented in that order; preparation checked independently before integrations. |
| Raw annual schema/count/date coverage | PASS | 2023: 338,262; 2024: 361,672; 2025: 410,201; 25 original columns each; Jan 1–Dec 31 each year. No duplicate/missing IDs, invalid dates or nonpositive/nonfinite weights. |
| Age, product columns, literal treadmill eligibility, null narrative | PASS | Standalone invented tests cover 0/205/64/121 excluded, 65/120 included, product in any column, mixed case, text-only/product-only excluded. |
| P/Q/R export/finalize boundary | PASS | Retain P/Q at 10/20, exclude R with reason; count 2, reviewed count 3, digest exact. Missing/foreign/duplicate IDs, edited candidates, pending review, bad label or absent exclusion reason reject publication. |
| Valid zero-candidate bundle | PASS | Empty CSV keeps header; zero prepared/reviewed counts; matching digest; empty loader and view states tested. |
| Production human review | BLOCKED | All real candidates remain reviewed=false; finalizer fails with “Human review pending: every candidate requires reviewed=true”. No final artifacts published. |
| Loader dictionary/types/metadata/evidence | PASS | Tests reject digest/year/schema/ID/Boolean/severity/label/weight/eligibility/source/review failures; toy counts rejected by production source validator. No raw annual files loaded at runtime. |
| Disposition mapping | PASS | 2/4/5/8 severe; 0/1/6 other known; 9/missing/999 unknown. False does not imply confirmed mild. |
| Pure filtering + sidebar | PASS | Exact §04 fixture; OR within controls, AND across; trimmed literal query including fall.*; original columns, order, index and weights preserved; unknowns retained; reset and options after zero matches tested. |
| §05 checks 1–5, arithmetic and each renderer | PASS | 120/5/41.666666...; summary order/weights/counts/severity, uniform scatter markers/tooltips, diagnosis weights/shares, primary-only invariance and table schema checked within 1e-8. |
| §05 checks 6–8, filtered/empty/invalid/fallback | PASS | Fall 40/2/25%; severe 50/3/100%; empty 0/0/N/A; invalid input suppresses totals; death mapping, missing dispositions, unmapped 999, duplicate DIAG lookup covered. |
| §05 check 9, sample and multiyear | PASS | Sample scope suppresses all national views even when empty; 2023+2025 fixture totals 240/10/41.666666... with combined-not-annual labels and sampling caution. No multiyear UI added. |
| Initial state, all five views, exact placement | PASS (fixture) | AppTest verifies three metrics, three charts and table; browser visual check confirms burden left/scatter right, diagnosis next; summary last. |
| Fall / Severe / belt / empty search / reset wiring | PASS (fixture) | AppTest follows full combined-filter/reset cycle; no stale counts; options remain available. Browser verifies belt then reset. |
| Cache/state isolation and invalidation | PASS | Instrumented underlying loader called once across widget changes, again after fingerprint change; failed refresh clears results. Selection remains in session state only. |
| Bad config before data/widgets | PASS | String/Boolean year, unknown key, wrong layout, duplicate/unknown/missing/reordered views, nonempty defaults rejected. Integration test proves loader not called on configuration error. |
| Missing/invalid/sample artifacts, valid empty cohort | PASS | Missing data default and sample have no national outputs; bad refresh no stale results; distinct no-prepared-cases message with 0/0/N/A and reset. |
| Real 2025 browser initial/filter/reset | PARTLY / BLOCKED | Actual initial unavailable screen verified; production numeric/filter/reset cycle blocked by missing human-reviewed artifact. Not represented as completed. |
| Fresh-clone install/start | PASS builder smoke | Separate clone under TMPDIR, Python 3.11.15, locked dependency install, 87 tests passed in 10.68 s; Streamlit health/page HTTP 200 in 4.233 s, then stopped. No raw files in clone. This is a builder check; Coordinator section remains untouched. |
| macOS and Windows portability | PASS static / native untested | Explicit run commands; Python-only runtime; no platform-specific facilities in app/tests and no git symlinks. Native OS runners unavailable. |

## Real-world operation

- Data size used (rows, MB) and whether it is the full real size: all 1,110,135 annual source rows checked independently. Official files: 2023 XLSX 42.5 MB, 2024 XLSX 47.4 MB, 2025 TSV 85.9 MB; 2025 XLSX 54.0 MB used only for format-sheet verification. Real candidates: 122/148/188, not human-reviewed. Runtime production cohort unavailable; UI tested with five invented visits and complete lookup.
- Start-up time: fresh-clone Python 3.11 Streamlit health/page HTTP 200 in 4.233 s. Separately measured browser end-to-end launch to checked screen on this shared host: 30.42 s for real unavailable-data screen, 19.19 s for fixture charts. Includes Chrome startup; not an isolated server-load benchmark.
- Slowest interaction, and how slow: browser fixture reset 0.495 s; belt search 0.452 s. Real production interactions unavailable pending review.
- Memory at peak: peak not continuously instrumented. Largest sampled server RSS 181.1 MB (fixture); real unavailable-data server 145.8 MB. One annual source processed at a time. Browser processes excluded from these server RSS samples. No servers left running.

## Data

- Raw source: sibling dataset repository samples/lookups/documentation; official CPSC archived annual downloads at https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/2023/neiss2023.xlsx, corresponding 2024/2025 XLSX, and 2025/neiss2025.tsv. Only TSV used for 2025 case rows. Original bytes retained unchanged. Relevant annual NEISS_FMT comparisons passed. Browser acquisition instructions in README and missing-data page.
- Condensed files committed (name, rows, MB): data/reference/neiss_code_lookup_2025.csv, complete 1,250 rows × 4, 0.092 MB, byte-identical to dataset repo. No production cohort/provenance committed because no human review is complete. Prepared README/codebook are documentation, not findings. Candidate/review/source/quality files remain ignored local audit outputs.
- `data/raw/` deleted: no — ignored downloads and lookup-verification evidence retained locally as requested; none tracked.

## Build problems not caused by the prompt

- System `python` was absent, Python 3.14 had no pip. Used available uv to install Python 3.12 and create the local environment; student commands use a supported installed interpreter and pip.
- Initial dependency resolution selected a newer NumPy requiring Python 3.12; replaced it with a deliberately compatible locked Python 3.11–3.13 environment before final tests.
- One test expected an expanded diagnosis label, but actual complete lookup uses “53 - CONTUSIONS, ABR.” Corrected the assertion to preserve source wording.
- Cold AppTest initialization exceeded its default 3-second timeout on the shared machine. Set the test timeout to 20 seconds; normal completed UI runs remained short.
- First browser check asserted chart count before asynchronous rendering finished; changed it to wait for all charts. Subsequent browser search/reset succeeded. First cache integration test patched a different module instance; corrected the test entry to import the same module. These were harness issues, not product changes.
- The supplied lookup retains its original CRLF bytes and padded keys. Git attributes preserve it and the unchanged prompt; whitespace checks exclude the supplied prompt's existing final blank line.
- The initial pytest discovery picked a parent cache location; added repository-local pytest.ini. Scratch scripts, server logs, screenshots and clone checks are under the supplied TMPDIR.

## Coordinator

- Fresh clone starts: yes. `git -c core.symlinks=false clone` (as Windows clones) into a separate check folder, Python 3.12 venv, `pip install -r requirements.txt -r requirements-dev.txt`, 87 tests passed (12.2 s), `python -m streamlit run app.py --server.port 8600` returned HTTP 200 on `/` and health. Starting view (AppTest): title, year-2025 subtitle, sidebar year, and `Dashboard data unavailable` with browser-acquisition and human-review instructions, no numbers. That is what §06 prescribes when the reviewed artifact is missing. The app does not need the sibling dataset repo (lookup copied into `data/reference`).
- Cross-platform: there was no separate cross-platform fix session for this repo. The builder's instructions already included the macOS/Windows fresh-clone requirement, and nothing was changed for cross-platform reasons after the build. Checked on Linux with symlinks disabled (above): no symlinks tracked (`git ls-files -s | awk '$1==120000'` empty), no Linux-only modules (systemd, cgroup, /proc, fcntl, resource) imported by the app or tests, and README has macOS and Windows PowerShell venv/install/run commands, including a fallback when `Activate.ps1` is blocked. Native macOS and Windows runs were not done by the coordinator.
- Data used vs the prompt: official CPSC NEISS archived annual files, downloaded by direct URL into ignored `data/raw/` (§02 allows updating configured paths): 2023 and 2024 XLSX, 2025 TSV for case rows; the 2025 XLSX was used only to cross-check NEISS_FMT codes, so each year has one source representation. Source rows match the prompt's baselines exactly (338,262 / 361,672 / 410,201; 25 columns; Jan 1–Dec 31 each year). Candidates exported independently per year: 122 / 148 / 188, all unreviewed.
- Size notes: the only committed data file is `data/reference/neiss_code_lookup_2025.csv` (1,250 rows, 92 KB, byte-identical to the dataset repo; largest file). Pack 83 KiB. No raw, candidate, review or prepared production files are tracked. Candidate export on the 2025 TSV took 5.2 s at 0.55 GB RSS on the shared build machine.
- Build-setup notes behind entries: the dataset repo was a sibling folder of the build, so the builder copied the lookup into `data/reference` (row 2, BUILD). Committing only the files the app reads is a build-protocol rule (row 8, BUILD). Row 13 was added by the coordinator.
- Use cases re-walked: the human review gate blocks both on production data, as the prompt intends (§01 production-data gate; §06 "the launch does not bypass review"). To check the pipeline past the gate, the coordinator ran `candidates` on the official 2025 TSV in the check clone (188 candidates), filled the review CSV with crude keyword labels marked "COORDINATOR SIMULATION - not a human review", and ran `finalize`, which published 188 rows and valid provenance. These simulated files were deleted and never committed. With them, use case 1 works: 8,892 estimated visits, 188 records, 29.6% severe, all five views, Fall the largest bar, diagnosis stack with `57 - FRACTURE` (45% of severe Fall weight). Use case 2 works: Fall + Severe + `belt` gives the declared empty state 0/0/N/A with the denominator note; Fall + Severe alone gives 1,254 / 25 / 100%; a no-match search followed by Reset restores 8,892/188/29.6% with options kept. The software works for 2/2 use cases; real-data results stay blocked until a human does the review. The numbers above come from simulated labels and are not findings.
- Findings for the team to audit:
  - The app shows "Dashboard data unavailable" until the team reviews the exported candidates (122/148/188) and runs `finalize`, as the prompt designs. The final §06 step (open the real 2025 app, one filter/reset cycle) can only be done after that review.
  - The path past the gate was verified only with simulated labels that were never committed; no real review or production estimate exists yet.
  - The candidate narrative pool contains many non-injury medical events on or near a treadmill (for example chest pain, syncope); the simulated keyword pass left 81 of 188 as Unknown. Only 3 of the 188 2025 narratives mention "belt", so the use case 2 search is likely to return few or no records on real reviewed data.
  - The candidate export has no proposed-label/rule column, although §02.4 lists one (row 13).
  - `finalize` writes the absolute local source path into the provenance JSON (machine-specific).
- No raw data, secrets or identifiers; size limits met: yes. No raw/candidate/review files tracked (`data/raw/` ignored), no secrets or emails found by grep, no student identifiers. `one-shot-prompt.md` is byte-identical to the workspace copy; `change-requests.md` added unchanged.
