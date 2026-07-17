## potential-correction-interferometer
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/623
- completed: 2026-07-17
- library-pr: PyAutoLens#624, PyAutoLens#625, PyAutoGalaxy#508, PyAutoLens#626 (all MERGED)
- workspace-pr: autolens_workspace_test#177, autolens_workspace_test#178 (both MERGED)
- summary: Extended al.pc (potential corrections, epic #618) to Interferometer data with the SPARSE-OPERATOR (w-tilde) route as primary per user requirement — joint curvature [f|G]^T Wtilde [f|G] via InterferometerSparseOperator FFT machinery over extent-indexed COO triplets, data vector via the dirty image, chi2 via one NUFFT (or the normal-equation identity in the LM loop: ZERO per-candidate NUFFTs) — cost scales with real-space pixels, independent of n_vis. FitDpsiSrcInterferometer + IterFitDpsiSrcInterferometer + both analyses + dpsi_mask (arc-restricted mesh with row embedding). Sparse ≡ dense certified; chi2 identity ≡ direct NUFFT certified; xp=np ≡ xp=jnp ≡ jitted certified (wst#178). One-shot subhalo recovery corr 0.35 / peak 0.13" (wst#177).
- bugs-found-and-fixed: (1) InputPotential nearest-extrapolation smeared constant spurious deflections outside an arc-restricted dpsi mesh across the re-trace grid → extrapolate="zero" mode (ag#508). (2) LM damping mu*I is scale-blind — visibility curvatures ~1e11 left ~4 usable decades below the 1e15 cap → "damping exceeded" stalls → Marquardt scaling mu*diag(H) in dense_util.solve_lm_step_from (al#626; also benefits the imaging engine).
- traps: aa.Settings has no use_w_tilde; grids.border_relocator is an instance property (class hasattr false-negative); 4000 random vis on 64x64 OOM-kills WSL; uv beyond real-space Nyquist explodes chi2; global dkappa corr is sidelobe-limited under sparse random uv (assert parity+peak+gauge at smoke scale); LAPACK-vs-XLA slogdet differs beyond rtol 1e-10 at visibility condition numbers (use 1e-8).
- follow-up: draft/research/autolens/potential_correction_realistic_uv_campaign.md — iterative RECOVERY certification on a B1938-like/ALMA-like configuration (smoke scale cannot: source mesh cannot reach chi2/dof~1, corrections absorb source-model error).

## Original prompt

# Claude Development Prompt: Potential corrections for interferometer data

Type: feature
Target: PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> merge, and then the follow up will be to get this running on interferometer
> data as currently its just imaging

## Goal

Extend the potential-correction (gravitational imaging) subpackage `al.pc`
(shipped 2026-07-17, issue PyAutoLens#618, Cao et al. 2025 port) from
`Imaging` to `Interferometer` datasets: the joint source+dpsi inversion
(`FitDpsiSrcImaging`), the dpsi-only residual inversion (`FitDpsiImaging`),
the iterative LM engine (`IterFitDpsiSrcImaging`) and the analysis classes
should accept an `al.Interferometer` dataset, fitting in visibility space.

This is scientifically important: the benchmark detections this technique
targets are VLBI/radio — Powell et al. 2025 (Nat. Astron. 9, 1714) and
Vegetti et al. 2026 found the 1e6 Msun object in JVAS B1938+666 with a
visibility-space gravitational-imaging code (PRONTO). Imaging-only al.pc
cannot reproduce that regime.

## Key design work

- The imaging formalism uses the explicit PSF blur matrix B in
  delta_d = -B D_s D_psi delta_psi. For interferometer data B is replaced by
  the transformer/NUFFT operator mapping image-plane corrections to
  visibilities (real+imag), and the noise covariance by the visibility
  noise. Follow how `al.FitInterferometer`'s inversion builds its operated
  mapping matrix (w_tilde / transformer paths) and mirror the seam.
- The arc mask (`al.pc.util.arc_mask_from`) is image-plane; for
  interferometer fits the mask comes from the dirty image / real-space mask
  of the dataset — decide the convention.
- `dense_util` kernels are already data-agnostic (they take mapping matrix +
  noise vector) — the work is mostly in the fit-layer operators, the
  evidence's noise-normalization term for complex visibilities, and the
  iterative engine's source-mapping update (`convolved_mapping_matrix_from`
  → transformed mapping matrix).
- Keep the xp API: visibility transforms under numpy default, jax path via
  the existing transformer JAX support.
- Validation: simulate an interferometer dataset with an NFW subhalo
  (SimulatorInterferometer), mirror `subhalo_recovery.py` in
  autolens_workspace_test (+ a jax_likelihood_functions/interferometer/
  potential_correction.py), and cite Cao et al. 2025 + Powell/Vegetti
  throughout.

## Acceptance criteria

- `al.pc` fits + iterative engine run on `al.Interferometer` with finite
  evidence and recover a simulated subhalo in visibility space.
- Unit tests numpy-only; workspace_test scripts for regression + JAX parity.
- Docs/guide section extended; citations maintained.
