"""Build the working paper with release metadata locally; never publishes a record.

Requires Python 3.10+, reportlab, pypdf; Pandoc, Tectonic; the STIX Two
and DejaVu fonts bundled under tools/typesetting/fonts. Compiler and runtime
binaries are external dependencies.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
FONT_NAMES=['STIXTwoText-Regular.otf','STIXTwoText-Bold.otf','STIXTwoText-Italic.otf',
            'STIXTwoText-BoldItalic.otf','STIXTwoMath-Regular.otf','DejaVuSans.ttf',
            'DejaVuSans-Bold.ttf','DejaVuSans-Oblique.ttf','DejaVuSansMono.ttf']
def meta_text(value):
    if value['t']=='MetaString':return value['c']
    if value['t']=='MetaInlines':
        return ''.join(x['c'] if x['t']=='Str' else ' ' for x in value['c'])
    raise ValueError('Metadata must be plain text')

def tex_escape(value):
    return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_',
                    '{':r'\{','}':r'\}'}.get(c,c) for c in value)


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def draw_figure(fonts):
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.colors import HexColor, Color, white
    pdfmetrics.registerFont(TTFont('A1Sans',str(fonts/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('A1SansBold',str(fonts/'DejaVuSans-Bold.ttf')))
    out=HERE/'figures';out.mkdir(exist_ok=True)
    c=canvas.Canvas(str(out/'triangle.pdf'),pagesize=(428,195),invariant=1,initialFontName='A1Sans',initialFontSize=8)
    c.setTitle('Exact triangle fixture: same primary answer, different range')
    c.setAuthor('William J Foster')
    ink=HexColor('#172B36');teal=HexColor('#176B83');grey=HexColor('#607780');rust=HexColor('#AE613D')
    x0,x1=38,294; y0,y1=34,170
    X=lambda t:x0+(t-4)*(x1-x0)/4
    Y=lambda s:y0+(s-8.7)*(y1-y0)/3.2
    c.setFont('A1Sans',8); c.setFillColor(ink)
    c.drawString(x0,184,'Signal value');c.drawString(x1-12,10,'Time')
    for s in (9,10,11,11.5):
        c.setStrokeColor(HexColor('#E4EAED'));c.setLineWidth(.5);c.line(x0,Y(s),x1,Y(s))
        c.setFillColor(grey);c.drawRightString(x0-8,Y(s)-3,str(s))
    for t in (4,5,6,7,8):
        c.setFillColor(grey);c.drawCentredString(X(t),y0-14,str(t))
    c.setStrokeColor(grey);c.setLineWidth(.6);c.line(x0,y0,x0,y1);c.line(x0,y0,x1,y0)
    c.setStrokeColor(rust);c.setLineWidth(.9);c.setDash(4,3);c.line(x0,Y(11.5),x1,Y(11.5));c.setDash()
    c.setStrokeColor(grey);c.setLineWidth(1);c.setDash(3,3);c.line(x0,Y(10),x1,Y(10));c.setDash()
    p=c.beginPath();p.moveTo(X(4),Y(10))
    for t,s in [(5,11),(6,10),(7,9),(8,10)]:p.lineTo(X(t),Y(s))
    c.setStrokeColor(teal);c.setLineWidth(2);c.drawPath(p)
    for t,s in [(4,10),(6,10),(8,10)]:
        c.setFillColor(white if t==4 else teal);c.circle(X(t),Y(s),2.7,stroke=1,fill=1)
    c.setFillColor(ink);c.setFont('A1SansBold',8.5)
    c.drawString(310,156,'Primary: reach 11.5?')
    c.setFont('A1Sans',8.2);c.drawString(310,143,'Both answer no.')
    c.setFont('A1SansBold',8.5);c.drawString(310,115,'Exact range')
    c.setFont('A1Sans',9);c.setFillColor(teal);c.drawString(310,102,'[9, 11]')
    c.setFillColor(ink);c.setFont('A1SansBold',8.5);c.drawString(310,73,'Endpoint summary')
    c.setFont('A1Sans',9);c.setFillColor(grey);c.drawString(310,60,'[10, 10]')
    c.setFillColor(grey);c.setFont('A1Sans',7.3);c.drawString(310,29,'Auxiliary: reach 11?')
    c.drawString(310,18,'The answers differ.')
    c.save()

def draw_chain_figure(fonts):
    """Redraw the existing PPP extension witness; no molecular dynamics implied."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, white
    c=canvas.Canvas(str(HERE/'figures/chain-continuation.pdf'),pagesize=(428,230),
                    invariant=1,initialFontName='A1Sans',initialFontSize=8)
    c.setTitle('Same score, different available extension: existing finite chain witness')
    c.setAuthor('William J Foster')
    ink=HexColor('#172B36'); teal=HexColor('#176B83'); rust=HexColor('#AE613D')
    grey=HexColor('#607780'); grid=HexColor('#E4EAED')
    c.setFillColor(ink);c.setFont('A1SansBold',10)
    c.drawCentredString(214,215,'Same score. Same contact map. Different next action.')
    c.setFont('A1Sans',8.4);c.setFillColor(grey)
    c.drawCentredString(214,198,'Both chains: three P beads, score 0, no non-backbone contacts')
    for offset,title,points,target,color,verdict in [
        (22,'Straight chain',[(0,0),(1,0),(2,0)],(1,0),rust,'Blocked: the site is occupied.'),
        (244,'Bent chain',[(0,0),(1,0),(1,1)],(0,1),teal,'Allowed: the site is empty.')]:
        X=lambda x:offset+26+x*47
        Y=lambda y:72+y*47
        c.setFillColor(ink);c.setFont('A1SansBold',9);c.drawString(offset,175,title)
        c.setStrokeColor(grid);c.setLineWidth(.55)
        for i in range(3):c.line(X(i),Y(0)-18,X(i),Y(1)+18)
        for j in range(2):c.line(X(0)-15,Y(j),X(2)+15,Y(j))
        c.setStrokeColor(grey);c.setLineWidth(2.5)
        for a,b in zip(points,points[1:]):c.line(X(a[0]),Y(a[1]),X(b[0]),Y(b[1]))
        for i,(x,y) in enumerate(points):
            c.setFillColor(white);c.setStrokeColor(ink);c.setLineWidth(1.3)
            c.circle(X(x),Y(y),9,stroke=1,fill=1)
            c.setFillColor(ink);c.setFont('A1SansBold',8);c.drawCentredString(X(x),Y(y)-3,'P')
            c.setFont('A1Sans',7);c.setFillColor(grey)
            if y>0:
                c.drawString(X(x)+15,Y(y)-3,str(i))
            else:
                c.drawCentredString(X(x),Y(y)-21,str(i))
        end=points[-1]; ex,ey=X(end[0]),Y(end[1]);tx,ty=X(target[0]),Y(target[1])
        # Offset the directional arrow above the bond so both remain visible.
        ay=ey+25;c.setStrokeColor(color);c.setFillColor(color);c.setLineWidth(1.6)
        c.line(ex,ay,tx+3,ay)
        p=c.beginPath();p.moveTo(tx+3,ay);p.lineTo(tx+10,ay+3);p.lineTo(tx+10,ay-3);p.close()
        c.drawPath(p,fill=1,stroke=0)
        c.setFont('A1Sans',7.4);c.drawCentredString((ex+tx)/2,ay+9,'append west')
        c.setLineWidth(1.3)
        if target in points:
            c.circle(tx,ty,13,stroke=1,fill=0)
        else:
            c.setDash(2,2);c.circle(tx,ty,9,stroke=1,fill=0);c.setDash()
        c.setFillColor(color);c.setFont('A1SansBold',8)
        c.drawString(offset,25,verdict)
    c.setStrokeColor(grid);c.setLineWidth(.8);c.line(214,20,214,180)
    c.save()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pandoc',default=os.environ.get('RPRM_PANDOC') or shutil.which('pandoc'))
    ap.add_argument('--tectonic',default=os.environ.get('RPRM_TECTONIC') or shutil.which('tectonic'))
    ap.add_argument('--font-dir',type=Path,default=os.environ.get('RPRM_FONT_DIR'))
    ap.add_argument('--allow-fetch',action='store_true',help='Allow Tectonic to fetch missing public TeX packages')
    ap.add_argument('--outdir',type=Path,default=HERE.parent/'.process-mechanics-build')
    args=ap.parse_args()
    if not args.pandoc or not args.tectonic or not args.font_dir:ap.error('Supply --pandoc, --tectonic, and --font-dir, or corresponding RPRM_* environment variables.')
    fonts=args.font_dir.resolve()
    for f in FONT_NAMES:
        if not (fonts/f).is_file():ap.error(f'Missing font: {fonts/f}')
    out=args.outdir.resolve();out.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1789084800'
    commands=[]
    def run(cmd,label,input=None,cwd=HERE):
        commands.append([str(c) for c in cmd])
        p=subprocess.run([str(c) for c in cmd],input=input,cwd=cwd,env=env,
                         text=True,encoding='utf-8',errors='replace',capture_output=True)
        (out/f'{label}.stdout.txt').write_text(p.stdout,encoding='utf-8')
        (out/f'{label}.stderr.txt').write_text(p.stderr,encoding='utf-8')
        if p.returncode:raise RuntimeError(f'{label} failed; inspect {out}')
        return p.stdout
    versions={k:run([tool,'--version'],k+'-version').splitlines()[0] for k,tool in [('pandoc',args.pandoc),('tectonic',args.tectonic)]}
    draw_figure(fonts)
    draw_chain_figure(fonts)
    # XeTeX on Windows needs ordinary relative font filenames. Stage these
    # copies of the bundled font inputs only in the disposable build directory.
    (out/'fonts').mkdir(exist_ok=True)
    (out/'figures').mkdir(exist_ok=True)
    for f in FONT_NAMES:shutil.copyfile(fonts/f,out/'fonts'/f)
    shutil.copyfile(HERE/'figures/triangle.pdf',out/'figures/triangle.pdf')
    shutil.copyfile(HERE/'figures/chain-continuation.pdf',out/'figures/chain-continuation.pdf')
    sources=['MANUSCRIPT.md','APPENDICES.md','BIBLIOGRAPHY.md']
    combined='\n\n'.join((HERE/f).read_text(encoding='utf-8') for f in sources)
    # Table labels are built as actual LaTeX labels below, not printed caption text.
    combined=re.sub(r' \{#tbl-[^}]+\}(?=\n)', '', combined)
    (out/'combined.md').write_text(combined,encoding='utf-8')
    ast=json.loads(run([args.pandoc,'-f','markdown+smart+raw_tex+tex_math_dollars','-t','json'], 'parse', combined))
    metadata={k:meta_text(ast['meta'][k]) for k in ['title','subtitle','author','author-given-names',
        'author-family-names','date','version','status','pdf-filename','doi','url','license']}
    if metadata['status']!='Working paper':raise ValueError('This builder is contracted for a working paper')
    if not re.fullmatch(r'10\.\d{4,9}/\S+',metadata['doi']):raise ValueError('Supply a valid DOI')
    if not metadata['url'].startswith('https://zenodo.org/records/'):
        raise ValueError('Supply the Zenodo record URL for the paper')
    full_title=metadata['title']+': '+metadata['subtitle']
    pdf_name=metadata['pdf-filename']
    if Path(pdf_name).name!=pdf_name or not pdf_name.endswith('.pdf'):raise ValueError('PDF name must be a local filename')
    date_value=datetime.strptime(metadata['date'],'%d %B %Y').replace(tzinfo=timezone.utc)
    env['SOURCE_DATE_EPOCH']=str(int(date_value.timestamp()))
    table_widths=[[.24,.76],[.25,.25,.25,.25],[.70,.30],[.29,.71],[.55,.15,.30],[.16,.40,.44]]
    # The long claim ledger may break between rows, with its header repeated.
    table_heights=[240,135,150,245,230,180]
    idx=0
    laid_out=[]
    statement_open=False
    source_block=False
    def is_display(block):
        return (block['t']=='Para' and len(block['c'])==1 and block['c'][0]['t']=='Math'
                and block['c'][0]['c'][0]['t']=='DisplayMath')
    def starts_marked(block,kind,word):
        return (block['t']=='Para' and block['c'] and block['c'][0]['t']==kind
                and block['c'][0]['c'] and block['c'][0]['c'][0]=={'t':'Str','c':word})
    for block_index,b in enumerate(ast['blocks']):
        if statement_open and starts_marked(b,'Emph','Proof.'):
            laid_out.append({'t':'RawBlock','c':['latex',r'\end{samepage}\nopagebreak[3]']})
            statement_open=False
        if starts_marked(b,'Strong','Proposition'):
            if statement_open:raise RuntimeError('Unclosed proposition statement')
            laid_out.append({'t':'RawBlock','c':['latex',r'\Needspace{9\baselineskip}\begin{samepage}']})
            statement_open=True
        if b['t']=='Header':
            level=b['c'][0]
            label=' '.join(x.get('c','') for x in b['c'][2] if x['t']=='Str')
            if source_block:
                laid_out.append({'t':'RawBlock','c':['latex',r'\par\endgroup']})
                source_block=False
            if label.startswith('C.2 '):
                laid_out.append({'t':'RawBlock','c':['latex',r'\begingroup\RaggedRight']})
                source_block=True
            if label.startswith('Appendix A.'):
                laid_out.append({'t':'RawBlock','c':['latex',r'\par\vspace{14pt}{\color{accent}\rule{36pt}{.6pt}}\par\clearpage']})
            elif (level==1 and label.startswith('1. ')) or label.startswith('8.5 '):
                laid_out.append({'t':'RawBlock','c':['latex',r'\clearpage']})
            elif level==1 and label=='References':
                laid_out.append({'t':'RawBlock','c':['latex',r'\Needspace{7\baselineskip}\begingroup\fontsize{10.1}{12.5}\selectfont\setlength{\parskip}{7pt}']})
            else:
                header_space=7 if level==1 else 4
                if label.startswith(('2.2 ', '4.2 ', '5.2 ', '8.2 ', 'B.3 ')):
                    header_space=7
                if label.startswith('5. '):
                    header_space=13
                if label.startswith('Appendix B.'):
                    header_space=18
                if label.startswith('6.3 '):
                    header_space=10
                if label.startswith('8. '):
                    header_space=12
                if (block_index+2<len(ast['blocks']) and ast['blocks'][block_index+1]['t']=='Para'
                        and is_display(ast['blocks'][block_index+2])):
                    header_space=10
                laid_out.append({'t':'RawBlock','c':['latex',f'\\Needspace{{{header_space}\\baselineskip}}']})
        if b['t']=='Table':
            for spec,w in zip(b['c'][2],table_widths[idx]):spec[1]={'t':'ColWidth','c':w}
            laid_out.append({'t':'RawBlock','c':['latex',f'\\Needspace{{{table_heights[idx]}pt}}']})
            idx+=1
        if (b['t']=='Para' and not is_display(b)
                and ' '.join(x.get('c','') for x in b['c'] if x['t']=='Str')
                .startswith('The workflow is therefore a sequence')):
            laid_out.append({'t':'RawBlock','c':['latex',r'\Needspace{5\baselineskip}']})
        if (b['t']=='Para' and not is_display(b)
                and ' '.join(x.get('c','') for x in b['c'] if x['t']=='Str')
                .startswith('RPRM Process Mechanics proposes to connect')):
            laid_out.append({'t':'RawBlock','c':['latex',r'\Needspace{9\baselineskip}']})
        if (not statement_open and b['t']=='Para' and not is_display(b) and block_index+1<len(ast['blocks'])
                and is_display(ast['blocks'][block_index+1])):
            laid_out.append({'t':'RawBlock','c':['latex',r'\Needspace{6\baselineskip}']})
        if is_display(b) and block_index>0 and ast['blocks'][block_index-1]['t']=='Para' and not is_display(ast['blocks'][block_index-1]):
            laid_out.append({'t':'RawBlock','c':['latex',r'\nopagebreak[4]']})
        is_reference=b['t']=='Div' and b['c'][0][0].startswith('bib-')
        if is_reference:
            laid_out.append({'t':'RawBlock','c':['latex',r'\begin{samepage}']})
        laid_out.append(b)
        if is_reference:
            laid_out.append({'t':'RawBlock','c':['latex',r'\end{samepage}']})
    if statement_open:raise RuntimeError('Proposition has no following proof')
    ast['blocks']=laid_out
    ast['blocks'].append({'t':'RawBlock','c':['latex',r'\endgroup']})
    if idx!=6:raise RuntimeError(f'Expected six intentional tables, found {idx}')
    (out/'manuscript.ast.json').write_text(json.dumps(ast,ensure_ascii=False),encoding='utf-8')
    body=run([args.pandoc,'-f','json','-t','latex','--wrap=preserve','--syntax-highlighting=none'], 'typeset-body',json.dumps(ast))
    # The unnumbered disclosure needs its own hyperlink destination.
    body=body.replace(r'\subsection*{Assistance disclosure}\label',
                      r'\subsection*{Assistance disclosure}\phantomsection\label')
    body=body.replace(r'\texttt{public\_evidence/pc1/}',
                      r'\mbox{\texttt{public\_evidence/pc1/}}')
    # Preserve the abstract's final phrase as a typographic unit, without
    # changing its words or reducing the body font size.
    body=body.replace('what to do next.',r'\mbox{what to do next.}',1)
    body=body.replace('3. Preserve the answer, or preserve the ability to continue',
        r'3. Preserve the answer,\texorpdfstring{\\}{ }or preserve the ability to continue')
    body=body.replace('5. Compose correct parts, then decide what can be reused',
        r'5. Compose correct parts,\texorpdfstring{\\}{ }then decide what can be reused')
    body=body.replace('6.3 Measurement: a number can be computable before its meaning is established',
        r'6.3 Measurement: a number can be computable\texorpdfstring{\\}{ }before its meaning is established')
    template=(HERE/'preamble.tex').read_text(encoding='utf-8')
    title_lines=tex_escape(metadata['title']).replace('Answer Is',r'Answer\\Is')
    subtitle_lines=tex_escape(metadata['subtitle']).replace(': ',r':\\',1)
    fields={'FONTDIR':'fonts','FULLTITLE':tex_escape(full_title),'AUTHOR':tex_escape(metadata['author']),
            'TITLELINES':title_lines,'SUBTITLELINES':subtitle_lines,'RUNNINGTITLE':tex_escape(metadata['title'].upper()),
            'DATE':tex_escape(metadata['date']),'VERSION':tex_escape(metadata['version']),
            'SUBJECT':tex_escape('Methods and development calibration; working paper '+metadata['version']),
            'DOI':tex_escape(metadata['doi']),'DOIURL':'https://doi.org/'+metadata['doi'],
            'FOOTER':tex_escape('WORKING PAPER v'+metadata['version']), 'BODY':body}
    tex=template
    for key,value in fields.items():tex=tex.replace('@@'+key+'@@',value)
    if re.search(r'@@[A-Z]+@@',tex):raise ValueError('Unresolved template token')
    (out/'paper.tex').write_text(tex,encoding='utf-8')
    command=[args.tectonic,'--keep-logs','--keep-intermediates','--outdir',out]
    if not args.allow_fetch:command+=['--only-cached']
    command+=[out/'paper.tex']
    run(command,'compile',cwd=out)
    shutil.copyfile(out/'paper.pdf',HERE/pdf_name)
    from pypdf import PdfReader
    pdf=PdfReader(HERE/pdf_name)
    logs='\n'.join((out/f).read_text(encoding='utf-8',errors='replace') for f in ['compile.stdout.txt','compile.stderr.txt','paper.log'] if (out/f).exists())
    review_path=HERE/'LAYOUT_REVIEW.json'
    review=json.loads(review_path.read_text()) if review_path.exists() else {'status':'NOT_YET_REVIEWED'}
    pdf_hash=sha(HERE/pdf_name)
    if review.get('pdf_sha256')!=pdf_hash:review={'status':'NOT_YET_REVIEWED','note':'Any earlier page review is invalid for these PDF bytes.'}
    inputs=sources+['preamble.tex','build_paper.py','figures/triangle.pdf','figures/chain-continuation.pdf']
    result={'schema':'rprm.process-mechanics.document-build.v2','status':'BUILT','edition':metadata['version'],
        'layout_revision':'A1-PUBLICATION; working-paper release metadata only',
        'metadata':metadata,'metadata_source':'MANUSCRIPT.md YAML header',
        'title':full_title,'author':metadata['author'],'built_at_utc':datetime.now(timezone.utc).isoformat(),
        'source_date_epoch':int(env['SOURCE_DATE_EPOCH']),'pages':len(pdf.pages),
        'inputs':{f:sha(HERE/f) for f in inputs},'pdf':pdf_name,'pdf_sha256':pdf_hash,
        'canonical_sources':sources,'template_is_immutable_during_build':True,
        'font_files_bundled':True,'font_directory_in_companion':'tools/typesetting/fonts',
        'font_files':{f:sha(fonts/f) for f in FONT_NAMES},
        'toolchain':versions,'python':sys.version.split()[0],
        'commands':[['python','build_paper.py','--pandoc','<pandoc-executable>','--tectonic','<tectonic-executable>',
                     '--font-dir','../../tools/typesetting/fonts','--outdir','<disposable-build-directory>']],
        'tex_warnings':{'overfull':len(re.findall(r'Overfull \\[hv]box',logs)),
                        'missing_glyph':len(re.findall(r'Missing character:',logs)),
                        'undefined_reference':len(re.findall(r'Reference .* undefined',logs))},
        'layout_review':review,
        'verification_scope':'Build receipt only. Current PDF and layout checks are separately hash-bound; historical scientific grades remain unchanged.',
        'publication_approved':True,'publication_status_at_build':'Release metadata ready; record operation is separate',
        'doi':metadata['doi'],'record_url':metadata['url'],
        'license':metadata['license'],'publication_event_performed':False}
    # A separate citation for this work; the root Manifesto citation is untouched.
    q=lambda s:json.dumps(s,ensure_ascii=False)
    citation='\n'.join(['cff-version: 1.2.0',
        'message: '+q('If you use this working paper, please cite the record below.'),
        'title: '+q(full_title),'version: '+q(metadata['version']),
        'doi: '+q(metadata['doi']),'url: '+q(metadata['url']),'license: '+q(metadata['license']),
        'authors:', '  - family-names: '+q(metadata['author-family-names']),
        '    given-names: '+q(metadata['author-given-names']),
        'preferred-citation:', '  type: report', '  title: '+q(full_title),
        '  authors:', '    - family-names: '+q(metadata['author-family-names']),
        '      given-names: '+q(metadata['author-given-names']),
        '  year: '+str(date_value.year), '  version: '+q(metadata['version']),
        '  doi: '+q(metadata['doi']),'  url: '+q(metadata['url']),
        '  notes: '+q('Working-paper date: '+metadata['date']+'. Original prose and figures: '+metadata['license']+'.')])+'\n'
    (HERE/'CITATION.cff').write_text(citation,encoding='utf-8')
    (HERE/'DOCUMENT_BUILD.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'BUILT','pages':len(pdf.pages),'pdf_sha256':pdf_hash,'warnings':result['tex_warnings']},indent=2))

if __name__=='__main__':main()
