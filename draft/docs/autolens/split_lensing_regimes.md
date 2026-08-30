# Split lensing regimes: multi_galaxy / group / cluster (epic plan)

Type: docs
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoGalaxy
- autolens_workspace
- autolens_workspace_test
- autogalaxy_workspace
- autogalaxy_workspace_test
- autolens_assistant
Themes:
- cluster
- docs-hub
- notebooks
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: planned (epic — execute via the child prompts below)
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Filed: 2026-07-25 (backfilled from git)

Reorganize the PyAutoLens (and mirrored PyAutoGalaxy) documentation and example
library by splitting systems above the standard single-galaxy strong-lens
regime into THREE distinct categories, each with its own tutorials, example
scripts, API documentation and modelling philosophy:

  1. `multi_galaxy`  (NOT `multi_galaxy_lens` — concise, and mirrors the
     autogalaxy package name; no collision with `multi/`, which stays
     multi-dataset/wavelength)
  2. `group`
  3. `cluster`

This file is the coordinating plan: the regime design, the literature research
grounding each regime's examples, the current-state audit, the technical
conventions checklist, and the index of PR-sized child prompts. It was
re-planned in Fable from the original intake on 2026-07-25.

## The taxonomy (applies to all narrative prose)

All group- and cluster-scale lenses are multi-galaxy systems, but not vice
versa. The three regimes form a ladder, not three islands:

- `multi_galaxy` — ≥2 co-dominant galaxy-scale deflectors (individual halos
  ~10^11–10^13 M_sun), NO dominant host halo. Mass = one EPL/SIE per
  significant deflector (+ external shear). Source = standard extended-source
  workflow (Sersic/MGE or Delaunay/adaptive pixelizations), unchanged from
  `imaging/`.
- `group` — adds a DOMINANT group-scale dark halo (~10^13–10^14 M_sun) as an
  EXPLICIT, OPTIONAL modelling choice, and represents member galaxies as
  tidally truncated subhalos (dPIE / truncated isothermal) tied by luminosity
  scaling relations. Typically ONE dominant extended source, so the
  source-modelling philosophy is UNCHANGED — the sophistication moves into
  the mass model. Every group tutorial teaches BOTH compositions
  (members-only vs members+halo) and when a halo is scientifically motivated.
- `cluster` — the SAME mass framework as group (host halo(s) >10^14 M_sun,
  many truncated members, scaling relations). What changes is the
  observational regime and therefore the SOURCE STRATEGY: dozens–hundreds of
  members lens many independent sources over a wide redshift range, so the
  default workflow is multiple-image positions / point-source constraints
  with per-source redshifts and joint optimization of one mass model
  (multi-plane). Extended-source reconstruction is a specialised follow-up of
  individual systems, never the default.

Key design principle: group and cluster share the mass-modelling framework;
the regime boundary PyAutoLens draws between them is the source-modelling
strategy, not the mass parameterization.

Three-tier galaxy API: the main_galaxies / extra_galaxies / scaling_galaxies
tiers are retained across ALL regimes. Basic multi_galaxy examples use just
main_galaxies (extra/scaling as feature extensions); group and cluster
defaults use all three tiers. Scaling galaxies at galaxy/multi_galaxy scale
use UNTRUNCATED isothermals — truncation encodes tidal stripping by a host
halo, which those regimes lack by definition; truncated dPIE members appear
at group scale. This physical thread ties the ladder together.

## Literature research (grounding for examples and citations)

Researched via web search 2026-07-25; all arXiv IDs verified against arxiv.org.

### Cluster regime

Flagship `start_here`: **Abell 2744** on the Bergamini et al. 2023 (A&A 670,
A60; arXiv:2207.09416) spectroscopic gold subset — CONFIRMED as the right
choice (already implemented). Two caveats for the docs: (i) state explicitly
that the tutorial uses the pre-JWST spectroscopic gold subset by design
(speed + robustness) — JWST-era models of the same cluster now use ~135–150
images (Bergamini et al. GLASS-JWST, arXiv:2303.10210; Furtak et al. 2023,
arXiv:2212.04381/UNCOVER); (ii) A2744 is a merging multi-halo system — good
for teaching "one or more host halos", but point to AS1063 (Caminha et al.,
arXiv:1512.04555) as the "simplest relaxed real cluster" counterpoint.

Secondary systems for feature examples (public constraint catalogues):

- **MACS J0416** — Bergamini et al. 2023 (arXiv:2208.14020): 237
  spectroscopic images from 88 sources (z=0.94–6.63), the largest secure
  sample for any cluster; team inputs public. The "scaling-up" example.
- **SMACS J0723** (JWST First Deep Field) — Mahler et al. 2023
  (arXiv:2207.07101), Caminha et al. 2022 (arXiv:2207.07567); compact,
  iconic, modest constraint count — the mid-size example.
- **MACS J1149 + SN Refsdal** — Grillo et al. 2016 (arXiv:1511.04093),
  Kelly et al. 2023 Science (arXiv:2305.06367, H0 from the reappearance),
  Grillo et al. 2024 (arXiv:2401.10980) — the time-delay-cosmography
  feature example (point sources + delays + multi-plane).
- **Abell 370** — Lagattuta et al. 2019 (arXiv:1904.02158), BUFFALO
  strong+weak Niemiec et al. 2023 (arXiv:2307.03778) — a second HFF cluster
  with a very different (bimodal giant-arc) configuration.
- **SDSS J1004+4112** — genuinely cluster-scale (~10^14 M_sun) 5-image
  lensed quasar, longest measured delay (6.73 yr); Forés-Toribio et al.
  2022 (arXiv:2206.09856). Bridges galaxy-scale point-source users to the
  cluster machinery.

Benchmark programs to cite: HFF (Lotz et al. 2017, arXiv:1605.06567; public
lens models from ~8 teams at MAST, incl. LensTool .par files — feeds the
lenstool/ interop example), CLASH (arXiv:1106.3328), RELICS
(arXiv:1903.02002), BUFFALO (arXiv:2001.09999), JWST UNCOVER
(arXiv:2212.04026), SGAS (Sharon et al. 2020, arXiv:1904.05940 — LensTool
models for 37 clusters, the volume source for interop testing), MUSE atlas
(Richard et al. 2021, arXiv:2009.09784 — public redshifts + LensTool models
for 12 clusters).

Methodology reading list: Kassiola & Kovner 1993 ApJ 417,450 (PIEMD;
pre-arXiv — cite journal); Elíasdóttir et al. 2007 (arXiv:0710.5636, dPIE
defined in the appendix); Jullo et al. 2007 (arXiv:0706.0048, Lenstool
Bayesian MCMC); Broadhurst et al. 2005 (astro-ph/0409132, first ~100-image
cluster, A1689); Bergamini et al. 2019 (arXiv:1905.13236, kinematically
calibrated scaling relations); Meneghetti et al. 2017 (arXiv:1606.04548, HFF
model-comparison project); Meneghetti et al. 2020 Science (arXiv:2009.04471,
GGSL substructure excess — the science case for r_cut_ref); Natarajan et al.
2024 review (arXiv:2403.06245 — the modern overview). Other codes to name:
GLEE (Suyu & Halkola 2010), GLAFIC (Oguri 2010, arXiv:1005.3103), free-form
GRALE / WSLAP+ / SWUnited.

### Group regime

Flagship recommendation: **CASSOWARY 19 (SDSS J0900+2234)** — extended bright
arc + counter-images from a single dominant source (z=2.03, a merging pair),
lens group z~0.49, theta_E ~ 7", M(<theta_E) ~ 1.4e13 M_sun; public HST via
MAST; and the published model (Ding et al. 2025, RAA, arXiv:2504.11445) is
ALREADY a PyAutoLens model co-authored by the team — dPIE group halo + 16
dPIE members + external shear, Sersic-to-adaptive-pixelization source chain —
so the docs reproduce a refereed result. Suggested split: keep the current
fast Euclid dataset for `start_here` (2 main galaxies, minutes-scale) and
make CSWA 19 the `features/group_halo/` halo-choice tutorial's system (model
the 3–5 brightest members explicitly + scaling relation for the rest, with
and without the group halo). Final call at implementation time.

Secondary systems for feature examples:

- **SL2S J02140-0535** — the clean "3 central galaxies + one NFW group halo"
  system; dynamics breaks the r_s degeneracy; Verdugo et al. 2011
  (arXiv:1005.1566), 2016 (arXiv:1608.03687).
- **CASSOWARY 31** — BGG-dominated fossil group; BGG dominates <20 kpc, halo
  beyond — i.e. whether you NEED the halo depends on the radii the arcs
  probe; Wang et al. 2022 (arXiv:2203.13759), multi-plane extension
  arXiv:2404.13205.
- **SL2S J08544-0121** — a member's tidally TRUNCATED halo measured directly
  from arc perturbation (Suyu & Halkola 2010, arXiv:1007.4815; Limousin et
  al. 2010, arXiv:0906.4118) — the canonical observational justification for
  dPIE member profiles.
- **Cheshire Cat (SDSS J1038+4849)** — two BGGs, merging fossil group, two
  sources (Irwin et al. 2015, arXiv:1505.05501) — the "when one halo is not
  enough" showcase.
- **Cosmic Horseshoe** — CONTRAST case, verified galaxy-scale: group-scale
  theta_E (~5") from a single ultra-massive LRG + shear, NO group halo
  needed in any published model (Belokurov et al. 2007 astro-ph/0706.2326;
  Melo-Carneiro et al. 2025 arXiv:2502.13788 — PyAutoLens-based SMBH
  measurement). SDSS J1004+4112 and Abell 3827 are cluster-scale — cross
  reference them from cluster docs, not group examples.

The halo-choice literature chain (the regime's signature tutorial): AGEL
environments — ~half of deflectors live in group/cluster halos but <10% have
group-scale Einstein radii, i.e. environment often contributes shear without
dominating (Gottemoller et al. 2026, arXiv:2602.11068); Newman, Ellis & Treu
2015 (arXiv:1503.05282, bridging galaxy-to-cluster profiles with 10 group
lenses); More et al. 2012 (arXiv:1109.1821, arc radius >~2" implies
environmental mass); Verdugo (halo suffices) vs Suyu & Halkola (member
subhalo individually constrained) as the two poles; Foëx et al. 2014
(arXiv:1409.5905, lensing selection bias toward concentrated groups — why
tutorial systems are not "typical" groups).

Samples/surveys to cite: SL2S groups (Limousin et al. 2009, arXiv:0812.1033
— 13 systems framed exactly as the 1e13–1e14 M_sun gap), SARCS (More et al.
2012 arXiv:1109.1821; Foëx et al. 2013 arXiv:1308.4674 — 80 secure groups),
CASSOWARY (Belokurov et al. 2009 arXiv:0806.4188; Stark et al. 2013
arXiv:1302.2663), AGEL DR2 (arXiv:2503.08041), Euclid Q1 discovery engine
(arXiv:2503.15324) — which operationally defines group-scale as ">1 and <25
member galaxies", a definition worth quoting in the docs.

### Multi-galaxy regime

Flagship `start_here`: **SDSS J1011+0143** — the system of the user-suggested
arXiv:1602.02927 (Shu et al. 2016, ApJ 820, 43), which holds up as the best
verified match. A close MERGING PAIR of lens galaxies (projected sep ~4.2 kpc)
at z=0.331 lensing a Lya emitter at z=2.701 into a wide (theta_E ~ 1.84")
cross/arc with three resolvable knots; the published model is exactly the
regime's default (two SIEs + shear); public archival HST F555W/F814W (MAST);
science hook: mass/light offsets up to ~1.7 kpc — a result a single-SIE model
physically cannot produce, which motivates the whole regime. Discovery paper:
Bolton et al. 2006 (astro-ph/0606210). Runner-up: B1608+656 (richer extended
ring, deeper public ACS, but dust + AGN images + group environment make it an
advanced example, not a start_here). Implementation note: pin down the HST
program ID in MAST when building the dataset; simulate a look-alike if the
real frames prove unsuitable for redistribution.

Secondary systems for feature examples:

- **B1608+656** — two INTERACTING deflectors + extended dusty host ring;
  Suyu et al. 2009 (arXiv:0804.2827) potential reconstruction and Suyu et
  al. 2010 (arXiv:0910.2773) H0 — the canonical two-deflector cosmography.
- **PS J0630-1201** — five-image quasar from a dual-SIE lens with a host
  arc; Lemon et al. 2018 (arXiv:1803.07601) — image-multiplicity feature.
- **2M1310-1714** — galaxy pair inside a ~2.9" Einstein ring, public
  HST/WFC3; Lucey et al. 2018 (arXiv:1711.02674).
- **HE0230-2130** — two same-redshift deflectors and a missing fifth image
  constraining cored profiles; Ertl et al. 2024 (arXiv:2308.05181).
- **J1721+8842** — the "Einstein zigzag": two deflectors at DIFFERENT
  redshifts (z=0.184, 1.885), six images; Dux et al. 2025
  (arXiv:2411.04177) — the bridge to multi-plane features. Pair with
  **J0946+1006** (the Jackpot, Gavazzi et al. 2008 arXiv:0801.1555) while
  stating explicitly that the Jackpot is a SINGLE deflector with multiple
  source planes — i.e. multi-plane, NOT multi-galaxy; a useful taxonomy
  clarification for the docs.

Statistics/context: no clean literature number exists for "what fraction of
galaxy-scale lenses have co-dominant secondary deflectors" — the literature
splits into satellite-incidence statistics (Jackson et al. 2010
arXiv:0912.0614; Nierenberg et al. 2011 arXiv:1102.1426) and per-sample
modelling choices (Shajib et al. 2019 arXiv:1807.09278; STRIDES 30-quad
sample Shajib et al. 2022 arXiv:2206.04696) — state that gap honestly in the
docs. Theory anchor: Möller et al. 2001 (astro-ph/0103093). Forward-looking
motivation: Euclid Q1 discovery engines (arXiv:2503.15324, 2503.15327 —
~500 candidates in 63 deg^2, >100k forecast full-survey). PyAutoLens
precedent to cite: Etherington et al. 2022 (arXiv:2202.09201, 59 automated
HST lens fits) and Ding et al. 2025 (arXiv:2504.11445, CSWA 19 modelled at
pixel level with PyAutoLens through a Sersic-to-adaptive-mesh chain).

## Current-state audit (2026-07-25)

Already in place (do not rebuild):

- `autolens_workspace/scripts/cluster/` — real Abell 2744 `start_here` (7 gold
  systems / 25 images from the Bergamini et al. 2023 model inputs, 2 BCGs, 188
  scaling members, NFW host, multi-plane, JAX point solver), `csv_api.py`
  (mass/light/point + scaling_galaxies CSVs), `lenstool/` interop,
  `mass_parameterizations.py` (+ `_pyautolens.py`) with the expert-reviewed
  Lenstool-convention models.
- `autolens_workspace/scripts/group/` — real Euclid dataset `start_here`
  (2 main lens galaxies, MGE light, centre-GUI JSON), `features/`
  (scaling_relation, pixelization, MGE, …), SLaM. Gaps: `start_here` fits
  main_galaxies only (no scaling/extra tiers); NO host-halo example — the
  halo-choice tutorial does not exist; README still frames groups only by
  galaxy count.
- `autolens_workspace/scripts/imaging/features/` — `extra_galaxies/` and
  `scaling_relation/` exist; regime-caveat prose and
  interferometer/point_source parity need auditing.
- PyAutoGalaxy library — multiple-galaxy composition, `sr` scaling-relation
  namespace, and the CSV APIs (`galaxy_table_from_csv`,
  `galaxies_from_csv_tables`, `galaxy_models_from_csv`) already exist and
  re-export through autolens. The library side of this epic is docs, not API.
- PyAutoLens `docs/overview/overview_2_new_user_guide.md` — routes
  galaxy/group/cluster; needs the multi_galaxy rung and the ladder rewrite.

Missing entirely: `multi_galaxy` packages (both workspaces), autogalaxy
`cluster` package, group halo-choice tutorial, cluster extended-source
follow-up feature, regime restructure of both RTD doc trees.

## The galaxy/lens divergence (record once, state everywhere relevant)

autogalaxy mirrors the regime split with `multi_galaxy` and `cluster`
packages of its own (light-only: no mass, no sources). Deliberate divergence:
the autogalaxy cluster workflow MODELS the foreground galaxies' light (that is
its entire subject), while the autolens cluster default workflow does NOT
model foreground lens light (point-source constraints only; lens-light
modelling arrives later as an autolens feature). This is the first significant
structural departure between the galaxy and lens doc trees — both New User
Guides must state it so users moving between libraries are not surprised.

## Technical conventions checklist (from expert review, 2026-07 Slack)

Verify these hold everywhere the group/cluster mass framework is documented.
STATUS 2026-07-25: applied to `cluster/mass_parameterizations.py` and
`cluster/mass_parameterizations_pyautolens.py` (the expert-reviewed guides)
and to the dPIE library docstrings (sigma_LT/sigma_0 attribution corrected
per the H. Ding derivation note) on this task branch. STILL DATED:
`cluster/start_here.py`, `cluster/simulator.py`, `cluster/modeling.py` (and
the bundled `cluster/simple` dataset simulated from the old truths —
r_core scaled with L, radius exponent 0.5, r_cut_ref 15.8") — swept by the
cluster_regime_narrative child prompt, which must re-run the simulator to
regenerate the dataset alongside the convention change.

- Members: r_core fixed to a negligibly small value and NOT scaled with
  luminosity (r_a = 0 is safe — handled analytically, no division-by-zero).
- Scaling relation: Bergamini et al. 2019 form — dispersion exponent alpha
  and truncation exponent beta tied via 2*alpha + beta = 1 + gamma, with
  gamma = 0.2 fixed (the old Lenstool-paper slopes are dated); exponents
  free-able in detailed modelling, and beta_a vs beta_s need not be equal
  unless r_a/r_s is assumed constant.
- r_cut_ref: reference member truncation ~5", not 20" (lensing-constrained
  typical values; scientifically interesting via the Meneghetti et al.
  substructure-lensing excess).
- Host halo: dPIE with fixed r_cut is the Lenstool-literature default and
  stays the default example; the (G)NFW alternative is documented as the
  physically preferred choice ("beyond the LensTool default" guide).
- sigma vs b0: dPIEMass takes velocity dispersion (dPIEMassB0 keeps the
  angular parameterization); the sigma_LT-vs-sigma_0 convention mismatch
  (Elíasdóttir et al. 2007 vs Kassiola & Kovner 1993) is documented per the
  contributed derivation note — b0 != Einstein radius for finite r_s.

## Child prompts (one prompt = one task = one PR) and execution order

1. `draft/docs/autolens/multi_galaxy_package.md` — new
   `autolens_workspace/scripts/multi_galaxy/` package (+ workspace_test
   mirror). Unblocks everything user-facing; do first.
   CORE SHIPPED 2026-07-25; features/scaling_galaxies, fit.py and the
   workspace_test jax_likelihood variant 2026-07-26. Remaining: real
   J1011+0143 data swap-in (MAST unreachable from cloud sessions — needs a
   local/unrestricted-network session).
2. `draft/docs/workspaces/group_halo_explicit_choice.md` — group start_here
   gains all three tiers; new `features/group_halo/` halo-choice tutorial.
   SHIPPED: halo tutorial 2026-07-25; three-tier start_here (with an
   image-derived scaling_galaxies.csv for the real Euclid dataset) and the
   modeling/simulator halo-narrative threading 2026-07-26. Full scope
   landed; CSWA 19 real-data flagship recorded as a non-blocking future
   option.
3. `draft/docs/workspaces/cluster_regime_narrative.md` — cluster narrative
   alignment + `features/extended_source/` follow-up example + conventions
   cross-check.
4. `draft/docs/autolens/docs_three_regime_restructure.md` — PyAutoLens RTD
   docs ladder rewrite (after 1, so links resolve). SHIPPED 2026-07-26:
   New User Guide ladder + flagships, overview_1 enumerations, api
   mass/point/galaxy regime notes + CSV-catalogue section, model_cookbook
   regime recipes.
5. `draft/docs/workspaces/galaxy_scale_scaling_extra_features.md` —
   imaging/interferometer/point_source extra_galaxies + scaling_galaxies
   feature parity with regime caveats.
6. `draft/docs/workspaces/autogalaxy_multi_galaxy_package.md` — SHIPPED
   2026-07-25 (autogalaxy_workspace#168 + test#97).
7. `draft/docs/workspaces/autogalaxy_cluster_package.md` — SHIPPED 2026-07-25
   (same PRs; catalogue-driven light tier + divergence note).
8. `draft/docs/libraries/autogalaxy_docs_regime_guides.md` — SHIPPED
   2026-07-25 (PyAutoGalaxy#526, New User Guide system-scale ladder).
9. `draft/docs/workspaces/assistants_regime_extension.md` — assistants
   follow-up (deferred until 1–8 ship).

1–4 are the PyAutoLens-facing core (Priority: high); 5–8 are the mirror and
parity passes (normal); 9 is deferred. 1, 6 and 7 are independent of each
other and parallelizable; 2 and 3 touch disjoint packages and can run in
parallel with 1.
