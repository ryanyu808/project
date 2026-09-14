# Data Fit: NEISS Sports and Recreation Injuries

## Proposed audiences and decisions

**Audience A - CPSC epidemiology.** An Associate Executive Director for Epidemiology at the U.S. Consumer Product Safety Commission (CPSC) must decide whether severe treadmill injury mechanisms among adults age 65 and older justify deeper investigation and standards work.

**Audience B - NFHS soccer.** The Director of Sports and a Soccer Rules Committee liaison at the National Federation of State High School Associations (NFHS) must decide which adolescent soccer injury mechanism should enter a Point of Emphasis or a prospective pilot study.

This analysis treats NEISS as a screening signal for both decisions. It can identify patterns among emergency-department visits and help prioritize follow-up research, but it cannot by itself show that a treadmill feature or soccer rule caused an injury.

## Dataset interpretation

### What one row represents

One row represents one product- or recreation-related emergency-department visit, on one treatment date, at one hospital participating in the NEISS probability sample. The sports and recreation slice contains a visit when at least one of `Product_1`, `Product_2`, or `Product_3` matches a CPSC sports or recreation code. Rows are visits rather than unique people, so the same person could appear in more than one unlinked row.

### Who, where, and when were observed

- **People:** Patients treated at reporting NEISS sample-hospital emergency departments for an injury associated with a consumer product or recreational activity.
- **Places:** Approximately 100 sampled U.S. hospitals; 78 hospital identifiers appear in 2023 and 77 in each of 2024 and 2025. The public data provide no state, county, city, ZIP code, hospital name, or geographic crosswalk.
- **Events:** Emergency-department visits connected to products or recreation. Injuries treated only by athletic trainers, urgent-care clinics, physicians outside an ED, or at home are absent.
- **Time:** January 1, 2023 through December 31, 2025, at day-level resolution.
- **National estimates:** `Weight` must be summed for national visit estimates. Raw row counts describe only the reporting hospitals. `Stratum` and `PSU` are also needed to estimate sampling uncertainty.

## Audience A: CPSC treadmill hazard investigation

### Exact evidence that could help

- `Product_1`, `Product_2`, and `Product_3` can identify rows coded **3277 - Exercise Equipment**. Because this is a broad code rather than a treadmill-specific code, `Narrative_1` must also be searched and reviewed to confirm treadmill involvement.
- `Age` can restrict the evidence to adults age 65 and older. Codes 201-223 represent age in months and must not be interpreted as adult ages; age 0 means unrecorded.
- `Narrative_1` is the only field that may describe a treadmill mechanism, such as a fall while using the machine, contact with the moving belt, entrapment, a struck-by event, or an injury while moving or repairing the equipment. The text is brief, abbreviated, inconsistent, and not a standardized mechanism field, so a coding rubric and manual validation are necessary.
- `Diagnosis` and `Diagnosis_2`, plus `Other_Diagnosis` and `Other_Diagnosis_2`, can describe injury type. Code 71 means other or not stated, so its corresponding text must be reviewed rather than treated as a clinical category.
- `Body_Part` and `Body_Part_2` can identify the body regions injured.
- `Disposition` can distinguish treated-and-released visits from transfers, hospital admissions, observation, and fatalities at or before arrival. It is the dataset's only consistent severity indicator.
- `Treatment_Date` can describe timing within a year.
- `Location` may separate home and recreation settings, but location code 0 means not recorded and location is missing for roughly one-third of the overall sports slice.
- `Weight` can estimate the national number of treadmill-related ED visits represented by validated records. `Stratum` and `PSU` are necessary for uncertainty estimates.

### Supported by the data

NEISS can support a national screening analysis of treadmill-associated emergency-department visits among adults 65 and older. After validating treadmill mentions, the analysis can describe:

- recurring narrative mechanisms;
- the diagnoses and body parts associated with those mechanisms;
- the weighted number of represented ED visits;
- the proportion or weighted share resulting in admission, transfer, observation, or ED fatality; and
- which mechanism-severity combinations appear most important for deeper investigation.

This is enough to prioritize a hazard signal. For example, repeated belt-related falls with a relatively high admission share could justify obtaining richer incident reports or conducting engineering and human-factors research.

### Partly supported

- **Comparing mechanism severity:** `Disposition` provides a limited severity proxy, but NEISS has no injury-severity score, length of stay, cost, recovery, disability, or post-discharge outcome.
- **Comparing mechanisms over time:** Annual estimates are possible, but the hospital sample and weights changed between 2023 and 2024. A level trend across that break could be misleading. Within-year comparisons are safer; any cross-year result needs a prominent comparability warning.
- **Identifying a mechanism:** Narratives may mention how an incident happened, but they are short clinical summaries and may omit key details. Missing text cannot be interpreted as proof that a mechanism was absent.
- **Focusing on adults 65+:** Age is directly observed, but the dataset contains no measure of how many older adults own or use treadmills or how long they are exposed.

### Outside the data's scope

NEISS cannot determine:

- the injury rate per treadmill user, workout, or hour of use;
- whether a particular brand, model, design, maintenance condition, warning, or safety feature was involved;
- whether the treadmill was defective or compliant with a standard;
- the person's balance, mobility, health conditions, medication use, supervision, or experience;
- outcomes after the ED visit; or
- whether a new standard would prevent the observed injuries.

The file contains no uninjured treadmill users and no exposure denominator, product brand/model, or standardized causal investigation. Associations between a narrative mechanism and severe disposition therefore do **not** establish that the mechanism caused the severity. NEISS should trigger deeper investigation, not serve as the sole basis for a causal conclusion or final standard.

### Open questions for follow-up

1. What narrative rules will distinguish active treadmill use from moving, storing, repairing, or merely being near a treadmill?
2. How many candidate records survive manual validation, and are the resulting weighted estimates precise enough for reporting?
3. Can CPSC obtain full incident reports, product details, in-depth investigations, exposure estimates, or engineering-test results for the leading mechanism?

## Audience B: NFHS adolescent soccer rule-study priority

### Exact evidence that could help

- `Product_1`, `Product_2`, and `Product_3` can identify soccer using code **1267 - Soccer (Activity, Apparel or Equipment)**. The lookup also contains historical organized/informal soccer codes, but the overview reports that these codes do not appear in the 2023-2025 files.
- `Age` can define an adolescent range chosen by the team. That range must be stated explicitly; NEISS does not contain school grade or high-school participation status.
- `Narrative_1` may describe candidate mechanisms such as player-to-player contact, falls, twists, ball contact, goal contact, or surface-related events. These mechanisms are not standardized fields and require a documented text-coding rubric plus manual review.
- `Diagnosis`, `Diagnosis_2`, `Other_Diagnosis`, and `Other_Diagnosis_2` can distinguish injury types such as concussion, fracture, sprain, or laceration, subject to coding and free-text limitations.
- `Body_Part` and `Body_Part_2` can characterize the injured area.
- `Disposition` can provide a limited measure of acute severity.
- `Location` can sometimes distinguish school/daycare from a place of recreation or sport, although missingness is substantial and neither category proves NFHS-sanctioned play.
- `Sex`, `Race`, and `Hispanic` can describe recorded patient groups, but missingness and the absence of participation denominators limit comparisons.
- `Weight`, `Stratum`, and `PSU` allow appropriately weighted national estimates and uncertainty calculations.

### Supported by the data

NEISS can support a national screening analysis of soccer-associated ED visits among a defined adolescent age range. It can identify commonly documented mechanisms, connect those mechanisms to acute diagnoses and body parts, and compare limited severity indicators. That evidence can help NFHS choose one mechanism for a prospective study or Point-of-Emphasis discussion.

For example, the analysis could rank manually coded mechanism categories using both weighted visit estimates and a severe-disposition measure, while separately showing concussion, fracture, and sprain patterns. The appropriate output is a prioritized hypothesis for NFHS to investigate—not a claim that a rule change is already warranted.

### Partly supported

- **Adolescent soccer:** Age and soccer involvement are recorded, but high-school enrollment, NFHS membership, team level, organized versus informal play, match versus practice, and competition rules are generally not.
- **Mechanism identification:** Narratives sometimes describe contact, falls, twisting, heading, the ball, the goal, or the surface, but the wording is inconsistent and important details may be absent.
- **Severity comparisons:** Diagnosis, body part, and disposition describe the ED visit, but there is no validated injury-severity score, time lost from sport, return-to-play date, or long-term outcome.
- **Subgroup comparisons:** Patient characteristics are available, but NEISS contains no counts of participants or athlete-exposures for the comparison groups.
- **National relevance:** Survey weights support national ED-visit estimates, but not estimates specifically for NFHS-sanctioned soccer.

### Outside the data's scope

NEISS cannot determine:

- whether the injury occurred in an NFHS-sanctioned game or practice;
- which rule set was in effect or whether a violation occurred;
- the player's position, skill level, playing time, team, league, grade, or prior injury history;
- detailed equipment use, playing surface, weather, coaching, officiating, or supervision unless briefly mentioned;
- athlete-exposures, participation hours, or the risk per player;
- injuries treated only by trainers, clinics, or team physicians; or
- whether a Point of Emphasis or rule change would reduce injuries.

NEISS includes only injured people who reached an emergency department. A mechanism with more recorded visits may simply occur more often in soccer, not be more dangerous per exposure. Likewise, an association between a mechanism and concussion or admission does not prove the mechanism caused that outcome. Testing rule effectiveness requires stronger evidence, ideally a prospective pilot with exposure counts, standardized injury surveillance, implementation measures, and a comparison group.

### Open questions for follow-up

1. What exact adolescent age range should represent the intended NFHS population?
2. Can a blinded sample of narratives be coded reliably into a small set of decision-relevant mechanisms?
3. Can NFHS combine the NEISS signal with its own participation, match/practice exposure, rule, and injury-surveillance data?
4. Which mechanism is both visible enough in NEISS to measure and actionable enough for an NFHS rule study?

## Overall data-fit conclusion

Both decisions are **partly supported**. NEISS fits the first stage of each decision: finding national emergency-department injury signals and choosing where to investigate next. It does not fit the final causal decision. The CPSC audience has the stronger institutional fit because NEISS is CPSC's own surveillance system and its decision explicitly calls for deeper investigation. The NFHS decision is also plausible if framed as selecting a prospective research priority, but the gap between a general soccer ED visit and an NFHS-sanctioned event is substantial.

The honest boundary is therefore:

- **Supported:** describe and prioritize weighted ED-visit patterns by age, product/activity, narrative-coded mechanism, diagnosis, body part, and disposition.
- **Partly supported:** compare apparent severity and time patterns, provided the analysis accounts for narrative uncertainty, missingness, survey weights, and the 2023-2024 sample break.
- **Outside scope:** estimate injury risk per exposure, identify product defects or rule violations, measure long-term outcomes, or claim that a design feature, playing mechanism, standard, or rule caused or prevented injuries.

## Checks performed and sources

- Read sections 1-3 and the data dictionary and limitations in sections 5-6 of `data_overview_neiss-sports-injuries.md`.
- Checked `sample/sports_product_codes.csv` and `sample/neiss_code_lookup_2025.csv` for the relevant product labels: 3277 for broad exercise equipment and 1267 for soccer.
- Checked the 20,000-row sports sample to confirm the available columns and that both exercise-equipment and soccer records appear. This check was only structural; sample counts were not presented as population estimates.
- Treated AI-generated interpretations in this file as hypotheses bounded by the documented fields and limitations. The linked CPSC sources in the overview remain the authority for factual claims.
