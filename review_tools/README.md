# Human review and checked finalization

Use only `data/prepared/treadmill_2025.ai_completed_review.xlsx`. Policy: `data/prepared/final_policy_recommendation.md`, ID injury-focused-2025-proposed-v2. Current AI counts are 108 Include, 72 Exclude, 8 Unresolved. They are screening recommendations, never production findings.

**Human gate is incomplete.** There are 171 recorded approval entries (99 Include, 72 Exclude) and 17 blank priority decisions (eight inclusion, nine mechanisms). All 171 entries were assistant-transcribed from blanket chat endorsement, with AI reasoning copied into notes. Informed case-level review cannot be established from those entries; 59 also have adjudication flags and no independent human resolution. Missing evidence does not prove review never occurred. Preserve all existing values and establish the review basis truthfully. Do not merely repeat a batch approval or treat software acceptance as proof. Workbook policy acceptance also records chat endorsement, while the fingerprinted policy document retains its AI-proposal status; reconcile the team's actual scope/approval record without changing evidence silently.

Read the single private decision table `data/prepared/treadmill_2025.mvp_decision_report.md`. No additional review workbook is needed. The existing Review guide and Human review form remain intact. The first 17 rows are the unresolved priority queue. Amber human fields are editable by the real reviewer; assigned_reviewer is planning only and entry_status reports entries, not genuine verification. The prior Approval review sheet is retained as AI evidence. Do not enter approvals on both sheets or edit original narratives/AI source columns.

`python review_tools/review_readiness.py` is a read-only entry/provenance diagnostic. Its 171 passing row checks are not 171 verified human reviews. It lists the assistant-transcribed case IDs for verification. All 188 original `reviewed` flags in the candidate review template remain False. No review values or policy/source fingerprints were changed by this session.

1. The team reads and agrees the policy, original prompt differences and codebook boundaries. A human fills Policy B3:B6: policy approval, named approver, mapping acceptance and explanation. Do not edit the candidate fingerprint, policy ID or policy-document fingerprint. A changed policy needs a deliberate new review/version, not a stale approval.
2. Read every narrative and its source fields. Resolve the eight Unresolved recommendations with Human Correct and explicit Include/Exclude plus a valid included mechanism. Review the 35 adjudications, 29 reassessed mechanisms and all other rows. Mechanism priority breaks chronological ties; it does not replace the initiating event.
3. Enter actual Human Approve or Correct, explicit human_reviewed=True and reviewer identity. No approval is inferred. Exclusions/corrections require a human note; flagged issues need explanation. Included taxonomy_gap=True requires human_resolution explaining why the unchanged codebook label fits the evidence, or a separately approved taxonomy change. A known uncovered mechanism cannot simply be hidden in Unknown.
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
