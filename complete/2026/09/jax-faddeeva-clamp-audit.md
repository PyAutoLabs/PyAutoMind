## jax-faddeeva-clamp-audit
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/600 (closed, completed)
- completed: 2026-09-03
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/603 (MERGED 50599c2c4)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/215 (MERGED 370583a47)
- parent: complete/archive/epics/numpy_deflections_cpu_speedup.md — the JAX-path follow-up the
  numpy-deflections-cpu epic filed at phase 2; not itself an epic member.
- verdict: **Weideman N=32 replaces `_wofz_rational` on the JAX path.** The hand-rolled rational
  approximation is a three-region `xp.where` cascade — ~6 significant figures, and a *derivative* that
  jumps at each region boundary. Weideman-32 is a single expression over the whole domain: **1.9e-13
  relative accuracy against mpmath on the MGE domain versus 3.4e-6** for the rational form, at **0.75x
  the cost**, and seam-free by construction (the same seam table that gives the rational form up to
  5.8e-5 relative derivative jump gives Weideman 2.55e-9 at every boundary — exactly the genuine
  variation of `w'` across the same offset). Valid for Im z >= 0, which is the whole MGE domain.
- verdict: **the exact spherical MGE branch is now static on both backends.** Phase 2 had added it on
  numpy only, leaving JAX on the `q = 0.9999` clamp. The clamp bias it replaces measured **6.3e-5**
  relative (gNFWSph) and **1.1e-4** (Gaussian), with a **1.45e-4 arcsec cross-axis** deflection error;
  all three are removed rather than reduced, since the branch is the exact q -> 1 radial form. JAX
  gNFWSph is **16x** faster as a side effect — the elliptical path it no longer takes was doing the MGE
  sum in the complex plane for a real answer.
- finding: **the seams produce no measurable likelihood kink.** The whole reason the audit was filed was
  the suspicion that seam crossings roughen the likelihood surface under gradient-based inference. They
  do not: the kink count over the probe's parameter sweep is **93, identical to the smooth baseline**.
  What the seams *did* break is finite-difference *validation* of JAX gradients — FD checks against
  `jax.jacfwd` came out **O(1) wrong below h ~ 1e-5**, which is exactly the regime an FD audit uses. That
  is now gone: **1.8e-7 at h = 1e-6**. So the defect was real but its victim was the verification
  machinery, not the sampler.
- finding: the residual **~1e-7 JAX-vs-numpy floor on MGE-routed profiles is not the Faddeeva kernel**.
  It is amplitude summation order in `decompose_convergence_via_mge`, where the terms cancel by a factor
  of **4e9** — so the two backends' different summation orders land 1e-7 apart on a quantity whose own
  terms are nine orders larger than the result. Pre-existing, out of scope here, **not fixed**; naming it
  is the point, because it is the floor any future JAX/numpy parity pin must sit above.
- finding: reverse-mode `jax.grad` returns **NaN at a pixel-aligned profile centre** (forward-mode
  `jacfwd` is fine). Filed as `draft/bug/autogalaxy/mge_deflections_reverse_mode_nan_at_grid_centre.md`.
- measured: `autolens_workspace_test` jax_likelihood **15/15 pass**; the `mge.py` likelihood pin moved
  **3.2e-10** — the whole numerical footprint of replacing the kernel and lifting the clamp.
  test_autogalaxy **1162 passed**.
- hazards: `component.mge.faddeeva-seam-gradient` and `component.mge.spherical-clamp-bias` — both
  **resolved**; the two checks live in `autolens_profiling/scripts/misc/hazards/checks/mge_faddeeva.py`
  and the study in `scripts/misc/hazards/mge_faddeeva.py`, artifact
  `results/hazards/component/mge/faddeeva_audit.{json,png}`.
- heart: RED at PR-open, human-acknowledged for PR-open only, two reasons carried verbatim on the
  `active.md` entry — release validation FAILED (stage integrate), and PyAutoArray open PR 11d old.
  Neither touches this diff.
- session: local CLI; merged and closed out via /prm 2026-09-03. PyAutoGalaxy is pending-release.
- affected-repos:
  - PyAutoGalaxy
  - autolens_profiling

## Original prompt

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
Status: active
Consequence: judge
Witness: a gradient-continuity probe across the three wofz region seams and a spherical-vs-elliptical(q→1) deflection comparison under jax.jit, with the measured seam jump in d(alpha)/d(theta) and the clamp bias recorded in autolens_profiling/results/notes/numpy_deflections_cpu.md.
Review-minutes: 20
Unattended: ready
Parent: complete/archive/epics/numpy_deflections_cpu_speedup.md
Filed: 2026-09-02
Issued: 2026-09-03

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
