"""Render the standalone O05 short note to a Desktop PDF. Not a verifier."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle

HERE = Path(__file__).resolve().parent
SRC = HERE / "SHORT-NOTE.md"
DEST = Path.home() / "Desktop" / "O05-obstruction-short-note.pdf"


def html_line(line):
    parts = line.split("`")
    html = []
    for index, part in enumerate(parts):
        part = part.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        part = part.replace("**", "")
        if index % 2:
            html.append('<font face="Courier" size="9">' + part + "</font>")
        else:
            html.append(part)
    return "".join(html)


def build(source=SRC, dest=DEST):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontSize=14, spaceAfter=8, leading=18))
    styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontSize=12, spaceBefore=10, spaceAfter=6, leading=15))
    styles.add(ParagraphStyle(name="Bodyx", parent=styles["Normal"], fontSize=10, leading=13, spaceAfter=6))
    styles.add(ParagraphStyle(
        name="CodeX", parent=styles["Code"], fontSize=8, leading=10, spaceAfter=6,
        backColor=colors.Color(0.95, 0.95, 0.95)))
    story = []
    in_code = False
    code_buf = []
    table_rows = []

    def flush_table():
        if not table_rows:
            return
        data = []
        for row in table_rows:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if cells and set("".join(cells).replace("-", "").replace(":", "")):
                data.append([Paragraph(html_line(cell), styles["Bodyx"]) for cell in cells])
        table_rows.clear()
        if not data:
            return
        table = Table(data, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 8))

    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_buf), styles["CodeX"]))
                code_buf = []
                in_code = False
            else:
                flush_table()
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue
        if line.startswith("|"):
            if "---" not in line:
                table_rows.append(line)
            continue
        flush_table()
        if not line.strip():
            continue
        if line.startswith("# "):
            story.append(Paragraph(html_line(line[2:]), styles["H1x"]))
        elif line.startswith("## "):
            story.append(Paragraph(html_line(line[3:]), styles["H2x"]))
        else:
            story.append(Paragraph(html_line(line), styles["Bodyx"]))
    flush_table()
    dest.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(dest), pagesize=letter,
        leftMargin=0.8 * inch, rightMargin=0.8 * inch,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch)
    document.build(story)
    return dest


if __name__ == "__main__":
    path = build()
    print(path, path.stat().st_size)
