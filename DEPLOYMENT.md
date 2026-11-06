# Reviewed public Streamlit release

**Verified app:** [https://treadmill-injury-dashboard.streamlit.app/](https://treadmill-injury-dashboard.streamlit.app/). The user deployed main/app.py. The assistant independently opened the running public dashboard in a separate browser session without signing in; all six observed mechanisms and all severity states, literal search, empty results, Reset/Undo, definitions, baselines, sensitivity and full-precision export passed. This is direct interactive evidence, not an HTTP-shell or CI inference. No cloud Python-settings screenshot or second physical device test is claimed.

Initial headlines 5,120 / 109 / 22.3%; Fall 3,114 / 65 / 28.3%; Fall + Severe 883 / 18 / 100%, with all-outcome baseline 28.340164%; Fall + Severe + belt 0 / 0 / N/A. All-cohort belt three nonsevere records / 123.7879. Visible prepared SHA c97b9ef421000d5a6e476a5e1598e16d6c8fde9ad20b5cd32d83c626480e985f. The actual public download reconciles all weights/metadata (maximum floating-point difference 1E-12). Captures and machine-readable evidence: validation/results/public_dashboard_verification.json and public_export_check.json.

## Runtime manifest

app.py, configuration.py, contracts.py, loader.py, filters.py, views.py, codebook.py, config.toml, requirements.txt, pyproject.toml, uv.lock, .python-version, data/prepared/mechanism-codebook.md, data/reference/neiss_code_lookup_2025.csv and the final treadmill_2025.csv / treadmill_2025.provenance.json. Python 3.13, no packages.txt, databases or API keys. Paths resolve against the code location; no Windows absolute path is required. Git -text attributes preserve hashed CSV/provenance/codebook bytes on Linux. The GitHub Ubuntu workflow tests the committed runtime; its actual outcome is recorded separately.

## Maintenance and remaining release gates

Keep the app available through December 16. Wake/test it before grading; an observed working session does not guarantee future uptime. Check hosting logs if a cold start fails. Never expose private source/review workbooks or substitute fixture data. If redeploying, use ryanyu808/project, main, app.py, Python 3.13, public sharing and no secrets.

The genuine public footage and 300-second AI narration have been combined and encoded outside the repository. The [Unlisted demonstration](https://www.youtube.com/watch?v=f45CShykzbI) has verified playback in a separate browser session without signing in. Obtain the team's legitimate distinct cases before final ZIP creation. PDFs contain authentic live evidence; Ryan's break verdict is accepted, CR-09 remains open. Read submission/READINESS.md. Do not equate release-audit PASS with completed case coverage.
