# Current production release - November 5, 2026

The final four mappings and the Equipment/cord obstacle or landing falls clarification were explicitly accepted in Ryan Yu's FINAL RELEASE message. All 188 reviews now pass the existing human/policy/source verification guards: 109 Include / 79 Exclude; zero holds. The original 171 approval rows are unchanged, supported by Ryan's subsequent explicit personal-review confirmation. The eight relationship mappings record this specific authorization without claiming additional independent inspection. Earlier AI/source fields and original reviewed=False fields remain intact. Original source, candidates, blank review template, inclusion-policy bytes/fingerprint and one-shot prompt are unchanged.

Version 1.2 describes equipment/cord obstacle or landing involvement without assuming operation, exercise, non-use or initiation of imbalance. Eight equipment cases use it; operating/on-from-surface falls remain Fall, including the approved unpowered supporting-surface case. The inclusion policy remains injury-focused-2025-proposed-v2; only its historical mechanism-version reference is superseded by separately authorized taxonomy versions. Earlier codebooks are archived, and earlier audit notes below are historical.

The unchanged guarded workflow validated and exported actual human decisions, finalized the real source, rejected no cases, and independently checked all production numbers before publishing five outputs. Runtime CSV/provenance are public preparation outputs; human-approved reviews, quality and validation audit files stay private. All retained IDs and Decimal weights match the original approved source. Runtime results: 109 visits / 5119.6280 weighted visits / 22.302804% severe. See validation/REAL_DATA_RESULTS.md. Never overwrite finalized outputs; use a fresh directory for deliberate future releases.

Current software validation: 180 tests pass; actual configured production AppTest and independent real-data/CSV comparisons pass. Public deployment/screenshots/video and submission-ready ZIP remain pending authenticated access and genuine public evidence. No further case approvals are requested.

---

Historical log below; current status above supersedes earlier pending-review statements.

# Human review and checked finalization

Use only `data/prepared/treadmill_2025.ai_completed_review.xlsx`. Policy: `data/prepared/final_policy_recommendation.md`, ID injury-focused-2025-proposed-v2. Current AI counts are 108 Include, 72 Exclude, 8 Unresolved. They are screening recommendations, never production findings.

**Current status, November 5, 2026:** Ryan Yu explicitly confirms the original 171 decisions and supplies eight final inclusion decisions plus nine further inclusion approvals. Membership decisions total 109 Include / 79 Exclude. Version 1.1 supports 184 complete review entries; four conditional Non-use mappings lack use context and remain held. Read the private decision report for their exact narratives and the single pending taxonomy/context choice. No repeat approval of the original 171 is requested absent a substantive change.

The v2 inclusion-policy file/fingerprint and original AI/source sheets remain unchanged. Ryan's separately recorded v1.1 authorization supersedes the policy's historical mechanism-version reference only. The current Codebook 1.1 sheet and docs/MECHANISM_CHANGELOG.md preserve this versioned extension; do not rewrite old AI recommendations. Human corrections are separate input fields.

Read the single private decision table `data/prepared/treadmill_2025.mvp_decision_report.md`. No additional review workbook is needed. The existing Review guide and Human review form remain intact. The first 17 rows preserve the original priority queue; current human fields identify only four held mappings. Amber human fields are editable by the real reviewer; assigned_reviewer is planning only and entry_status reports entries, not genuine verification. The prior Approval review sheet is retained as AI evidence. Do not enter approvals on both sheets or edit original narratives/AI source columns.

`python review_tools/review_readiness.py` is a read-only entry/provenance diagnostic. Its row checks alone cannot establish human activity. The assistant-transcription flag describes historical entry origin; read the subsequent explicit personal-review confirmation in the private record rather than treating that flag as a new request to reapprove the 171. All 188 original `reviewed` flags in the candidate review template remain False. Only Ryan's explicitly supplied, supported new decisions were transcribed; the source/AI values, original 171 human rows and policy/source fingerprints are unchanged.

1. Policy B3:B6 already record Ryan's accepted policy, named approval and inclusion mapping. The version 1.1 addendum is recorded separately; do not require repeat acceptance absent a substantive change. Do not edit the candidate fingerprint, policy ID or policy-document fingerprint. A changed policy needs a deliberate new review/version, not a stale approval.
2. Read every narrative and its source fields. The eight original Unresolved recommendations now have Ryan's explicit Human Correct decisions. Preserve them; resolve only the four held mechanisms with a defensible approved definition. The earlier 35 adjudications and 29 mechanism reassessments remain audit history; the full-cohort migration found no definite additional change among the prior approvals. Mechanism priority breaks chronological ties; it does not replace the initiating event.
3. Enter actual Human Approve or Correct, explicit human_reviewed=True and reviewer identity. No approval is inferred. Exclusions/corrections require a human note; flagged issues need explanation. Included taxonomy_gap=True requires human_resolution explaining why the current approved codebook label fits the evidence, or a separately approved taxonomy change. A known uncovered mechanism cannot simply be hidden in Unknown.
4. Save and close the workbook. The original candidate CSV and blank review template must remain unchanged. The prior broader-scope column is historical comparison, not the selected injury policy.

Validate all actual approvals without creating files, from the repository root:

```powershell
.\.venv-mvp\Scripts\python.exe review_tools/finalize_approved_dataset.py --workbook data/prepared/treadmill_2025.ai_completed_review.xlsx --candidates data/prepared/treadmill_2025.candidates.csv --template data/prepared/treadmill_2025.reviews.csv --codebook data/prepared/mechanism-codebook.md --policy-document data/prepared/final_policy_recommendation.md --lookup data/reference/neiss_code_lookup_2025.csv --output-dir data/prepared
```

This is expected to reject the current workbook at the first pending case. Only after actual human verification and a successful validation, repeat that exact command with `--execute` appended. Do not add --execute to bypass a rejection.

The workflow validates the workbook/policy fingerprint and all decisions, source/candidate IDs and fingerprints, then copies inputs to a temporary private workspace. It exports a separate human-approved review CSV, invokes the existing prepare_data.finalize, checks provenance and exact Decimal weight preservation, and compares independent arithmetic with the actual dashboard builders and export. It publishes nothing until those checks pass. No production validation-bypass or fixture flag exists.

Outputs (existing files are rejected, never overwritten): treadmill_2025.csv, treadmill_2025.provenance.json, treadmill_2025.human_approved.reviews.csv, treadmill_2025.finalization.quality.json and treadmill_2025.validation.json. Only the final small CSV/provenance are runtime publication inputs. Reviews and quality/audit outputs remain private. The original quality/source files are preserved. Public provenance retains every fingerprint and source count/date but uses the raw filename instead of a personal absolute path; original full source evidence stays local.

If interrupted during file publication, preserve the partial output for inspection and use a fresh output directory; do not overwrite it. A matching CSV/provenance and successful validation report are required before release.

Run the independent post-approval checker separately (new report path required):

```powershell
.\.venv-mvp\Scripts\python.exe validation/verify_dashboard.py --cohort data/prepared/treadmill_2025.csv --provenance data/prepared/treadmill_2025.provenance.json --lookup data/reference/neiss_code_lookup_2025.csv --output validation/results/real_2025_dashboard_check.json
```

No complete actual 188-record review was transferred or finalized. Tests approve only explicitly invented fixture records. Software cannot establish that a reviewer genuinely read a narrative; named team members remain responsible for truthful attestations.
