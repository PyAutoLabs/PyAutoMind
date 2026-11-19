# CDM dark matter sightlines (research)

Type: research
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoGalaxy
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Lane: gpu

## Original request (verbatim, 2026-11-19)

I want to begin simulating strong lens dark matter sightlines corresponding to CDM, with other DM matter models
follow up for a future issue. I want to be able to simulate two types:

1) Lens subhalos, the CDM subhalos found at the same red as the lens galaxy.
2) Line of sight halos, the CDM halos found at different redshifts along the line of sight to the source galaxy.

For line of sight halos, I am happy to do full multi plane ray tracing (but maybe with sliced redshift planes)
rather than trying to use approximations like the Born approximation.

In fact, I think the source code can already do line of sight subhalos, but verifying the existing code is worth
while as its been a while since we used it and comparing it to l,iterature approahes and other software packages
is a good starting point. It is pretty much based on the work https://arxiv.org/abs/2010.13221

This functionality should fully support JAX and run on GPU, I think the existing implementation does but I could
be wrong. There is also the Kappinghat SIDM implementation that I developed with someone on GitHub, this defintely
supports JAX and gives an example API for how we support itm, but again we can review and assess if theres
a better API or approach.

In terms of lens subhalos, I tihnk we want the implementation of Conor O'Riodan:

https://arxiv.org/abs/2509.02660

and earlier works by him and Simona Vegetti. This means we need to think carefully about how we treat stuff
like truncation, tidal stripping, and the mass function of subhalos. I think we should be able to use the existing
subhalo implementation in the code base, but we should review it and make sure it is consistent.

We probably want to be simulating subhlalso all the way from 10^6MSun to 10^10MSun (anything above we would defect individually, 
and line of sight halos from 10^6MSun to 10^0MSun.

Building on the Conor paper, It hink we would benefit from at-time-simulation outputs which provide figures
showing how, if at all, the subhalos change the image and give some kind of chi sqaured metric for how it changes.
Note that these are optimstic because most the signal will be lost to the lens mass model and the source model, and
mass sheet transform.

Review the dark package in PyAutoGalaxy and assess if we need new profiles or parameterizations.

Kassidy's paper focuwed on SIDM, but we should also think about this parameterization which allows for steeper
and shallower slopes than CDM and I would be keen to have it work its way into this implementation even if its
going a bit WDM or SIDM-y, but only if you think theres a physically motivated reason to use it.

https://arxiv.org/abs/2510.17956

This is a Fable high research dive so do deep research and come up with a plan, we may well do a lot of work and development
as a science project standalone before we bring stuff into the source code.

## Status

Research dive done 2026-11-19; no library code was changed. The work continues as the development
science project `dm_sightlines` (`Science/development/dm_sightlines`, Cortex key `dm_sightlines`,
born 2026-11-19, local git, no remote). Its `wiki/project/plan.md` is the plan of record, with the
numerical checks in `results/verification_2026-11-19/` and the literature and software notes in
`wiki/project/literature/`. Code audited: `@PyAutoLens` `main` a79a6b22c (`autolens/lens/los.py`,
`autolens/lens/substructure_util.py`) and `@PyAutoGalaxy` `main` b9232172
(`autogalaxy/profiles/mass/dark/`).

The project is exploratory and separate from the Mind orchestrator (see Decisions). Library
changes it leads to are filed here one bounded prompt at a time, when they are ready.

## Findings in brief

Line-of-sight halos. `LOSSampler` follows the He et al. 2022 recipe (arXiv 2010.13221) and passed
independent checks: the power-law fit is within 2.7% of the Sheth-Tormen function it fits; the
concentration fit is within 0.3% of colossus Ludlow16; the negative sheets match the Monte Carlo
mean halo convergence to 0.1% over 20,000 seeds; `NFWTruncatedSph` matches lenstronomy `TNFW` to
5e-9; the three workspace-test JAX scripts pass. It is not ready for a 1e6 solar mass lower limit:

- The default is 4 + 4 planes (slices 0.10 to 0.15 wide in redshift). The paper uses 0.01 and its
  Appendix A shows 0.05 can already matter. No convergence test of our default has been run.
- The cone behind the lens narrows by 1.0 arcsecond times the distance ratio in the code and by
  2.0 arcseconds in the paper.
- At a 1e6 lower limit there are about 10,390 halos (1,282 at 1e7): 30 s per image on CPU and
  9.3 GB without chunking on a 101 by 101 grid; 1.28 s per image on the laptop GPU at 1e7.
- The negative-sheet integral costs 28 to 39 s per realisation although it does not depend on the
  seed.
- Five library defects, filed as separate bug prompts (see Filed tasks).

Lens subhalos. No subhalo population sampler exists in the libraries or workspaces. The O'Riordan
papers (arXiv 2211.15679, 2310.10714, 2509.02660) use M_max as the mass, untruncated NFW subhalos in
(v_max, r_max), a mass function proportional to m^-1.9 normalised by f_sub = 0.01 of the lens mass
inside two Einstein radii, uniform placement inside two Einstein radii, a single plane and no
line-of-sight halos. Their concentration relation differs between the 2023 paper (own power law,
r_max = 0.344 kpc (v_max / 10 km/s)^1.607) and the 2024 and 2025 papers (Moliné et al. 2022, equation
not stated) by about 2.6 times in r_max at z = 0.5. Their table maps a virial mass of 1e8 solar
masses to M_max = 10^6.2.

Profiles. No new profile is needed for CDM: `NFWTruncatedSph` is what pyHalo, paltas and He et al.
use. It needs the fixes filed below, constructors from (v_max, r_max) and from (M200, c, r_t in
kpc), and a real-valued deflection. The gNFW inner slope of Kollmann et al. (arXiv 2510.17956) has
a physical case only for subhalos above about 10^9.5 solar masses, which host galaxies (Heinze et
al. 2024 find inner slopes near -2 in TNG50), and for the non-CDM follow-up. Recommendation: carry
`inner_slope` as an optional per-halo column from the start and build a truncated gNFW later.

Diagnostics. Recommended: a ladder of expected chi-squared differences written at simulation time.
Tier 0 is the raw image difference; tier 1 is a linearised refit using JAX Jacobians over nested
parameter sets (macro mass, source, a mass-sheet direction, multipoles); tier 2 is a pixelised
source inversion; tier 3 is a full non-linear refit on a subset. Also the difference as a function
of a lower mass cut, the analogue of O'Riordan's cutoff experiment.

Plan. Six phases: (0) library bugs; (1) population layer for line-of-sight halos, arrays-first with
colossus; (2) chunked JAX render layer plus plane-spacing, cone, mass-limit and truncation
convergence studies and a lenstronomy cross-check; (3) subhalo sampler with a fiducial preset and
an `ORiordan2025` preset; (4) diagnostics; (5) science checks and a statistical cross-check against
pyHalo; (6) promotion into PyAutoGalaxy, PyAutoLens and the workspace.

## Decisions

All by the human, 2026-11-19.

- "file the five library bugs and record it in PyAutoMind, go with conors most rercent
  parametterization." The five bugs are filed (below). The `ORiordan2025` preset follows the most
  recent papers (2024 and 2025: the Moliné et al. 2022 v_max to r_max relation and the 2509.02660
  mass function), not the 2023 power law.
- "go with your recommendations, create the dm_sightlines project." So: the fiducial mass variable
  is infall M200c over 1e6 to 1e10 solar masses for both populations, with M_max and bound mass as
  derived columns; the fiducial subhalo truncation is the Roche radius first, tidal-track bound
  masses later; the project lives at `Science/development/dm_sightlines`.

- "not sure on Moline so just choose one." The session chose the redshift-dependent fit of Moliné
  et al. 2022 (arXiv 2110.02097; no distance-from-host term) for the preset, because O'Riordan and
  Vegetti 2024 call it "the redshift dependent v_max to r_max relation" and it is the only
  redshift-dependent subhalo fit in that paper. The O'Riordan papers do not name the equation, so
  this is a reading of them. Formula and coefficients are in the project's `AGENTS.md`.
- "I think its prob separate.... the insight we learn which then would make its way into the
  source code is what makes its way into Mind but the point is this project is exploratory." So
  the project is not a Mind epic and is not run by the Mind orchestrator. Mind receives bounded
  prompts for library source changes as the project produces them; the five bugs below are the
  first. The project's phases are never filed here.

Nothing is open in this record. It stays as the pointer from Mind to the project.

## Filed tasks

- Five library defects, one prompt each (all shipped 2026-11-19; follow-ups in `draft/bug/autogalaxy/nfwtruncatedsph_convergence_loses_precision_near_scale_radius.md`, `draft/bug/autolens/substructure_jax_grad_is_nan_when_a.md`, `draft/bug/autolens/lossampler_silently_ignores_a_non_planck_cosmolo.md`, `draft/bug/pyautoheart/colab_gate_colossus_rationale_is_stale_once.md`):
  - `complete/2026/11/nfwtruncatedmcr-truncation-radius.md` (shipped 2026-11-19, PyAutoGalaxy#733)
  - `complete/2026/11/lossampler-hmf-import-fails-and-los-halos.md` (shipped 2026-11-19, PyAutoLens#868 + autolens_workspace#681)
  - `complete/2026/11/nfwtruncatedsph-total-mass.md` (shipped 2026-11-19, PyAutoGalaxy#735)
  - `complete/2026/11/substructure-halo-arrays-overflow.md` (shipped 2026-11-19, PyAutoLens#870 + autolens_workspace#682)
  - `complete/2026/11/nfwtruncatedsph-small-radius-deflection.md` (shipped 2026-11-19, PyAutoGalaxy#737)
- Further candidate tasks are staged as bullets in `ideas.md` tagged
  `[from: research dm-sightlines-cdm]`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/research.md -->
