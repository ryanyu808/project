# Framework deployment before production data

The existing app can start without the production CSV/provenance. It intentionally displays `Dashboard data unavailable`, with no injury metrics or charts. This is an honest framework/status deployment, not a functioning real-data MVP and not HW11 screenshot evidence. No synthetic dataset or review bypass is needed. Adding the genuine finalized runtime pair at the configured paths later enables the existing dashboard; the loader's checks remain unchanged.

## Host setup

Use Streamlit Community Cloud, repository `ryanyu808/project`, branch `main`, entrypoint `app.py`, Python **3.13**, no secrets. The repository is private; the authorized GitHub account has admin access. Keep the repository private. Only the app should be public. The runtime files are already tracked on main; no private review workbook, candidates or raw dataset is required by the app.

Official instructions: [Deploy](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies). Current documentation prioritizes `uv.lock` over `requirements.txt` in the same directory. Both exist; select Python 3.13 explicitly and inspect the host installation logs. Do not remove the lockfile merely to change the installer. No external apt packages are required by the inspected runtime imports.

1. At https://share.streamlit.io choose Create app, existing app, and the repository/branch/entrypoint above. Set Python 3.13 in Advanced settings and deploy.
2. Set app visibility to public; verify signed-out access. Expect the unavailable-data screen, not zeros or injury results. Record the actual URL only after opening it. A hosting health check alone does not establish valid data or complete functionality.
3. After genuine review, use the unchanged finalization workflow in `review_tools/README.md`. Publish only the matching `data/prepared/treadmill_2025.csv` and `.provenance.json` after all checks pass. Preserve review inputs and private outputs locally. Inspect the staged paths; never use `git add .` for this release.
4. Recheck the public dashboard against independent real-data results, including filters, severity baselines, diagnosis, narratives, unknown sensitivity and CSV precision. Capture live evidence, then finish cases, demo and validation.

## This session's blocker

Browser inventory returned `The browser access host is unavailable`. Discovered hosting integrations were disabled by the administrator; no accessible Streamlit host management session exists here. GitHub authentication works, but GitHub repository access alone cannot create a Community Cloud application. No deployment URL has been obtained and no hosting deployment is claimed. Reconnect browser access or perform the host setup above; the data review can proceed independently.

## Current data review

Use `review_tools/review_readiness.py` for a read-only entry/provenance audit. It reports 171 structurally populated approvals and 17 pending cases. All 171 were assistant-transcribed after blanket endorsement; informed per-case human review cannot be established, and 59 have unresolved adjudication provenance. Preserve the entries and verify the real review basis. The policy approval cells likewise record chat acceptance, not independent evidence of deliberation. The complete data gate is not satisfied by finishing only the 17 blanks.
All 17 remaining cases must receive truthful decisions. Eight Unresolved recommendations require explicit Correct and Include/Exclude; the other nine included taxonomy mappings require a defensible resolution or correction. If the existing taxonomy cannot describe an event, resolve the policy/codebook contract deliberately rather than relabeling a known event Unknown to pass validation. A changed policy/codebook may require renewed approval and compatible workflow changes; a free-text note cannot repair an incompatible definition.
