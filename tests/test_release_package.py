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
