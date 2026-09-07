# Rebuild the complete book

The build preserves the manuscript's mathematical notation through Pandoc's parsed representation and native LaTeX. ReportLab draws the cover; pypdf joins it to the body, retains navigation and adds the font notices. The six supplied print assets accompany the readable SVGs. No external dataset is needed.

This optional document build is separate from `verify.py`. A successful conversion is not a theorem proof or a completed visual review.

[DOCUMENT_BUILD.json](../../DOCUMENT_BUILD.json) identifies the earlier review Markdown/PDF pair at its recorded source commit and its selected build inputs. The working manuscript now contains reader revisions; rebuilding is deferred until the text is settled. Rebuilding creates a fresh receipt for the new output; it does not update that distributed record automatically.

## Dependencies and command

Use Python 3.10 or later with ReportLab and pypdf, [Pandoc 3.11](https://github.com/jgm/pandoc/releases/tag/3.11), and [Tectonic 0.17.0](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0). Compiler versions are checked because a parser or font-engine change can alter notation and pagination. The build records executable hashes and Python package versions. The reference environment uses ReportLab 4.4.9 and pypdf 6.10.0; another environment requires its own output inspection.

From the repository root, when the two executables are on PATH:

```text
python -I -B tools/build_paper.py
```

Otherwise supply their installed paths with `--pandoc PATH --tectonic PATH`. No machine-specific location is built into the script. The default creates a private review edition and admits only Tectonic support files already in its local cache. On an initial setup, `--allow-fetch` explicitly permits the compiler to acquire missing support files from its configured bundle. It does not download project code or data. A warmed cache can then be reused with the default cached-only command. An input hash list records selected project bytes; it is not an attestation of every compiler dependency or a cross-platform bit-reproducibility claim.

`--prepare-only` retains the parsed source, adapted representation and LaTeX without compiling. `--edition release` changes the cover and footer label; it does not publish or certify the text. Review the manuscript's status and reserved sections before choosing that label. Changing the label does not remove draft text.

Every invocation owns a new `.artifacts/paper/<build-id>/` directory. An optional `--build-id NAME` chooses a new directory name; existing directories are rejected. The tool leaves the distributed `RPRM-Manifesto.pdf` unchanged. Its new `RPRM-Manifesto.pdf`, the body, cover, intermediate representations, logs, dependency rules and `BUILD.json` remain in the generated directory. Copy a reviewed output to the root only after checking the exact result.

## What the conversion changes

The source's navigation list becomes a linked print table of contents, with the source headings retained. The cover carries the book title. Long inline mathematical lists receive reversible break opportunities after top-level commas. Two tables receive explicit column widths; two short comparisons receive page-space reservations. Each explanatory image stays with its supplied caption, printed once. DOI tokens gain reversible line-break opportunities. These are recorded presentation changes, not substitutions for the equations, table cells or proof statements.

`ASSETS.json` names every selected font, figure and print input with its SHA-256. Update a changed asset's binding deliberately and review its output. The selected before/after input hashes must agree; a persistent difference fails the build. The log check rejects overfull boxes, missing characters and undefined controls; it cannot detect every possible rendering error. The output status remains `BUILT_PENDING_LAYOUT_REVIEW` until an actual review of the resulting pages supplies separate evidence.

The final file opens at the cover with a fit-page view and has a cover label followed by body page labels starting at 1. Internal navigation is retained through the merge; font notices are attached as plain text. The PDF is not advertised as tagged, PDF/A or accessibility-certified. The Markdown remains an alternative text entrance, with source alt text on each figure.

## Fonts and licenses

The nine selected font programs are unmodified STIX Two 2.13b171 and DejaVu files. They retain [STIX Two's OFL notice](../../LICENSES/STIXTwo-OFL.txt) and [DejaVu's notice](../../LICENSES/DejaVu.txt). The TeX support bundle supplies MSAM10 version 003.002; the PDF's subset retains its [AMS notice and OFL](../../LICENSES/AMS-MSAM10-OFL.txt). The corresponding three notices are attached to the merged PDF. External compilers, their support caches and Python libraries are not distributed as project software.

The build scripts are original software under 0BSD; that license does not replace the font licenses. See the repository's [third-party inventory](../../THIRD_PARTY_NOTICES.md).
