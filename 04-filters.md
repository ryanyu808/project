# 04 — Sidebar Filters and Narrative Search (Parth)

## Purpose and boundaries

Let the CPSC epidemiology user narrow the prepared treadmill injury cases by
injury mechanism, severity, and narrative text. All charts and tables must use
the same filtered DataFrame so the user can compare the selected cases consistently.

This component receives the loaded DataFrame from `03-loader.md` and passes a
filtered DataFrame to `05-views.md`. It runs on each filter change. Data preparation
owns the ages 65–120, product-code 3277, and treadmill-confirmation rules; filters
must not reload raw files or reclassify mechanisms. `06-setup.md` owns page layout
and calls the sidebar renderer. There is no job-title field in this dashboard;
the text-search control searches injury narratives instead.

## Input and output contract

The loader must provide these columns; `Injury_Mechanism` and `Severity` are
proposed prepared-column names that the preparation and loader pieces must adopt.

| Column | Required representation |
|---|---|
| `Injury_Mechanism` | One nonblank display label per case, assigned during preparation. Missing or unclassifiable mechanisms use `Unknown / unclear`. |
| `Severity` | One of `Severe`, `Other known disposition`, or `Unknown`. Preparation maps numeric `Disposition` codes 2, 4, 5, 8 to `Severe`; 0, 1, 6 to `Other known disposition`; code 9, missing, or unrecognized codes to `Unknown`. |
| `Narrative_1` | Narrative text, possibly null. Treat null as empty text for search only. |

`Other known disposition` is a grouping of the remaining recognized disposition
codes, not a claim that those injuries were mild. Confirm the disposition mapping
against each source year's codebook during preparation. The 2025 lookup in the
dataset repository supports the codes above.

Return matching rows with their original columns, values, index, and order,
including `Weight`, `Stratum`, and `PSU`. Do not aggregate, deduplicate, rescale
weights, or mutate the input. Missing required columns or invalid severity labels
must produce an actionable validation error naming the column or value.

Implement in `filters.py` with these public interfaces:

```python
from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class FilterSelection:
    mechanisms: tuple[str, ...] = ()
    severities: tuple[str, ...] = ()
    narrative_query: str = ""

def render_sidebar(data: pd.DataFrame) -> FilterSelection:
    """Render Streamlit controls and return the current selection."""

def apply_filters(data: pd.DataFrame, selection: FilterSelection) -> pd.DataFrame:
    """Apply selections without Streamlit calls, file access, or hidden state."""
```

Keep the filtering function independent of the UI so it can be checked with a
small DataFrame and reused if the sidebar changes.

## Controls and matching rules

| Sidebar control | Options and behavior | Initial value |
|---|---|---|
| Injury mechanism | Multiselect, using sorted distinct labels from the full loaded cohort, including `Unknown / unclear` when present. | Empty selection: all mechanisms. |
| Severity | Multiselect: `Severe`, `Other known disposition`, `Unknown`. | Empty selection: all severities. |
| Search injury narratives | Text input with a hint such as `e.g., belt or fell; enter one phrase`. Match the entire trimmed query as one case-insensitive, literal substring of `Narrative_1`. | Empty text: no text restriction. |
| Reset filters | Clear both multiselects and search text using a Streamlit callback before widgets render again. | Available on first load. |

Within each multiselect, selected values are combined with OR. Combine the two
multiselects and narrative search with AND. Whitespace-only queries match all
rows. Punctuation is literal: `fall.*` searches for those exact characters, with
no regex, wildcard, or keyword-OR behavior. Null narratives remain eligible when
the query is blank and cannot match a nonblank query.

Use stable widget keys. Build options from the full loaded cohort on every rerun,
not from the filtered result, so choices do not disappear after a zero-match search.
Apply a vectorized pandas Boolean mask (`isin` and `str.contains` with
`case=False, regex=False, na=False`); reuse the loader's cached data rather than
reading files on each interaction. The application passes this one result to
every view. Show `Showing X of Y prepared cases` using unweighted row counts.

If no rows match, preserve the controls and show `No cases match these filters.
Try clearing a selection or changing the search text.` Views must skip empty
charts and show unavailable percentages as `N/A`, rather than dividing by zero.
If the loaded cohort itself is empty, show `No prepared treadmill cases are
available.` Keep reset available. A single matching case must still render.

## Build order and completion checks

Implement `apply_filters` first, then the sidebar renderer, then connect its
result to the views. Check behavior using this invented prepared fixture:

| Case | Injury_Mechanism | Severity | Narrative_1 | Weight |
|---|---|---|---|---:|
| A | Fall | Severe | FELL from treadmill belt | 10 |
| B | Fall | Other known disposition | Tripped beside treadmill | 20 |
| C | Belt contact | Severe | Hand caught in BELT | 30 |
| D | Unknown / unclear | Unknown | null | 40 |

| Selection or interaction | Expected result |
|---|---|
| First load; or reset after changing every control | A, B, C, D, unchanged weights; count `4 of 4`. |
| Mechanisms `Fall` and `Belt contact` | A, B, C. |
| Mechanism `Fall`, severity `Severe` | A only. |
| Search `  belt  ` | A and C; trimming and case-insensitive matching work. |
| Mechanism `Fall`, severity `Severe`, search `belt` | A only: all three restrictions apply together. |
| Search containing only spaces | A, B, C, D, including the null narrative. |
| Search `fall.*` | No rows; literal punctuation and the empty-state message work. |
| Severity `Unknown` | D only; missing severity is not silently treated as non-severe. |
| Search producing zero matches, then clear search | All rows return and mechanism options remain available. |

Also verify that filtering leaves the source DataFrame unchanged, that every view
receives the same selected cases, and that missing required columns fail clearly.
Use this fixture for filter checks only; national estimates require the full
prepared dataset and belong to the views component.
