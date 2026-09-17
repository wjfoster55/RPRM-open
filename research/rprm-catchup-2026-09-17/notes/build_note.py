"""Render the standalone note to PDF. Independent of the monograph build."""
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(HERE, "extremal-order-TXP.md")
BODY = os.path.join(HERE, "_note_body.typ")
MAIN = os.path.join(HERE, "_note_main.typ")
PDF = os.path.join(HERE, "extremal-order-TXP.pdf")

TMPL = r'''
#set page(paper: "a4", margin: (x: 2.6cm, y: 2.4cm),
  footer: context [#set align(center); #set text(9pt, fill: rgb("#555"));
    #counter(page).display("1")])
#set text(font: ("Georgia", "Times New Roman", "DejaVu Serif"), size: 10.5pt, lang: "en")
#set par(justify: true, leading: 0.62em, first-line-indent: 0pt, spacing: 0.95em)
#show heading: set text(font: ("Georgia", "Times New Roman"), weight: "bold")
#show heading.where(level: 1): it => block(above: 1.5em, below: 0.85em)[
  #set text(15pt); #it.body]
#show heading.where(level: 2): it => block(above: 1.25em, below: 0.7em)[
  #set text(12pt); #it.body]
#show heading.where(level: 3): it => block(above: 1.0em, below: 0.55em)[
  #set text(10.8pt, style: "italic"); #it.body]
#show raw: set text(font: ("Consolas", "DejaVu Sans Mono"), size: 9pt)
#set table(stroke: (x, y) => (
  top: if y == 0 { 0.7pt } else if y == 1 { 0.5pt } else { 0pt },
  bottom: 0.7pt))
#show table.cell.where(y: 0): strong
#set math.equation(numbering: none)

#align(center)[
  #block(above: 1.2cm, below: 0.3cm)[#text(17pt, weight: "bold")[
    Extremal partition shapes for the order of $T(X, cal(P))$]]
  #block(below: 0.9cm)[#text(11pt, style: "italic", fill: rgb("#444"))[
    Which partition shape admits the most partition-preserving transformations]]
]
#line(length: 100%, stroke: 0.5pt + rgb("#999"))
#v(0.5cm)

#include "_note_body.typ"
'''


def run(cmd):
    print("$", " ".join(cmd[:3]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        raise SystemExit("FAILED: %s" % cmd[0])
    if r.stderr.strip():
        print("stderr:", r.stderr.strip()[:1200])


def main():
    src = io.open(MD, encoding="utf-8").read()
    # the title is rendered by the template; drop the markdown title block
    marker = "## Abstract"
    src = src[src.index(marker):]
    tmp = os.path.join(HERE, "_note_src.md")
    io.open(tmp, "w", encoding="utf-8", newline="").write(src)

    run(["pandoc", "-f",
         "markdown+pipe_tables+tex_math_dollars+backtick_code_blocks-smart",
         "-t", "typst", tmp, "-o", BODY])
    io.open(MAIN, "w", encoding="utf-8", newline="").write(TMPL)

    import typst
    typst.compile(MAIN, output=PDF, root=HERE)
    print("PDF:", PDF, os.path.getsize(PDF), "bytes")
    for f in (tmp, BODY, MAIN):
        os.remove(f)


if __name__ == "__main__":
    main()
