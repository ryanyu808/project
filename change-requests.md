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
