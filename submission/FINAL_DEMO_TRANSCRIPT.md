# Final demo transcript

Synthetic narration: Microsoft Zira Desktop. All application footage comes from native captures of isolated Chrome windows using the deployed live app; no UI or numeric results were recreated. Live segments were edited for narrative framing and the final decision. The native address bar is visible. Timing below refers to the encoded final MP4.

## 00:02-00:23 - opening

Welcome to Team T nine's CPSC Treadmill Injury Dashboard. Imagine you are an epidemiology analyst deciding which injury mechanism deserves your next round of follow up investigation: falls, or belt contact. This is the actual public application at the address shown in the browser. It opens without signing in. We will turn the overview into a concrete investigation shortlist, inspect the evidence, and test what happens when our filters become too narrow.

## 00:24-00:50 - overview

The opening view shows five thousand, one hundred twenty estimated national emergency department visits, from one hundred nine sampled records, with a weighted severe outcome percentage of twenty two point three percent. These are a reviewed subset of visits among older adults that mention a treadmill. Some screened visits were set aside after review. Severe includes transfer, hospital admission, observation, and fatalities recorded in the emergency department. Visits are not unique people, and these estimates do not measure injury risk per treadmill user.

## 00:52-01:16 - comparison

The mechanism summary gives us the comparison behind the decision. Fall accounts for about three thousand, one hundred fourteen estimated visits, from sixty five records. Belt contact accounts for about three hundred thirty visits, from nine records. Belt contact has a severe share of thirty one point six percent, compared with twenty eight point three percent for Fall. A higher percentage from such a small group is not enough to rank Belt contact above Fall. We need burden, supporting counts, and the original narratives together.

## 01:21-01:41 - belt

Here is Belt contact selected on its own. The reliability warning is now directly beside the headline. This group falls below both the minimum estimate and sampled record screens. The survey design coefficient of variation is not calculated. The dashboard therefore does not certify that the estimate is statistically reliable. Belt contact remains a useful category to inspect, but its apparent severe share should not become an automatic investigation priority.

## 01:47-02:04 - fall

Now I select Fall. Its larger observed burden makes it the stronger starting point for this analyst's follow up shortlist. That is an investigation choice, not a conclusion that a treadmill defect caused these injuries. Mechanism labels come from short, reviewed narratives. They cannot establish exposure, explain every initiating event, or replace a detailed investigation.

## 02:09-02:26 - severe

Adding Severe narrows Fall to eighteen sampled records. The selected headline is now one hundred percent severe because severity is the filter we just applied. It is not the severe percentage for all Fall visits. Notice that the reliability warning also follows this smaller selected population. The app keeps the selected records and the all outcome comparison conceptually separate.

## 02:27-02:43 - baseline

The comparison table makes that distinction explicit. The baseline retains all Fall outcomes, while the selection contains only the severe Fall visits. We can compare the severe burden with the full population instead of mistaking a filtered percentage for a population rate. Keeping that denominator visible matters when an analyst explains why these records were selected.

## 02:45-03:03 - narratives

The selected narrative browser turns the aggregate result into records we can follow up. Here I open the severe Fall narratives. The case identifiers and original descriptions give us circumstances to investigate, rather than a claim about causation. An analyst could ask about loss of balance, the surrounding environment, medical events, and the equipment relationship before drawing a stronger conclusion.

## 03:06-03:22 - empty

Typing belt while keeping Fall and Severe produces no matching records. This does not mean there are no belt injuries overall. It means this particular intersection is empty. The message tells us which selection to change and how many records each alternative would restore. That guidance prevents an empty table from looking like a substantive finding.

## 03:28-03:43 - undo

I reset the controls twice, and then choose Undo reset. The previous Fall, Severe, and belt combination returns, including the empty result and its recovery guidance. A repeated Reset no longer destroys the saved selection. This lets an analyst explore broadly and still return to the exact question they were examining.

## 03:50-04:06 - entry

Next, I reset and select Entering slash exiting. This is a different question: which narratives describe getting onto or off the equipment? The small group has four sampled records and the warning remains visible. No severe outcomes in this small selection cannot establish that entering or exiting is safe, or that a particular training intervention works.

## 04:09-04:22 - getting

I type getting into the narrative search and apply it. The selected count is three. The controls show that the mechanism is still Entering slash exiting. This is a literal text search, not an automatic classification of every possible way someone might describe mounting or leaving the equipment.

## 04:30-04:45 - got-off

I replace the search with got off and apply it. This returns one record. Those two searches must actually be run, because describing them without showing the interaction could hide which population produced the answer. Clearing the search restores all records in the mechanism, so a guessed keyword does not silently define the full investigation.

## 04:54-05:21 - decision

Returning to Fall and Severe, my decision is to begin follow up with this severe Fall shortlist. The dashboard has brought the burden comparison, recorded outcomes, and original narrative evidence into one reproducible workflow. The next step is to investigate the circumstances behind these selected visits, review classification boundaries, and consult official surveillance uncertainty measures. It does not justify declaring a defect, prescribing supervision, or estimating personal injury risk. That is the value of this tool: a clearer, inspectable starting point for investigation, with the limits kept in view.

