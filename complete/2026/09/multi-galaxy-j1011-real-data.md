## multi-galaxy-j1011-real-data
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/549 (closed completed 2026-09-17)
- completed: 2026-09-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/554 (head `48c9298`, merge `30104f6`, label `pending-release`)
- summary: |
    The last open item of the `multi_galaxy` package prompt: `scripts/multi_galaxy/start_here.py`
    now fits the real HST ACS/WFC F814W imaging of SDSS J1011+0143 (programme 10831,
    `j9qj02010_drc.fits`, 2088 s, 0.05"/px — the frame Shu et al. 2016, ApJ 820, 43 modelled)
    instead of the simulated look-alike it shipped with on 2026-07-25. The data are bundled as a
    ~700 KB 201x201 cutout under `dataset/multi_galaxy/sdssj1011+0143/` (`data.fits`,
    `noise_map.fits`, `psf.fits`, `main_lens_centres.json`, `info.json`, a2744-style provenance
    `README.md`) with a committed, re-runnable `prep.py`: astroquery download of the archive's
    AstroDrizzle DRC product to a cache outside the repo, cutout centred on the midpoint of the two
    light centroids (0.860" apart), sky from the outer annulus, RMS noise-map from the WHT
    exposure-time map plus measured background RMS, PSF from an isolated star in the same frame.
    Nothing inside the 3" fit region needs an extra-galaxies mask, so the dataset ships without one
    and the script's noise-scaling step is gone; the mask GUI is kept behind `run_extra_galaxies_gui
    = False`. The simulated `simple` dataset and `simulator.py` are untouched (17 other
    multi_galaxy scripts use them); prose in `multi_galaxy/{README.md,simulator.py,slam.py}` now
    says `simple` is the look-alike and `start_here` fits the real frame. `.gitignore` +
    `dataset/.gitignore` allowlist the folder (and ignore its `__pycache__`); notebook mirrors and
    the navigator catalogue regenerated; `multi_galaxy/start_here.py` stays in `smoke_tests.txt`.

    The package itself landed in waves before this: core 2026-07-25 (start_here, simulator,
    modeling, README, smoke, notebooks), features/fit/jax legs 2026-07-26, and the feature tier via
    extra_galaxies (#391), scaling_relation (#396) and the group-parity phases (#417-#433) closed
    2026-07-31 — all recorded in the prompt's own `## Landed` sections below.

    Shipped under a human override. Heart was RED at PR-open on, verbatim, "install verification
    FAILED (testpypi; checks F)" and "release validation FAILED (stage integrate)" — the known Colab
    check F class that only a human release clears, unrelated to this workspace change. The human
    authorised the wrap-up in-session on 2026-09-17 ("So can we wrap up this all? e.g. push and
    whatnot") and then typed `/prm`; the reasons are quoted on the PR body and issue #549.
- witness: |
    `prep.py` re-run from a cold cache (215 MB MAST download) reproduces `data.fits`,
    `noise_map.fits`, `psf.fits` and `main_lens_centres.json` byte-for-byte; `info.json` differs
    only in `prep_date`. `check_dataset_allowlist.py` exit 0 (56 tracked dataset files, no capped
    should_simulate deletion path). `start_here.py` exit 0 under the CI smoke profile with
    `full_datasets` released, 17.4 s before and 17.0 s after merging main (#550/#551).
- ci: |
    PR CI 7/7 legs green (Smoke 3.12 + 3.13 + changes, Navigator x3, Size Guard). Merged as
    `30104f6`.
- notes: |
    (1) Two cloud-session resumes (09-11, 09-17) wrote "branch not on the remote (local-only or
    never created)" — but the local worktree already held the whole implementation uncommitted
    from a 2026-09-15 local session; a cloud note describes the remote only. Verify the worktree
    before re-planning from the issue.
    (2) The legacy MAST product name `j9qj02010_drc.fits` still resolves from the obs_id query even
    though a programme-level query lists HAP names (`hst_10831_02_acs_wfc_f814w_j9qj02_drc.fits`);
    prep.py needed no change.
    (3) A real fit of the data (24-start capped run) was started and stopped on the human's call;
    the human inspection round is deferred and nothing in the prose claims a fit result.
    (4) The workspace `.gitignore`'s `dataset/**` plus `dataset/.gitignore`'s `*` need BOTH
    negation sets; the folder-level `!**` then un-ignores `__pycache__` too, so an explicit ignore
    line for it is required.

## Original prompt

# multi_galaxy package: new regime package in autolens_workspace

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
- autolens_workspace_test
Themes:
- notebooks
- cluster
Difficulty: large
Autonomy: supervised
Priority: high
Status: in progress — core landed 2026-07-25; features/fit/jax legs landed 2026-07-26 (branch claude/pyautolens-doc-reorganization-w6a1l5); only the real-data swap-in remains
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Parent: draft/docs/autolens/split_lensing_regimes.md
Filed: 2026-07-25 (backfilled from git)
Issued: 2026-09-15

## Landed (2026-07-25, this task branch)

- autolens_workspace: scripts/multi_galaxy/ with start_here.py, simulator.py
  (J1011+0143-like merging pair — 0.9" separation, ~1.8" Einstein cross
  verified with 4 bright images + central image), modeling.py,
  README.md (regime-ladder + analysis-split table), features/README.md;
  top-level README ladder section; group/cluster README + start_here
  pointers; smoke registration (both fit scripts validated green under
  PYAUTO_TEST_MODE=2 from a clean slate); notebooks + navigator regenerated.
- autolens_workspace_test: scripts/multi_galaxy/model_fit.py (end-to-end,
  structural assertions locking the regime) + imaging/multi_galaxy_mge.py
  relocated to multi_galaxy/composition_mge.py; smoke updated; validated.
- PyAutoLens docs: New User Guide four-rung ladder + multi_galaxy links
  (full RTD restructure remains with docs_three_regime_restructure.md).

## Landed (2026-07-26, this task branch)

- `features/scaling_galaxies/` (simulator + modeling): five faint galaxies
  4–7" out on an untruncated-`IsothermalSph` relation
  (`einstein_radius = einstein_radius_ref * (L/L_ref)**0.5`, truth ref
  0.15"), shared-prior tier costing one free parameter, the "load of
  galaxies far from the lens / not a standard ingredient" framing, and the
  group/cluster truncation contrast. Smoke-registered and validated green.
- `fit.py`: N-deflector fit anatomy — per-galaxy deflection fields compared
  (mean-|deflection| co-dominance ratio 0.82), truth-composition
  `FitImaging` (full-res truth LL +27220), pointing at `imaging/fit.py` for
  the step-by-step API anatomy. Smoke-registered and validated green.
  Scope decision: a `likelihood_function.py` mirror was deliberately NOT
  added — the likelihood machinery is regime-independent and fully
  documented by `imaging/` + the group package; `fit.py` covers the one
  regime-specific piece (summed deflection fields).
- autolens_workspace_test `multi_galaxy/jax_likelihood/lp.py`: batched
  `fitness._vmap` literal + `jit(fit_from)` NumPy-parity round-trip over a
  two-co-dominant-deflector model; smoke-registered, runner-validated
  (15s).

## Remaining

- Swap start_here to the REAL SDSS J1011+0143 HST data (F555W/F814W via
  MAST) once frames are prepared; the simulated look-alike is the interim.
  BLOCKED from cloud sessions (2026-07-26): MAST is unreachable through the
  session proxy (`Tunnel connection failed: 403`) — needs a
  local/unrestricted-network session to download + prepare the frames.
  Re-measured 2026-09-11 (`/start_dev` from a cloud session): `mast.stsci.edu`
  and `archive.stsci.edu` both still `CONNECT tunnel failed, response 403`,
  so `/start_dev` was not run to an issue here — run it from a local CLI
  session, where the only work left is: download the F555W/F814W frames,
  prepare them with the `data_preparation` scripts, swap them into
  `multi_galaxy/start_here.py` in place of the simulated look-alike,
  regenerate the notebook and re-run the smoke entry.
  Re-measured 2026-09-17 (`/start_dev` resume of #549 from a cloud session):
  still blocked — `mast.stsci.edu`, `archive.stsci.edu`, `hla.stsci.edu`,
  `hst.esac.esa.int`, CADC, `zenodo.org`, `data.sdss.org` and VizieR all
  answer `CONNECT tunnel failed, response 403` through the session proxy, so
  no route to the frames exists from the web. The `autolens_workspace` remote
  carries no `feature/multi-galaxy-j1011-real-data` branch and `main` has no
  `dataset/multi_galaxy/` (the `dataset/` tree is gitignored; `start_here.py`
  still auto-simulates `dataset/multi_galaxy/simple`), so nothing has landed
  since the 2026-09-15 issue. The next `/start_dev` must be a local CLI
  session: `/start_workspace` creates the branch there, then the four steps
  above.
- ~~Extra-galaxies / pixelization feature variants remain README cross-links
  (the group/imaging feature scripts apply verbatim with the lens loop).~~
  **CLOSED 2026-07-31.** The feature tier is complete. `extra_galaxies` (PR#391)
  and `scaling_relation` (PR#396) shipped first; the rest was carried by
  `draft/docs/workspaces/multi_galaxy_features_group_parity.md` across four
  phases and eight PRs (#417, #421, #422, #423, #424, #427, #429, #431, #433 and
  the 4c PR), which also added the top-level `multi_galaxy/slam.py`.

  `scripts/multi_galaxy/features/` now equals `scripts/group/features/` minus
  `group_halo` (no analogue at this scale — a multi-galaxy lens has no host halo
  by definition) plus `extra_galaxies`, and `features/advanced/` matches
  `group/features/advanced/` folder for folder. `potential_correction` and
  `los_halos` are imaging-only and deliberately excluded; subhalo sensitivity
  mapping is out of scope, the same boundary group draws.

Create the new `scripts/multi_galaxy/` package in @autolens_workspace — the first
of the three above-galaxy-scale regimes (see the parent plan for the full design
and literature research). The name is **`multi_galaxy`**, NOT `multi_galaxy_lens`
— concise, and mirrors the `multi_galaxy` package planned for
@autogalaxy_workspace. No collision with the existing `multi/` package (which is
multi-*dataset*/wavelength and keeps its name).

## Regime definition (from the parent plan)

Galaxy-scale strong lenses where two or more galaxies contribute significantly
(co-dominantly) to the lensing potential, with NO dominant group/cluster dark
matter halo. Individual halos ~10^11–10^13 M_sun. Mass model = one EPL/SIE per
significant deflector + external shear where appropriate; deflectors are
co-dominant lenses, not satellites in a host halo. Source modelling is the
standard extended-source workflow (parametric Sersic/MGE or pixelized
Delaunay/adaptive meshes) — unchanged from `imaging/`.

Taxonomy note for all narrative prose: all group- and cluster-scale lenses are
multi-galaxy systems, but not vice versa. `multi_galaxy` is the base rung of the
three-regime ladder; group adds the (optional) host halo + truncated members;
cluster keeps that mass framework and changes the source strategy.

## Contents

- `start_here.py` — modeled on `group/start_here.py`'s structure (JAX section,
  Colab setup, centre-input JSON/GUI, live visual update). Two co-dominant lens
  galaxies, one extended source, standard `AnalysisImaging` fit. Use REAL data:
  **SDSS J1011+0143** (arXiv:1602.02927, Shu et al. 2016) — a merging PAIR of
  lens galaxies (~4.2 kpc separation, z=0.331) lensing a z=2.701 Lya emitter
  into a theta_E ~ 1.84" cross/arc; published model is exactly two SIEs +
  shear; public archival HST F555W/F814W via MAST (pin down the program ID at
  implementation time; simulate a look-alike if the frames prove unsuitable).
  Science hook for the prose: the ~1.7 kpc mass/light offsets a single-SIE
  model cannot produce. Runner-up if J1011+0143 falls through: B1608+656
  (see plan — advanced-example caveats).
- `simulator.py` — simulate a two/three-deflector lens (also used to generate
  the bundled example dataset if real data cannot be redistributed).
- `modeling.py` — detailed modeling walkthrough (compose N main galaxies,
  centres from JSON, priors, MGE lens light per galaxy).
- `likelihood_function.py`, `fit.py` — mirror the group package equivalents.
- `features/` — extra_galaxies and scaling_galaxies as EXTENSIONS (not in the
  default model), plus pixelization, MGE, no_lens_light, following
  `group/features/` layout. Scaling galaxies here use UNTRUNCATED isothermals
  (no dPIE/truncation — truncation is physically motivated by a host halo's
  tidal field, which this regime lacks) and the prose must say that at this
  scale scaling galaxies are just "a load of galaxies far from the lens".
- `README.md` — regime definition, file inventory, pointers up the ladder to
  `group/` and `cluster/`.

## Cross-cutting edits (same PR)

- Top-level `autolens_workspace` `README.md`, root `start_here.py` and any
  "which regime am I?" prose: introduce the three-regime ladder and link
  `multi_galaxy/start_here.ipynb`.
- `group/README.md` + `group/start_here.py` opening prose: point down to
  `multi_galaxy/` for systems without a host halo (currently they point only
  to `imaging/` and up to `cluster/`).
- `smoke_tests.txt` + `config/build/profile_smoke.yaml`: register the new
  scripts; regenerate notebooks + navigator catalogue via PyAutoHands.

## autolens_workspace_test (same-named branch, second PR)

Mirror the taxonomy: add `scripts/multi_galaxy/` integration tests (model_fit +
jax_likelihood variant) following the existing per-dataset subfolder pattern.

## Acceptance

- `python .github/scripts/run_smoke.py` green with the new entries.
- Notebooks + navigator catalogue regenerated.
- No use of the string `multi_galaxy_lens` anywhere.
