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
