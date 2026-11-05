"""Validate human review, finalize privately, and publish a checked runtime bundle.

Without --execute this is validation only. No production bypass or fixture flag.
Existing artifacts and every source/candidate/review template remain untouched.
"""
import argparse,csv,hashlib,json,shutil,sys,tempfile
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from review_tools import transfer_approved_reviews as transfer
from prepare_data import finalize
from contracts import validate_source_evidence,sha256
from validation.verify_dashboard import validate_cohort

def validate_inputs(workbook,candidates,template,codebook,policy_document):
    candidates,template,codebook,policy_document=map(Path,(candidates,template,codebook,policy_document))
    rows,_=transfer.read_csv(candidates);blank,fields=transfer.read_csv(template)
    if fields!=transfer.FIELDS or set(transfer.unique_by_id(blank,'Template'))!=set(transfer.unique_by_id(rows,'Candidates')):raise ValueError('Template schema/IDs mismatch')
    decisions,policy=transfer.read_approval_workbook(workbook)
    if policy.get('policy_document_sha256')!=sha256(policy_document):raise ValueError('Policy document fingerprint mismatch')
    approved=transfer.validate_approvals(rows,decisions,policy,transfer.approved_labels(codebook),sha256(candidates))
    stem=candidates.name.removesuffix('.candidates.csv')
    source=candidates.with_name(stem+'.source.json');quality=candidates.with_name(stem+'.quality.json')
    evidence=json.loads(source.read_text(encoding='utf-8'))
    validate_source_evidence(evidence,evidence['analysis_years'][0])
    if evidence['source_scope']!='full_annual':raise ValueError('Production requires full_annual')
    if evidence['candidate_sha256']!=sha256(candidates) or evidence['candidate_row_count']!=len(rows):raise ValueError('Candidate/source evidence mismatch')
    if sha256(evidence['source_files'][0]['path'])!=evidence['source_files'][0]['sha256']:raise ValueError('Raw annual source fingerprint changed')
    if not quality.exists():raise ValueError('Candidate quality report missing')
    return approved,source,quality,evidence

def run(workbook,candidates,template,codebook,policy_document,lookup,output_dir,execute=False):
    candidates=Path(candidates);output_dir=Path(output_dir)
    approved,source,quality,evidence=validate_inputs(workbook,candidates,template,codebook,policy_document)
    stem=candidates.name.removesuffix('.candidates.csv')
    result=dict(status='human_review_validated_no_files_written',candidates=len(approved),included=sum(r['treadmill_confirmed']=='True' for r in approved))
    if not execute:return result
    names=[stem+'.csv',stem+'.provenance.json',stem+'.human_approved.reviews.csv',stem+'.finalization.quality.json',stem+'.validation.json']
    if any((output_dir/n).exists() for n in names):raise ValueError('Output exists; use a new output directory, never overwrite a release')
    inputs=[Path(workbook),candidates,Path(template),Path(codebook),Path(policy_document),source,quality,Path(lookup)]
    before={p:sha256(p) for p in inputs}
    output_dir.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.review-finalize-',dir=output_dir.parent) as tmp:
        stage=Path(tmp);copied=stage/candidates.name
        for p in [candidates,source,quality]:shutil.copyfile(p,stage/p.name)
        reviews=stage/(stem+'.human_approved.reviews.csv')
        transfer.export_new_csv(reviews,approved,inputs)
        final=finalize(copied,reviews,codebook,stage)
        original_rows,_=transfer.read_csv(candidates)
        original_weights={r['CPSC_Case_Number']:Decimal(r['Weight']) for r in original_rows}
        final_rows,_=transfer.read_csv(final)
        if any(Decimal(r['Weight'])!=original_weights[r['CPSC_Case_Number']] for r in final_rows):raise ValueError('Final CSV weight precision differs from original candidates')
        prov_path=stage/(stem+'.provenance.json');prov=json.loads(prov_path.read_text(encoding='utf-8'))
        if prov['review_sha256']!=sha256(reviews) or prov['codebook_sha256']!=sha256(codebook):raise ValueError('Final review/codebook fingerprint mismatch')
        if prov['reviewed_candidate_count']!=len(approved) or prov['prepared_row_count']!=result['included']:raise ValueError('Final review counts do not reconcile')
        if prov['source_files']!=evidence['source_files']:raise ValueError('Finalizer changed original source evidence')
        # Keep raw evidence locally; the runtime contract only needs an identifying
        # filename, not the preparer's personal absolute directory.
        for s in prov['source_files']:s['path']=Path(s['path']).name
        prov['source_path_policy']='Public basename only; original source JSON preserved locally'
        prov['inclusion_policy_id']=transfer.POLICY_ID
        prov['inclusion_policy_sha256']=sha256(policy_document)
        prov_path.write_text(json.dumps(prov,indent=2)+'\n',encoding='utf-8')
        verification=validate_cohort(final,prov_path,lookup)
        verification.update(policy_id=transfer.POLICY_ID,policy_document_sha256=sha256(policy_document),reviewed_candidate_count=len(approved))
        (stage/(stem+'.validation.json')).write_text(json.dumps(verification,indent=2,default=str)+'\n',encoding='utf-8')
        if any(sha256(p)!=digest for p,digest in before.items()):raise ValueError('Input changed during finalization; nothing published')
        mapping={names[0]:final,names[1]:prov_path,names[2]:reviews,names[3]:stage/(stem+'.quality.json'),names[4]:stage/(stem+'.validation.json')}
        # Exclusive creation prevents overwriting a concurrent/earlier release.
        for name,path in mapping.items():
            with path.open('rb') as src,(output_dir/name).open('xb') as dest:shutil.copyfileobj(src,dest)
    result.update(status='checked_human_reviewed_bundle_created',output_dir=str(output_dir),files=names)
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['workbook','candidates','template','codebook','policy-document','lookup','output-dir']:parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--execute',action='store_true',help='Only after actual human approvals; absent means read-only validation')
    args=vars(parser.parse_args())
    try:print(json.dumps(run(**args),indent=2))
    except (ValueError,OSError,KeyError) as exc:parser.exit(2,'Review/finalization rejected: '+str(exc)+'\n')

if __name__=='__main__':main()
