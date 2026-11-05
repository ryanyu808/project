# Case: Alex - prioritizing treadmill falls among older adults

> **Individual. Hand in one PDF file**, not this Markdown file: one case for **your team's
> app**, one specific person using it for one real decision, with screenshots of your team's
> **live app**. Upload the PDF to **Brightspace → Hand In Work** before Quiz 11. Your team also
> puts it in Section 2 (*Cases*) of its MVP `validation.pdf`, graded by MVP criteria 6 and 7 in
> `mvp.md` (in your section's repo). Full instructions: Module 11 handout, 11.7 and *What to hand in*. The four
> questions are in 11.1, and how to make the PDF is in 11.4.
>
> **Where to write.** Copy this file into your team's private repo, in any folder your team
> chooses, and rename it for your person, such as `ana-orders.md`. Save screenshots in a folder
> `screenshots/` next to it. Push as you go, so teammates can see your case.
>
> **In class, for Mei,** use `mei-case.md` in your section's repo instead: it is set up for
> copying in your `/class` answers.
>
> **Claim your person first.** Agree as a team who takes which person and decision, or fill in
> part 1, push this file and tell your teammates: the earlier claim keeps it. A case for the same
> person and decision as a teammate's earlier claim does not count. Together, the team's cases
> should cover your main kinds of users and at least one difficult case.
>
> Five parts: **1** the person and the decision; **2** their real situation and their
> alternatives, from at least two sources; **3** the app in use, with live-app screenshots; **4**
> reading the result for their decision; **5** the verdict: prove the app is as good as it gets
> for this person, or break it with a change request. Codex can find sources, take screenshots
> and make the PDF. What the result means for this person, and the verdict, are yours.

<!--
  How to fill it in:
  - All five parts are required. Replace every placeholder that says "Write" or "Paste",
    including the title. Keep the headings. The boxed lines,
    which start with >, may stay in the PDF; these comments do not show in it.
  - Show what you did and what you saw, not only a conclusion: the selections, the numbers on
    the screen, the source and what it says, the check you ran and its result.
  - Make the PDF as in handout 11.4, with the Markdown Preview Enhanced extension installed in
    VS Code: right-click in the file, "Markdown Preview Enhanced: Open Preview to the Side",
    then right-click in the preview, "Export -> Chrome (Puppeteer) -> PDF". Name it for your
    person, such as case-ana-orders.pdf. Open it and check that every screenshot is readable.
    If the export fails, ask Codex to fix it.
-->

## 1. The person and the decision

> **Enough:** a specific person and one decision your app is for, so that a reader who has never
> seen your project can picture it.

<!-- Who they are, with a name you make up and their job or situation; the decision; when it comes up;
     and what they lose if they decide badly. "A store manager" is too general; "Ana, who
     manages a grocery store and decides each Thursday how much fresh produce to order for the
     next week" is a person. A difficult case is welcome: a user the app serves badly, or one at
     the edge of what it is for. Two to four sentences. -->

Alex is a fictional CPSC epidemiology analyst investigating injuries among older adults, not a person I interviewed. During investigation planning, Alex must decide whether treadmill-related falls among adults 65 and older warrant priority for follow-up investigation compared with other treadmill injury mechanisms. Choosing poorly could divert limited investigative attention from more informative or consequential injury patterns.

## 2. Their real situation and alternatives

> **Enough:** how this kind of person makes this decision today, what they are trying to
> achieve and what matters to them, and the alternatives they have to your app, from at least
> two sources you read.

<!-- Sources you can open free online: an official rule or government page, job postings, a news
     or trade article, the alternatives' own websites, or a forum where people in that role
     discuss the decision. Say which source each claim comes from.
     Say what matters to this decision that your app's data do not contain, such as a rule, a
     cost, the person's own circumstances or a recent change. Then name their alternatives: other tools or
     websites, other public data, people they can ask, or how they decide now. Part 5 compares
     your app with these. One or two paragraphs. -->

CPSC describes analysts screening ED surveillance for emerging hazards and combining NEISS with other sources when setting study priorities. Follow-back interviews can add person, product and environmental detail. This supports the role's plausibility, not a claim that CPSC uses our dashboard or a particular ranking formula. Source: CPSC, [NEISS Frequently Asked Questions](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Neiss-Frequently-Asked-Questions).

Alex's alternatives include the official NEISS query/download tools and an independently reviewed analysis of the records. The official tool offers uncertainty outputs; a separate analysis can apply a broader definition of fall-involving events. Follow-back investigation can address circumstances that brief narratives cannot resolve. Our dashboard's proposed advantage is faster, consistent comparison of a reviewed treadmill cohort, rather than new underlying evidence. CPSC's [Instructions for Using the NEISS Estimates Query Builder](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Instructions-for-Using-the-NEISS-Estimates-Query-Builder) document filters, downloadable records and optional CV/confidence intervals. These alternatives complement the dashboard; a broader product query is not an exact cohort match.

**Sources:**

- See the linked CPSC sources above and the title/publisher/fact/excerpt audit in [supporting evidence](ryan-treadmill-falls-evidence.md).
- Third source: CPSC, [Explanation Of NEISS Estimates Obtained Through The CPSC Website](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Explanation-Of-NEISS-Estimates-Obtained-Through-The-CPSC-Website).

## 3. The app in use

> **Enough:** your team's live link, what the person selects, at least one screenshot **of the
> live app** with the selections visible, and what they see, in your own words.

<!-- Take every screenshot from the live app at its public link, not from the app running on
     your laptop. (Mei's case in class is the exception: its screenshots are of the H-1B
     explorer on your laptop.) One block per screen,
     in the order the person would use them. Insert each screenshot with
     ![what it shows](screenshots/file-name.png). If a selection does not show in the
     screenshot, write it in the line above the image. If a table is cut off, enlarge the window
     or take a second screenshot of the rest. -->

**Live link: unavailable.** Repository documentation says not deployed, and both configured runtime data files are absent. The following are planned selections, not observed results. Save screenshots from the public app with selections visible; do not replace them with local screens.

| Planned screen | Exact selections and evidence to capture |
|---|---|
| A: Compare mechanisms | Fixed 2025; Injury mechanism empty (all); Severity empty (all); narrative search blank. Capture burden/scatter and mechanism/supporting-evidence tables, including Fall and comparators. **[LIVE SCREENSHOT PENDING: screenshots/alex-comparison.png]** |
| B: Examine Fall | Injury mechanism `Fall`; Severity empty; search blank. Capture diagnosis and expanded Outcome completeness and conditional sensitivity; repeat for each comparator if missingness could affect priority. **[LIVE SCREENSHOT PENDING: screenshots/alex-fall-context.png]** |
| C: Inspect severe narratives | Injury mechanism `Fall`; Severity `Severe`; search `belt`. Capture matching narratives and the labeled all-outcome severity/diagnosis baselines. This is a narrow diagnostic subset, not the primary ranking. **[LIVE SCREENSHOT PENDING: screenshots/alex-narratives.png]** |

**What Alex sees: pending actual public-app use.** Record weighted visits, severe percentages, sample counts, unknown weights, diagnoses and sensitivity endpoints without supplying guessed values. Capture extra images if tables do not fit. Keep the data hash from the reconciliation export.

## 4. Reading the result for their decision

> **Enough:** an answer to each question below, each backed by evidence: a number from the
> data, a rule, a source, or a check you ran.

<!-- Handout 11.1 gives the questions. Questions 1-3 are answered here; question 4 (better off
     than with the alternatives, and what not to use the app for) is part 5. The fourth prompt
     below asks how the person could misread the result, which part 5 then rules out. Handout 11.5 lists nine kinds of number that answer a
     different question: 1 one row per what, 2 which rows belong, 3 the real thing or a stand-in,
     4 a total or a rate, 5 which dates belong, 6 share of whom, 7 same mix, 8 were the groups
     alike before, 9 could it be luck. If a number the person relies on is one of these, name
     the kind, show the evidence, such as the line of code or a count from the data, and say
     what the right number is. For a rate from a small group (kind 9), say how many rows
     stand behind it. Then check whether it holds: compare it with the overall rate, or split
     the data by year. Or say that there are too few rows to tell. Codex can find the code
     behind a number and compute another
     version in a file you run; paste its code and output in the box. -->

**Does the number measure what Alex cares about?** Verified code in `views.py:build_view_data` sums `Weight` for ED visits and computes recorded severe weight / all selected weight. `contracts.py` defines severe as dispositions 2/4/5/8. These can inform burden screening, but they do not measure preventable injuries or investigation value directly. Critically, codebook 1.0 puts some falls under Entering/exiting or Belt contact; `Fall` is not every fall-involving event. **Candidate interpretation for Ryan:** decide whether this initiating-mechanism definition fits the chosen decision before relying on its rank (11.5 kinds 3 and 4).

**Who is in the rows, and who is not?** The intended cohort is reviewed 2025 ED visits, ages 65-120, product 3277 in any product field, with a literal treadmill mention. A row is a visit, not a unique person. Other years/ages, non-ED injuries and records missing the required mention are outside this analysis. Human eligibility/policy review is unfinished. **Candidate interpretation for Ryan:** the cohort is a useful surveillance subset whose exclusions could change a broader fall-priority decision (kinds 1, 2 and 5).

**What outside the data matters?** Investigation feasibility, preventability, equipment details, medical triggers and current incident information could change the choice; their importance here remains to be assessed. The dashboard has neither treadmill-use exposure nor a causal study design. CPSC's [Explanation Of NEISS Estimates Obtained Through The CPSC Website](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Explanation-Of-NEISS-Estimates-Obtained-Through-The-CPSC-Website) explains survey variability. Visible sample counts do not replace design-based uncertainty. **Ryan must judge** whether missing evidence makes a comparison too weak to act on (kinds 7-9).

**What could Alex wrongly conclude?** A high visit total could be mistaken for risk per user; a high severe percentage from a small group could be mistaken for a stable difference. Severe-only headlines change the denominator; use the explicit all-outcome baseline. Unknown outcomes remain in unrestricted denominators. Sensitivity endpoints S/T and (S+U)/T assume none/all unknown weight is severe; they are not confidence intervals (kinds 4, 6 and 9). Primary-diagnosis shares use only `Diagnosis`, retaining missing/unmapped buckets, rather than counting every diagnosis.

A fresh independent fixture check passed on November 5; its saved report is `ryan-treadmill-falls-fixture-check.json`. This supports arithmetic on invented records, not any real mechanism ranking. **Ryan's answers remain pending:** which of these limitations changes Alex's choice, and what actual live evidence supports that judgment?

See the candidate evidence above and [the full code, source and check log](ryan-treadmill-falls-evidence.md). These are preparation for my own answers, not my completed judgments.

## 5. The verdict: prove or break

> **Enough:** whether this person is better off with the app than with the alternatives in
> part 2, the app's place among them, and what they must not use it for. Then **either**
> compelling evidence that, for this person, the app is as good as it gets with the data
> available, **or** a change request that makes it better for this case without being made
> only for this case or making other users' answers worse.

<!-- Saying plainly that the app should not be used for some decision is a finding, and counts in
     your favor. So is showing that it holds up: say what you checked and why nothing better is
     possible with the data. A change request can be a new number or view, a label, a warning,
     or removing something misleading; say whom else it affects, such as your teammates' cases
     and the app's other users, and why it does not hurt them. Paste it as it appears in
     change-requests.md, or delete the box if you prove the app. -->

**Provisional assessment:** the coordinated views could reduce manual comparison work while preserving links to evidence. The official query offers uncertainty outputs, independent analysis can revise cohort/taxonomy choices, and investigation can supply missing circumstances. The dashboard's comparative practical value has not yet been demonstrated on a live reviewed cohort, so an "as good as it gets" conclusion is unsupported today.

CR-01 through CR-08 already address baselines, supporting counts, diagnosis context, narrative visibility, Undo, unknown sensitivity, definitions and precision reconciliation. They are marked built and corresponding features are in the inspected code. No new request was added merely to fill this part.

**Final personal verdict: pending Ryan.** After examining live results and the alternatives, Ryan must either substantiate the prove branch or identify an evidence-backed, nonduplicate change that improves this and other cases. The current draft does not settle whether falls deserve priority.
