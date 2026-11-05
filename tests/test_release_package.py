import pytest
from submission.check_release import private_path
@pytest.mark.parametrize('name',['.venv/a','data/raw/neiss2025.xlsx','dataset_neiss-sports-injuries/data/neiss2025.tsv','data/prepared/x.candidates.csv','data/prepared/x.human_approved.reviews.csv','.env','.streamlit/secrets.toml','data/prepared/x_scope_audit_report.md'])
def test_private_release_paths(name):assert private_path(name)
def test_small_runtime_bundle_is_publishable_by_path():
 for name in ['app.py','requirements.txt','validation.pdf','data/prepared/treadmill_2025.csv','data/prepared/treadmill_2025.provenance.json','data/reference/neiss_code_lookup_2025.csv']:assert not private_path(name)

@pytest.mark.parametrize('name',[
 'data/prepared/final_policy_recommendation.md',
 'data/prepared/treadmill_2025.mvp_decision_report.md',
 'data/prepared/treadmill_2025.validation.json',
 'data/prepared/arbitrary_approval_evidence.csv',
 'data\\prepared\\nested\\human-notes.txt',
])
def test_only_declared_prepared_runtime_files_can_be_packaged(name):
 assert private_path(name)

def test_prepared_public_documentation_is_preserved():
 assert not private_path('data/prepared/README.md')
 assert not private_path('data/prepared/mechanism-codebook.md')

def test_git_staging_preserves_hashed_runtime_bytes_across_line_endings(tmp_path):
 import subprocess
 from pathlib import Path
 root=Path(__file__).resolve().parents[1]
 subprocess.run(['git','init','--quiet',str(tmp_path)],check=True)
 (tmp_path/'.gitattributes').write_bytes((root/'.gitattributes').read_bytes())
 names=['data/prepared/treadmill_2025.csv','data/prepared/treadmill_2025.provenance.json','data/prepared/mechanism-codebook.md']
 payload=b'INVENTED byte-preservation fixture\r\nnot real NEISS data\r\n'
 for name in names:
  path=tmp_path/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(payload)
 subprocess.run(['git','-C',str(tmp_path),'add','--','.gitattributes',*names],check=True)
 for name in names:
  assert subprocess.check_output(['git','-C',str(tmp_path),'show',':'+name])==payload
