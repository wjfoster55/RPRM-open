"""Render MANIFESTO.md to a compact PDF with its four included figures.

Optional build dependencies: reportlab, matplotlib (for DejaVu fonts), pypdf.
No network access, source repository paths or author metadata are embedded.
"""
from functools import partial
from html import escape
from pathlib import Path
import re
from urllib.parse import quote
import matplotlib
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path(matplotlib.get_data_path()) / "fonts/ttf"
BASE = "https://github.com/wjfoster55/RPRM-open/blob/main/"


def rich(text):
    # This is a deliberately small renderer for this source's plain paragraphs,
    # headings, links, emphasis, lists and inline notation; not general Markdown.
    tokens = []
    def keep(value):
        tokens.append(value)
        return f"@@TOKEN{len(tokens)-1}@@"
    text = re.sub(r"`([^`]+)`", lambda m: keep('<font name="Mono" size="9">'+escape(m.group(1))+"</font>"), text)
    def link(match):
        label, target = match.groups()
        if not re.match(r"https?://", target): target = BASE + quote(target, safe="/#")
        return keep('<link color="#176b83" href="'+escape(target, quote=True)+'">'+escape(label)+"</link>")
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for i in range(len(tokens)-1,-1,-1): text = text.replace(f"@@TOKEN{i}@@", tokens[i])
    return text


def main():
    for name, file in (("Body","DejaVuSans.ttf"),("BodyBold","DejaVuSans-Bold.ttf"),
                       ("BodyItalic","DejaVuSans-Oblique.ttf"),("BodyBoldItalic","DejaVuSans-BoldOblique.ttf"),
                       ("Mono","DejaVuSansMono.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR/file)))
    pdfmetrics.registerFontFamily("Body",normal="Body",bold="BodyBold",italic="BodyItalic",boldItalic="BodyBoldItalic")
    ink=colors.HexColor("#142d3a")
    base=ParagraphStyle("Body",fontName="Body",fontSize=9.6,leading=14.1,textColor=ink,
                        spaceAfter=7,alignment=TA_LEFT,allowWidows=0,allowOrphans=0)
    styles={"body":base,
            "title":ParagraphStyle("Title",parent=base,fontName="BodyBold",fontSize=26,leading=31,spaceAfter=12,keepWithNext=True),
            "h2":ParagraphStyle("H2",parent=base,fontName="BodyBold",fontSize=14,leading=19,spaceBefore=14,spaceAfter=8,keepWithNext=True),
            "h3":ParagraphStyle("H3",parent=base,fontName="BodyBold",fontSize=10.5,leading=15,spaceBefore=9,spaceAfter=5,keepWithNext=True),
            "caption":ParagraphStyle("Caption",parent=base,fontSize=8.3,leading=11.8,textColor=colors.HexColor("#405864"),spaceAfter=11),
            "list":ParagraphStyle("List",parent=base,leftIndent=15,firstLineIndent=-12,spaceAfter=4)}
    target=ROOT/"RPRM-Manifesto.pdf"
    doc=SimpleDocTemplate(str(target),pagesize=A4,leftMargin=54,rightMargin=54,
                          topMargin=47,bottomMargin=47,title="The RPRM Manifesto",
                          author="",subject="A relational framework for mathematical unification",
                          creator="RPRM", invariant=1)
    lines=(ROOT/"MANIFESTO.md").read_text(encoding="utf-8").splitlines()
    story=[]; index=0
    while index<len(lines):
        line=lines[index].strip()
        if not line: index+=1; continue
        picture=re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)",line)
        if picture:
            img=Image(str(ROOT/picture.group(2)))
            factor=min(doc.width/img.imageWidth,180/img.imageHeight)
            img.drawWidth=img.imageWidth*factor; img.drawHeight=img.imageHeight*factor
            group=[Spacer(1,7),img,Spacer(1,7)]
            index+=1
            while index<len(lines) and not lines[index].strip(): index+=1
            caption=[]
            if index<len(lines) and lines[index].startswith("*Figure "):
                while index<len(lines) and lines[index].strip(): caption.append(lines[index].strip()); index+=1
                group.append(Paragraph(rich(" ".join(caption)),styles["caption"]))
            story.append(KeepTogether(group)); continue
        heading=re.match(r"^(#{1,3}) (.+)$",line)
        if heading:
            style={1:"title",2:"h2",3:"h3"}[len(heading.group(1))]
            story.append(Paragraph(rich(heading.group(2)),styles[style])); index+=1; continue
        paragraph=[line]; index+=1
        is_list=bool(re.match(r"^\d+\. ",line))
        while index<len(lines) and lines[index].strip():
            if re.match(r"^(#|!\[|\d+\. )",lines[index]): break
            paragraph.append(lines[index].strip()); index+=1
        text = " ".join(paragraph)
        entry = Paragraph(rich(text), styles["list" if is_list else "body"])
        if text.endswith("Its complete fiber is"):
            entry.keepWithNext = True
        story.append(entry)
    story.append(Paragraph("Typeface: DejaVu. Its full license is attached as DejaVu.txt "
                           "and included in the repository's LICENSES directory.", styles["caption"]))
    def page(c, d):
        c.saveState(); c.setFont("Body",7.3); c.setFillColor(colors.HexColor("#526873"))
        c.drawString(54,A4[1]-28,"RPRM  /  A relational framework for mathematical unification")
        c.drawString(54,27,"First release candidate")
        c.drawRightString(A4[0]-54,27,str(d.page)); c.restoreState()
    doc.build(story,onFirstPage=page,onLaterPages=page,canvasmaker=partial(canvas.Canvas,invariant=1))
    # Carry the font notice with a standalone copy of the PDF. This is the only
    # attachment: an exact public license, never an arbitrary source payload.
    reader = PdfReader(target)
    writer = PdfWriter(clone_from=reader)
    writer.add_attachment("DejaVu.txt", (ROOT / "LICENSES/DejaVu.txt").read_bytes())
    temporary = target.with_suffix(".tmp.pdf")
    writer.write(temporary)
    reader.close()
    temporary.replace(target)
    print(target.name)


if __name__=="__main__": main()
