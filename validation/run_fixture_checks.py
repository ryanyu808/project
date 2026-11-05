"""Reproducible, explicitly invented dashboard-number validation, never production."""
import argparse,csv,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from validation.verify_dashboard import compare
def main():
 import pandas as pd
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 fixture=ROOT/'validation/fixtures/invented_visits.csv'
 with fixture.open(newline='') as stream:rows=list(csv.DictReader(stream))
 from contracts import validate_visits
 frame=pd.DataFrame(rows);frame['is_severe']=frame.Disposition.isin(['2','4','5','8'])
 frame=validate_visits(frame,[2025])
 lookup=pd.read_csv(ROOT/'data/reference/neiss_code_lookup_2025.csv',dtype=str)
 result=compare(dict(data=frame,diagnosis_lookup=lookup,provenance=dict(analysis_years=[2025],source_scope='test_fixture')),rows)
 result.update(label='INVENTED FIXTURES ONLY - NOT NEISS FINDINGS',fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest())
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
 print('PASS: invented-fixture dashboard checks saved to '+str(args.output))
if __name__=='__main__':main()
