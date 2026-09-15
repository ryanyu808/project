# Auxiliary Data

The supplied NEISS files are useful for identifying injury patterns, but they do not contain all of the information needed for either team's decision. The two additions below fill one important gap for each audience. They should supplement NEISS rather than be treated as exact extensions of it.

## Audience A: CPSC treadmill follow-back investigations

### Missing decision input

NEISS does not provide a validated, detailed account of how a severe treadmill incident happened. Product code 3277 covers exercise equipment broadly, so `Narrative_1` must first be used to confirm treadmill involvement. Even then, the file has no structured information about treadmill brand or model, safety features, operating settings, product condition, or the sequence connecting the user, treadmill, and surrounding environment.

### Proposed auxiliary source

A targeted CPSC follow-back or in-depth investigation of selected treadmill cases would provide this detail. CPSC states that some incidents identified through NEISS receive telephone or on-site follow-back interviews and that these investigations examine interactions among the person, product, and environment. CPSC uses them to classify hazard patterns and identify possible preventive actions ([CPSC NEISS FAQ](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Neiss-Frequently-Asked-Questions)).

### Who collects and maintains it

CPSC administers and maintains follow-back investigations. CPSC investigators or its contractors collect additional information from the patient, a relative, or another knowledgeable respondent. The NEISS hospital supplies the original emergency-department record, while the follow-back provides more detail about the incident.

### What one row represents and useful fields

One row would represent one completed investigation of one selected NEISS visit. CPSC does not publish one universal set of fields for every in-depth investigation, so the following are **proposed fields for a treadmill study**, not verified columns in an existing file:

- the initiating `CPSC_Case_Number` or another documented linkage key;
- confirmation that a treadmill was involved and whether the person was using, moving, repairing, or standing near it;
- a structured incident sequence;
- manufacturer, brand, model, serial number, and approximate product age;
- belt speed or incline, handrail use, and whether the user was mounting or dismounting;
- presence and use of an emergency-stop device or safety key;
- treadmill placement, nearby objects, and relevant product condition; and
- later medical outcome, if available.

The NEISS fields would continue to supply age, diagnosis, injured body part, disposition, treatment date, and the survey design variables.

### How we would obtain and connect it to NEISS

We would first identify candidate NEISS records where any of `Product_1`, `Product_2`, or `Product_3` equals 3277, `Age` is 65 through 120, and manual review of `Narrative_1` confirms treadmill involvement. After applying a documented definition of severe disposition, CPSC could select cases for follow-up.

For a newly designed CPSC study, the originating `CPSC_Case_Number` should be retained as the exact linkage key. Existing public incident or investigation records may also be requested through CPSC's Clearinghouse, which permits users to query and download public incident data ([CPSC Clearinghouse instructions](https://www.cpsc.gov/Research--Statistics/Instructions-For-Using-The-Clearinghouse-Query-Builder)). However, we would need to verify that a released record contains a key that matches the public NEISS case number. We would not assume that another CPSC identifier is equivalent.

### What could fail or limit the connection

Patients may be unreachable, decline an interview, or not remember treadmill settings or product identifiers. Fatal or cognitively impaired patients may require proxy reports. Followed cases may be a selective subset of severe cases, and nonresponse may also vary by mechanism. Therefore, the original NEISS weights cannot automatically be applied to completed investigations without accounting for selection and nonresponse.

The public version of an investigation may omit the linkage key. Product details may remain unknown, and a detailed account still cannot prove that a treadmill feature caused the injury. It can identify a pattern worth engineering study, not establish defect or causality.

### New question made answerable

The combined data could answer: **Among investigated severe treadmill-associated ED visits involving adults age 65 and older, which event sequences and product or safety-feature configurations recur often enough to justify a targeted engineering or standards investigation?**

### Synthetic fallback

If investigation records are unavailable, a small, fully synthetic NEISS-like table and follow-back table could demonstrate exact-key linkage, structured mechanism coding, missing follow-up, and comparisons across proposed safety-feature fields. All case identifiers and auxiliary values would be fictional. The example would test the workflow only; it would not show that any configuration is common or dangerous.

## Audience B: High School RIO soccer surveillance

### Missing decision input

NEISS lacks a mechanism-specific injury rate for organized high-school soccer. It contains no athlete-exposure denominator and does not reliably identify whether an injury occurred in a high-school practice or competition. A mechanism with many NEISS visits may be common because athletes encounter it frequently, not because it is unusually risky.

### Proposed auxiliary source

The proposed source is the National High School Sports-Related Injury Surveillance Study, collected through High School Reporting Information Online (High School RIO). High School RIO records weekly athlete-practice and athlete-competition exposures, injuries, and injury-event details. It is intended to inform high-school sports safety decisions ([Datalys Center program description](https://www.datalyscenter.org/programs/)).

### Who collects and maintains it

Certified athletic trainers at participating high schools submit weekly exposure reports and individual injury reports. The study is supported by NFHS and has been managed by the Datalys Center for Sports Injury Research and Prevention since 2019. The 2024-25 report describes its school sampling, reporting, and injury definitions ([2024-25 High School RIO summary report](https://www.datalyscenter.org/wp-content/uploads/2025/11/2024-25-High-School-RIO-ORIGINAL-Summary-Report.pdf)).

### What one row represents and useful fields

One injury row represents one reportable injury during an organized high-school practice or competition. The published study definition generally requires medical attention and at least one day of participation restriction after the injury, while fractures, concussions, dental injuries, and exertional heat events are included regardless of time loss.

Verified fields in the published codebook include `Age`, `Sport`, `BodyPart_or_System_Code`, `Injury_or_Illness_Code`, `Outcome`, `Level_of_Play`, and `Event_Type`. Soccer-specific fields include `SO_Surface`, `SO_Specific_Mechanism`, `SO_Activity`, `SO_Position`, and `SO_Location`. The standardized soccer mechanisms include ball contact, goal contact, being stepped on, fallen on, or kicked, slide tackle, player contact, planted-foot rotation, and uneven surface ([High School RIO codebook](https://www.datalyscenter.org/wp-content/uploads/2025/07/High-School-RIO-Codebook-2019-20_FINAL_for-distribution.pdf)). A separate weekly exposure record supplies counts of athlete-practices and athlete-competitions for the school and sport.

### How we would obtain and connect it to NEISS

Datalys publishes aggregate annual reports. Researchers can request de-identified raw High School RIO data through its Data Injury Statistics Clearinghouse. The request requires study aims, methods, requested data, and evidence of Institutional Review Board approval or exemption before release ([Datalys data request process](https://www.datalyscenter.org/request-data/)).

A person-level join is not possible because NEISS has no school, team, location, or shared athlete identifier. We would instead integrate the sources at an aggregate level. NEISS soccer visits would be selected using product code 1267 in any of the three product fields and restricted to an explicitly chosen adolescent age range. We would manually code `Narrative_1` into a small mechanism set aligned as closely as possible with the High School RIO categories. We could then compare, by sex, mechanism, injury category, and school year where possible:

- High School RIO injuries per 1,000 athlete-exposures; and
- weighted NEISS ED-visit burden and severe-disposition measures.

This would be a side-by-side comparison of harmonized groups, not a relational join of individual records.

### What could fail or limit the connection

The two systems observe different populations. High School RIO covers reportable injuries in organized high-school sports, including injuries treated by athletic trainers or physicians that never reach an ED. NEISS includes club, recreational, and informal soccer but only observes injuries treated in an ED. Its age field cannot prove high-school enrollment or NFHS participation.

NEISS narratives may not support reliable mapping to RIO's standardized mechanisms. The systems also use different injury definitions and time periods: NEISS uses treatment dates, while RIO reports by academic year. Schools without a participating athletic trainer may be underrepresented. Finally, total soccer athlete-exposures do not measure exposure to a particular action, such as the number of headers or slide-tackle attempts. The sources should not be merged into one risk estimate or used to claim that a rule caused an injury.

### New question made answerable

The combined data could answer: **Which standardized soccer mechanism has both a comparatively high injury rate in organized high-school soccer and a meaningful adolescent ED burden or severe-disposition signal, making it the strongest candidate for an NFHS Point of Emphasis or prospective pilot?**

### Synthetic fallback

If raw High School RIO data are unavailable, a small synthetic injury table and weekly exposure table could show how to calculate practice and competition rates, map RIO mechanisms to narrative-coded NEISS mechanisms, and compare rate, time loss, and ED severity in one decision table. The synthetic values could demonstrate the method but could not be presented as evidence about real soccer injury risk.
