# MVP work report — approved implementation and Git integration

The team approved integration on main using an implementation commit followed by
a separate change-request status commit. Actual implementation commit hashes are
recorded in change-requests.md after the implementation commit exists. No public
deployment, dataset finalization, or automatic human approval occurred. The production app still
shows the correct unavailable-data state until genuine human review is complete.

## Completed

- Inspected the app, original prompt, requirements PDF, all tests and eight change
  requests. Saved an internal baseline and checked for concurrent/unrelated edits.
- Reconciled 188 unique IDs across candidates, review template and all three AI
  workbooks. Original narratives match. No out-of-codebook labels or literal
  disagreements between the original and assistant mechanism columns were found.
  Repeated labels are not independent verification; 81 assistant inclusion
  recommendations remained unresolved, plus 53 flagged likely-eligible cases.
- Created data/prepared/treadmill_2025.consolidated_review.xlsx with all 188 cases,
  source narratives, original proposals/confidence, assistant assessments/reasons,
  overlapping flags, policy questions, and blank human correction fields.
  Queue: 105 scope/inclusion questions, 29 remaining mechanism/evidence cases,
  54 straightforward cases. Original flags: 134 flagged, 54 unflagged. All
  reviewed fields remain False. No candidate label or eligibility was finalized.
- Implemented all eight change requests sequentially with focused and full tests.
- Aligned original runtime pins across pyproject.toml, uv.lock and requirements.txt;
  created .venv-mvp under Python 3.13.15 without replacing the old .venv (3.14).
- Added independent csv/Decimal arithmetic and saved fixture-only results.
- Drafted root validation.md with exactly Design, Cases, Numbers and Tests as the
  four numbered sections. Updated README and added DEPLOYMENT.md with placeholders
  and explicit human/live/real-data evidence still needed.
- Added ignore rules for review workbooks, the new environment and credentials.

## Implemented behavior and checks

| CR | Behavior | Full suite after that request |
|---|---|---:|
| CR-01 | Selected severe burden vs all-outcome baseline; baseline removes only severity, preserving mechanism/search | 93 passed |
| CR-02 | Visible selected mechanism record counts, unknown counts/weights and weighted severe share | 95 passed |
| CR-04 | Exact matching IDs and narratives after every active filter | 96 passed |
| CR-07 | Approved version-1.0 definitions and precedence next to the sidebar controls | 98 passed |
| CR-03 | All-outcome diagnosis baseline alongside the severity-filtered composition | 99 passed |
| CR-05 | Session-specific Undo reset restores all three controls | 100 passed |
| CR-06 | Selected-population unknown share and conditional S/T, (S+U)/T endpoints; empty unavailable | 102 passed |
| CR-08 | Full-precision mechanism contributions, sum/headline comparison and versioned CSV download | 104 passed |

The baseline was 90 passing tests (original 87 plus three pre-existing Ryan cases).
Added 14 change-request tests and two independent-number tests. **Final full run:
106 passed, 0 failed, 0 errors,
0 skipped, 12.434 seconds** on Windows/Python 3.13.15.
The final run includes the chart-title/readable-label polish found during browser QA.
Test results are summarized in validation/results/test_summary.json.

The CR-07 first focused run caught Streamlit trimming a Markdown boundary newline;
the assertion now compares all codebook content with only boundary whitespace
removed. A smoke-harness import-path issue was corrected before the isolated
execution check. Workbook QA caught and corrected combined-flag mapping and a
summary-formula compatibility issue before delivery. No validation gate was relaxed.

The existing five view IDs, runtime review gate, eligible cohort, primary-only
diagnoses, severe disposition codes 2/4/5/8, and selected headline formulas remain
unchanged. Explicit baselines and conditional endpoints are additional labeled
populations/calculations. The original one-shot prompt was not edited. The CR log
records all eight real requests as implemented and verified. The accidentally
modified lottery example is restored. Actual implementation hashes are recorded
in the separately committed status update; request descriptions/evidence are preserved.

## Independent numerical evidence

The default independent calculator imports no dashboard code and uses Decimal
loops over an explicitly invented CSV. Hand checks: total 120, count 5, severe
weight 50, severe share 41.666666…%; mechanism contributions 60/40/20; Fall primary
diagnoses 75% contusion/25% fracture. Filtered, empty and diagnosis-share checks
agree with the dashboard. Three 10.4 contributions explain why separately rounded
10+10+10 differs from a rounded headline of 31. No real-data estimate is claimed.

## Launch and deployment checks

An isolated copy containing only runtime modules, config, committed lookup and
codebook started from an unrelated working directory. Health and page both
returned HTTP 200; measured launch 1.768 seconds.
AppTest executed the copied app and confirmed the honest missing-reviewed-data
screen without numeric output. There was no raw dataset or review workbook in
that copy. This proves the runtime import/path boundary on Windows, not Linux
hosting or production interaction performance.

Local browser QA used an explicitly titled INVENTED FIXTURE — UI QA ONLY page;
it is not a public app or live validation screenshot. It exposed a clipped chart
title; titles now put the period on a separate line. Readable evidence labels,
sensitivity numerators/denominators and reconciliation fields were checked by
the final UI test suite. Temporary smoke servers are stopped after inspection.

Dataset Git cleanup approved: the complete standalone dataset repository was
copied to `../backups/dataset_neiss-sports-injuries-before-mvp-integration` outside the team repository. All 40
files, including nested Git metadata and the four annual downloads, were verified
by SHA-256 against their originals. Only the parent index gitlink is removed, and
the dataset directory is ignored by the parent. Original datasets and nested Git
repository remain intact. The runtime has no dependency on that directory.

## Preserved evidence and unrelated work

SHA-256 checks confirm all 17 protected files
unchanged, including the original prompt, raw annual files, candidate/review/source/
quality evidence, original review workbooks, and pre-existing check_number.py and
tests/test_ryan_module10.py. The original review CSV still contains 188 False values
and blank human decisions. The two pre-existing prepared Markdown line-ending
changes remain untouched. No raw annual data or review workbooks are tracked;
none is included in the approved commit. A targeted scan found no obvious API-key/private-key patterns in
tracked/owned text files; this is not proof of absence of every possible secret.

## Files modified in this session

- `.gitignore`
- `README.md`
- `app.py`
- `change-requests.md`
- `filters.py`
- `pyproject.toml`
- `requirements.txt`
- `tests/test_app.py`
- `uv.lock`
- `views.py`

## New reviewable project files

- `.python-version`
- `DEPLOYMENT.md`
- `codebook.py`
- `tests/test_independent_numbers.py`
- `tests/test_mvp_changes.py`
- `validation.md`
- `validation/README.md`
- `validation/fixtures/invented_visits.csv`
- `validation/independent_numbers.py`
- `validation/results/fixture_results.json`
- `validation/results/test_summary.json`
- `MVP_WORK_REPORT.md` (this report)
- `data/prepared/treadmill_2025.consolidated_review.xlsx` (local, git-ignored)

The isolated environment .venv-mvp and its downloaded dependencies are local and
ignored. Authoring scripts, snapshots, screenshots/previews and temporary tests are
under this chat's work folder, outside the application repository. Existing user
files were not moved or overwritten.

## Remaining blockers and next steps

1. Team must approve inclusion meaning for medical-only events, uncertain injury,
   mixed activities and stationary equipment/cords, then genuinely review every
   candidate. Involvement is not automatically injury eligibility or causation.
   Conditional recommendations include a dismount fall explicitly reporting no
   pain/external trauma (251223274). Resolve codebook gaps rather than invent labels.
2. Transfer verified decisions by ID into the review CSV; run finalization only
   after all human reviews are complete. This session never called production
   finalization; existing tests finalize only invented temporary fixtures.
3. Verify the final production CSV/provenance and independently recalculate real
   totals, diagnosis shares and representative filtered results. No final bundle
   currently exists.
4. Code integration is approved; the broken gitlink is removed without deleting
   local data. Release only reviewed runtime artifacts after human review. Deploy
   later to Community Cloud using Python 3.13 and locked dependencies.
5. Test Linux/cloud behavior, cold/multi-user performance and incognito access;
   compare live/local numbers and filters. Keep the app accessible through December 16.
6. Supply sourced persona/workflow research and genuine live screenshots, finish
   validation.md, export/inspect root validation.pdf, record the approximately
   five-minute demo, replace README links and inspect the submission archive.

README URLs and draft sections are intentionally pending. No final PDF, video,
production totals, stakeholder interviews or public deployment were fabricated.

## Integration verification

The original implementation-session timings above are historical. Fresh pre-commit
verification is recorded in validation/results/test_summary.json. The approved
commit excludes check_number.py, all review/audit artifacts, raw data, environments,
secrets, caches, and the two newline-only prepared Markdown changes.


## Submission preparation session - 2026-11-01

- AI-recommended v2 injury policy documented; not human-approved. 108 Include / 72 Exclude / 8 Unresolved; all 188 human review flags remain False. The single current AI workbook supersedes older suggestions; source/candidate values are preserved. Thirty-five boundary cases and all 29 prior mechanism reassessments are documented.
- Guarded post-approval workflow added: policy/source/candidate validation, separate review export, isolated existing finalizer, provenance checks, original-weight precision and independent dashboard comparison before publication. No production finalization run.
- 147 full-suite tests passed with zero failures/errors/skips on Python 3.13.15 (13.431 seconds); packages compatible and lock verified. Local Streamlit HTTP/root healthy and expected missing-data screen verified without exceptions.
- README, deployment process, independent validation guide, five-minute demo/recording plan and safe archive/checklists prepared. Root validation.pdf is a four-section evidence draft with real/public evidence explicitly pending.
- Remaining gates: genuine policy and 188-record human verification, eight indeterminate decisions and included taxonomy mappings; checked real runtime bundle; authorized safe commit/integration/public deployment; public screenshots and interpreted cases; recording and verified links; final PDF/ZIP. No public deployment, commit, push or completed video is claimed.


## Human review handoff - 2026-11-01

- The team confirmed no human-approved workbook exists yet. Policy/row approvals remain blank; production finalization and publication are blocked. No AI recommendation is relabeled as human verification.
- Added a focused Human review input tab and Review guide to the existing workbook. Eight inclusion cases and nine included mechanism mappings are first; all 188 still require actual review. All original audit/source sheets remain preserved.
- Added a reader that rejects conflicting legacy input, changed canonical AI fields and mismatched IDs; six invented-record guard tests pass. The full suite passes 153 tests with no errors/failures/skips. Dependencies, locked manifest and fixture-number checks pass. Remote main remains d63e392 with no teammate updates.
- Validation PDF remains an evidence draft: test evidence updated, real-data/public screenshots/interpretations still pending. No release ZIP, production dataset, public app, recording, commit or push was generated.

## Completion preparation - November 5, 2026

This section supersedes earlier release-readiness interpretations, not their preserved historical test results. Current state: 171 assistant-transcribed approval entries (99 Include / 72 Exclude), 17 blank priority decisions, and AI proposals 108 Include / 72 Exclude / 8 Unresolved. Informed human review cannot be established for any of the 171 from the blanket endorsement and copied AI rationale; 59 have adjudication flags. Saved entries are preserved, not revoked or treated as independently verified. Policy document status and chat acceptance need explicit team reconciliation.

Fresh suite initially passed 155 tests, including Colby's two committed properties. Added six prepared-file publication tests and two approval-provenance reporting tests; the complete run passed 163 with zero failures/errors/skips on Python 3.13.15. No runtime code, dependency, CR description/status, one-shot prompt, source/candidate/review value, policy fingerprint or approval field changed. Existing uncommitted work and HW11 artifacts were backed up before edits and preserved. The dedicated dataset backup and original annual files still exist with matching hashes.

The unchanged validation-only finalizer rejected the first missing approval and wrote nothing. Independent fixture arithmetic/dashboard/export checks passed; no real-data findings were substituted. Isolated runtime AppTest and HTTP checks passed in the honest missing-data state. Browser access was retried and remains unavailable. No public URL, live screenshots, final real-data cohort or completed HW11/video is claimed.

Public preparation documents now distinguish row completeness from genuine human review, integrate Ryan's preserved HW11 case into validation, strengthen alternatives/decision limitations, and provide an exact recording sequence and dependency-ordered checklist. Root validation.pdf is visibly an evidence draft. submission/READINESS.md records all ten rubric gates. No final submission ZIP is warranted while the review, public evidence and video remain pending. Safe preparation work may be committed/pushed under the user's current instruction; inspect the recorded Git results rather than interpreting older no-commit session notes as the latest state.

## Version 1.1 migration and explicit adjudication - November 5

Recorded Ryan's stated eight inclusion decisions and supported conditional mappings separately from AI proposals. Original 171 human rows and all source/AI values are preserved. All 188 narratives were independently read against revised rules; no definite additional prior-label change was identified. Inclusion decisions: 109 Include / 79 Exclude. Complete review entries: 184; four mappings held for missing use context. No production finalization was run. Versioned codebook preparation/transfer/loading/sidebar and exact codebook fingerprint checks are implemented; archive 1.0 and private pre-edit evidence are preserved. No original prompt or policy bytes changed. Offline narration/FFmpeg work; browser/public recording remains unavailable. New tests protect the taxonomy and video input/evidence gates; fresh results are in validation/results/test_summary.json.
