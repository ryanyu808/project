"""Render current full Markdown sources; never load a historical Git PDF.
Document tools: reportlab, Pillow. These are not app dependencies.
"""
from pathlib import Path
from html import escape
import re, textwrap
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles['BodyText'].fontSize=9
styles['BodyText'].leading=13
styles.add(ParagraphStyle(name='Cell',fontSize=7,leading=10,wordWrap='CJK'))
styles.add(ParagraphStyle(name='Output',fontName='Courier',fontSize=7,leading=9))
def markup(s):
    s=escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="blue">\1</link>',s)
    return re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s).replace('`','')
def build(source,destination):
    lines=source.read_text(encoding='utf-8').splitlines(); story=[]; i=0
    while i<len(lines):
        line=lines[i].strip(); i+=1
        if not line or line.startswith('<!--'): continue
        if line.startswith('```'):
            code=[]
            while i<len(lines) and not lines[i].startswith('```'):
                code.extend(textwrap.wrap(lines[i],110,replace_whitespace=False,drop_whitespace=False) or ['']); i+=1
            i+=1; story.append(Preformatted('\n'.join(code),styles['Output']))
        elif line.startswith('|'):
            rows=[line]
            while i<len(lines) and lines[i].startswith('|'): rows.append(lines[i]); i+=1
            rows=[r for r in rows if not re.match(r'^\|[\s:|\-]+$',r)]
            cells=[[Paragraph(markup(c.strip()),styles['Cell']) for c in r.strip('|').split('|')] for r in rows]
            n=max(map(len,cells)); cells=[r+['']*(n-len(r)) for r in cells]
            t=Table(cells,colWidths=[516/n]*n,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1edf2')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.25,colors.lightgrey)]))
            story.extend([t,Spacer(1,10)])
        elif line.startswith('!['):
            m=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line)
            if m:
                caption,path=m.groups(); path=ROOT/path
                with PILImage.open(path) as im: w,h=im.size
                scale=min(516/w,590/h)
                story.extend([Image(str(path),width=w*scale,height=h*scale),Paragraph(markup(caption),styles['Cell']),Spacer(1,10)])
        elif line.startswith('#'):
            level=len(line)-len(line.lstrip('#'))
            story.append(Paragraph(markup(line.lstrip('# ')),styles['Heading'+str(min(level,3))]))
        else:
            while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','![','```','- ','* ')):
                line+=' '+lines[i].strip(); i+=1
            story.append(Paragraph(markup(line),styles['BodyText']))
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8); canvas.drawRightString(564,24,str(doc.page))
    SimpleDocTemplate(str(destination),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=40,bottomMargin=40,title=source.stem,author='Team T9').build(story,onFirstPage=footer,onLaterPages=footer)
if __name__=='__main__':
    for name in ['validation','response-letter']: build(ROOT/(name+'.md'),ROOT/(name+'.pdf'))
    print('Built current complete validation and response letter sources.')
