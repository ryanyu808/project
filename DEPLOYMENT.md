# Deployment readiness

Not deployed. Real-data release is blocked by human policy/record approvals. The tested local server starts and correctly displays the missing-data state. This is not a working real-data public MVP yet. Do not publish fixtures as real NEISS data.

## Reproducible environment

Use Python 3.13, tested locally on 3.13.15. `uv sync --locked --python 3.13` reproduces the lock; the root requirements.txt also pins the runtime packages. `uv pip check --python .venv-mvp/Scripts/python.exe` and an offline locked-manifest check passed. Streamlit 1.45.1, pandas 2.2.3, NumPy 2.2.6, Plotly 6.0.1 and openpyxl 3.1.5 remain the runtime versions. No runtime package changes were made. Native Linux/cloud execution is not yet verified.

## Runtime manifest

- Root Python files: app.py, configuration.py, contracts.py, loader.py, filters.py, views.py, codebook.py.
- Root configuration/dependencies: config.toml, .python-version, pyproject.toml, uv.lock, requirements.txt.
- Final, genuinely reviewed `data/prepared/treadmill_2025.csv` and matching `.provenance.json` (PENDING).
- `data/prepared/mechanism-codebook.md` and `data/reference/neiss_code_lookup_2025.csv`.

The app reads no dataset repository, raw annual file, review workbook or candidate/review CSV at runtime. It requires no secrets. Publish the small final runtime pair only after source/review/provenance and independent checks succeed. The checked workflow preserves raw fingerprints and publishes only a source filename, not the preparer's personal directory. Keep all review/audit files private.

## Framework-first option

The already committed framework can be hosted now with its honest unavailable-data screen, then enabled by adding the genuinely finalized CSV/provenance later. This is not a completed real-data MVP or HW11 evidence. See [the exact host handoff](deployment/FRAMEWORK_HANDOFF.md). Browser-host access is currently unavailable in this session; no deployment is claimed.

## Community Cloud setup after data approval

1. Complete the human-review workflow in review_tools/README.md. Verify the real 2025 pair locally and run validation/verify_dashboard.py. Keep the resulting aggregate report as evidence.
2. Review the safe code/docs/runtime diff with teammates, commit and push only the approved release files. Only verified, non-sensitive preparation work may be committed and pushed; no production release is claimed while the data gate is open. Confirm the GitHub revision contains every runtime manifest file and no private artifacts.
3. In Streamlit Community Cloud select Create app, the team GitHub repository, the approved branch and `app.py`. Under Advanced settings select Python 3.13. Do not use an automatically newer Python version. Deploy and inspect installation/startup logs. Follow the current [deployment instructions](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) and [dependency instructions](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies); inspect the actual host build rather than assuming a dependency-file priority.
4. Set app Sharing to public and test access while signed out in a fresh incognito session. The [sharing instructions](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app) explain this setting. No account login may be required of viewers.
5. Execute the checklist below, record screenshots and the cohort hash, and replace the README URL placeholder only with the verified actual public URL. Keep the app available through December 16 as required by 03-mvp.pdf; confirm the submission deadline in the course calendar before Quiz 11.

## Deployment verification checklist

- [ ] Incognito and a second device open the actual URL without authentication.
- [ ] Cloud logs show compatible pinned dependencies and no traceback; cold start succeeds.
- [ ] Initial 2025 totals match the independent real-data report and same prepared SHA-256.
- [ ] All five views render. Mechanism, severity and literal search combinations agree on membership.
- [ ] Severity and diagnosis baselines remove severity only, retaining mechanism/search.
- [ ] Search displays the matching case IDs/narratives; clear, whitespace, case and literal metacharacters work.
- [ ] No-match selection gives an honest empty state and unavailable percentages.
- [ ] Reset and Undo restore all controls; separate browser sessions do not leak state.
- [ ] Record counts, unknown-outcome counts/weights and sensitivity endpoints match independently.
- [ ] Codebook definitions are accessible. No hidden causal/precision/risk claim is implied.
- [ ] Downloaded CSV retains precision and correct filters, period and data-version metadata.
- [ ] Missing/corrupt bundle behavior is checked in an isolated test copy or existing automated tests, without damaging live data.
- [ ] No raw annual data, candidate/review CSV, review workbook, .env or secrets is in the deployed revision.
- [ ] Capture initial, filtered/baseline, diagnosis, narratives, sensitivity and reconciliation screens with filters visible.
- [ ] Record actual values, limitations and decision interpretation in validation.md, regenerate validation.pdf, and check readability.

The local health and AppTest checks do not replace public/incognito/Linux verification. Streamlit credentials and the release-data gate remain external prerequisites; nothing was publicly deployed in this session.

## Completion recheck, November 5

Fresh full suite: 163 passed, no failures/errors/skips on Windows/Python 3.13.15. Runtime pins match a fresh locked export; all 45 installed packages are compatible. An isolated copy of only the 14 runtime files started from an unrelated working directory: AppTest had no exceptions and showed no metrics/charts; actual HTTP health and root returned 200. The server was stopped. This is the honest unavailable-data application, not real-data validation. No application runtime code or dependencies changed.

Browser inventory was retried and again returned `The browser access host is unavailable`. GitHub admin access works, but no authenticated Streamlit interface is available here. No public URL, incognito test or live screenshot is claimed. Use the exact Create app steps above; current official docs say uv.lock takes priority over requirements.txt at the same location. Keep both project manifests and explicitly select Python 3.13. The app requires no secrets or packages.txt.

Do not release data solely because 171 saved entries pass row checks. Their case-level human review basis is unestablished; see review_tools/README.md. The remaining 17 cases also require real decisions. Framework deployment can proceed independently with the honest missing-data screen, but it cannot supply rubric/HW11 evidence for the real-data app.
