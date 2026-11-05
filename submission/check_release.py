"""Read-only release audit by default. ZIP creation requires a clean, ready HEAD."""
import argparse,json,re,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['app.py','loader.py','contracts.py','configuration.py','filters.py','views.py','codebook.py','config.toml','pyproject.toml','uv.lock','requirements.txt','.python-version','README.md','validation.pdf','data/prepared/treadmill_2025.csv','data/prepared/treadmill_2025.provenance.json','data/prepared/mechanism-codebook.md','data/reference/neiss_code_lookup_2025.csv']
PUBLIC_PREPARED={'readme.md','mechanism-codebook.md','treadmill_2025.csv','treadmill_2025.provenance.json'}
def private_path(name):
 p=name.lower().replace('\\','/');parts=p.split('/')
 return (any(x in parts for x in ['.git','.venv','.venv-mvp','__pycache__','.pytest_cache','dataset_neiss-sports-injuries']) or p.startswith('data/raw/') or p.endswith(('.xlsx','.candidates.csv','.reviews.csv','.source.json','.quality.json','.inspect.ndjson','.log')) or parts[-1].startswith('.env') and parts[-1]!='.env.example' or p.endswith('secrets.toml') or p.startswith('data/prepared/') and p.removeprefix('data/prepared/') not in PUBLIC_PREPARED)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def audit():
 names=git('ls-tree','-r','--name-only','HEAD').decode().splitlines()
 private=[n for n in names if private_path(n)];secret_files=[];too_large=[]
 token=re.compile(rb'(?:AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
 for n in names:
  content=git('show','HEAD:'+n)
  if len(content)>=100_000_000:too_large.append(n)
  if token.search(content):secret_files.append(n)
 missing=[n for n in REQUIRED if n not in names]
 readme=git('show','HEAD:README.md').decode('utf-8')
 urls_pending=any(x in readme for x in ['[PENDING','[TO COMPLETE'])
 dirty=bool(git('status','--porcelain','--untracked-files=no').strip())
 return dict(ready=not any([private,secret_files,too_large,missing,urls_pending,dirty]),commit=git('rev-parse','HEAD').decode().strip(),tracked_files=len(names),private_paths=private,possible_secret_files=secret_files,oversized_files=too_large,missing_required_files=missing,README_links_pending=urls_pending,tracked_worktree_dirty=dirty,note='HEAD scan only; no secret values printed. Inspect the final ZIP manifest and public app separately.')
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--create-zip',type=Path);args=parser.parse_args();report=audit();print(json.dumps(report,indent=2))
 if args.create_zip:
  if not report['ready']:parser.exit(2,'Release not ready; no ZIP created.\n')
  if args.create_zip.exists():parser.exit(2,'ZIP already exists; do not overwrite.\n')
  subprocess.run(['git','archive','--format=zip','--output',str(args.create_zip.resolve()),'HEAD'],cwd=ROOT,check=True)
  with zipfile.ZipFile(args.create_zip) as z:
   if any(private_path(n) for n in z.namelist()) or args.create_zip.stat().st_size>=2_000_000_000:raise ValueError('Unsafe or oversized archive')
   print(json.dumps(dict(zip=str(args.create_zip),entries=z.namelist()),indent=2))
if __name__=='__main__':main()
