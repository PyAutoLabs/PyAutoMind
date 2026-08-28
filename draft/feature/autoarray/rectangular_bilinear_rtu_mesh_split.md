# Rectangular mesh split: Bilinear (fast CPU default) vs RTU (advanced/GPU)

Type: feature
Target: autoarray
Repos:
- @PyAutoArray
- @autolens_workspace
- @autogalaxy_workspace
- @autolens_workspace_test
Themes:
- pixelization
- numba-cpu
Difficulty: medium
Autonomy: supervised
Priority: high
Filed: 2026-08-21 (backfilled from git)

## Original request (verbatim, 2026-08-21)

> Ok, I think we want RectangularBilinearAdaptDensity (workspace default)
> RectangularBilinearAdaptImage, RectangularRTUAdaptDensity and
> RectangularRTUAdaptImage. Confirm RectangularBilinearAdaptDensity is CPU fast
> and gradient robust. Thsi will prob means we need to again updated all _test
> workspace likelihood values in certain scripts, see if history has them but
> over write if not (and keep RTU files somewhere)? make prompt to hand off to
> mobile

Preceding context (same conversation): the RTU kernel-CDF transform dominates
the numba CPU likelihood (55% of a euclid eval, 89% at hst; O(M_sub x N_data)
erf sum), making the workspace-default rectangular mesh slow on CPU and on the
interferometer path. Proposal: a simpler/faster rectangular mesh becomes the
workspace default; RTU is documented separately as the recommended option for
advanced modeling, especially on GPU. This subsumes option (2) of the Phase 14
default-mesh decision (`autolens_profiling` PROGRAMME.md Phase 14, issue
autolens_profiling#153) — resolve/update that issue as part of this work.

## Grounding (verified 2026-08-21, this session)

- Current classes (`PyAutoArray autoarray/inversion/mesh/mesh/__init__.py`):
  `RectangularAdaptDensity` / `RectangularAdaptImage` (RTU kernel-CDF,
  Enzi et al. arXiv:2606.30620) and `RectangularUniform` (plain uniform
  lattice + bilinear, no transform). There is no bare `Rectangular`.
- **Naming caveat:** BOTH the RTU meshes and every historical adaptive variant
  use the same 4-pixel bilinear interpolation on the warped lattice
  (`interpolator/rectangular.py:435-442`). What "Bilinear vs RTU" actually
  distinguishes is the lattice transform: the resurrect candidate is the
  **empirical rank-CDF** adaptive transform (sort + cumsum), deleted in
  PyAutoArray `22b28463` (#402, 2026-07-23, -3738 lines) when kernel-CDF took
  the plain names. Recover its implementation from that commit
  (`create_transforms` with `argsort`/`cumsum`) — do NOT reinvent it.
- **CPU fast: YES.** The rank-CDF transform is O(N log N) sort/cumsum and
  eliminates the erf sum that is 55-89% of the numba CPU eval (post-#458 the
  RTU eval is euclid 1.17 s / hst 10.1 s on a 4-core container). Measure the
  new class in the existing `autolens_profiling` cells
  (`scripts/imaging/likelihood_runtime/pixelization_numba.py` etc.) and record
  a versioned result.
- **Gradient robust: CONDITIONALLY.** Certified evidence from the July
  gradient audit (`autolens_workspace_developer/jax_profiling/gradient/README.md`):
  - os_pix=1 (the current default): rank-CDF likelihood is *exactly
    piecewise-constant* in mass/shear — gradients exactly zero. Unusable.
  - over_sample_size_pixelization=4: full FD sweeps validate both adaptive
    meshes — AdaptImage production shape <=~1% on mass, AdaptDensity <=~3%.
    Acceptable for most JAX gradient samplers.
  - Interferometer sparse path: no over-sampling exists — the staircase with
    no escape hatch. RTU (and RectangularUniform) are the only certified
    gradient meshes there.
  So docs MUST say: gradient inference on the Bilinear default needs
  os_pix>=4 (imaging); interferometer gradient work needs RTU. Sampler-level
  mesh-family ranking is already PROGRAMME Phase 5 — do not duplicate it here.
- Alternative implementation considered: interpolated-kernel-CDF forward
  (K=8192 -> dlnL <= +4e-3, 18-55x on the step, measured in #151/#153 work).
  Rejected for the *Bilinear* pair (it is still RTU with a bandwidth
  hyperparameter, defeating "conceptually simple"); it remains #153's lever
  for making RTU itself faster on CPU.

## Goal

1. **PyAutoArray**: four adaptive classes —
   `RectangularBilinearAdaptDensity` (resurrected rank-CDF transform +
   bilinear) and `RectangularBilinearAdaptImage`;
   `RectangularRTUAdaptDensity` / `RectangularRTUAdaptImage` (pure renames of
   the current kernel-CDF classes, values unchanged). `RectangularUniform`
   stays as-is (library-test baseline; certified interferometer gradient
   mesh). **Never delete the RTU implementation.** Breaking rename → release
   notes need the `## API Changes` heading.
2. **Workspaces** (`autolens_workspace` ~224 uses, `autogalaxy_workspace`,
   HowToLens ~42): default examples switch to
   `RectangularBilinearAdaptDensity`; RTU documented separately as the
   recommended advanced option (GPU / gradient samplers / interferometer),
   folding in the queued Enzi-citation docs draft
   (`draft/docs/workspaces/rectangular_mesh_enzi_citation_examples.md`).
   Prior configs: add `mesh/rectangular_bilinear_adapt_*.yaml`, rename the
   RTU yamls to match the new class names (autonerves lowercases keys).
3. **_test workspace**: likelihood pin scripts
   (`scripts/{imaging,multi_dataset,interferometer}/jax_likelihood/rectangular*.py`
   and siblings) — keep RTU pin scripts alive under the renamed classes
   (values unchanged by a pure rename), add/switch default-mesh scripts to
   Bilinear and **regenerate pins, overwriting**. History does hold
   pre-consolidation (empirical-CDF era) values but under older paths/configs
   (over-sampling changed since: `3b4156e`, `602ffce`) — not reusable.
4. Update autolens_profiling#153 / PROGRAMME Phase 14 with the decision.

Library first, workspace follow-up once the API lands (standard both-routing).

## Carried in from the pixelization-eager-jit-divergence task (2026-08-21)

That task (PyAutoGalaxy#580; PyAutoGalaxy#581 + autolens_workspace_developer#127,
both merged) did the `jax_profiling/` slice of this campaign and left two things
undone that belong here. It also learned a trap the hard way — read the trap
before touching any of the ~40 remaining files.

### 4. `misc/pixelization_spline_*.py` are broken on a deleted class

`autolens_workspace_developer/jax_profiling/misc/pixelization_spline_vs_linear.py`
and `pixelization_spline_fit_comparison.py` reference
`RectangularSplineAdaptDensity` / `RectangularSplineAdapt*`, which **no longer
exists at all** — PyAutoArray `22b28463` (#402) deleted the spline-CDF pair
(#289) along with the linear empirical-CDF implementation. This is a
pre-existing break from that consolidation, not from the #461 split, and it was
deliberately left untouched by the divergence task (out of its scope).

These are not renameable — there is no surviving class to rename to. Decide per
script: retarget to Bilinear/RTU if the comparison still has meaning, or delete
them as dead comparisons against a removed mesh. Check whether their committed
results under `jax_profiling/results/` should be retained or tombstoned.

### 5. The sibling scripts are symbol-verified but never executed

The divergence task renamed `jax_profiling/gradient/imaging/pixelization.py`,
`misc/mapper_grad_probe.py` and `misc/pixelization_sparse_cpu.py`, and verified
only that the new symbols resolve and construct against the live API plus
`py_compile`. They are long-running gradient/CPU sweeps and were **not run**.
Only `jit/imaging/pixelization.py` was executed end-to-end (green, exit 0).
Someone should actually run the three when this campaign reaches them — a
name-only change is low-risk but unproven, and the gradient script's findings
feed `gradient/README.md`.

### TRAP: never blanket-rename these symbols — relabel by DATE

The name `RectangularAdaptDensity` meant the **empirical rank-CDF** transform
until `22b28463` (#402, 2026-07-23) and the **kernel-CDF** transform after it.
The implementation changed under an unchanged name. So:

- findings/results dated **≤ 2026-07-09** are rank-CDF → today's
  **`RectangularBilinear*`**
- findings/results dated **≥ 2026-07-26** are kernel-CDF → today's
  **`RectangularRTU*`**

A `sed -i` across a file relabels historical findings as belonging to a mesh
that never produced them. The divergence task made exactly this mistake on
`jax_profiling/gradient/README.md` and had to correct it (`08d5d86`): that file
is **mixed**, carrying 2026-07-09 rank rows *and* a 2026-07-26 kernel section,
and it states the distinction in its own text ("Post-consolidation
(PyAutoArray#403 — the kernel-CDF meshes now ARE `RectangularAdaptDensity` /
`RectangularAdaptImage`)"). Two reliable tells that an entry is rank-era: prose
about "rank-transform knots" / "rank-reordering jumps", and a file whose last
real authoring predates 2026-07-23 (`git log -- <file> | tail`).
`jax_profiling/gradient/README.md` now carries a dated-names warning above its
status table; consider the same wherever else findings are tabulated.

### Bearing on Goal 3 (the `_test` likelihood pins)

Goal 3 above says pre-consolidation values are "not reusable" because paths and
over-sampling changed. That is right for the `_test` scripts, but the divergence
task found the stronger fact for a script whose fiducial did *not* change:

`jax_profiling/jit/imaging/pixelization.py`'s constant `24746.105672366088`,
pinned 2026-05-11, is reproduced **bit-for-bit** by
`RectangularBilinearAdaptDensity` today (`.hex()` equal). Nothing else in the
library moved that value in 3.5 months — an exact match across that span proves
it. So the pin was never stale; #402 silently changed what the script computed,
and the stale pin masked it. Naming Bilinear explicitly **restored** the
constant rather than re-pinning it, preserving its pre-#402 history.

Corroborated independently of the pin by the era's committed artifacts —
`results/jit/imaging/pixelization/{hpc_a100,local_gpu,local_cpu}_fp64.json`
(A100, RTX 2060, CPU; v2026.5.1.4 and v2026.5.8.2) all recorded
`eager_log_evidence` bit-identical to it, with the `_mp` siblings at
`24746.105678802393` — and by code identity: the May-era `create_transforms`
(`bc00c113:autoarray/inversion/mesh/interpolator/rectangular.py:70`) is
line-for-line identical to today's `create_transforms_rank`.

**Therefore, before overwriting any `_test` pin:** check whether that script's
fiducial actually changed. Where it did not, the Bilinear run should reproduce
the pre-#402 pinned value exactly — and a match is a free correctness check that
the rank-CDF restoration is faithful for that configuration. Only overwrite pins
where the fiducial genuinely moved. Blindly regenerating every pin would discard
this check and repeat the laundering that hid #402 for a month.

Note also: the transform lives in
`autoarray/inversion/mesh/interpolator/rectangular.py`, **not** in the mesh
class — grep the interpolator, not the class, to identify which CDF a mesh uses.
