"""Read-only audit of existing entries; never approves, exports or finalizes data."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from contracts import sha256
from review_tools import transfer_approved_reviews as transfer


def approval_provenance(rows):
    """Describe recorded entries without claiming to verify human activity."""
    recorded = [r for r in rows if transfer.text(r.get('human_approval')) in {'Approve','Correct'}]
    transcribed = [r for r in recorded if transfer.text(r.get('human_review_note')).startswith('Recorded by assistant from ')]
    return dict(recorded_approval_count=len(recorded),
                assistant_transcribed_approval_count=len(transcribed),
                informed_human_review_established_by_audit=False,
                transcribed_case_ids_requiring_provenance_verification=[transfer.text(r['CPSC_Case_Number']) for r in transcribed],
                transcribed_adjudication_count=sum(transfer.explicit_true(r.get('requires_adjudication')) for r in transcribed),
                explanation='Populated fields and copied AI reasons cannot establish informed human review. Preserve entries and verify their actual review basis before release; missing external evidence does not prove review never occurred.')


def audit():
    folder = ROOT / 'data/prepared'
    workbook = folder / 'treadmill_2025.ai_completed_review.xlsx'
    candidates = folder / 'treadmill_2025.candidates.csv'
    rows, policy = transfer.read_approval_workbook(workbook)
    original, _ = transfer.read_csv(candidates)
    source = transfer.unique_by_id(original, 'Candidates')
    decisions = transfer.unique_by_id(rows, 'Workbook')
    if set(source) != set(decisions):
        raise ValueError('Workbook/candidate IDs differ')
    labels = transfer.approved_labels(folder / 'mechanism-codebook.md')
    digest = sha256(candidates)
    if policy.get('policy_document_sha256') != sha256(folder / 'final_policy_recommendation.md'):
        raise ValueError('Policy document fingerprint mismatch')
    pending = []
    valid = 0
    for number, row in enumerate(rows, 2):
        case = transfer.text(row['CPSC_Case_Number'])
        try:
            # Reuse the unchanged validator to diagnose each existing entry.
            # This is NOT full production validation and cannot write a release.
            transfer.validate_approvals([source[case]], [row], policy, labels, digest)
            valid += 1
        except ValueError as exc:
            pending.append(dict(case=case, excel_row=number,
                                recommendation=row['recommended_inclusion'],
                                proposed_mechanism=row['recommended_mechanism'],
                                taxonomy_gap=transfer.explicit_true(row.get('taxonomy_gap')),
                                reason=str(exc)))
    return dict(status='read_only_entry_audit_not_release_validation',
                total=len(rows), entries_passing_row_checks=valid, pending=pending,
                approval_provenance=approval_provenance(rows),
                policy_approval_recorded=transfer.explicit_true(policy.get('policy_approved_by_human')),
                policy_mapping_acceptance_recorded=transfer.explicit_true(policy.get('mapping_accepted_by_human')),
                note='Existing attestations only; software cannot establish that a human read the records. Full finalization validation remains mandatory.')


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
