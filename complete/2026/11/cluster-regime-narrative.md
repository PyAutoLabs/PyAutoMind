## cluster-regime-narrative
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/670
- completed: 2026-11-18
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/671
- scope merged: the prose half only. `scripts/cluster/README.md` gained the regime-ladder framing (same mass framework as `group/`, point-source default, lens light not modelled) and a "Literature and benchmark systems" section; `scripts/cluster/start_here.py` notes the pre-JWST gold subset and points to `mass_parameterizations.py` (dPIE→gNFW host) and AS1063.
- merge fixes (2026-11-18, /health session): the README no longer names `features/extended_source` (it does not exist and failed the navigator path check); `main` merged into the branch and the navigator catalogue regenerated (`cluster/mass_parameterizations.py` was missing from `workspace_index.json`, stale on `main` too). CI 8/8 GREEN incl. smoke 3.12 and 3.13.
- not shipped — deferred: the `features/extended_source/` example and its `autolens_workspace_test` integration script. Human ruling 2026-11-18: cluster extended sources will not be developed for a while. The three open questions from #670 (data, mass-model handoff, sequencing after phase 9) were moved to `draft/feature/workspaces/cluster_pixelized_analysisfactor.md` (Source & Cluster arc phase 10), which already owned this plan.
- shipped by: shift worker batch 2026-11-14-pm2 (supervised --auto, decision-taken PR); merged from a /health session on the human's explicit command.

## Original prompt

# Cluster package: point-source-default narrative + extended-source follow-up feature

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
- autolens_workspace_test
Themes:
- cluster
- point-source
- notebooks
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: notify
Witness: `start_here.py`, `simulator.py` and `modeling.py` carry the corrected Bergamini+19 conventions (tied exponents at gamma=0.2, vanishing unscaled member cores, r_cut_ref ~5"), the regenerated `cluster/simple` dataset is committed in the same change as the simulator truths that produced it, and `modeling.py` and `start_here.py` both run end-to-end against that regenerated dataset.
Review-minutes: 0
Unattended: ready
Verified: 2026-11-14 c2c8b256 (autolens_workspace), 75e30695 (autolens_workspace_test)
Lane: any
Epic: cluster-strong-lensing
Phase: 10
Parent: draft/docs/autolens/split_lensing_regimes.md
Filed: 2026-07-25 (backfilled from git)

Align the `scripts/cluster/` package of @autolens_workspace with the
three-regime design (see parent plan). The mass framework (host halo(s) +
truncated members + scaling relations) is intentionally SHARED with the group
regime — the cluster regime is distinguished by the observational setting and
therefore the SOURCE MODELLING STRATEGY: dozens–hundreds of members, many
multiply-imaged sources across a wide redshift range, so the default workflow
is multiple-image positions / point-source constraints with individual source
redshifts, jointly optimizing one cluster mass model (multi-plane). Extended
source reconstruction is a specialised follow-up analysis of individual
systems, NOT the default.

Much of this package already exists (real Abell 2744 start_here on the
Bergamini et al. 2023 gold sample, dPIE + scaling relations, CSV API,
LensTool interop, mass_parameterizations guide). This task is narrative
alignment + gap-filling, not a rebuild.

## Changes

- `README.md` + `start_here.py` prose: state the regime-ladder design
  explicitly — same mass framework as `group/`, different source strategy;
  all clusters are multi-galaxy systems but not vice versa; link down the
  ladder to `group/` and `multi_galaxy/`.
- New `features/extended_source/` follow-up example: take one system from the
  cluster fit (e.g. one A2744 arc) and do a targeted extended-source
  reconstruction (imaging + pixelized source) with the cluster mass model as
  the starting point — framed explicitly as the specialised follow-up, and as
  the bridge back to the group/galaxy-scale source machinery. Note the
  foreground lens light is NOT modelled in the default cluster workflow (a
  deliberate divergence from @autogalaxy_workspace's cluster package, which
  is *about* the galaxies' light); an autolens lens-light cluster feature is
  future work, out of scope here.
- Conventions sweep — the guides (`mass_parameterizations.py`,
  `mass_parameterizations_pyautolens.py`) and the dPIE library docstrings
  were corrected on 2026-07-25 (Bergamini et al. 2019 tied exponents with
  gamma=0.2, vanishing unscaled member cores, r_cut_ref ~5", sigma_LT vs
  sigma_0 attribution per the H. Ding derivation note). STILL TO SWEEP here:
  `start_here.py` (scaling_radius_exponent=0.5, r_core scaled with L,
  r_cut_ref 15.8"), `simulator.py` (same dated truths) and `modeling.py`
  (refs fixed at those truths). The simulator truths and the bundled
  `cluster/simple` dataset must change TOGETHER — re-run the simulator and
  commit the regenerated dataset in the same PR, then re-validate modeling
  and start_here end-to-end (this is why the sweep was deferred to this
  child task rather than done alongside the guides).
- gNFW guidance: ensure the "beyond the LensTool default" prose (dPIE host →
  (G)NFW host) is present and linked from start_here, per the expert feedback
  recorded in the parent plan.
- Ground the narrative in the parent plan's cluster literature section
  (HFF/CLASH/JWST-era benchmarks, model-comparison projects) with citations.
  Specifics from the research: state that start_here uses the PRE-JWST
  spectroscopic gold subset of Bergamini et al. 2023 by design (JWST-era
  models of A2744 now use ~135–150 images); name AS1063 as the "simplest
  relaxed cluster" counterpoint to merging A2744; candidate future feature
  systems — MACS J0416 (largest spec sample, scaling-up), SMACS J0723
  (mid-size, JWST-iconic), MACS J1149/SN Refsdal (time-delay cosmography),
  SDSS J1004+4112 (cluster-lensed quasar bridge from point_source users).

## Conventions-sweep validation note (2026-07-25)

The sweep of simulator.py/modeling.py/start_here.py + regenerated
cluster/simple dataset landed on the task branch. modeling.py validated
green end-to-end (PYAUTO_TEST_MODE=2) against the regenerated data.
start_here.py (real a2744, 188 members, multi-plane) did NOT complete a
45-minute bypass-mode run on the dev container's CPU — the JAX compile of
the point solver dominates and is unchanged by the sweep (constants only;
2 fewer free parameters). It is not smoke-gated. First GPU session should
run it once to confirm end-to-end (expected ~10 min).

## autolens_workspace_test

Add/extend a cluster extended-source follow-up integration script.

## Acceptance

- Smoke suite green; notebooks + navigator regenerated.
- A new user reading cluster/README understands why cluster examples fit
  positions not pixels, and where the extended-source path lives.
