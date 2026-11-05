# Final submission gates

Current status: NOT SUBMISSION-READY. See [READINESS.md](READINESS.md) for the current verified results and ordered handoff. Code and fixture evidence are prepared; actual policy/record approvals, final real-data validation, public access and video remain pending. One teammate submits for the team before Quiz 11; confirm the calendar date. The assignment limit is 2 GB and the app must stay available through December 16.

- [ ] Establish informed per-case human review for all 171 assistant-transcribed approvals; populated cells and AI-copied reasons alone cannot establish it. Reconcile and actually approve the injury-focused policy or explicitly revise it; preserve the unchanged one-shot prompt as the original contract.
- [ ] Resolve eight indeterminate inclusion cases and the codebook mapping gaps; genuinely review all 188 records and enter actual human attestations.
- [ ] Run the validate-only workflow, then --execute only after it succeeds. Keep review/audit files local.
- [ ] Inspect the final small CSV/provenance and independent real-data dashboard check. No unexplained differences, rounded data substitutions or AI labels passed as human decisions.
- [ ] Review safe code, tests, docs and runtime artifacts with teammates. Inspect Git diff, ignored files and the staged diff. Never use git add . indiscriminately.
- [ ] Commit/push the verified safe work and approved small runtime pair. Never commit raw annual files, candidate/review CSVs, review workbooks, audit reports, secrets, environments or caches.
- [ ] Deploy the actual release, run DEPLOYMENT.md checklist including incognito access and record cohort fingerprint/screenshots.
- [ ] Replace README public app and video placeholders with verified links. Record the five-minute demo; test it without login.
- [ ] Complete the pending evidence in validation.md and regenerate root validation.pdf. Verify exactly 1. Design, 2. Cases, 3. Numbers, 4. Tests after the introduction. The current PDF is an accurately labeled evidence draft, not final validation.
- [ ] Re-run all tests and independent calculations on the final release; own the definitions and interpretations as a team.

## Build and inspect the required repository ZIP

First ensure every teammate's safe work is committed and pushed. With a clean tracked working tree, fetch and integrate teammate work safely; stop on conflicts. The assignment's git archive method includes only committed HEAD files, so an uncommitted validation.pdf or runtime pair would be omitted.

```powershell
git pull --ff-only
uv run --locked python submission/check_release.py
uv run --locked python submission/check_release.py --create-zip team-repo.zip
```

The helper audits committed paths, required runtime files, pending README links, candidate secret patterns, file limits and dirty tracked files before creating an archive. It refuses an existing ZIP and prints the full entry list after creation. It does not commit/push or infer human review. Inspect flagged paths without printing secret values; a pattern scan is not proof of absence of secrets.

Equivalent assignment command after all gates pass: `git archive --format=zip -o team-repo.zip HEAD`. Inspect every entry and confirm no .venv/.venv-mvp, caches, raw downloads, nested dataset repository, reviews/workbooks, secrets or private audit files. Confirm README.md and validation.pdf are at the ZIP root, links work signed out, the final small processed pair is present and the archive is below 2 GB. Upload exactly that ZIP to Brightspace. No submission archive was created in this session because the gates remain open.
