"""Invented-only end-to-end workflow; production validators have no fixture flag."""
import csv,json,hashlib
from copy import deepcopy
from pathlib import Path
import pytest
from review_tools import finalize_approved_dataset as pipeline
from review_tools.transfer_approved_reviews import validate_approvals
from tests.test_review_transfer import fixture,LABELS
from validation.verify_dashboard import compare,extended

@pytest.mark.parametrize('fault',['policy_formula','taxonomy_gap','invalid_adjudication_flag'])
def test_additional_human_gates(fault):
 c,r,p=fixture()
 if fault=='policy_formula':p['policy_approver']='=USERNAME()'
 elif fault=='taxonomy_gap':r[0]['taxonomy_gap']=True;r[0]['human_resolution']=''
 else:r[0]['requires_adjudication']='maybe'
 with pytest.raises(ValueError):validate_approvals(c,r,p,LABELS,'a'*64)

def test_taxonomy_resolution_remains_explicit_and_not_auto_filled():
 c,r,p=fixture();r[0].update(taxonomy_gap=True,human_resolution='INVENTED reviewer verified existing Fall definition fits this invented exercise-use event')
 before=deepcopy(r);assert validate_approvals(c,r,p,LABELS,'a'*64)[0]['injury_mechanism']=='Fall';assert r==before

def make_bundle(tmp_path,monkeypatch,lookup):
 import pandas as pd
 import prepare_data,loader
 from tests.conftest import fixture_data
 data=fixture_data().iloc[:3].copy()
 data.loc[2,'injury_mechanism']='Belt contact';data.loc[2,'Narrative_1']='INVENTED hand caught in moving treadmill belt';data.loc[2,'Disposition']=9;data.loc[2,'is_severe']=False
 candidate=tmp_path/'treadmill_2025.candidates.csv';data.drop(columns='injury_mechanism').to_csv(candidate,index=False,date_format='%Y-%m-%d')
 raw=tmp_path/'invented_source.txt';raw.write_text('INVENTED fixture only, not annual NEISS')
 digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 evidence=dict(schema_version=1,analysis_years=[2025],source_scope='test_fixture',source_checks_passed=True,
 source_files=[dict(path=str(raw),sha256=digest(raw),row_count=3,column_count=25,min_date='2025-01-01',max_date='2025-01-01')],candidate_sha256=digest(candidate),candidate_row_count=3)
 source=tmp_path/'treadmill_2025.source.json';source.write_text(json.dumps(evidence))
 quality=tmp_path/'treadmill_2025.quality.json';quality.write_text('{}')
 book=tmp_path/'mocked_read_workbook.xlsx';book.write_text('INVENTED read boundary mocked')
 template=tmp_path/'original.reviews.csv';template.write_text('INVENTED preserved template')
 # Fingerprints bind exact bytes, including line endings. The fixture must use
 # the same canonical file as the production loader on Windows and Linux.
 from codebook import CODEBOOK_PATH
 codebook=tmp_path/'codebook.md';codebook.write_bytes(CODEBOOK_PATH.read_bytes())
 policy=tmp_path/'policy.md';policy.write_text('INVENTED approved policy')
 look=tmp_path/'lookup.csv';lookup.to_csv(look,index=False)
 approved=[dict(CPSC_Case_Number=r.CPSC_Case_Number,treadmill_confirmed='True',injury_mechanism=r.injury_mechanism,reviewed='True',review_note='INVENTED test approval') for r in data.itertuples()]
 monkeypatch.setattr(pipeline,'validate_inputs',lambda *a:(approved,source,quality,evidence))
 def fixture_source(e,y):
  assert e['source_scope']=='test_fixture' and e['source_files'][0]['row_count']==3
 monkeypatch.setattr(pipeline,'finalize',lambda c,r,b,o:prepare_data.finalize(c,r,b,o,_source_validator=fixture_source))
 def fixture_verify(c,p,l):
  loaded=loader._load_dashboard_data(c,p,l,2025,source_validator=fixture_source)
  with c.open(newline='') as stream:rows=list(csv.DictReader(stream))
  return compare(loaded,rows)
 monkeypatch.setattr(pipeline,'validate_cohort',fixture_verify)
 args=dict(workbook=book,candidates=candidate,template=template,codebook=codebook,policy_document=policy,lookup=look,output_dir=tmp_path/'release')
 return args,digest

def test_complete_invented_pipeline_preserves_inputs_and_checks_dashboard(tmp_path,monkeypatch,lookup):
 args,digest=make_bundle(tmp_path,monkeypatch,lookup)
 before={p:digest(p) for p in tmp_path.iterdir() if p.is_file()}
 dry=pipeline.run(**args);assert dry['status']=='human_review_validated_no_files_written' and not args['output_dir'].exists()
 result=pipeline.run(**args,execute=True);assert result['included']==3
 release=args['output_dir'];report=json.loads((release/'treadmill_2025.validation.json').read_text())
 assert report['status']=='PASS' and report['source_scope']=='test_fixture'
 assert report['scenarios']['all']['severe_record_count']==1
 assert report['scenarios']['all']['unknown_record_count']==1
 from decimal import Decimal
 assert Decimal(report['scenarios']['all']['unknown_weight'])==20
 assert all(digest(p)==v for p,v in before.items())
 assert json.loads((release/'treadmill_2025.provenance.json').read_text())['source_files'][0]['path']=='invented_source.txt'
 provenance=json.loads((release/'treadmill_2025.provenance.json').read_text())
 assert provenance['inclusion_policy_sha256']==digest(args['policy_document'])
 assert provenance['inclusion_policy_id'].endswith('v2')
 with pytest.raises(ValueError,match='Output exists'):pipeline.run(**args,execute=True)

def test_no_publish_when_independent_validation_fails(tmp_path,monkeypatch,lookup):
 args,digest=make_bundle(tmp_path,monkeypatch,lookup)
 before={p:digest(p) for p in tmp_path.iterdir() if p.is_file()}
 def fail(*args):raise ValueError('Invented discrepancy')
 monkeypatch.setattr(pipeline,'validate_cohort',fail)
 with pytest.raises(ValueError,match='discrepancy'):pipeline.run(**args,execute=True)
 assert list(args['output_dir'].iterdir())==[]
 assert all(digest(p)==v for p,v in before.items())

def test_numeric_checker_catches_wrong_export_precision(monkeypatch,visits,lookup,context):
 import views
 from decimal import Decimal
 rows=[]
 for r in visits.fillna('').to_dict('records'):
  r={k:str(v) for k,v in r.items()};r['Disposition']=r['Disposition'].removesuffix('.0');r['Diagnosis']=r['Diagnosis'].removesuffix('.0');rows.append(r)
 original=views.build_weight_reconciliation
 def wrong(*args):
  result=original(*args);result['csv']=result['csv'].replace(b'120.0',b'121.0');return result
 monkeypatch.setattr(views,'build_weight_reconciliation',wrong)
 with pytest.raises(ValueError,match='CSV precision'):compare(dict(data=visits,diagnosis_lookup=lookup,provenance=context),rows)

def test_reproducible_fixture_command_uses_runtime_numeric_types(tmp_path,monkeypatch):
 from validation.run_fixture_checks import main
 import sys
 output=tmp_path/'invented.json'
 monkeypatch.setattr(sys,'argv',['run_fixture_checks.py','--output',str(output)])
 main();report=json.loads(output.read_text())
 assert report['label'].startswith('INVENTED') and report['status']=='PASS'
 assert report['scenarios']['all']['severe_record_count']==3
 assert report['scenarios']['all']['all_unknown_severe_pct']=='75'
