# Audit the JAX-path Faddeeva approximation and the spherical axis-ratio clamp in MGE deflections

Type: research
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- autolens_profiling
Themes:
- jax
- mass-profiles
- profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: a gradient-continuity probe across the three wofz region seams and a spherical-vs-elliptical(q→1) deflection comparison under jax.jit, with the measured seam jump in d(alpha)/d(theta) and the clamp bias recorded in autolens_profiling/results/notes/numpy_deflections_cpu.md.
Review-minutes: 20
Unattended: ready
Parent: complete/archive/epics/numpy_deflections_cpu_speedup.md
Filed: 2026-09-02

> Follow-up flagged by the human 2026-09-02 during phase 2 planning of the `numpy-deflections-cpu` epic.
> Phase 2 moves the numpy path to `scipy.special.wofz` and adds a numpy-only spherical branch; the JAX
> path keeps the hand-rolled Faddeeva and the `q = 0.9999` spherical clamp. This audit decides whether
> that is acceptable for gradient-based inference, and fixes it if not.

## Evidence (2026-09-02 design probe, hst grid 15,361 points, gNFW MGE-30 inputs)

- Hand-rolled `MGEDecomposer.wofz` (`autogalaxy/profiles/mass/abstract/mge.py`) vs mpmath at dps 40:
  max relative error **3.0e-6** (median 1.7e-10); `scipy.special.wofz` **1.3e-14**. The error is a
  designed ~6-significant-figure rational fit, worst near |z| ≈ 1.5–2 on the real axis (region 6).
  Deflection-angle impact ~4e-6 relative — far below data precision. Not a correctness concern by itself.
- The three regions are selected by `xp.where`; the function is continuous to ~1e-6 across the seams but
  its derivative is not. Under `jax.grad` this puts small kinks in the likelihood surface wherever a grid
  point crosses a seam as parameters move. Never measured.
- Spherical MGE profiles are evaluated as elliptical at the clamp `MGEDecomposer.axis_ratio = 0.9999`
  (`mge.py:291-293`; `Gaussian.axis_ratio` clamp at `stellar/gaussian.py:159-161`). Against the exact
  q→1 radial form `α(r) = Σ_j 2 A_j σ_j² (1 − e^{−r²/2σ_j²}) / r` the current path has a **6.3e-5 relative
  bias** (gNFWSph) / **1.1e-4** (Gaussian), scaling linearly with 1−q, plus a spurious cross-axis
  deflection of −3e-8 at (0, 1"). Affects every spherical MGE-routed class: gNFWSph, cNFWSph,
  gNFWVirialMass*Sph, dPIEPotentialSph, SersicCoreSph. Phase 2 removes it on numpy only.

## Questions

1. Seam smoothness: measure the jump in ∂α/∂θ (and in the log-likelihood gradient of a gNFW fit)
   across each region boundary under `jax.jit`/`jax.grad`; compare NUTS / Prodigy acceptance and
   step-size adaptation on a gNFW lens with the hand-rolled routine vs a smooth alternative
   (e.g. a single higher-order continued fraction / Weideman N=64 valid over the whole upper half-plane,
   or `jax.scipy.special.erfc`-based evaluation where available).
2. Clamp: lift the spherical clamp under JAX either by a formulation smooth in q (the elliptical kernel
   has a removable singularity at q=1 — the `sqrt(2π/(1−q²))` prefactor cancels against `zeta`) or by
   raising the clamp toward 1 − 1e-7 if the kernel is stable there; quantify the residual bias.
3. Decide: keep / replace the JAX routine, and record the verdict in the epic ledger.

## Out of scope

The numpy path (phase 2 handles it); CSE; any new public API.

<!-- formalised by the Intake (Conception) Agent on 2026-09-02 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/d3971bba-0e8d-4c4f-bc59-7808e6bfa6cd/scratchpad/intake_jax_faddeeva_audit.md -->
