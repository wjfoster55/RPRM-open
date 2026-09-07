# Explanatory figures

Four small diagrams are selected because the joint/fiber structure, future
distinction, erasure/error distinction and representation types are easier
to compare visually. Each includes a failed inference or its boundary.
They are illustrations of stated laws, not empirical plots or proof receipts.

1. **Joint aperture:** every one of the 25 pairs in `{0,…,4}²` is shown.
   Exactly five satisfy `a+b=4`. The product of the marginals admits 20 extra
   pairs. Both panels use the same axes and carrier.
2. **Future distinction:** the displayed transitions are exactly `p→r` and
   `q→q`, with current observations 0,0 and later observations 1,0. The single
   action is a complete separating witness; no sampling inference is used.
3. **Erasure and error:** four bits obey even parity. The erased fourth bit
   is uniquely 0; odd parity in the second panel detects an error but cannot
   localize an arbitrary changed bit. This states the error model explicitly.
4. **Number descriptions:** integer value, a base-ten word, an operation path
   and geometric dimension have separate types. The pictured paths do not
   establish a geometric adapter.

Regenerate with `python tools/build_figures.py` after installing matplotlib
in a development environment. The generator is included; no data download
is used. SVG uses local font selection and embeds no font file. PNG assets
are provided for renderers without SVG support. The four originals are CC0;
the generator is 0BSD. Matplotlib is an optional external build dependency,
not bundled or required to read the repository or run its core checks.
