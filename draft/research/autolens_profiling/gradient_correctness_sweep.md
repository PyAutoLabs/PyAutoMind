# Gradient-correctness sweep: triage and investigate every open JAX-gradient bug and hazard in one chat

Type: research
Target: autolens_profiling
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_profiling
- autolens_workspace_test
Themes:
- jax-gradient
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: every item below ends with a recorded verdict — fixed (merged PR + autodiff-vs-FD evidence), explained-not-a-bug (measured mechanism, written into the gradient research note / Pulse knowledge), duplicate (retired into its parent), already-fixed (retired with the commit that fixed it) or re-filed narrower — and the summary table is posted on the sweep's issue
Review-minutes: 30
Unattended: never
Filed: 2026-11-02

Human request (2026-11-02): "find all gradient related issues that investigate bugs or things like this and give me a prompt to have a single chat to investigate them all."

## How to run this chat

1. **Triage first, no code.** Read every item's source (paths below), check each against current `main` (several predate fixes), merge duplicates, and present the human a table: item → suspected mechanism → repo → cost (local / RAL) → proposed order. Get the order approved before any fix.
2. **One shared method for every gradient claim:**
   - compare autodiff with the central FD at the **smallest** steps (1e-8 to 1e-6) as well as at the plateau. A gap at every small step on a non-tiny gradient is a wrong derivative; FD noise or roughness is not;
   - check **where** the point is evaluated (`knowledge/gradient_witness_evaluation_point.md` in PyAutoPulse). Exact symmetry or a grid point on a mass centre can fake a bug;
   - bisect **stage by stage**, comparing eager vs `jit` and forward (`jvp`) vs reverse (`jacrev`). Use reverse mode where NNLS is involved, because the NNLS solver is a `custom_vjp` with no forward mode;
   - when a fix leaves values unchanged, do a before/after on the same cell. The stored `gradient.json` FD values stay valid, so only the autodiff needs recomputing.
   Tools from the last two investigations: `Science/scratch/gradient_campaign_impact_2026-11-02/` (`small_step_check.py`, `ab_cell.sh`, `ab_compare.py`) and `Science/scratch/rectangular_gradient_rtu_sparse_2026-11-02/` (`repro.py`, `stages.py`, `stages2.py`).
3. **One sub-task per fix.** Each library fix ships through the normal `start_dev` → `ship_library` → `/prm` flow, as its own issue and branch, so a stuck item never holds the others. This prompt is the umbrella and records the verdicts.
4. **Compute.** Run locally where it fits (15 GB; the real HST cell needs `XLA_FLAGS=--xla_disable_hlo_passes=constant_folding`). RAL needs an explicit human go per batch, on a private checkout, partition `ral`, never `gpu` for CPU work.

## Items

### A. Suspected wrong derivatives (library bugs)

1. **MGE likelihoods: the FD plateau sits off autodiff (mechanism B).**
   - Source: `draft/bug/autogalaxy/wrong_jax_gradient_on_mge_likelihoods_fd.md`.
   - Symptom: on `imaging/mge/{ao,euclid,hst,jwst}` the FD plateau differs from autodiff by 0.1–0.4 %, identically on CPU and A100. `interferometer/mge/sma` differs by up to 74 % in one direction.
   - These imaging cells hold the mass fixed, so only light parameters are involved. First suspect: the gradient of the linear-light solve (positive-only NNLS `custom_vjp`).
   - **Duplicate:** items 2 and 3 of `draft/research/autolens_profiling/unexplained_gradient_gaps_cpu_sparse_delaunay_and_mge.md` are this same finding; fold them in.
2. **CPU-sparse vs GPU-dense Delaunay gradient gap.**
   - Source: item 1 of `draft/research/autolens_profiling/unexplained_gradient_gaps_cpu_sparse_delaunay_and_mge.md`.
   - Symptom: `group/delaunay/euclid` (CPU 0.2 at every small step, GPU 2e-4), `imaging/delaunay/jwst`, `imaging/delaunay_nn/hst`, `interferometer/delaunay/jvla`. The log L is the same on both paths and only the gradient differs.
   - This is the same shape as the original PyAutoArray#671 "Bilinear CPU sparse" report.
   - Suspects: the sparse curvature and mapped-data path (`inversion/imaging/sparse.py`, `sparse_operator.curvature_matrix_*`), or a `jit`-unstable reduction like the one #672 fixed.
3. **MGE-routed deflections give NaN under reverse mode at a pixel-aligned centre.**
   - Source: `draft/bug/autogalaxy/mge_deflections_reverse_mode_nan_at_grid_centre.md` (filed 2026-09-03).
   - Symptom: gNFW / MGE-30 deflection with the centre on a grid coordinate: `jax.grad` gives NaN, `jacfwd` is finite.
   - It's the same family as #671's Isothermal-core finding (a grid point on the profile centre). Check whether it still reproduces.
4. **Same-class ellipticity gradient sites.**
   - Source: `draft/bug/autogalaxy/q_clamp_and_bare_sqrt_ellipticity_grad_sweep.md` (filed 2026-09-27).
   - The sites: dPIE `MAX_ELLIP` clamps and bare `sqrt` ellipticity sites left over after PyAutoGalaxy#631.
5. **Interferometer sparse inversion: the gradient with respect to the regularization coefficient is off FD by 1.3 % (unverified).**
   - Source: `draft/research/autoarray/interferometer_sparse_jax_grad_vs_finite_difference_1pct.md`.
   - Its own witness is an FD-step sweep. It may be a step artefact; settle it with the small-step method.
6. **Measure-thin solver branch flips in pixelized likelihoods.**
   - Source: PyAutoArray#377 (open), plus the documented `einstein_radius` exclusion in `autolens_workspace_test/scripts/imaging/jax_grad/pixelization.py`.
   - Decide whether it's a real non-smoothness of the positive-only solve or another tie / `jit` artefact (re-test with PyAutoArray#672 in).

### B. Likelihood structure, where FD can't judge (research, not bugs)

7. **Densely non-smooth pixelized likelihoods (mechanism C).** Source: `draft/research/autolens_profiling/densely_non_smooth_pixelized_likelihoods_what_gr.md`. The Delaunay roughness was ruled intrinsic by the human on 2026-11-02. The open question is what gradient samplers can use; it isn't a bug hunt.
8. **Noisy interferometer rectangular likelihood (mechanism D).** Source: `draft/research/autolens_profiling/noisy_interferometer_rectangular_likelihood_fd_c.md`. log L jitters by about 1e-6 between evaluations (confirmed locally in #515: h = 1e-8 FD 52/5/50 in the campaign vs 13/−40/15 locally). Find the noise source: solver tolerance, W~ precision, or float accumulation.
9. **Piecewise-constant image-plane point and cluster likelihoods (mechanism E).** Source: `draft/research/autolens_profiling/piecewise_constant_image_plane_point_and_cluster.md`. FD is zero at fine steps while autodiff is nonzero.

### C. Bookkeeping, tests and corrections

10. **`gradient.json` `point` mislabel.** Source: `draft/bug/autolens_profiling/gradient_json_point_label_standard_cells.md` (glance; a quick win, do it early).
11. **Correct the #515 research note.** In autolens_profiling `wiki/research/gradient_campaign_impact_border_tie.md`, the table row for `point_source_image/image_plane` and `cluster/image_plane` says *autodiff* is exactly zero. It is the **FD** that is zero and autodiff that is nonzero (mechanism E). Fix that row and link item 9.
12. **Verify the rectangular mapper row-weights bug is fixed.** Source: `draft/bug/autoarray/rectangular_mapper_bilinear_row_weights.md` (filed 2026-08-26, Status: draft). The code in `autoarray/inversion/mesh/interpolator/rectangular.py` now carries comments saying the mirrored row weights and the `ceil` bracketing were fixed (autolens_workspace_test#279). Verify, then retire it with the fixing commit.
13. **Critical-curve / caustic `jit` / `grad` parity test.** Source: `draft/test/autolens_workspace_test/jax_zero_contour.md` (notify).

### D. Adjacent value bug (do it if it falls out of item 2)

14. **Sparse vs dense log L mismatch with a non-linear lens light.** Source: `draft/bug/autoarray/sparse_vs_dense_log_likelihood_mismatch_nonlinear_lens_light.md`. A value bug, not a gradient one, but it lives on the same sparse path as item 2.

### Out of scope

- Gradient **cost** hazards (`draft/feature/autolens_profiling/gradient_cost_hazard_on_ral_cpu_value.md`; cluster source-plane CPU 11.7x, weak CPU 4.9x): performance, not correctness.
- PyAutoFit prior / density work (PyAutoFit#1498, #1484, #1500): not JAX-gradient correctness.

## Background already settled (don't redo)

- PyAutoArray#671 → #672 (merged, pending release): the border-relocator `max` tie gradient under `jit`. The HST-fiducial 1e9 is the Isothermal 1e-8 core at a grid-point centre. Record: `complete/2026/11/rectangular-gradient-rtu-sparse.md`.
- autolens_profiling#515: the #671 defects touched no phase-6 verdict, because standard cells evaluate at iid draw 0. Record: `complete/2026/11/gradient-campaign-impact.md`. The PyAutoPulse knowledge page `knowledge/gradient_witness_evaluation_point.md` holds the rules.
- Phase-6 campaign records: autolens_profiling `results/**/gradient.json` (73 cells, witness v2 with a 13-step FD sweep). Epic log: `draft/research/autolens_profiling/likelihood_lifecycle_epic.md`.
