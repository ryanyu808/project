# Individual Project Vision

## 1. What are you proposing, and for whom?

I propose a Sports Injury Risk Dashboard that helps athletic program administrators and coaches identify patterns in sports related injuries and decide where prevention efforts should be focused. The tool would use NEISS sports injury data to show which sports have the most reported injuries, what types of injuries are common, which age groups are most affected, and how injury patterns change throughout the year.

A user could select a sport, age group, and time period from simple dropdown menus. The dashboard would then display charts showing common diagnoses, affected body parts, injury trends over time, and the proportion of cases resulting in hospital admission. For example, an administrator planning safety initiatives for a youth sports program could select soccer and a younger age group and examine the most common injuries and when they occur. Based on those results, the administrator could decide whether to focus resources on specific safety training, equipment, or prevention programs. The main interface would include filters at the top, summary statistics, and several charts that update based on the user's selections.

## 2. Why is it relevant?

High school sports organizations need to make safety decisions while still keeping the sport practical and accessible for athletes and schools. For soccer, understanding which injuries occur most often and which result in more serious outcomes can help decision makers determine where prevention efforts should be focused. Without a tool like this, stakeholders may have to review injury reports or broad statistics separately, making it harder to identify patterns that could support a specific safety action.

This tool would help by turning the NEISS injury data into information that is easier to compare and use. Stakeholders could examine adolescent soccer injuries by factors such as diagnosis, body part, age, and disposition and identify patterns that may deserve additional investigation. The goal would not be for the tool to automatically recommend a rule change. Instead, it would help NFHS safety stakeholders decide which injury issue should receive further attention, such as becoming a Point of Emphasis or being studied through a prospective safety pilot. This approach is useful because it supports the decision with injury data while still allowing stakeholders to consider practical factors such as cost, athlete participation, and whether a proposed intervention would actually be realistic for high schools.

## 3. Why is it feasible?

This tool is feasible because the assigned NEISS sports injury dataset already contains many of the fields needed for the analysis. Each row represents an injury case reported through a participating emergency department. Relevant fields include the patient’s age, treatment date, diagnosis, body part injured, disposition, and product or sport information. I would first use Python and pandas to clean and filter the data to adolescent soccer injuries. I could then group the cases by factors such as age, diagnosis, body part, and disposition to identify patterns and create summary statistics and visualizations.

One limitation is that NEISS emergency department data does not capture every high school soccer injury or provide a direct measure of athlete exposure, such as the number of practices or games played. Because of this, the tool should not treat the number of NEISS cases as a true injury rate. To provide more context, I would use High School RIO data, which tracks injuries and athlete exposures in U.S. high school sports. This auxiliary source would supplement the NEISS analysis rather than being directly joined to individual NEISS cases.

For implementation, I would use pandas for cleaning and analyzing the data and Streamlit to create an interactive interface with filters, charts, and summary results. The cleaned data could initially be stored in CSV files because the project is relatively small. These tools would provide a better path from the existing injury data to a functional application.

## 4. What is novel?

Existing resources provide useful injury information, but they are not designed specifically to support NFHS decision making about adolescent soccer safety. For example, the CPSC NEISS Query Builder allows users to filter injury records by variables such as age, product, diagnosis, body part, and disposition and obtain national injury estimates. However, it is primarily a general injury data query system rather than a tool that translates the data into a soccer specific safety decision.

My proposed tool would build on this existing data by focusing specifically on adolescent soccer injuries and organizing the results around a decision that NFHS stakeholders could act on. Instead of only returning injury records or estimates, the tool would highlight patterns in injury type, affected body part, severity, and timing and allow stakeholders to compare these patterns through an interactive interface. This is relevant because NFHS already uses Points of Emphasis to draw attention to issues in high school soccer, including safety related topics such as player equipment.

The main contribution is therefore not a new injury database, but a decision support layer connecting existing injury evidence to a specific high school soccer safety workflow. Combining NEISS patterns with contextual information from high school injury surveillance could also help distinguish issues that appear frequently in emergency department data from issues that may warrant further investigation in the high school setting. The tool would not automatically decide that a rule should change. Instead, it would help stakeholders identify and prioritize an injury mechanism for further investigation, a potential Point of Emphasis, or a prospective safety pilot.

## References

https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data/Instructions-for-Using-the-NEISS-Estimates-Query-Builder

https://www.nfhs.org/sports/soccer/resources?

https://nfhs.org/resources/sports/soccer-points-of-emphasis-2026-27