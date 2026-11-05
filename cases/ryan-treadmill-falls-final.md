# Alex: should older-adult treadmill falls receive investigation priority?

**Provisional memo for Ryan's review - not ready to submit.** The dashboard could help Alex screen mechanisms for follow-up by bringing ED burden, recorded outcomes and narratives together. It cannot yet establish whether falls deserve priority: the reviewed data release and public app are unavailable, and Ryan's interpretation and final verdict remain pending. It provides no treadmill-use exposure denominator or evidence that a product caused an injury.

## 1. The person and the decision

Alex is a fictional CPSC epidemiology analyst investigating injuries among older adults, not someone I interviewed. During investigation planning, Alex must decide whether treadmill-related falls among adults 65 and older warrant priority over other treadmill injury mechanisms. A poor choice could divert limited investigative attention from a more consequential or informative pattern.

## 2. Their real situation and alternatives

CPSC describes analysts screening ED surveillance for emerging hazards and combining NEISS with other sources when setting study priorities. Follow-back interviews can add person, product and environmental detail. This supports the role's plausibility, not a claim that CPSC uses our dashboard or a particular ranking formula. Source: CPSC, [NEISS Frequently Asked Questions](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Neiss-Frequently-Asked-Questions).

Alex's alternatives include the official NEISS query/download tools and an independently reviewed analysis of the records. The official tool offers uncertainty outputs; a separate analysis can apply a broader definition of fall-involving events. Follow-back investigation can address circumstances that brief narratives cannot resolve. Our dashboard's proposed advantage is faster, consistent comparison of a reviewed treadmill cohort, rather than new underlying evidence. CPSC's [Instructions for Using the NEISS Estimates Query Builder](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Instructions-for-Using-the-NEISS-Estimates-Query-Builder) document filters, downloadable records and optional CV/confidence intervals. These alternatives complement the dashboard; a broader product query is not an exact cohort match.

## 3. The app in use

**Live link: unavailable.** Repository documentation says not deployed, and both configured runtime data files are absent. The following are planned selections, not observed results. Save screenshots from the public app with selections visible; do not replace them with local screens.

| Planned screen | Exact selections and evidence to capture |
|---|---|
| A: Compare mechanisms | Fixed 2025; Injury mechanism empty (all); Severity empty (all); narrative search blank. Capture burden/scatter and mechanism/supporting-evidence tables, including Fall and comparators. **[LIVE SCREENSHOT PENDING: screenshots/alex-comparison.png]** |
| B: Examine Fall | Injury mechanism `Fall`; Severity empty; search blank. Capture diagnosis and expanded Outcome completeness and conditional sensitivity; repeat for each comparator if missingness could affect priority. **[LIVE SCREENSHOT PENDING: screenshots/alex-fall-context.png]** |
| C: Inspect severe narratives | Injury mechanism `Fall`; Severity `Severe`; search `belt`. Capture matching narratives and the labeled all-outcome severity/diagnosis baselines. This is a narrow diagnostic subset, not the primary ranking. **[LIVE SCREENSHOT PENDING: screenshots/alex-narratives.png]** |

**What Alex sees: pending actual public-app use.** Record weighted visits, severe percentages, sample counts, unknown weights, diagnoses and sensitivity endpoints without supplying guessed values. Capture extra images if tables do not fit. Keep the data hash from the reconciliation export.

## 4. Reading the result for their decision

**Does the number measure what Alex cares about?** Verified code in `views.py:build_view_data` sums `Weight` for ED visits and computes recorded severe weight / all selected weight. `contracts.py` defines severe as dispositions 2/4/5/8. These can inform burden screening, but they do not measure preventable injuries or investigation value directly. Critically, codebook 1.0 puts some falls under Entering/exiting or Belt contact; `Fall` is not every fall-involving event. **Candidate interpretation for Ryan:** decide whether this initiating-mechanism definition fits the chosen decision before relying on its rank (11.5 kinds 3 and 4).

**Who is in the rows, and who is not?** The intended cohort is reviewed 2025 ED visits, ages 65-120, product 3277 in any product field, with a literal treadmill mention. A row is a visit, not a unique person. Other years/ages, non-ED injuries and records missing the required mention are outside this analysis. Human eligibility/policy review is unfinished. **Candidate interpretation for Ryan:** the cohort is a useful surveillance subset whose exclusions could change a broader fall-priority decision (kinds 1, 2 and 5).

**What outside the data matters?** Investigation feasibility, preventability, equipment details, medical triggers and current incident information could change the choice; their importance here remains to be assessed. The dashboard has neither treadmill-use exposure nor a causal study design. CPSC's [Explanation Of NEISS Estimates Obtained Through The CPSC Website](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Explanation-Of-NEISS-Estimates-Obtained-Through-The-CPSC-Website) explains survey variability. Visible sample counts do not replace design-based uncertainty. **Ryan must judge** whether missing evidence makes a comparison too weak to act on (kinds 7-9).

**What could Alex wrongly conclude?** A high visit total could be mistaken for risk per user; a high severe percentage from a small group could be mistaken for a stable difference. Severe-only headlines change the denominator; use the explicit all-outcome baseline. Unknown outcomes remain in unrestricted denominators. Sensitivity endpoints S/T and (S+U)/T assume none/all unknown weight is severe; they are not confidence intervals (kinds 4, 6 and 9). Primary-diagnosis shares use only `Diagnosis`, retaining missing/unmapped buckets, rather than counting every diagnosis.

A fresh independent fixture check passed on November 5; its saved report is `ryan-treadmill-falls-fixture-check.json`. This supports arithmetic on invented records, not any real mechanism ranking. **Ryan's answers remain pending:** which of these limitations changes Alex's choice, and what actual live evidence supports that judgment?

## 5. The verdict: prove or break

**Provisional assessment:** the coordinated views could reduce manual comparison work while preserving links to evidence. The official query offers uncertainty outputs, independent analysis can revise cohort/taxonomy choices, and investigation can supply missing circumstances. The dashboard's comparative practical value has not yet been demonstrated on a live reviewed cohort, so an "as good as it gets" conclusion is unsupported today.

CR-01 through CR-08 already address baselines, supporting counts, diagnosis context, narrative visibility, Undo, unknown sensitivity, definitions and precision reconciliation. They are marked built and corresponding features are in the inspected code. No new request was added merely to fill this part.

**Final personal verdict: pending Ryan.** After examining live results and the alternatives, Ryan must either substantiate the prove branch or identify an evidence-backed, nonduplicate change that improves this and other cases. The current draft does not settle whether falls deserve priority.

## Taxonomy update for the later live evaluation

Version 1.1 now explicitly includes an unpowered supporting-surface Fall and separates established non-use equipment/cord falls. Original research and Ryan's pending personal verdict above are preserved. The four held mappings block production release, so no live findings or screenshots are added. When data and a public URL exist, compare Fall with the non-use category explicitly; an all-fall-involving question also requires narrative review of entering/exiting and belt categories, rather than treating those categories as entirely falls. This is an analytical scope question, not Ryan's final conclusion.
