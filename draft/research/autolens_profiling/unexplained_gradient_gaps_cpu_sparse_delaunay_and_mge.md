# Unexplained autodiff-vs-FD gaps in the phase-6 gradient records: CPU-sparse Delaunay, imaging MGE, interferometer MGE

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- jax-gradient
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: for each family below, a measured explanation (or a library bug filed with a repro) that accounts for the stored autodiff-vs-FD gap at the smallest sweep steps, posted on the issue with the cell evidence
Review-minutes: 10
Unattended: never
Lane: any
Filed: 2026-11-02

Found in autolens_profiling#515 (research note `wiki/research/gradient_campaign_impact_border_tie.md`, table "What the remaining disagreements are"). None of these is caused by PyAutoArray#671. Method used there: compare each `gradient.json` `fd_sweep` direction's `analytic` against the stored central difference at h = 1e-8 / 1e-7 / 1e-6 (script `Science/scratch/gradient_campaign_impact_2026-11-02/small_step_check.py`).

1. **CPU-sparse vs GPU-dense Delaunay.** *(Being investigated as item 2 of autolens_profiling#517; for interferometer/delaunay/jvla both devices run the same sparse path, so it is CPU-vs-GPU, not sparse-vs-dense.)* `group/delaunay/euclid` (CPU 0.2 at every small step in one direction; GPU 2e-4), `imaging/delaunay/jwst` (CPU 0.2; GPU 7e-4), `imaging/delaunay_nn/hst`, `interferometer/delaunay/jvla` (CPU 1e-2; GPU 2e-6). Same likelihood value, different gradient by backend/path. Same shape as the original #671 "Bilinear CPU sparse" report.
2. **Imaging MGE.** *(Folded 2026-11-02 into `draft/bug/autogalaxy/wrong_jax_gradient_on_mge_likelihoods_fd.md` by autolens_profiling#517: the gap is evaluation exactly at `ell_comps` = 0, not NNLS.)* `imaging/mge/{ao, euclid, hst, jwst}`: a constant 0.1–0.4 % gap at every step, CPU = GPU. No pixelization; mass fixed, so only light parameters. Candidate: the linear-light solve's gradient (positive-only NNLS custom_vjp).
3. **Interferometer MGE.** *(Folded into the same bug prompt, to confirm there.)* `interferometer/mge/sma`: 70 % gap in one direction (NUFFT route).

Not in scope (already explained): FD noise on small gradients (interferometer rectangular, the sma cells); exactly-zero image-plane gradients.
