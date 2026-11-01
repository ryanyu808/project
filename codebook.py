"""Read the committed approved definitions; never classify a record at runtime."""
from configuration import ROOT

CODEBOOK_PATH = ROOT / 'data/prepared/mechanism-codebook.md'


def read_codebook(path=CODEBOOK_PATH):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('Version: 1.0'):
        raise ValueError('Expected approved mechanism codebook version 1.0')
    return text
