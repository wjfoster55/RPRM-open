"""ReportLab cover for the mathematical book; original design under 0BSD."""
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor


def build_cover(destination, fonts, edition="review"):
    for name, filename in (("CoverSans", "DejaVuSans.ttf"), ("CoverSansBold", "DejaVuSans-Bold.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(fonts / filename)))
    width, height = 504, 720
    c = canvas.Canvas(str(destination), pagesize=(width, height), invariant=1, pageCompression=1)
    c.setTitle("The RPRM Manifesto")
    c.setAuthor("")
    c.setSubject("A relational framework for mathematical unification")
    ink, teal = HexColor("#172B36"), HexColor("#176B83")
    c.setFillColor(HexColor("#FCFCFA"))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    left = 51
    c.setFillColor(teal)
    c.setFont("CoverSansBold", 8)
    c.drawString(left, 644, ("PRIVATE REVIEW EDITION" if edition == "review" else "FIRST EDITION") + "  /  SEPTEMBER 2026")
    c.setStrokeColor(teal)
    c.setLineWidth(1.1)
    c.line(left, 621, width-left, 621)
    c.setFillColor(ink)
    c.setFont("CoverSansBold", 36)
    c.drawString(left, 523, "The RPRM")
    c.drawString(left, 477, "Manifesto")
    c.setFont("CoverSans", 13)
    c.drawString(left, 417, "A relational framework")
    c.drawString(left, 397, "for mathematical unification")
    c.setFont("CoverSans", 9.2)
    c.drawString(left, 162, "Definitions, proofs, applications and proposed tests")
    c.setStrokeColor(HexColor("#C8D2D6"))
    c.setLineWidth(.5)
    c.line(left, 140, width-left, 140)
    c.setFont("CoverSans", 8)
    if edition == "review":
        c.drawString(left, 117, "Prepared for review. This copy has not been released.")
    else:
        c.drawString(left, 117, "Original material is freely reusable under the accompanying licenses.")
    c.drawString(left, 102, "The scope and evidence grade of each result are stated in the text.")
    c.showPage()
    c.save()
