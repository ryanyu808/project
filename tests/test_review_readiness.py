"""Provenance reporting uses invented records and never changes approvals."""
from copy import deepcopy
from review_tools.review_readiness import approval_provenance


def test_transcribed_attestation_is_flagged_without_revoking_or_verifying_it():
    rows=[dict(CPSC_Case_Number='INVENTED-1',human_approval='Approve',human_reviewed=True,
               reviewer='INVENTED reviewer',requires_adjudication=True,
               human_review_note='Recorded by assistant from INVENTED chat endorsement')]
    before=deepcopy(rows)
    result=approval_provenance(rows)
    assert result['recorded_approval_count']==result['assistant_transcribed_approval_count']==1
    assert result['transcribed_case_ids_requiring_provenance_verification']==['INVENTED-1']
    assert result['transcribed_adjudication_count']==1
    assert result['informed_human_review_established_by_audit'] is False
    assert rows==before


def test_notes_and_booleans_alone_never_prove_informed_review():
    rows=[dict(CPSC_Case_Number='INVENTED-2',human_approval='Correct',human_reviewed=True,
               reviewer='INVENTED reviewer',human_review_note='INVENTED case-specific note'),
          dict(CPSC_Case_Number='INVENTED-3',human_approval='Defer',human_reviewed=False)]
    result=approval_provenance(rows)
    assert result['recorded_approval_count']==1
    assert result['assistant_transcribed_approval_count']==0
    assert result['informed_human_review_established_by_audit'] is False
