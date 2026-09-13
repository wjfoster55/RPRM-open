# Primary research and documented starting points

Consulted online for the 2026-09-10 recommendation. These are source leads and feasibility checks, not evidence that their software or datasets were executed in this task. Pin versions and artifact hashes during each project's own admission pass.

## Recommended transport project

- USGS, MODFLOW 6 overview: https://www.usgs.gov/software/modflow-6-usgs-modular-hydrologic-model
- MODFLOW 6 GWT immobile storage/transfer package: https://modflow6.readthedocs.io/en/6.7.0/_mf6io/gwt-ist.html
- Official dual-domain supplementary problem 6.3.2 description: https://modflow6-examples.readthedocs.io/en/master/_examples/ex-gwt-mt3dsupp632.html
- Corresponding Python example: https://modflow6-examples.readthedocs.io/en/latest/_notebooks/ex-gwt-mt3dsupp632.html
- USGS FloPy software page: https://www.usgs.gov/software/flopy-python-package-creating-running-and-post-processing-modflow-based-models
- Harte and Brandon (2020), Borehole-scale testing of matrix diffusion for contaminated-rock aquifers, DOI 10.1002/rem.21637: https://www.usgs.gov/publications/borehole-scale-testing-matrix-diffusion-contaminated-rock-aquifers

The cited dual-domain numerical example includes production and optionally sorption. First reproduce it as published; specify a passive-tracer successor separately. The field study is context for delayed release, not a proposed field operation.

## Pore-scale physical-mechanism scout

- Zhang et al. (2026), The Impact of System Softness on Haines Jumps and Drainage in Porous Media, Water Resources Research, DOI 10.1029/2024WR039565: https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024WR039565
- Multiscale drainage dynamics with Haines jumps monitored by stroboscopic 4D X-ray microscopy, PNAS, online December 2023 / 2024 issue, DOI 10.1073/pnas.2305890120: https://doi.org/10.1073/pnas.2305890120
- OpenPNM invasion tutorial (pressure and sequence outputs): https://openpnm.org/examples/tutorials/09_simulating_invasion.html

## Reserved waves and other candidates

- Clawpack/PyClaw one-dimensional shallow-water example: https://www.clawpack.org/gallery/pyclaw/gallery/dam_break.html
- USGS, GeoClaw software for depth-averaged flows with adaptive refinement: https://www.usgs.gov/publications/geoclaw-software-depth-averaged-flows-adaptive-refinement
- TSNet authors' transient pipe-network simulator: https://github.com/glorialulu/TSNet
- EPA Storm Water Management Model: https://www.epa.gov/water-research/storm-water-management-model-swmm
- PySWMM quickstart: https://pyswmm.github.io/pyswmm/quickstart.html
- EPA EPANET water-quality capabilities: https://www.epa.gov/water-research/epanet
- Dedalus Rayleigh–Bénard convection example: https://dedalus-project.readthedocs.io/en/latest/pages/examples/ivp_2d_rayleigh_benard.html

## Methodology

- Munafò and Davey Smith (2018), Robust research needs many lines of evidence, Nature, DOI 10.1038/d41586-018-01023-3: https://www.nature.com/articles/d41586-018-01023-3
- Center for Open Science, preregistration: https://www.cos.io/initiatives/prereg

Use these as methodological context, not a claim that a local Git freeze equals independent replication or journal-accepted preregistration.
