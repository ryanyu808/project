"""Invented file/probe boundaries only; never synthesize dashboard evidence."""
import hashlib,json
import pytest
from submission.assemble_demo import validate_manifest


def fixture_manifest(tmp_path):
    for name in ['recording.mp4','voice.wav']:(tmp_path/name).write_bytes(b'INVENTED test bytes; not real footage')
    digest=hashlib.sha256(b'INVENTED test bytes; not real footage').hexdigest()
    m=dict(public_app_url='https://test-app.streamlit.app',unauthenticated_access_verified=True,genuine_public_footage=True,footage='recording.mp4',narration='voice.wav',footage_sha256=digest,narration_sha256=digest)
    path=tmp_path/'test.json';path.write_text(json.dumps(m));return path,m


@pytest.mark.parametrize('fault',['no_public_access','no_genuine_footage','stale_hash','duration','output_exists'])
def test_video_assembly_refuses_missing_or_inconsistent_evidence(tmp_path,monkeypatch,fault):
    from submission import assemble_demo as tool
    p,m=fixture_manifest(tmp_path);out=tmp_path/'output.mp4'
    if fault=='no_public_access':m['unauthenticated_access_verified']=False
    if fault=='no_genuine_footage':m['genuine_public_footage']=False
    if fault=='stale_hash':m['footage_sha256']='a'*64
    if fault=='output_exists':out.write_bytes(b'PRESERVE')
    p.write_text(json.dumps(m))
    monkeypatch.setattr(tool,'probe',lambda path:dict(streams=[dict(codec_type='video'),dict(codec_type='audio')],format=dict(duration='10' if fault=='duration' else '300')))
    with pytest.raises(ValueError):validate_manifest(p,out)
    if fault=='output_exists':assert out.read_bytes()==b'PRESERVE'
