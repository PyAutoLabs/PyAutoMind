Realistic-uv iterative delta-kappa recovery certification for the interferometer
potential-correction implementation (al.pc, sparse w-tilde route), closing the
potential-correction port arc (PyAutoLens#618/#623/#627, all closed).

**Certified:** one-shot at local (corr 0.83 / 0.14" / 6.2 sigma) and mid
(0.84 / 0.34" / 9.3 sigma) tiers on earth-rotation-synthesis uv; iterative ==
one-shot at mid tier after the LM formulation-bug fix (al#629: objective
double-counted state dpsi; warm start exposed it as anti-correlation -0.83;
interferometer-only). Certified recipe = warm-start from one-shot +
reg_optimize_every=1 (al#628) + regime gate; evidence self-protects in every
configuration tested.

**Full-tier A100 mass sweep (RAL job 330633, 70,200 vis, 128x128):** 1e10 =
5.8 sigma 0.46" (gate 203 — the subhalo's own imprint dominates smooth
residuals at noise 0.5); 1e9 = DETECTED 4.1 sigma 0.51" (gate 1.37); 1e8 =
non-detection (uncorrelated 3-sigma field peak 2.5" away). Sensitivity floor
of this configuration between 1e8 and 1e9 Msun; ~2.5-3.5 min per mass
end-to-end on one A100 (sparse route = mask-pixel scaling). VLBI-resolution
config toward the ~1e6 Msun B1938 regime is the natural follow-up.

**Shipped:** campaign harness merged (autolens_workspace_developer#107 —
3 tiers, synthesis uv, regime gate, noise-keyed precision-operator cache,
NUFFT above the 10k-vis guard, --warm-start/--reg-optimize/--subhalo-mass);
interferometer workspace feature layer merged (autolens_workspace#286:
features/potential_correction/start_here.py = certified local-tier recipe
verbatim + likelihood_function.py = hand-built dual-route evidence, dense ==
sparse == fit to 8 decimals); guide interferometer section (ws#285) and
imaging x0 parity (al#630) merged earlier in the arc.

**Traps recorded:** RAL sbatch must source autolens_profiling/activate.sh
(no /mnt/ral/jnightin/PyAuto/activate.sh); >10k vis needs
transformer_class=al.TransformerNUFFT in simulator AND re-wrap; precision
operator is noise-dependent (key the cache); local outputs preserved in
canonical autolens_workspace_developer/output/potential_correction_campaign.

## Original prompt

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
