# Deploy the reviewed Streamlit app

Production data and local validation are complete: 109 retained records, 5119.6280 weighted ED visits, 22.302804% severe, codebook 1.2. No public deployment is claimed. Browser inventory reports the browser access host unavailable; hosting-plugin discovery returned administrator-disabled integrations. No documented supported Community Cloud deployment CLI/API was found. GitHub authentication does not confer Streamlit login.

## Minimal account action

Open https://share.streamlit.io and sign in with the authorized GitHub account. Select Create app > Yup, I have an app > repository ryanyu808/project > branch main > main file app.py. Under Advanced settings select **Python 3.13**, then Deploy. No secrets are needed. Set Sharing to public; keep the GitHub repository private if desired. Copy the actual deployed URL. Recheck current [official deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies) and [sharing](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app) instructions. Community Cloud prioritizes uv.lock here; runtime pins also match requirements.txt/pyproject.toml.

## Runtime manifest

app.py, configuration.py, contracts.py, loader.py, filters.py, views.py, codebook.py, config.toml, requirements.txt, pyproject.toml, uv.lock, .python-version, data/prepared/mechanism-codebook.md, data/reference/neiss_code_lookup_2025.csv and the final treadmill_2025.csv / treadmill_2025.provenance.json. Python 3.13, no packages.txt, databases or API keys. Paths resolve against the code location; no Windows absolute path is required. Git -text attributes preserve hashed CSV/provenance/codebook bytes on Linux. The GitHub Ubuntu workflow tests the committed runtime; its actual outcome is recorded separately.

## Verify before claiming completion

Open the actual URL signed out/incognito and on a second device. Inspect cloud logs/cold start. Initial headlines must be **5,120 / 109 / 22.3%** with all controls clear, matching prepared SHA c97b9ef421000d5a6e476a5e1598e16d6c8fde9ad20b5cd32d83c626480e985f. Fall alone: **3,114 / 65 / 28.3%**. Fall + Severe: 18 records / 882.6389 weight, selected 100%, all-outcome baseline 28.340164%. Fall + Severe + belt: zero / zero / N/A. All-cohort belt: 3 records / 123.7879 weight / 0% severe. Literal searches are case-insensitive, trimmed and not regex. Test Reset, Undo, no-match, codebook, all charts, visible supporting evidence, diagnoses and unknown sensitivity. There are zero unknown outcomes in this release; both endpoints equal observed severe share. Do not infer certainty from missingness being zero.

Download the actual public full-precision CSV and compare contributions/selected total, filters, period and hash with validation/results/real_2025_dashboard_check.json. Capture genuine public screenshots with controls visible for all-cohort comparison, Fall diagnoses/sensitivity, severe baselines, empty belt subset and reconciliation. Record URL, UTC capture time, selections and data hash in an evidence manifest. Local AppTest and CI are not public/incognito/visual evidence. Do not expose private workbooks, reviews, credentials or account settings on screen.

Then update README links and live case/validation evidence, render and inspect both PDFs, record genuine public footage with the prepared narration, verify the complete MP4 and publish Unlisted. Keep the app available through December 16 and confirm the Brightspace deadline. Run submission/check_release.py before a git archive ZIP; no incomplete archive is submission-ready.
