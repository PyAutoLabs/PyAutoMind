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
