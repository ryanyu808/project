"""Invented dictionaries only; actual human verification is never manufactured."""
from copy import deepcopy
import pytest
from review_tools.transfer_approved_reviews import review_values

class Sheet:
 def __init__(self,rows):
  headers=list(rows[0]);self.values=[tuple(headers)]+[tuple(r.get(k) for k in headers) for r in rows]
class Book:
 def __init__(self,old,new):self.sheetnames=['Approval review','Human review'];self.sheets={'Approval review':Sheet(old),'Human review':Sheet(new)}
 def __getitem__(self,key):return self.sheets[key]
def invented():
 old=[dict(CPSC_Case_Number='INVENTED-X',Narrative_1='INVENTED fall during treadmill use',recommended_inclusion='Include',recommended_mechanism='Fall',taxonomy_gap='True',requires_adjudication='True',reviewed='False',human_approval=None,human_inclusion=None,human_mechanism=None,human_reviewed=None,reviewer=None,human_review_note=None,human_resolution=None)]
 new=deepcopy(old);new[0].update(human_approval='Approve',human_reviewed=True,reviewer='INVENTED fixture reviewer',human_resolution='INVENTED explanation of an exercise-use fall')
 return old,new
def test_focused_form_preserves_source_and_uses_explicit_invented_entries():
 old,new=invented();before=deepcopy((old,new));values=review_values(Book(old,new))
 assert dict(zip(values[0],values[1]))['human_reviewed'] is True
 assert (old,new)==before and old[0]['human_approval'] is None
@pytest.mark.parametrize('fault',['id','narrative','proposal','flag','legacy_approval'])
def test_focused_form_rejects_conflicts_and_source_edits(fault):
 old,new=invented()
 if fault=='id':new[0]['CPSC_Case_Number']='INVENTED-FOREIGN'
 if fault=='narrative':new[0]['Narrative_1']='INVENTED changed source'
 if fault=='proposal':new[0]['recommended_mechanism']='Belt contact'
 if fault=='flag':new[0]['taxonomy_gap']='False'
 if fault=='legacy_approval':old[0]['human_approval']='Approve'
 with pytest.raises(ValueError):review_values(Book(old,new))
