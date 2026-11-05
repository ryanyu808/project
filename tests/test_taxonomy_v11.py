"""Invented records only: taxonomy contract, fingerprints and human gates."""
from copy import deepcopy
import json
import pytest
from codebook import CODEBOOK_VERSION, MECHANISMS, approved_text, read_codebook
from filters import FilterSelection, apply_filters
from views import build_view_data, build_weight_reconciliation
from review_tools.transfer_approved_reviews import approved_labels, validate_approvals
from tests.test_review_transfer import fixture
from tests.test_loader import make_bundle
from loader import _load_dashboard_data


def test_v11_definitions_are_explicit_and_preserve_chronology():
    text=approved_text()
    assert CODEBOOK_VERSION=='1.2' and len(MECHANISMS)==len(set(MECHANISMS))==7
    assert 'Equipment/cord obstacle or landing falls' in MECHANISMS
    assert 'unpowered treadmill' in text
    assert 'Do not infer non-use' in text
    assert 'if a general fall merely lands on the belt' in text
    assert 'without a preceding fall' in text


@pytest.mark.parametrize('mutation',['version','definition','missing_label'])
def test_mismatched_codebook_never_passes_as_v11(tmp_path,mutation):
    text=approved_text()
    if mutation=='version':text=text.replace('Version: 1.2','Version: 1.0')
    if mutation=='definition':text=text.replace('Do not infer non-use','Assume non-use')
    if mutation=='missing_label':text='\n'.join(l for l in text.splitlines() if not l.startswith('| `Equipment/cord'))+'\n'
    path=tmp_path/'codebook.md';path.write_text(text,encoding='utf-8')
    with pytest.raises(ValueError):approved_labels(path)


def test_new_category_filters_aggregates_and_exports_without_aliasing(visits,lookup,context):
    frame=visits.copy(deep=True);label='Equipment/cord obstacle or landing falls'
    frame.loc[frame.injury_mechanism=='Contact','injury_mechanism']=label
    before=frame.copy(deep=True)
    selected=apply_filters(frame,FilterSelection(mechanisms=(label,)))
    assert selected.CPSC_Case_Number.tolist()==['C','D']
    result=build_view_data(selected,context=context,diagnosis_lookup=lookup)
    assert result['headline']['weighted_ed_visits']==60
    assert result['headline']['record_count']==2
    assert result['quality']['unknown_disposition_weight']==40
    assert label.encode() in build_weight_reconciliation(result,context,{})['csv']
    assert frame.equals(before)


def test_new_label_does_not_create_human_approval_or_resolve_mapping():
    c,r,p=fixture()
    c[0]['Narrative_1']='INVENTED tripped over treadmill equipment while dusting around it'
    r[0]['Narrative_1']=c[0]['Narrative_1']
    r[0].update(human_approval='Correct',human_inclusion='Include',
      human_mechanism='Equipment/cord obstacle or landing falls',taxonomy_gap=True,
      human_resolution='INVENTED reviewer confirms an explicitly non-use obstacle event')
    before=deepcopy(r)
    assert validate_approvals(c,r,p,set(MECHANISMS),'a'*64)[0]['injury_mechanism']==r[0]['human_mechanism']
    assert r==before
    r[0]['human_resolution']=''
    with pytest.raises(ValueError,match='taxonomy gap'):validate_approvals(c,r,p,set(MECHANISMS),'a'*64)


@pytest.mark.parametrize('fault',['old_version','wrong_hash','wrong_lookup_hash'])
def test_loader_binds_current_version_and_exact_definition_bytes(tmp_path,visits,fault):
    csv,path,lookup,year=make_bundle(tmp_path,visits)
    prov=json.loads(path.read_text())
    if fault=='old_version':prov['codebook_version']='1.0'
    elif fault=='wrong_hash':prov['codebook_sha256']='c'*64
    else:prov['diagnosis_lookup_sha256']='c'*64
    path.write_text(json.dumps(prov))
    with pytest.raises(ValueError,match='codebook|lookup'): _load_dashboard_data(csv,path,lookup,year,source_validator=lambda p,y:None)


def test_old_nonuse_label_is_not_silently_aliased_in_production(tmp_path,visits):
    import pandas as pd
    from contracts import sha256
    csv,path,lookup,year=make_bundle(tmp_path,visits)
    frame=pd.read_csv(csv);frame.loc[0,'injury_mechanism']='Non-use equipment/cord-related falls'
    frame.to_csv(csv,index=False)
    prov=json.loads(path.read_text());prov['prepared_sha256']=sha256(csv);path.write_text(json.dumps(prov))
    with pytest.raises(ValueError,match='label absent'):
        _load_dashboard_data(csv,path,lookup,year,source_validator=lambda p,y:None)


def test_operating_surface_falls_remain_separate_from_equipment_role(visits,lookup,context):
    from views import build_severity_comparison
    frame=visits.copy();label='Equipment/cord obstacle or landing falls'
    frame.loc[frame.injury_mechanism=='Contact','injury_mechanism']=label
    selected=apply_filters(frame,FilterSelection(severities=('Severe',)))
    table=build_severity_comparison(selected,frame,context=context,diagnosis_lookup=lookup).set_index('injury_mechanism')
    assert table.loc['Fall','baseline_weighted_ed_visits']==40
    assert table.loc['Fall','selected_severe_weighted_ed_visits']==10
    assert table.loc[label,'baseline_weighted_ed_visits']==60
    assert table.loc[label,'selected_severe_weighted_ed_visits']==20
