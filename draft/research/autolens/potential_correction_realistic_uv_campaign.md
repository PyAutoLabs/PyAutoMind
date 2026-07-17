# Claude Development Prompt: Realistic-uv iterative potential-correction recovery campaign

Type: research
Target: PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## Goal

Certify iterative dkappa RECOVERY (not just mechanics) for the visibility-space
potential-correction engine `al.pc.IterFitDpsiSrcInterferometer` on a
realistic interferometer configuration — the missing validation tier from
PyAutoLens#623.

## Background (from the 2026-07-17 engineering arc)

All engineering is merged (#624, #625, ag#508, al#626, wst#177, wst#178):
sparse w-tilde route certified ≡ dense; chi2 identity certified; zero-fill
InputPotential extrapolation; Marquardt-scaled LM damping. The one-shot fit
recovers a 1e10 Msun subhalo at smoke scale (corr 0.35, peak 0.13" with an
arc dpsi_mask). What smoke scale CANNOT certify: iterative recovery — the
tiny source mesh cannot fit high-S/N visibilities to noise level
(best pure-source chi2/dof ~ 4e3), so iterative corrections absorb
source-model error instead of the subhalo.

## The campaign

- Realistic configuration: B1938+666-like (Powell et al. 2025, Nat. Astron.
  9, 1714; Vegetti et al. 2026) or ALMA-like (SDP.81 uv coverage already on
  RAL from the jax-joss work): dense uv coverage, resolution matched to the
  real-space grid, source pixelization fine enough to reach chi2/dof ~ 1 on
  the smooth model.
- Likely RAL/A100 compute (sparse-operator precision matrix + LM loop at
  10^5-10^6 visibilities); xp=jnp path available throughout.
- Metrics: iterative dkappa correlation vs truth (global + local window),
  peak localization, evidence-ranked hyper-parameter sampling
  (IterDpsiSrcInvInterferometerAnalysis), sensitivity vs subhalo mass
  (approach the ~1e6 Msun regime of the papers as stretch).
- Deliverable: campaign scripts + results writeup; promote thresholds back
  into wst regression if a CI-affordable configuration is found.

## Notes

Cite Cao et al. 2025 (caoxiaoyue/potential_correction_paper) + the
Powell/Vegetti papers. Traps from the smoke work: WSL OOM at 4000 random
vis on 64x64 (run heavy configs on RAL); uv beyond the real-space Nyquist
explodes chi2; global corr is sidelobe-limited under sparse random uv.
