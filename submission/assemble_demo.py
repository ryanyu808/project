"""Assemble genuine recorded public footage and narration; never creates scenes.

Supply a manifest only after public-app verification and recording. This tool
checks files, hashes, declarations and durations; it cannot certify truthfulness
of a supplied recording. Default is validation only. Outputs stay outside repo.
"""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def validate_manifest(manifest_path,output):
    manifest_path=Path(manifest_path);output=Path(output).resolve()
    m=json.loads(manifest_path.read_text(encoding='utf-8'))
    if not m.get('public_app_url','').startswith('https://') or any(x in m['public_app_url'].lower() for x in ['localhost','pending','example.']):
        raise ValueError('Actual verified HTTPS public app URL required')
    if m.get('unauthenticated_access_verified') is not True or m.get('genuine_public_footage') is not True:
        raise ValueError('Actual public access/footage verification required; do not infer from local tests')
    if output.is_relative_to(ROOT) or output.suffix.lower()!='.mp4' or output.exists():
        raise ValueError('Use a new MP4 output outside the submitted repository')
    base=manifest_path.resolve().parent
    for key,stream_type in [('footage','video'),('narration','audio')]:
        p=(base/m[key]).resolve()
        if hashlib.sha256(p.read_bytes()).hexdigest()!=m.get(key+'_sha256'):raise ValueError(key+' fingerprint mismatch')
        info=probe(p)
        if not any(s['codec_type']==stream_type for s in info['streams']):raise ValueError(key+' stream missing')
        duration=float(info['format']['duration'])
        if not 270<=duration<=330:raise ValueError(key+' must be approximately five minutes (270-330 seconds)')
        m[key]=str(p);m[key+'_duration']=duration
    if abs(m['footage_duration']-m['narration_duration'])>2:raise ValueError('Footage/narration duration mismatch; synchronize before assembly')
    return m

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
    m=validate_manifest(a.manifest,a.output)
    if not a.execute:print(json.dumps(dict(status='validated_no_video_written',**m),indent=2));return
    a.output.parent.mkdir(parents=True,exist_ok=True)
    # Encode privately and publish with exclusive create, never overwrite a deliverable.
    with tempfile.TemporaryDirectory(dir=a.output.parent) as tmp:
        staged=Path(tmp)/'demo.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',m['footage'],'-i',m['narration'],'-map','0:v:0','-map','1:a:0','-vf','scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(staged)],check=True)
        info=probe(staged)
        if not 270<=float(info['format']['duration'])<=330:raise ValueError('Encoded duration outside expected range')
        with staged.open('rb') as src,a.output.open('xb') as dest:
            import shutil;shutil.copyfileobj(src,dest)
    print(json.dumps(dict(status='assembled_needs_full_visual_audio_review',output=str(a.output),sha256=hashlib.sha256(a.output.read_bytes()).hexdigest()),indent=2))

if __name__=='__main__':main()
