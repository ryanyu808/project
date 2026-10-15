# Vision — CPSC Treadmill Injury Dashboard

Our stakeholder is a member of the CPSC epidemiology team who needs to decide which types of treadmill injuries among adults aged 65 and older deserve further investigation. The dashboard will provide a quick way to compare injury mechanisms based on estimated national emergency department (ED) visits and how frequently they result in severe outcomes.

For this prototype, we are focusing only on treadmill injuries among adults ages 65–120 rather than the entire sports injury dataset. A case must have product code `3277` in at least one of the three product columns and mention a treadmill in `Narrative_1`. We will use `Weight` to estimate national ED visits and define a severe outcome as a case involving transfer, hospital admission, observation, or death.

The dashboard will help the epidemiology team identify injury mechanisms that may warrant closer investigation by comparing their estimated frequency and severity in one place.