# Deployment readiness — not yet deployed

The production data gate remains closed. All 188 candidate reviews are pending;
there is no final 2025 CSV/provenance pair. Deploying this checkout now would show
the honest unavailable-data screen, not a completed real-data MVP.

## Tested environment

Use Python 3.13 (tested on 3.13.15). The supported declared range is 3.11–3.13;
native testing in this session was Windows/Python 3.13 only. The existing .venv
using Python 3.14 was preserved. This session used .venv-mvp with uv sync and
the runtime versions already pinned in requirements.in: Streamlit 1.45.1,
pandas 2.2.3, NumPy 2.2.6, Plotly 6.0.1, openpyxl 3.1.5. Pytest is 9.1.1.
pyproject.toml, uv.lock and the exported requirements.txt now agree on these
runtime pins. Transitive versions are fixed by uv.lock and the exported file.

PowerShell, from the application root:

```powershell
$env:UV_PROJECT_ENVIRONMENT = '.venv-mvp'
uv sync --locked --python 3.13
uv run --locked python -m pytest -q -p no:cacheprovider
uv run --locked python -m streamlit run app.py
```

macOS/Linux, from the application root:

```bash
export UV_PROJECT_ENVIRONMENT=.venv-mvp
uv sync --locked --python 3.13
uv run --locked python -m pytest -q -p no:cacheprovider
uv run --locked python -m streamlit run app.py
```

For a clean clone without an existing environment, omit the environment override
to use uv's default .venv. .python-version selects 3.13. If package declarations
change, run uv lock, uv sync, then `uv export --no-hashes --no-dev
--no-emit-project -o requirements.txt` as one command line and recheck tests.

## Release steps requiring genuine review and later authorization

1. Approve and document medical-only, uncertain injury, incidental exposure and
   stationary-equipment policies. The consolidated workbook is a suggestion aid.
   A human must inspect all 188 narratives, resolve decisions, and transfer them
   by case ID to the review CSV. Do not automatically accept AI suggestions.
2. Only after genuine review, run the documented offline finalizer. Check quality
   reconciliation, retained/excluded counts, SHA-256, and the final loader.
3. Independently recalculate real-cohort numbers using validation/independent_numbers.py;
   compare against local app outputs for initial, Fall, Severe, literal search,
   empty and Reset/Undo cases. No real-data totals have yet been validated.
4. Include only small, final runtime artifacts: data/prepared/treadmill_2025.csv,
   its matching provenance JSON, data/reference/neiss_code_lookup_2025.csv, and
   data/prepared/mechanism-codebook.md. Review provenance paths for local personal
   directory disclosure; filenames identify evidence and are not opened at runtime.
   Do not rewrite audit provenance without an agreed reproducible approach.
5. Review/commit/push code and approved runtime artifacts only when authorized.
   Raw files, candidate/review CSVs, review workbooks, credentials, and environments
   are ignored. Never upload the nested dataset repo's annual downloads.
6. In Streamlit Community Cloud choose the team repo, approved branch and root
   app.py. Choose Python 3.13 under Advanced settings. No secrets or database are
   required by this app. Community Cloud prefers uv.lock over requirements.txt;
   both must stay consistent. See [dependency documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).
7. Make the app public under Sharing. Verify in an incognito window without a
   sign-in. See [sharing documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app).
8. Match live/local numbers and filters, empty states, Reset/Undo, downloads,
   missing-data failures, cold startup and independent sessions. Check host logs
   and practical response time with several users; no Linux-host load test has
   occurred yet. Keep it available through December 16 per the assignment.
9. Capture screenshots from the live app with selections visible. Finish the
   four validation sections, export root validation.pdf and inspect readability.
   Record an approximately five-minute analyst-oriented demo; publish its link
   so viewers need no login. Replace both README link placeholders.
10. Once all required work is committed, inspect a repository archive for .venv,
    caches, raw data, review workbooks and secrets before submission. No public deployment or submission archive was created. Git integration is
    recorded separately in change-requests.md and MVP_WORK_REPORT.md. Confirm the deadline in
    the course calendar before Quiz 11.

## Runtime portability

Configuration paths are relative to app.py and use forward slashes. The loader
reads only prepared CSV/provenance and the copied complete reference. The sidebar
reads the committed codebook. There is no runtime dependency on annual files,
the nested dataset repository, the AI review workbooks, or this chat workspace.
Native Linux deployment remains to be verified on the host.


## Dataset Git reference cleanup

The team approved removing the malformed parent gitlink and ignoring
`/dataset_neiss-sports-injuries/`. Its full standalone repository was backed up at
`C:\Users\ryany\dso576\backups\dataset_neiss-sports-injuries-before-mvp-integration` and verified against the originals with SHA-256. Only the parent
index entry is removed; no local dataset or nested Git metadata is deleted or
modified. The app uses committed runtime artifacts and does not need this folder.
