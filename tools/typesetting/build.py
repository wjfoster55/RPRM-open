"""Build MANIFESTO.md using native TeX mathematics and a ReportLab cover.

Outputs go to a fresh .artifacts/paper directory. This command does not replace
the distributed PDF, publish anything, run mathematical checks or certify layout.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
from urllib.parse import quote, unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FORMAT = "markdown+tex_math_single_backslash+raw_tex"
EPOCH = "1788739200"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(names):
    return {name: sha((ROOT / name).read_bytes()) for name in sorted(set(names))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pandoc", default=shutil.which("pandoc"), help="Pandoc 3.11 executable")
    parser.add_argument("--tectonic", default=shutil.which("tectonic"), help="Tectonic 0.17.0 executable")
    parser.add_argument("--prepare-only", action="store_true", help="Produce retained AST and LaTeX without compiling or merging a PDF")
    parser.add_argument("--allow-fetch", action="store_true", help="Allow Tectonic to acquire missing TeX support files; default uses only its local cache")
    parser.add_argument("--edition", choices=("review", "release"), default="review", help="Cover/footer label only; never publishes the artifact")
    parser.add_argument("--build-id", help="Optional new output-directory name (letters, digits, hyphen or underscore)")
    args = parser.parse_args()
    if not args.pandoc or (not args.prepare_only and not args.tectonic):
        parser.error("Supply Pandoc and, for compilation, Tectonic. See tools/typesetting/README.md.")
    name = args.build_id or str(uuid.uuid4())
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", name):
        parser.error("Invalid build id")
    output_base = (ROOT / ".artifacts/paper").resolve()
    if not output_base.is_relative_to(ROOT):
        parser.error("The generated-output directory must stay within this checkout")
    out = output_base / name
    out.mkdir(parents=True, exist_ok=False)
    receipt = {"schema": "rprm.paper-build.v1", "status": "PENDING", "edition": args.edition, "source_date_epoch": int(EPOCH), "tex_support": "FETCH_ALLOWED" if args.allow_fetch else "ONLY_CACHED", "scope": "Source-bound document conversion. Mathematical verification, every-page layout review and publication are separate."}
    def publish():
        temp = out / "BUILD.tmp"
        temp.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(temp, out / "BUILD.json")
    publish()

    def run(command, label):
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = EPOCH
        process = subprocess.run([str(x) for x in command], cwd=out, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        (out / (label + ".stdout.txt")).write_text(process.stdout, encoding="utf-8")
        (out / (label + ".stderr.txt")).write_text(process.stderr, encoding="utf-8")
        if process.returncode:
            raise RuntimeError(f"{label} failed with exit {process.returncode}; see the retained log")
        return process.stdout

    try:
        versions = {}
        tools = [("pandoc", args.pandoc, "pandoc 3.11")]
        if not args.prepare_only:
            tools.append(("tectonic", args.tectonic, "Tectonic 0.17.0"))
        for label, executable, expected in tools:
            full = Path(shutil.which(executable) or executable).resolve(strict=True)
            actual = run([full, "--version"], label + "-version").splitlines()[0]
            if actual.lower() != expected.lower():
                raise ValueError(f"Expected {expected}; got {actual}. A toolchain change needs a new conversion and layout review.")
            versions[label] = {"version": actual, "executable_sha256": sha(full.read_bytes())}
            if label == "pandoc":
                args.pandoc = full
            else:
                args.tectonic = full
        receipt["toolchain"] = versions
        manifest = json.loads((HERE / "ASSETS.json").read_text(encoding="utf-8"))
        inputs = ["MANIFESTO.md", "tools/build_paper.py", "tools/typesetting/build.py", "tools/typesetting/cover.py", "tools/typesetting/layout_ast.py", "tools/typesetting/preamble.tex", "tools/typesetting/ASSETS.json", "LICENSES/DejaVu.txt", "LICENSES/STIXTwo-OFL.txt", "LICENSES/AMS-MSAM10-OFL.txt"]
        for asset in manifest["assets"]:
            relative = Path(asset["path"])
            resolved = (ROOT / relative).resolve(strict=True)
            if relative.is_absolute() or not resolved.is_relative_to(ROOT):
                raise ValueError("Asset must stay in this checkout")
            if sha(resolved.read_bytes()) != asset["sha256"]:
                raise ValueError("Asset binding changed: " + asset["path"])
            inputs.append(asset["path"])
        before = snapshot(inputs)
        receipt["inputs"] = before
        raw = (ROOT / "MANIFESTO.md").read_bytes()
        text = raw.decode("utf-8")
        (out / "fonts").mkdir()
        (out / "images").mkdir()
        figures = []
        for asset in manifest["assets"]:
            source = ROOT / asset["path"]
            if source.suffix in (".ttf", ".otf"):
                shutil.copyfile(source, out / "fonts" / source.name)
            elif source.suffix == ".svg":
                print_asset = source.with_suffix(".pdf" if source.stem.startswith("two_path_") else ".png")
                relative_print = print_asset.relative_to(ROOT).as_posix()
                if relative_print not in before:
                    raise ValueError("Unbound print asset: " + relative_print)
                needle = "](" + asset["path"] + ")"
                if text.count(needle) != 1:
                    raise ValueError("Each selected figure must occur exactly once: " + asset["path"])
                text = text.replace(needle, "](images/" + print_asset.name + ")")
                shutil.copyfile(print_asset, out / "images" / print_asset.name)
                figures.append({"source": asset["path"], "print_asset": relative_print})
        (out / "reading.md").write_text(text, encoding="utf-8", newline="\n")
        ast = json.loads(run([args.pandoc, "reading.md", "-f", FORMAT, "-t", "json"], "pandoc-source"))
        (out / "reading.ast.json").write_text(json.dumps(ast, ensure_ascii=False), encoding="utf-8")
        layout = load_module("rprm_print_layout", HERE / "layout_ast.py")
        adapted, layout_changes = layout.transform(ast)
        blocks, skip_contents, first_part_chapter = [], False, False
        compact_chapter = False
        header_changes = []
        for node in adapted["blocks"]:
            if node.get("t") == "Header":
                level, attr, content = node["c"]
                title = layout.plain(content)
                if title == "The RPRM Manifesto":
                    header_changes.append({"title": title, "treatment": "Title retained on separate cover and PDF metadata."})
                    continue
                if title == "Contents":
                    blocks.append(layout.raw(r"\clearpage\tableofcontents\clearpage"))
                    skip_contents = True
                    header_changes.append({"title": title, "treatment": "Generated print contents replaces the Markdown navigation list."})
                    continue
                skip_contents = False
                newlevel = max(1, level-1)
                is_part = title.startswith("Part ")
                is_chapter = level == 3 and bool(re.match(r"(?:II|III|IV)\.\d+\.", title))
                if compact_chapter and (newlevel == 1 or is_chapter):
                    blocks.append(layout.raw(r"\clearpage\endgroup"))
                    compact_chapter = False
                if newlevel == 1 or (is_chapter and not first_part_chapter):
                    blocks.append(layout.raw(r"\clearpage"))
                if is_part:
                    first_part_chapter = True
                elif is_chapter:
                    first_part_chapter = False
                node["c"][0] = newlevel
                if is_chapter and title.startswith(("II.2.", "IV.1.")):
                    blocks.append(layout.raw(r"\begingroup\setlength{\parskip}{3.5pt plus 1pt minus .5pt}\setlength{\abovedisplayskip}{8pt plus 2pt minus 3pt}\setlength{\belowdisplayskip}{8pt plus 2pt minus 3pt}"))
                    compact_chapter = True
                    header_changes.append({"title": title, "treatment": "Slightly tighter paragraph/display spacing to absorb short chapter-ending spillover; body font and leading unchanged."})
                if title == "Bibliography":
                    blocks.append(layout.raw(r"\fontsize{9.5}{12}\selectfont\setlength{\parskip}{4pt plus .5pt minus .5pt}"))
                header_changes.append({"title": title, "source_level": level, "typeset_level": newlevel})
            elif skip_contents:
                continue
            blocks.append(node)
        if compact_chapter:
            blocks.append(layout.raw(r"\clearpage\endgroup"))
        adapted["blocks"] = blocks
        (out / "reading.layout.ast.json").write_text(json.dumps(adapted, ensure_ascii=False), encoding="utf-8")
        (out / "LAYOUT_TRANSFORMS.json").write_text(json.dumps({"source": layout_changes, "headings": header_changes}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        body = run([args.pandoc, "reading.layout.ast.json", "-f", "json", "-t", "latex", "--syntax-highlighting=none", "--wrap=none"], "pandoc-latex")
        doi_layout = []
        def doi_breaks(match):
            token = match.group(0)
            doi = token.rstrip(".;,")
            replacement = r"\nolinkurl{" + doi + "}" + token[len(doi):]
            doi_layout.append({"before": token, "after": replacement})
            return replacement
        body = re.sub(r"(?<=DOI: )10\.\d{4,9}/[A-Za-z0-9._;()/:-]+", doi_breaks, body)
        (out / "DOI_LAYOUT.json").write_text(json.dumps(doi_layout, indent=2) + "\n", encoding="utf-8")
        preamble = (HERE / "preamble.tex").read_text(encoding="utf-8")
        if args.edition == "release":
            preamble = preamble.replace("THE RPRM MANIFESTO / PRIVATE REVIEW", "THE RPRM MANIFESTO")
            preamble = preamble.replace("; private working manuscript", "")
        tex = preamble + "\n\\begin{document}\n\\fontsize{10.5}{13.7}\\selectfont\n" + body + "\n\\end{document}\n"
        (out / "reading.tex").write_text(tex, encoding="utf-8", newline="\n")
        receipt.update(source_sha256=sha(raw), tex_sha256=sha(tex.encode()), figures=figures)
        if args.prepare_only:
            receipt["status"] = "PREPARED_NOT_COMPILED"
        else:
            command = [args.tectonic, "--untrusted", "--keep-logs", "--keep-intermediates", "--makefile-rules", "dependencies.mk"]
            if not args.allow_fetch:
                command.append("--only-cached")
            command += ["--outdir", out, "reading.tex"]
            run(command, "tectonic")
            log = (out / "reading.log").read_text(encoding="utf-8", errors="replace")
            defects = re.findall(r"(?:Overfull[^\n]*|Missing character[^\n]*|Undefined control sequence[^\n]*)", log)
            receipt["typesetting_log_defects"] = defects
            if defects:
                raise ValueError("Typesetting log has overflow or missing-glyph/control defects; inspect the retained output")
            import reportlab
            import pypdf
            from pypdf import PdfReader, PdfWriter
            from pypdf.constants import PageLabelStyle
            cover = load_module("rprm_print_cover", HERE / "cover.py")
            cover.build_cover(out / "cover.pdf", out / "fonts", args.edition)
            body_reader = PdfReader(out / "reading.pdf")
            # Clone the complete body catalog so named destinations and their
            # annotations remain together; importing pages alone can drop links.
            writer = PdfWriter(clone_from=body_reader)
            writer.insert_page(PdfReader(out / "cover.pdf").pages[0], 0)
            from pypdf.generic import ArrayObject, NameObject, TextStringObject
            repository_links = []
            for page_number, page in enumerate(writer.pages, 1):
                for annotation in page.get("/Annots", []):
                    action = annotation.get_object().get("/A")
                    if not action or action.get("/S") != "/URI":
                        continue
                    uri = str(action.get("/URI", ""))
                    parsed = urlsplit(uri)
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    relative = Path(unquote(parsed.path))
                    target = (ROOT / relative).resolve(strict=True)
                    if relative.is_absolute() or not target.is_relative_to(ROOT) or not target.is_file() or parsed.query:
                        raise ValueError("Unsupported repository link in PDF: " + uri)
                    destination = "https://github.com/wjfoster55/RPRM-open/blob/main/" + quote(target.relative_to(ROOT).as_posix(), safe="/")
                    if parsed.fragment:
                        destination += "#" + parsed.fragment
                    action[NameObject("/URI")] = TextStringObject(destination)
                    repository_links.append({"page": page_number, "source": uri, "destination": destination})
            receipt["repository_links"] = repository_links
            writer._root_object[NameObject("/OpenAction")] = ArrayObject([writer.pages[0].indirect_reference, NameObject("/Fit")])
            writer.add_outline_item("Cover", 0)
            writer.set_page_label(0, 0, prefix="Cover")
            writer.set_page_label(1, len(writer.pages)-1, style=PageLabelStyle.DECIMAL, start=1)
            writer.add_metadata({"/Title": "The RPRM Manifesto", "/Author": "", "/Subject": "A relational framework for mathematical unification", "/Creator": "RPRM manuscript build", "/CreationDate": "D:20260907000000Z", "/ModDate": "D:20260907000000Z"})
            for notice in ("DejaVu.txt", "STIXTwo-OFL.txt", "AMS-MSAM10-OFL.txt"):
                writer.add_attachment(notice, (ROOT / "LICENSES" / notice).read_bytes())
            final_path = out / "RPRM-Manifesto.pdf"
            with final_path.open("wb") as stream:
                writer.write(stream)
            merged = PdfReader(final_path)
            if len(merged.pages) != len(body_reader.pages) + 1:
                raise ValueError("Cover/body page-count mismatch")
            receipt.update(status="BUILT_PENDING_LAYOUT_REVIEW", body_pdf_sha256=sha((out / "reading.pdf").read_bytes()), pdf_sha256=sha(final_path.read_bytes()), body_pages=len(body_reader.pages), pages=len(merged.pages), python_version=sys.version.split()[0], python_packages={"reportlab": reportlab.Version, "pypdf": pypdf.__version__})
        receipt["source_unchanged"] = before == snapshot(inputs)
        if not receipt["source_unchanged"]:
            raise ValueError("A bound input changed during the build")
        publish()
        print(json.dumps({"status": receipt["status"], "directory": out.relative_to(ROOT).as_posix(), "pdf_sha256": receipt.get("pdf_sha256")}))
        return 0
    except Exception as error:
        receipt.update(status="FAIL", error=type(error).__name__ + ": " + str(error))
        publish()
        print(receipt["error"], file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
