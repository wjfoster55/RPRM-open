# Building the process-mechanics working paper

Run `build_paper.py` from this directory. It combines `MANUSCRIPT.md`, `APPENDICES.md`, and `BIBLIOGRAPHY.md` in that order, reads `preamble.tex` without rewriting it, and draws the existing triangle fixture and the first paper's finite chain-continuation witness. There is one active builder for this paper; the former draft builder is retired. The Manifesto has its own separate build recipe.

## Dependencies and command

Use Python 3.10 or newer, the packages in `requirements.txt`, Pandoc and Tectonic. The reference build uses Python 3.12.14, Pandoc 3.11 and Tectonic 0.17.0. The companion includes the exact nine font files under `tools/typesetting/fonts/`: STIX Two Text Regular, Bold, Italic and BoldItalic; STIX Two Math Regular; DejaVu Sans regular, Bold and Oblique; and DejaVu Sans Mono. `build_paper.py` declares the exact filenames. Compiler and runtime binaries remain external. The root `LICENSES/` directory retains the STIX Two, DejaVu and AMS MSAM10 notices; see `THIRD_PARTY_NOTICES.md`.

```text
python -I -B build_paper.py --pandoc <pandoc-executable> --tectonic <tectonic-executable> --font-dir ../../tools/typesetting/fonts --outdir <disposable-build-directory>
```

Keep the disposable directory outside the public payload. `RPRM_PANDOC`, `RPRM_TECTONIC`, and `RPRM_FONT_DIR` are equivalent defaults. Tectonic uses cached public packages; `--allow-fetch` permits fetching missing TeX packages on a new machine. The manuscript is compiled locally.

The YAML header in `MANUSCRIPT.md` is the metadata source. It determines title, subtitle, structured author name, working-paper date/version, DOI, Zenodo record URL, license, PDF filename, title block, running title, footer, PDF properties, citation record and build receipt. The builder fixes the PDF timestamp to that working-paper date for reproducibility, records versions and font hashes, and writes sanitized invocation placeholders rather than machine paths. When editing metadata, also synchronize the paper/navigation objects in the claim and evidence maps before export.

The build contract is a working paper with its DOI and record URL. The release metadata is prepared for authorized publication. Building the PDF does not publish a record or verify the record's publication status; that operation has its own receipt. The citation records the working-paper date in its notes. Original paper prose and figures use CC0-1.0; companion software licensing is separate.

The build writes `The-Right-Answer-Is-Not-Enough.pdf`, `figures/triangle.pdf`, `figures/chain-continuation.pdf`, `CITATION.cff`, and `DOCUMENT_BUILD.json`. Both vector figures are drawn locally from specified mathematical fixtures. Temporary TeX, logs and build-local copies of the bundled fonts stay in the disposable directory. A successful compile is not a layout approval: the receipt invalidates a prior layout review when the PDF hash changes. Reproducibility across different font/compiler versions is not promised.

## Check the rebuilt PDF

Render all pages with Poppler:

```text
pdftoppm -r 130 -png The-Right-Answer-Is-Not-Enough.pdf <existing-render-directory>/page
```

Inspect every page for readable text, equations, tables, page breaks, footers and references. `PDF_CHECKS.json` and `LAYOUT_REVIEW.json` identify the delivered file's structural and visual checks; they do not certify later builds. These checks do not certify PDF/UA, physical print output or every PDF viewer.

## Public companion verification

From the public payload root, create a receipt directory, then run:

```text
python -I -B experimental/process-mechanics/verify_all.py --output <absolute-receipt-directory>/VERIFY_ALL.json
python -I -B experimental/process-mechanics/public_evidence/pc1/reaggregate_tables.py
```

The runner creates `verify_parts/` beside the consolidated output. The arithmetic script requires only Python's standard library and the included saved rows. Both commands rewrite three derived summaries in `public_evidence/pc1/`: `CLAIM_TABLE.json`, `hard_decision_counts.json`, and `HARD_DECISION_SUMMARY.json`. Use a writable local copy. `--output` on the arithmetic script redirects only its claim table, not the other summaries. The original rows, pairs and producer extracts are inputs, not regenerated outputs. Node.js 18 or newer supports JavaScript checks; NumPy/SciPy enable the optional RLC path. Preserve optional skip reports. Historical editorial math checks are separately described in Appendix C.3 and are not part of these public commands.
