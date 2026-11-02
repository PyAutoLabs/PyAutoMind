# Assess how PyAutoArray#671's two gradient defects affected the likelihood-lifecycle / PyAutoPulse gradient campaign verdicts

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- jax-gradient
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: a table over every campaign `gradient.json` (v2 standard legs RAL 413791-413830 + p6 fiducial legs) marking each cell affected / unaffected by (a) the border-relocator tie bug and (b) the centre-on-grid Isothermal core, with the reasoning per cell family, plus a re-run list (cells whose fd.status verdict could flip) — posted on autolens_profiling#509 and the Pulse gradient knowledge entry
Review-minutes: 10
Unattended: never
Filed: 2026-11-02
Issued: 2026-11-02

Human request (2026-11-02, during PyAutoArray#671): "when active work on this task is done we need to assess if this issue has impacted the PyAutoPulse gradient campaign in general."

## The two defects (record: complete/2026/11/rectangular-gradient-rtu-sparse.md)

1. **Border-relocator tie gradient (library bug, FIXED in PyAutoArray#672, pending release).** `ellipse_params_via_border_pca_from` took `b = max(|y'|)`. A lens centred on the mask's symmetry centre traces the border into exact +/- pairs, so the maximum is an exact tie. JAX's tie-sharing `max` gradient is unstable under `jit` reverse mode: the gradient of `b` came out 2x / 0.5x. Eager mode was correct. Affects every jitted pixelized-source gradient with `use_border_relocator=True` evaluated with the lens on the mask's symmetry centre (prior medians typically are), for any mesh (rectangular, Delaunay, ...). It produced a 2–5% autodiff-vs-FD error on mass/shear in the repro.
2. **Centre-on-grid Isothermal core (evaluation-point artefact, not a library bug).** On odd grids (HST 141x141) at pixelization over-sampling 1, one source-grid point sits exactly at the mass centre at prior medians; the `psi` softening (1e-8 core) gives d(deflection)/d(centre) ~1e8. This gave |g| ~2e9 on the imaging/rectangular/hst fiducial. The evaluation-point fix belongs to autolens_profiling#509 (p6c).

## Questions

- Which campaign cells were evaluated at a symmetric point (centre at the mask's symmetry centre) with the border relocator on? Their fd verdicts may be wrong, either way.
- Which odd-grid instruments at os_pix=1 were evaluated with the centre on a grid point?
- Do the Delaunay "no_plateau" / mismatch verdicts (Science/scratch/delaunay_hilbert_2026-11-01/README.md) change once PyAutoArray#672 is in the RAL checkout?
- Re-run plan: which cells, which library pin (#672 needs a release or a private RAL checkout per [[RALpullMains]]).
