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
The complete book uses STIX Two text and mathematical fonts, DejaVu text and
figure fonts, and MSAM10 mathematical symbols. Nine unmodified STIX Two and
DejaVu font programs needed by the portable build are included under
`tools/typesetting/fonts`; [ASSETS.json](tools/typesetting/ASSETS.json) identifies
their bytes. The corresponding notices are
[STIX Two OFL](LICENSES/STIXTwo-OFL.txt), [DejaVu](LICENSES/DejaVu.txt), and
[AMS MSAM10 OFL](LICENSES/AMS-MSAM10-OFL.txt). All three are attached to the
merged PDF. MSAM10 is supplied by the external TeX support bundle and embedded
as a subset; its standalone font file is not bundled here. SVGs refer to font
families without embedding a font program. The font terms remain separate
from the project's CC0 and 0BSD terms.

The optional full-book build uses Pandoc, Tectonic, ReportLab and pypdf;
figure regeneration also uses matplotlib and NumPy. These external tools,
libraries and compiler support caches are not distributed as project software.
The [build recipe](tools/typesetting/README.md) names the reference versions,
commands, selected inputs and remaining review obligations. The paper and
figures can be read without installing these tools.

STIX Two's bundled notice comes from its official 2.13b171 distribution.
The MSAM10 version, copyright and reserved font name are those in the actual
font used by the compiler; its notice includes the full standard OFL 1.1.
See the [STIX Fonts project](https://github.com/stipub/stixfonts) and
[AMSFonts distribution](https://ctan.org/pkg/amsfonts) for their source and
licensing context. No private datasets, unrelated logos or historical
archives are included.
