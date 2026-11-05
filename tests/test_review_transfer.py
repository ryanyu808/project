"""Only invented records are approved in these tests; no production file is read/written."""
from copy import deepcopy
import csv
from pathlib import Path
import pytest
from review_tools.transfer_approved_reviews import validate_approvals, export_new_csv, FIELDS, POLICY_ID

LABELS={'Repair/moving','Entering/exiting','Belt contact','Struck by equipment','Fall','Unknown/Unclassified'}


def fixture():
    candidates=[{'CPSC_Case_Number':'0001','Narrative_1':'INVENTED: fell while walking on treadmill'},
                {'CPSC_Case_Number':'0002','Narrative_1':'INVENTED: medical symptoms without injury'}]
    rows=[]
    for c,decision,mechanism in zip(candidates,['Include','Exclude'],['Fall','Unknown/Unclassified']):
        rows.append(dict(**c,recommended_inclusion=decision,recommended_mechanism=mechanism,
                         human_approval='Approve',human_inclusion='',human_mechanism='',human_reviewed=True,
                         reviewer='Invented reviewer',human_review_note='Invented fixture decision only',
                         human_resolution='',requires_adjudication=False))
    policy=dict(policy_id=POLICY_ID,codebook_version='1.2',candidate_sha256='a'*64,
                policy_approved_by_human=True,policy_approver='Invented reviewer',mapping_accepted_by_human=True,
                policy_note='INVENTED policy acceptance for a unit test only')
    return candidates,rows,policy


def test_transfer_copies_explicit_human_verification_and_excludes_mechanism():
    c,r,p=fixture();original=deepcopy(r)
    out=validate_approvals(c,r,p,LABELS,'a'*64)
    assert [v['CPSC_Case_Number'] for v in out]==['0001','0002']
    assert [v['treadmill_confirmed'] for v in out]==['True','False']
    assert out[0]['injury_mechanism']=='Fall' and out[1]['injury_mechanism']==''
    assert all(v['reviewed']=='True' for v in out)
    assert r==original


@pytest.mark.parametrize('failure',['approval','defer','reviewed','reviewer','duplicate','missing','foreign',
    'mechanism','human_mechanism','unresolved','narrative','reason','resolution','policy','mapping','hash','formula'])
def test_transfer_rejects_unverified_or_inconsistent_rows(failure):
    c,r,p=fixture()
    if failure=='approval':r[0]['human_approval']=''
    if failure=='defer':r[0]['human_approval']='Defer'
    if failure=='reviewed':r[0]['human_reviewed']='False'
    if failure=='reviewer':r[0]['reviewer']=''
    if failure=='duplicate':r[1]['CPSC_Case_Number']='0001'
    if failure=='missing':r.pop()
    if failure=='foreign':r[1]['CPSC_Case_Number']='FOREIGN'
    if failure=='mechanism':r[0]['recommended_mechanism']='Invented category'
    if failure=='human_mechanism':r[0]['human_mechanism']='Invented category'
    if failure=='unresolved':r[0]['recommended_inclusion']='Unresolved'
    if failure=='narrative':r[0]['Narrative_1']='Edited text'
    if failure=='reason':r[1]['human_review_note']=''
    if failure=='resolution':r[0].update(requires_adjudication=True,human_review_note='')
    if failure=='policy':p['policy_approved_by_human']='False'
    if failure=='mapping':p['mapping_accepted_by_human']='False'
    if failure=='hash':p['candidate_sha256']='b'*64
    if failure=='formula':r[0]['human_reviewed']='=TRUE()'
    with pytest.raises(ValueError):validate_approvals(c,r,p,LABELS,'a'*64)


def test_unresolved_requires_explicit_correction_and_resolution():
    c,r,p=fixture();r[0].update(recommended_inclusion='Unresolved',human_approval='Correct',
                             human_inclusion='Include',human_mechanism='Fall',requires_adjudication=True,
                             human_review_note='Invented human correction resolving eligibility')
    assert validate_approvals(c,r,p,LABELS,'a'*64)[0]['injury_mechanism']=='Fall'


def test_export_refuses_template_and_existing_file_and_preserves_input(tmp_path):
    c,r,p=fixture();rows=validate_approvals(c,r,p,LABELS,'a'*64)
    template=tmp_path/'original.csv';template.write_text('UNCHANGED')
    with pytest.raises(ValueError):export_new_csv(template,rows,[template])
    assert template.read_text()=='UNCHANGED'
    output=tmp_path/'approved.csv';export_new_csv(output,rows,[template])
    with output.open(newline='') as stream:
        reader=csv.DictReader(stream);assert reader.fieldnames==FIELDS
        assert len(list(reader))==2
    before=output.read_bytes()
    with pytest.raises(FileExistsError):export_new_csv(output,rows,[template])
    assert output.read_bytes()==before

# Additional CLI tests mock Excel reading; all decisions remain invented fixtures.
@pytest.mark.parametrize('mode',['dry_run','write','missing_write_confirmation','missing_row_approval'])
def test_cli_validates_before_writing_and_requires_explicit_write_confirmation(tmp_path,monkeypatch,mode):
    import hashlib
    from review_tools import transfer_approved_reviews as tool
    c,r,p=fixture()
    candidates=tmp_path/'candidates.csv'
    with candidates.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['CPSC_Case_Number','Narrative_1'])
        writer.writeheader();writer.writerows(c)
    template=tmp_path/'reviews.csv'
    with template.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=FIELDS);writer.writeheader()
        writer.writerows([dict(CPSC_Case_Number=x['CPSC_Case_Number'],reviewed='False') for x in c])
    codebook=tmp_path/'codebook.md'
    from codebook import approved_text
    codebook.write_text(approved_text(), encoding='utf-8')
    p['candidate_sha256']=hashlib.sha256(candidates.read_bytes()).hexdigest()
    monkeypatch.setattr(tool,'read_approval_workbook',lambda path:(r,p))
    output=tmp_path/'human-approved.csv'
    args=['--workbook',str(tmp_path/'mocked.xlsx'),'--candidates',str(candidates),
          '--template',str(template),'--codebook',str(codebook)]
    before=template.read_bytes()
    if mode=='dry_run':
        assert tool.main(args)==0 and not output.exists()
    elif mode=='write':
        assert tool.main(args+['--output',str(output),'--confirm-human-verification'])==0
        assert output.exists()
    elif mode=='missing_write_confirmation':
        with pytest.raises(ValueError,match='confirm-human-verification'):
            tool.main(args+['--output',str(output)])
        assert not output.exists()
    else:
        r[1]['human_approval']=''
        with pytest.raises(ValueError,match='missing approval'):
            tool.main(args+['--output',str(output),'--confirm-human-verification'])
        assert not output.exists()
    assert template.read_bytes()==before
