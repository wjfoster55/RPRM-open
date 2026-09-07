# Third-party material and references

The Python mathematical library and its checks use the Python standard
library. Python and Node.js are external runtimes and are not bundled.
The Lean proofs import Init from Lean 4.22.0. Lean is an external compiler
and standard library and is not bundled or relicensed by this repository.

The atlas dependency inventory is recorded in its own README. Any optional
dependency must retain its applicable notice; a project-wide license cannot
override that notice.

Academic papers linked in the documentation are references. Their texts and
figures are not distributed as part of this repository. Attribution identifies
the relevant established mathematics, without implying endorsement or a new
priority claim.

The legal instruments in LICENSES are their standard texts. CC0's legal code
states that Creative Commons license text is dedicated to the public domain.
The PDF embeds subsets of DejaVu Sans and DejaVu Sans Mono. Their complete
notice is [LICENSES/DejaVu.txt](LICENSES/DejaVu.txt), also carried as the PDF's
sole attachment, DejaVu.txt. The figures use those typefaces when rendered;
the SVGs refer to fonts and do not bundle a font program. Those fonts retain
their own license and are not relicensed under this project's CC0 or 0BSD.

Rebuilding the optional figures and PDF uses matplotlib, ReportLab and pypdf.
These libraries are external build dependencies, not bundled software. The
distributed paper and figures can be read without installing them. No private
datasets, unrelated logos or historical archives are included.
