# Change requests

Our team's log of what we found and what should change, kept in the top folder of our team repo
from Module 9 to Module 13. Pull before you edit it and push soon after.

- For each finding, copy the request template below to the end of this file, give it the next
  number and fill in every field.
- Never delete a request. When it is built, set its status to `built` with the commit; when the
  team decides against it, `declined` with the reason.
- When this file gets long, ask Codex to move the built and declined requests into a dated file
  in `change-requests-archive/` (for example `change-requests-archive/2026-11-02.md`) and leave
  only the open ones here. Numbers continue; never reuse one.

Request template:

```markdown
### CR-NN: short title

- **From:** name, YYYY-MM-DD
- **Part:** the feature, number or function
- **Evidence:** what you did and saw: the input, what you expected, what the tool gave
- **Change:** what should change, in a sentence or two
- **Priority:** high, medium or low
- **Status:** open
```

A filled request (from the class lottery app):

```markdown
### CR-01: chance above 100% with two slots

- **From:** Ana, 2026-10-21
- **Part:** `odds` (the chance of selection by wage level)
- **Evidence:** one person at Level I and one at Level IV, two slots. Both must be selected,
  so each chance is 1. `odds` gave 0.4 and 1.6.
- **Change:** select each person at most once (without replacement), so no chance passes 1.
- **Priority:** high
- **Status:** open
```

## Requests

<!-- Add new requests below this comment, at the end of the file, newest last. -->

### CR-01: Preserve meaningful severity comparisons

- **From:** Ryan Yu, 2026-10-25
- **Part:** Frequency–severity scatter plot, Part 1 feature audit
- **Evidence:** Using the invented five-record fixture, the unfiltered scatter plot shows Contact: 60 weighted visits, 33.3% severe; Fall: 40 weighted visits, 25% severe; Unknown/Unclassified: 20 weighted visits, 100% severe. After selecting Severe only, all three mechanisms show 100% because the severity filter changes both the numerator and denominator. The scatter plot therefore loses its ability to compare overall severe-outcome percentages.
- **Change:** Keep the overall severe-outcome percentage from all eligible outcomes as a clearly labeled comparison baseline when the severity filter is active. Separately show the severe-visit burden for the currently selected records. Make the two populations and denominators explicit so they cannot be confused.
- **Priority:** medium
- **Status:** open

### CR-02: Make supporting evidence visible

- **From:** Ryan Yu, 2026-10-25
- **Part:** Frequency–severity scatter plot and weighted severe-outcome percentage, Parts 1 and 2
- **Evidence:** The invented fixture shows Unknown/Unclassified at 100% severe based on only one record with weight 20. The independent Python loop verified the overall headline percentage of 41.7% (50 severe weight / 120 total weight), but this arithmetic check does not establish statistical precision. The scatter currently shows record counts only on hover and does not display uncertainty estimates.
- **Change:** Add a visible supporting-evidence table or panel beside/below the scatter plot showing each mechanism's unweighted NEISS record count, unknown-disposition record count and weight, and weighted severe-outcome percentage. Include a clear explanation that record counts are not confidence intervals and that uncertainty is not estimated in this MVP. Do not invent statistical significance or unsupported reliability thresholds.
- **Priority:** medium
- **Status:** open

### CR-03: Preserve diagnosis context under severity filters

- **From:** James Liao, 2026-10-25
- **Part:** Primary-diagnosis composition chart, Part 1 feature audit
- **Evidence:** Using the five-record fixture, filtering to Fall showed about 75% contusions and 25% fractures. After also selecting Severe, only one severe Fall record remained and the chart changed to 100% fracture. The diagnosis percentages were recomputed from the filtered subset, so the overall Fall diagnosis pattern was no longer visible.
- **Change:** When a severity filter is active, show the overall diagnosis composition alongside the filtered composition, or otherwise preserve a clearly identified overall baseline so users can distinguish the filtered pattern from the overall pattern.
- **Priority:** medium
- **Status:** open

### CR-04: Show which records match narrative search

- **From:** James Liao, 2026-10-25
- **Part:** NEISS record count with narrative search, Part 2 number audit
- **Evidence:** With the five-record fixture and the search term "belt", I expected cases A and C to match. The app correctly showed a NEISS record count of 2, and an independent loop also found A and C. However, the dashboard shows only the aggregate count, so the user cannot directly verify which narratives produced that number.
- **Change:** When a narrative search is active, provide a reviewable list or table of the matching records, including case ID and narrative text, so users can verify what is included in the count without leaving the app.
- **Priority:** medium
- **Status:** open

### CR-05: Recover the selection after Reset

- **From:** Colby Messih, 2026-10-26
- **Part:** Reset filters, Part 1
- **Evidence:** On the invented fixture, Fall + Severe + `belt` shows 10 weight and one record. Reset clears all three inputs and restores 120 weight and five records. The app then offers no Undo button, and the reset callback replaces the selections with defaults without retaining a previous selection.
- **Change:** Save the selection immediately before Reset and provide Undo reset to restore all three controls together. This would support returning to a subset after comparing it with the full cohort.
- **Priority:** medium
- **Status:** open

### CR-06: Show the decision impact of unknown outcomes

- **From:** Colby Messih, 2026-10-26
- **Part:** Unknown-disposition weighted total, Part 2
- **Evidence:** The fixture caption correctly reports 40 unknown-disposition weight out of 120 total. The independent loop agrees. The interface does not calculate the unknown share or show how unknown outcomes could affect the severe-outcome share: the fixture's simple endpoints are 41.7% and 75.0% if none versus all unknown outcomes were severe.
- **Change:** Add an outcome-completeness panel showing unknown weight as a share of the selected total and the two conditional missing-outcome endpoints, with their numerators and denominator. Explain that these are sensitivity bounds, not confidence intervals. State which records form the population and when a severity selection excludes unknown outcomes. Handle an empty population as unavailable rather than dividing by zero.
- **Priority:** medium
- **Status:** open

### CR-07: Explain mechanism definitions and precedence in the app

- **From:** Author of `../09-audit/my-audit.md` (name not supplied), 2026-10-26
- **Part:** Injury Mechanism Analysis, Part 1 feature audit
- **Evidence:** Source inspection of `app.py`, `filters.py`, and `views.py` shows mechanism names, charts, and a summary without an in-app codebook explanation. `data/prepared/mechanism-codebook.md` version 1.0 distinguishes initiating belt contact from a fall that merely lands on the belt and reserves Unknown/Unclassified for reviewed unclear narratives. The audit's invented AUD1–AUD4 AppTest case successfully selected Fall, but interpreting that category requires consulting the external codebook. This is source and synthetic interface evidence; no real misclassification or personal browser verification is claimed.
- **Change:** Add accessible in-app mechanism definitions and precedence rules beside the mechanism control/chart, identifying the applicable codebook version. Explain that Unknown/Unclassified means reviewed but unclear, rather than unfinished review.
- **Priority:** medium
- **Status:** open

### CR-08: Reconcile weighted totals at full precision

- **From:** Author of `../09-audit/my-audit.md` (name not supplied), 2026-10-26
- **Part:** Estimated national ED visits and mechanism summary, Part 2 number audit
- **Evidence:** In the audit's invented AUD1–AUD4 fixture, the independent CSV/Decimal computation returned 31.2 overall and 10.4 for each of three mechanisms. Saved AppTest results in `../09-audit/audit_evidence/dashboard_results.json` show headline 31 and underlying summary values of 10.4 each. `app.py` formats the headline with `:,.0f` and summary weights with `%.0f`, so three displayed contributions of 10 sum to 30 while the headline shows 31. AppTest rendered no download button. This supports a rounding-reconciliation request, not a production arithmetic error; browser presentation and the real 2025 total remain unverified.
- **Change:** Add a weighted-total reconciliation view showing each selected mechanism's full-precision contribution, their sum, and the rounded headline. Allow downloading the breakdown with active filters and data-version identification, and explain any difference caused by rounding while retaining the concise headline.
- **Priority:** medium
- **Status:** open
