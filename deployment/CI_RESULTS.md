# Current verified release checks - November 6, 2026

The [public-evidence release CI run](https://github.com/ryanyu808/project/actions/runs/42185083554) passed all180 tests in11.09 seconds on Ubuntu/Python3.13.18, plus dependency checks, actual independent production arithmetic, dashboard filters/baselines/export, configured production AppTest and real Streamlit HTTP health. Committed revision05421e637527e91a3661c7cd6d88bb945e25249f. See ../validation/results/live_linux_release.json. The post-public-evidence Windows suite also passed180 in16.57 seconds with zero failures/errors/skips.

Public app controls, genuine screenshots and actual CSV are now separately verified in ../validation/results/public_dashboard_verification.json. Unlisted video access and1920x1080 playback without signing in are separately verified in ../validation/results/youtube_verification.json. Neither claim is inferred from CI. Historical CI findings below remain preserved.

---

# Actual Linux production verification

**PASS** on [GitHub Actions run 42125610831](https://github.com/ryanyu808/project/actions/runs/42125610831), committed revision cd7bf8311e854a40f52af486e810cb0eeeb9b3e1. Completed November 5, 2026 at 22:57:05 UTC. GitHub-hosted ubuntu-latest, Python 3.13.18, exact committed runtime/source files.

- Complete automated suite: **180 passed, 0 failures, 0 errors, 0 skipped**, pytest 12.00 seconds.
- Installed pinned requirements-dev dependencies and pip check: PASS, no broken requirements.
- Independent actual production csv/Decimal arithmetic: PASS.
- Real dashboard/filter/baseline/diagnosis/unknown/sensitivity/full-precision CSV comparison: PASS.
- Actual configured production AppTest with no fixture injection: PASS.
- Actual Streamlit server on Linux: HTTP health returns ok, root request succeeds; server stopped afterward.
- Matching hashed CSV/provenance/codebook loaded successfully on Linux, preserving Windows-produced bytes.

The [first run](https://github.com/ryanyu808/project/actions/runs/42124995826) had179 passed / 1 failed: the invented end-to-end workflow fixture generated its codebook with native Linux newlines while the loader checked the exact canonical committed bytes. Copying the canonical bytes fixed the fixture. No production file, fingerprint rule, guard or assertion was weakened. The full Windows suite also passed again afterward (180; Python 3.13.15).

This is genuine Linux CI/runtime evidence, not a public hosted app or signed-out browser/screenshot test. Actual hosting, visible plots/controls, public export and incognito access still require DEPLOYMENT.md. Summary: ../validation/results/linux_production_check.json.
