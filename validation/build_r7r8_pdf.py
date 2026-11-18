"""Append actual R7/R8 evidence without reflowing any existing team case page.

Requires reportlab and pypdf (document-generation tools, not app dependencies).
Base pages come from the exact pre-R7/R8 Git commit, not a recursively edited PDF.
"""
from pathlib import Path
from io import BytesIO
import json
import subprocess
import textwrap
import re
from html import escape
from pypdf import PdfReader, PdfWriter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted, PageBreak, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ROOT=Path(__file__).resolve().parents[1]
BASE='4f6e56b'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CodeSmall',fontName='Courier',fontSize=8,leading=10,spaceAfter=10))
styles.add(ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=8,leading=10))


def text(s):
    s=escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="blue">\1</link>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Courier" size="8">\1</font>',s)
    return Paragraph(s,styles['BodyText'])


def code(s):
    lines=[]
    for line in s.splitlines():
        lines.extend(textwrap.wrap(line,105,replace_whitespace=False,drop_whitespace=False) or [''])
    return Preformatted('\n'.join(lines),styles['CodeSmall'])


def render(story):
    stream=BytesIO()
    SimpleDocTemplate(stream,pagesize=(612,792),leftMargin=42,rightMargin=42,topMargin=38,bottomMargin=38).build(story)
    return PdfReader(BytesIO(stream.getvalue()))


def main():
    original=PdfReader(BytesIO(subprocess.check_output(['git','-c',f'safe.directory={ROOT.as_posix()}','show',BASE+':validation.pdf'],cwd=ROOT)))
    md=(ROOT/'validation.md').read_text(encoding='utf-8')
    section=md.split('### R7.1 publisher-file audit')[1].split('Historical MVP numerical validation follows unchanged.')[0]
    r7=[Paragraph('3. Numbers - R7.1 publisher-file continuation',styles['Heading1'])]
    for p in section.split('\n\n'):
        if p.startswith('|'):
            rows=[[Paragraph(escape(c.strip()),styles['Cell']) for c in line.strip('|').split('|')] for line in p.splitlines() if not line.startswith('| ---')]
            table=Table(rows,colWidths=[162,177,189],repeatRows=1)
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dbe9ed')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.lightgrey)]))
            r7.extend([table,Spacer(1,9)])
        elif p.strip():r7.append(code(p.strip('`\n').removeprefix('text\n')) if p.startswith('```') else text(p.strip()))
    raw=json.loads((ROOT/'validation/results/publisher_2025.json').read_text())
    raw.pop('mechanisms')
    r7 += [PageBreak(),Paragraph('R7.1 actual independent output',styles['Heading1']),
           text('Source metadata and main-result excerpt from publisher_2025.json. The full output, including every mechanism numerator and denominator, remains in the repository.'),
           code(json.dumps(raw,indent=2))]
    first=render(r7)
    r8=[Paragraph('4. Tests - R8.1 calculation-fault continuation',styles['Heading1']),
        text('November 18, 2026. Each following page reproduces a complete actual failing pytest output. Long lines are visually wrapped. Raw outputs and exact mutation definitions are committed alongside the runner. The original calculation file was never changed; child processes compile controlled faulty copies in memory.'),
        text('Correct implementation regression: python -m pytest -q -p no:cacheprovider'),
        code((ROOT/'validation/results/r7r8_regression.txt').read_text()),
        text('Nine new normal tests protect eight main results and import independence. The seven required mutation runs each exited 1 with an assertion failure; all were caught. The overall record count is also normally tested, and the severe Fall count is challenged. These demonstrations do not claim complete mutation coverage.'),
        code('\n'.join(f"{r['metric']}: exit={r['exit_code']}; caught={r['caught']}" for r in json.loads((ROOT/'validation/results/r8/summary.json').read_text())['mutations'])),
        text('The complete command arguments, environment override, source before/after hashes and raw output paths are in validation/results/r8/summary.json. Run python validation/run_result_mutations.py from the repository root to reproduce all seven runs.')]
    for file in sorted((ROOT/'validation/results/r8').glob('*.txt')):
        r8 += [PageBreak(),Paragraph('R8.1: '+file.stem,styles['Heading1']),code(file.read_text(encoding='utf-8'))]
    last=render(r8)
    out=PdfWriter()
    # Printed MVP page numbers and every original case/screenshot remain intact.
    for page in original.pages[:33]:out.add_page(page)
    for page in first.pages:out.add_page(page)
    for page in original.pages[33:]:out.add_page(page)
    for page in last.pages:out.add_page(page)
    out.add_metadata({'/Title':'T9 validation - R7/R8 evidence, November 18, 2026'})
    with (ROOT/'validation.pdf').open('wb') as f:out.write(f)
    current=PdfReader(ROOT/'validation.pdf')
    mapping=list(range(33))+list(range(33+len(first.pages),len(original.pages)+len(first.pages)))
    assert all(original.pages[i].extract_text()==current.pages[j].extract_text() for i,j in enumerate(mapping))
    print(f'Preserved all {len(original.pages)} original pages; added {len(first.pages)} R7 and {len(last.pages)} R8 pages; total {len(current.pages)}.')


if __name__=='__main__':main()
