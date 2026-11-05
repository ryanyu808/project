# Deployment checks - November 5, 2026

**Earlier-session log, preserved.** The later completion recheck in submission/READINESS.md supersedes the finish checklist below: 163 tests now pass, and all 171 assistant-transcribed approval entries have unestablished informed-review provenance. Finishing only the 17 blank cases is not a complete human gate. No recorded entry was changed or revoked.

Public deployment: **not performed; no URL**. Genuine finalized dataset: **absent**. Framework publication is independent of human data approval, but the existing no-data state does not satisfy functional MVP/HW11 evidence requirements.

## Commands and observed results

Executed from the project root:

```text
git pull
Already up to date.

.venv-mvp\Scripts\python.exe -m pytest -q -p no:cacheprovider
155 passed in 72.13s

uv pip check --python .venv-mvp/Scripts/python.exe
All installed packages are compatible

.venv-mvp\Scripts\python.exe review_tools/review_readiness.py
total: 188; entries_passing_row_checks: 171; pending: 17
policy_approval_recorded: true; policy_mapping_acceptance_recorded: true
```

The validation-only finalizer command documented in `review_tools/README.md` returned exit 2: `Review/finalization rejected: 250168690: missing approval or deferred case`. No --execute was used, no validator was modified and no production files were created.

GitHub CLI confirmed repository admin access for the existing authenticated account, private repository, default branch main. No GitHub deployment entries were returned. Browser inventory reported `The browser access host is unavailable`. Hosting integration discovery returned administrator-disabled providers; no usable Streamlit deployment control was found.

## Framework isolation and dependencies

Created `../output/deployment-framework-2026-11-05/framework-source.zip` from an explicit 14-path runtime allowlist at committed revision `4d4c213eeb9f93ee4681419b617d9201e70fa9bc`. The adjacent manifest records every packaged file's SHA-256. The package excludes reviews, raw data, candidates, workbooks, fixtures, personal case drafts and credentials. No runtime code changes were necessary.

Extracted the package into a temporary directory and ran a fresh subprocess with that directory as cwd:

- Streamlit AppTest: PASS, no exceptions, no metrics/charts, expected `Dashboard data unavailable` message.
- Started the actual Streamlit server on loopback in the temporary directory; `/_stcore/health` returned `200 ok`.
- Stopped the temporary server and verified process exit.

`uv export --locked --no-hashes --no-dev --no-emit-project` matched the runtime pins in requirements.txt. `uv pip compile requirements.txt --python-platform x86_64-unknown-linux-gnu --python-version 3.13 --no-deps --no-header --output-file ../output/deployment-framework-2026-11-05/linux-requirements-check.txt` resolved all 40 pinned packages. This checks target-platform pin resolution, not a Linux installation/build or native cloud run. Community Cloud documentation says uv.lock takes priority here; Python 3.13 must be selected explicitly.

## Preservation and scope

The annual XLSX SHA-256 matched the original source JSON. Hash snapshots of the source, existing prepared workbooks, candidates, blank review template, source/quality evidence and policy document remained unchanged after checks. The local hash file stays outside the deployment ZIP. The new pending-case report is ignored by git and contains original narrative evidence for human review; it is not for publication.

New reusable audit: `review_tools/review_readiness.py`. New deployment handoff and this log are in `deployment/`. Updated README/DEPLOYMENT/review workflow prose to distinguish framework deployment from data release and reflect the existing recorded approvals. No application code, data, approvals, validators or original evidence were changed. No commits or pushes were made during this session.

## Finish in this order

1. Create the framework app through the host setup in FRAMEWORK_HANDOFF.md (or restore browser access so this can be done here); verify the actual public URL while signed out.
2. Human completes only the 17 pending cases in workbook Human review rows 2-18, resolving inclusion and taxonomy truthfully. Existing policy acceptance must remain accurate; any incompatible policy/codebook change needs deliberate renewed approval.
3. Run unchanged validation-only finalizer; after success, repeat with --execute. Run independent real-data checks. Inspect and publish only safe release files, including the matching finalized runtime pair; never commit private review artifacts.
4. Verify real results publicly, capture live screenshots with selections, and finish individual interpretations/verdicts and PDFs.
5. Complete team validation with genuine cases/numbers/tests, public README and demo links, and the demo video; inspect the final PDF and clean submission package against mvp.md before submission. Keep the public app available for the course's required period.
