## dpie-lenstool-default
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/506
- completed: 2026-07-17
- prs: PyAutoGalaxy#509 (library) + autolens_workspace#287 + autolens_workspace_test#179 — all MERGED 2026-07-17
- summary: Made the Lenstool-native parameterization the DEFAULT dPIE. `dPIEMass`/`dPIEMassSph` now take the `.par`-file parameters (ellipticity, angle_pos, sigma=fiducial v_disp km/s, r_core, r_cut, redshifts, flat H0/Om0) so a fitted posterior reads like a published Lenstool results table; the internal (ra, rs, b0) form became `dPIEMassB0`/`dPIEMassB0Sph` + `dPIEMass.from_b0(...)` classmethods, and `from_lenstool` (general-cosmology converter) moved onto the B0 classes. Conventions re-verified against Elíasdóttir 2007 App. A (E0=6π·D_LS/D_S·σ²/c² A24; emass A26; r_em A21), Bergamini 2019 (σ0=√(3/2)σ_LT; β_cut=γ−2α+1) and the 6-leg parity script BEFORE the swap — it is a pure re-parameterization, no numerical change. Workspace phase migrated the whole cluster suite to σ_LT-space (tier free parameter is `sigma_ref` km/s — the referee's interpretable normalization), regenerated the simple + a2744 datasets, and rewrote the group SLaM scaling tiers to the reference-anchored `einstein_radius_ref·(L/L_BGG)^0.5` convention — absorbing the deferred `lenstool-scaling-slam` (PR3 of autolens_workspace#265), which is now superseded/done.
- traps:
  - **setattr on the Lenstool-parameterized class is a silent physics no-op**: b0 is derived from sigma+redshifts in `__init__` (same as NFWMCRLudlow), so perturbation/mutation harnesses must REBUILD the profile (fixed in wst likelihood_sanity.py).
  - **default dPIE config carries H0/Om0 PRIORS**: a main lens composed from a CSV lacking H0/Om0 columns floats those two cosmology constants as free params (a2744 start_here went N=22→26). Fix: pin mass.H0/mass.Om0 in the composition loops AND emit the columns in hand-authored CSVs (simulator-written CSVs already carry them via the instance constructor defaults). Caught only because the printed model N was wrong — verify free-param COUNT, not just "runs clean".
  - **navigator catalogue-staleness CI gate** now REQUIRES llms-full.txt/workspace_index.json committed current — the old #265 guidance ("revert catalogue drift, stage only scoped files") is obsolete; regenerate + commit the full catalogue (and any missing notebooks the prior PR left behind).
  - First `cluster/simple` regeneration emitted stub positions (1,0),(0,1) for both sources — transient (identical rerun perfect). Verify regenerated point datasets by ray-tracing positions through tracer.json: collapse happens at the FINAL source plane (PointSolver solves every source against the final plane; intermediate-plane collapse check fails by design).
  - Pre-existing/out-of-scope, untouched: `dPIEPotential` grad(ψ)=α FD FAIL in wst mass/total.py (O'Donnell profile); `database/scrape/scaling_relation.py` keeps its two-free-param compound-prior form deliberately; `potential_correction/subhalo_recovery.py` smoke failure was already RED on main (wst#179 merged with --admin for that one unrelated statistical assertion).
- notes: 3 `autolens_workspace_developer` scripts still reference the old parameterization (repo claimed by other tasks — deferred follow-up). Cluster/group science-teaching prose stayed on the judgment tier; mechanical ship steps delegated to Sonnet subagents.

## Original prompt

# dPIE: make the Lenstool-native parameterization the default profile

Type: feature
Target: PyAutoGalaxy (library) + autolens_workspace (cluster/group docs, slam pipelines)
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

## Original request (verbatim)

> The final step now is to make our default dPIE the LensTool one, whereas before
> I think we made it a classmethod of it, so swap them (e.g. the classmethod can
> be the current one which is non standard). Also, compare again to some lens
> tool papers to make sure we have the same parameterization, especially given
> that SLACK chat, and note that we had some issues making sure our slam.py
> pipelines are updated throughout in a consistent fashion. The end goal is for
> our dPIE to perfectly match the standard LensTool prescription, so readers of
> those papers know exactly what our model is doing.

## Context

Follows the recent dPIE-matches-Lenstool arc and the cluster-docs scaling-galaxy
work (Faber–Jackson reference-anchored convention: `einstein_radius_ref` free on
the brightest member / BGC, exponent fixed at 0.5, `rs ∝ L^0.5` truncation
scaling — see the Slack discussion with Niek Wielders around the reviewer
comment on Eq. 5).

Current state in
`PyAutoGalaxy/autogalaxy/profiles/mass/total/dual_pseudo_isothermal_mass.py`:

- `dPIEMass` / `dPIEMassSph` — base classes in the *internal* parameterization
  (`ell_comps`, `ra`, `rs`, `b0`), ported from Lenstool C code.
- `dPIEMass.from_lenstool` / `dPIEMassSph.from_lenstool` — classmethod
  converters from Lenstool-native inputs (`ellipticity`, `angle_pos`, `sigma`
  = fiducial v_disp, `r_core`, `r_cut`, redshifts, cosmology).
- `dPIEMassLenstool` / `dPIEMassLenstoolSph` — thin wrapper subclasses whose
  *free parameters are the Lenstool-native ones* (priors read like a Lenstool
  results table).

## Task

1. **Swap the hierarchy/naming so the Lenstool-native parameterization is the
   default dPIE** a user reaches for (e.g. `al.mp.dPIE*`), and the current
   internal `ra`/`rs`/`b0` parameterization becomes the non-standard variant
   (kept available, e.g. as a classmethod / secondary class). Decide and apply a
   clean naming scheme; update priors configs, `__init__.py` exports, and any
   `from_dict`/serialization touchpoints.
2. **Re-verify the parameterization against published Lenstool cluster papers**
   (Limousin et al. 2005; Elíasdóttir et al. 2007 App. A; Bergamini et al. 2019
   Eq. 5; plus a recent Lenstool-based cluster paper) — fiducial vs central
   sigma (sqrt(3/2)), b0 normalization and D_LS/D_S handling, emass vs epot
   ellipticity convention, r_core/r_cut mapping, and the scaling-relation form
   (sigma_0* L^1/4, r_cut* L^1/2 anchored to L* / BGC). The end goal: readers of
   Lenstool papers know exactly what our model is doing.
3. **Consistency sweep of downstream workspace scripts** — known problem: slam
   pipeline scripts drifted out of sync during earlier passes. Update
   consistently: `autolens_workspace/scripts/cluster/*` (modeling, simulator,
   csv_api, likelihood_function, start_here, lenstool/*),
   `scripts/group/features/scaling_relation/modeling.py`, weak a2744, guides
   (profiles/mass, light_and_mass_profiles), any slam pipelines referencing the
   dPIE/scaling tier, and the parity/test scripts in
   `autolens_workspace_test/scripts/cluster/` (lenstool_parity, likelihood_sanity,
   csv_api, simulator) + `mass/total.py` + developer scripts.
4. Keep the notebooks/scripts pairing consistent (notebooks regenerate at
   release, but scripts must be updated coherently).

## Acceptance

- Default dPIE profile exposes Lenstool-native free parameters; internal
  parameterization still reachable, clearly documented as non-standard.
- Lenstool parity script(s) still pass (deflections/convergence/potential match).
- All downstream scripts import/use the new default consistently; no stale
  `dPIEMassLenstool`-era references left half-migrated.
