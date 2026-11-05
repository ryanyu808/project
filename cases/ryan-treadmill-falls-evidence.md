# Ryan's HW11 evidence and completion review

Checked November 5, 2026. This is supporting research, not Ryan's final judgment. Application findings describe the current local working tree, which includes pre-existing uncommitted work; they are not all verified against the pushed release.

## Sources read and claim checks

All three pages opened successfully and were freely readable. Publisher: U.S. Consumer Product Safety Commission (CPSC).

- **S1: [NEISS Frequently Asked Questions](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Neiss-Frequently-Asked-Questions).** Supports ED surveillance, screening for emerging hazards, priorities informed by multiple CPSC sources, and telephone/on-site follow-back. Exact supporting excerpt: "screening the data for a potential emerging hazard." It does not specify a numeric rule for prioritizing treadmill mechanisms. Alex and the proposed workflow are fictional.
- **S2: [Explanation Of NEISS Estimates Obtained Through The CPSC Website](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Explanation-Of-NEISS-Estimates-Obtained-Through-The-CPSC-Website).** Supports probability-sample estimates, unequal case weights, sample-design uncertainty and stability criteria. Exact excerpt: "Each case is assigned a weight, which is used to compute the estimate." CPSC flags estimates below 1,200, fewer than 20 cases, or CV above 33% as unstable. These are criteria for national estimates, not a significance test for a mechanism's severe percentage. No actual case estimate has been checked against them.
- **S3: [Instructions for Using the NEISS Estimates Query Builder](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Instructions-for-Using-the-NEISS-Estimates-Query-Builder).** Supports an alternative with date/product/age/disposition filters, downloadable records and optional uncertainty outputs. Exact excerpt: "include the coefficient of variation (CV), 95 percent confidence interval, or the raw number of NEISS cases". Consult the coding manual/comparability table before choosing products. A broad official product query would not automatically reproduce our narrative-screened, manually classified cohort.

## Code evidence: what Alex would actually use

Paths below are relative to the team repository.

| Feature | Exact implementation and meaning |
|---|---|
| Mechanism comparisons | `views.py:build_view_data`, `render_mechanism_bar`, `render_severity_scatter`; groups by `injury_mechanism`. No severity restriction: scatter x is total mechanism weight; y is recorded severe weight / all mechanism weight. |
| Weighted ED visits | `total = float(frame.Weight.sum())`; mechanism totals use grouped sums. Estimated visits in the retained cohort, not people or user exposure. |
| Severe percentage | `contracts.py:SEVERE = {2,4,5,8}`; `100*severe/total`. Unknowns remain in total weight when selected. This is an app-defined disposition composite, not a clinical injury severity score or all eventual deaths. |
| Supporting records | `record_count=len(frame)` and grouped size; `build_supporting_evidence` adds unknown count/weight. Counts reveal evidence volume, not survey precision. |
| Diagnosis | Uses `Diagnosis`, not `Diagnosis_2`; groups weight by primary diagnosis and divides by total mechanism weight. Missing/unmapped diagnoses remain buckets. Not the percentage with any occurrence of a diagnosis. |
| Narrative evidence | `filters.py:apply_filters` uses stripped, case-insensitive `str.contains(..., regex=False)` on `Narrative_1`. `app.py` displays matching IDs/narratives only when the search is nonblank. A search for `fall` is a text subset, not a classifier for all fall events. |
| Severity-filter baseline | `filters.without_severity` preserves mechanism/search. With severity active, scatter x becomes selected severe weight and y becomes all-outcome baseline severe percentage. `app.py` also shows a baseline diagnosis chart and comparison table. |
| Unknown sensitivity | `build_outcome_completeness`: U/T; lower S/T; upper (S+U)/T, multiplied by 100. Conditional missing-outcome endpoints, not confidence intervals; compute separately for Fall and each comparator with severity unrestricted. |
| Reconciliation | `build_weight_reconciliation` sums unrounded contributions and exports filters, period and data hash. Rounded displays need not add exactly. |

`config.toml` fixes 2025. `contracts.py:validate_visits(cohort=True)` requires ages 65-120, product 3277 in any product field, literal treadmill mention, matching year and valid reviewed labels. `loader.py` requires matching provenance, review completeness and hashes. These are software checks, not proof that human review was substantively correct.

`data/prepared/mechanism-codebook.md` version 1.0 assigns the earliest initiating mechanism, with precedence. Entering/exiting and belt-initiated falls can be outside `Fall`. Unknown/Unclassified is reviewed ambiguity, not missing review. The injury-focused policy in `data/prepared/final_policy_recommendation.md` remains a recommendation requiring human ownership. Eligibility and taxonomy acceptance are unresolved; no final retained cohort or real injury ranking is asserted.

## Checks actually run

`git pull` returned a fast-forward from `d63e392` to `80e3468`; only a teammate's test file arrived. `git ls-files '*case*'` returned no earlier tracked claims; no `cases/` directory existed before this claim. This does not establish whether teammates have an unrecorded agreement.

`git diff --cached --stat` before commit showed only `cases/ryan-treadmill-falls.md`, 148 insertions. Commit `4d4c213` and `git push` succeeded (`80e3468..4d4c213 main -> main`). Subsequent research edits to the working claim and all other case artifacts are deliberately uncommitted.

From the team root, ran:

```text
.venv-mvp\Scripts\python.exe validation/run_fixture_checks.py --output cases/ryan-treadmill-falls-fixture-check.json
PASS: invented-fixture dashboard checks saved to cases\ryan-treadmill-falls-fixture-check.json
```

The saved report checks actual builders/filters against independent csv/Decimal calculations, including baselines, diagnosis, unknowns and CSV exports. It reports status PASS and source_scope test_fixture. It validates arithmetic on invented records only. No real-data findings, significance tests, public UI verification or full-suite rerun are claimed.

`Test-Path` for both configured runtime files returned `False`. README: public URL pending; DEPLOYMENT: not deployed. No actual public URL was found to test. No local app was started and no substitute screenshots were made.

## Candidate interpretation issues (not Ryan's answers)

1. **One row per what?** A visit, not a unique older adult. Repeated visits cannot establish the number of different people injured.
2. **Which rows belong?** ED-only surveillance plus the stricter age/product/text/review cohort excludes other care settings and ambiguous or omitted treadmill mentions. The retained group is not every treadmill injury.
3. **The real thing, or a stand-in?** Disposition severity and the `Fall` category are proxies for consequential fall hazards. An investigation priority also depends on preventability and the unanswered question an investigation could resolve.
4. **A total, or a rate?** A higher visit estimate means greater estimated retained ED burden, not greater injury probability per treadmill user/hour. Exposure data would be required for that rate.
5. **Which dates belong?** Fixed 2025 treatment dates support a historical annual comparison, not evidence of an emerging 2026 trend. No multi-year stability check is available in this app.
6. **Share of whom?** Severe-only headlines condition on Severe; percentages can become 100% by selection. Use the labeled all-outcome baseline. Unknown-excluding filters also change the sensitivity population.
7. **Same mix?** Mechanism groups could differ in age within 65-120, medical conditions or setting. A pooled difference does not isolate a mechanism effect. No Simpson reversal has been demonstrated.
8. **Were the groups alike before?** There is no intervention or before/after design here. A claim that a design change prevented falls would need a separate study; this is not a detected error in the descriptive app.
9. **Could it be luck?** Obtain each real mechanism's sample count and design-based uncertainty before treating small differences as meaningful. Compare Fall's all-outcome severe share with the entire cohort and review stability across compatible periods outside this app. No real count/ranking is available yet; too little evidence to judge stability.

## Existing change requests

Read CR-01 through CR-08: all marked built at `cf21acc...`. They cover severity baselines, visible evidence, diagnosis context, matching narratives, Undo, unknown sensitivity, codebook definitions and precision reconciliation. Current code contains the corresponding features; the fresh fixture check supports numerical behavior. This does not verify their public deployment. No CR-09 was added. Lack of survey uncertainty and broader fall-event coverage are questions for Ryan to evaluate before deciding whether a reusable change is necessary; deployment and review are existing release prerequisites.

## Rubric review and smallest finish checklist

| Criterion | Current evidence | Missing for highest score |
|---|---|---|
| 6 Realistic cases | Specific fictional person/decision; sourced context and alternatives; explicit difficult taxonomy case; exact planned filters | Actual live use and readable screenshots. Cases not shown live fit the rubric's level-1 description; this is not a score for the team's full case collection. Team-wide user coverage cannot be established by this one case. |
| 7 Interpretation | Code-backed definitions and candidates covering goal fit, exclusions, outside factors, misleading readings and alternatives | Ryan's own supported interpretation of actual results and a defensible prove-or-break conclusion. Evidence preparation alone cannot establish level 3. |

The case matches `one-shot-prompt.md`'s epidemiology investigation-aid vision. It does not expand into causal risk estimation. Sources support context, not Alex's existence or a formal CPSC prioritization formula. The final memo removes template instructions, repeated source notes, detailed audit tables and command logs; this evidence file preserves them. No personal conclusions were omitted because none have been supplied.

Finish only these steps:

1. Obtain a genuinely reviewed runtime release and working public URL from the team; this session does not approve records or start deployment/MVP submission.
2. Use the planned screens on the public app while signed out. Save readable images without spaces in `cases/screenshots/`; record actual values, filters and data version. Compare with the independent real-data check before citing results.
3. Ryan writes/accepts Part 4's interpretations, clarifies whether `Fall` or all fall-involving events answer the intended decision, and supplies Part 5's verdict. Either support the prove branch convincingly against alternatives or formulate a justified nonduplicate CR; a provisional assessment does not satisfy this requirement.
4. Replace draft markers and screenshot placeholders, then export the final Markdown using Markdown Preview Enhanced: Open Preview to the Side > Export > Chrome (Puppeteer) > PDF. Inspect every page/image at normal zoom and upload the individual PDF to Brightspace before the section's official deadline.

No PDF has been created: required live evidence and Ryan's judgment are pending. The attached handout was text-extracted in full, including 11.1, 11.5 and 11.7; its page layout was not visually audited because no PDF editing or layout assessment was needed.
