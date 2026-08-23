# extra_galaxies feature parity: point_source + multi_galaxy (both workspaces)

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
- autogalaxy_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-07-29 (backfilled from git)

The user's request, verbatim:

> Extra galxies:
>
> - documentation is imaging/features/extra_galaxies is excellent, the stnadard,
>   same for interferometer.
> - Add to point_source/features, same style but wont have a slam.py
> - Adopt same style and approach for documenting extra galaxies in
>   multi_galaxy, do same in autogalaxy_workspace.
> - its right that group uses them in start_here.py and modeling.py, nothing to
>   change.
> - For a cluster, I think its right not to document extra galaxies as it is.
>
> So only a few small tasks to do above on extra galaxies.

## Current state (audited 2026-07-29)

`extra_galaxies` worked examples exist in exactly four places, all four
confirmed by the user as the standard to copy:

| Package | README | simulator | modeling | slam |
|---|---|---|---|---|
| `autolens_workspace/scripts/imaging/features/extra_galaxies` | yes | yes | yes | yes |
| `autolens_workspace/scripts/interferometer/features/extra_galaxies` | yes | yes | yes | yes |
| `autogalaxy_workspace/scripts/imaging/features/extra_galaxies` | yes | yes | yes | — |
| `autogalaxy_workspace/scripts/interferometer/features/extra_galaxies` | yes | yes | yes | — |

Gaps to close:

- `autolens_workspace/scripts/point_source/features/` — no `extra_galaxies`
  anywhere; the package contains **zero** references to extra galaxies.
- `autolens_workspace/scripts/multi_galaxy/features/` — `features/README.md`
  already describes extra galaxies at multi-galaxy scale in prose, but
  cross-links to `imaging/features/extra_galaxies` for the code. Its sibling
  tier (`features/scaling_galaxies/`) gets a full worked example, so extra
  galaxies is the odd one out.
- `autogalaxy_workspace/scripts/multi_galaxy/` — has **no `features/` folder
  at all**; its README ends with a one-line "standard single-galaxy features
  apply per-galaxy here" pointer.

Explicitly out of scope, confirmed by the user:

- `group/` — already uses the extra-galaxies API in `start_here.py` and
  `modeling.py`; nothing to change.
- `cluster/` — correctly does not document extra galaxies; nothing to change.
- `imaging/` and `interferometer/` in both workspaces — already the standard.

## Phasing (Brain override, 2026-07-29)

The Feature Agent returned `too-large (score 13) / split-into-phases` with the
generic design → core_api → workspace_examples → docs template. That template is
wrong here: **no library code is touched at all**, so the `core_api` and `design`
phases are vacuous — the score is the repo-count proxy again
([[feedback_brain_repo_count_difficulty_proxy]]). Overridden to two phases split
by regime, both independent, phase 1 first:

- `extra_galaxies_feature_parity_phase_1_point_source.md` — autolens_workspace, 1 PR.
  **SHIPPED** 2026-07-30: issue #374 closed, PR#376 merged `e005caca`.
- `extra_galaxies_feature_parity_phase_2a_multi_galaxy_autogalaxy.md` — autogalaxy_workspace.
- `extra_galaxies_feature_parity_phase_2b_multi_galaxy_autolens.md` — autolens_workspace,
  **BLOCKED on #370** (`multi-galaxy-imaging-parity`) merging.

Phase 2 was split by repo on 2026-07-30: #370 is rewriting
`autolens_workspace/scripts/multi_galaxy/` wholesale (2,959 insertions, incl. adding
extra-galaxy noise scaling to the core scripts), so the autolens half must be written against
that merged result. The autogalaxy half has zero contention and runs now.

## Scope

**Human decision 2026-07-29:** full worked example (own simulator + own
simulated dataset), not a cross-link, in every gap below.

1. **`autolens_workspace/scripts/point_source/features/extra_galaxies/`** —
   new `README.md`, `__init__.py`, `simulator.py`, `modeling.py`. **No
   `slam.py`** (user-specified; SLaM is imaging/interferometer-only).
   - Point-source data has no image pixels, so the two levers the imaging
     example teaches do not both exist here: there is nothing to noise-scale
     and no extra-galaxy light to fit. The example is **mass-only** — extra
     galaxies perturb the deflection field and therefore the solved multiple
     image positions.
   - Follow the imaging example's arc: centres loaded from
     `extra_galaxies_centres.json`, `IsothermalSph` with `centre` fixed to the
     loaded centre and a capped `UniformPrior` on `einstein_radius`,
     `af.Collection(...)` passed as `extra_galaxies=`.
   - Mirror the sibling point-source features (`multiple_sources/`,
     `deblending/`) for the `PointSolver` / `AnalysisPoint` / name-pairing
     boilerplate and the `should_simulate` auto-simulation block.
   - Update `point_source/features/README.md` — add `extra_galaxies` under
     `# Folders`.

2. **`autolens_workspace/scripts/multi_galaxy/features/extra_galaxies/`** —
   new `README.md`, `__init__.py`, `simulator.py`, `modeling.py`.
   - Two co-dominant deflectors (the `lens_0`, `lens_1`, ... loop of the
     package) **plus** a lower tier of extra galaxies with fixed centres.
     The regime framing already written in `multi_galaxy/features/README.md`
     is the prose source: extra galaxies are perturbers *below* co-dominance,
     using the same tiered API that becomes the default at group scale.
   - Rewrite the extra-galaxies bullet in `multi_galaxy/features/README.md` so
     it points at the new local example instead of cross-linking to
     `imaging/features/extra_galaxies` (keep the imaging pointer as the fuller
     API walkthrough).
   - Update `multi_galaxy/README.md` `# Folders` if the features list changes.

3. **`autogalaxy_workspace/scripts/multi_galaxy/features/`** — new folder
   (`README.md`, `__init__.py`) plus `extra_galaxies/` with `README.md`,
   `__init__.py`, `simulator.py`, `modeling.py`.
   - PyAutoGalaxy has no mass, so this is the **light-only** case: extra
     galaxies blend with the co-equal blended pair and are either
     noise-scaled out or fitted with their own light model at fixed centre.
     `autogalaxy_workspace/scripts/imaging/features/extra_galaxies` is the
     direct prose source.
   - Add a `# Folders` section to `autogalaxy_workspace/scripts/multi_galaxy/README.md`.

## Constraints / known traps

- **Prose is the deliverable.** These are tutorial scripts — keep the
  register, section headings (`__Contents__` first, then the numbered
  sections) and depth of the canonical `imaging/features/extra_galaxies`
  examples. Do not port near-identical prose verbatim where the physics
  differs (point source: mass-only; autogalaxy: light-only).
- **`should_simulate` tests directory EXISTENCE only** — delete any
  pre-existing `dataset/<type>/extra_galaxies*` folder before a validation run
  or the simulator silently will not regenerate.
- **Workspace bulk-edit rule** — never whole-file `Write` a file that was not
  fully read; run `scripts/check_sizes.sh` before committing (new files only
  should mean no shrink, but run it anyway).
- **Parallel claim** — `autolens_workspace#368` (likelihood-function-jax-pointer)
  holds a claim on the same two repos (#366 multistart-prodigy MERGED
  2026-07-29). Human decision 2026-07-29: proceed in parallel; this task
  creates only NEW folders (zero source-file overlap). The generated
  artifacts (`notebooks/`, `llms-full.txt`, `workspace_index.json`) do
  collide — whichever PR merges last re-runs `generate.py` rather than
  hand-resolving.
- **`multi-galaxy-imaging-parity`** (planned.md, blocked on #366) adds a faint
  extra galaxy + `mask_extra_galaxies.fits` to `multi_galaxy/simulator.py` and
  an `__Extra Galaxies Noise Scaling__` section to
  `start_here/modeling/fit/likelihood_function`. That is the *core-script*
  noise-scaling treatment; this task is the *features/* modeling example.
  They are complementary and touch disjoint files — exactly the imaging
  arrangement. Do not merge them.
- **Supersedes part of** `draft/docs/workspaces/galaxy_scale_scaling_extra_features.md`
  — that draft's `extra_galaxies`-for-`point_source` leg and its
  imaging/interferometer audit leg are absorbed here (the user has confirmed
  imaging + interferometer are already the standard). Its `scaling_galaxies`
  legs remain open in that draft.

## Acceptance

- Smoke suite green in both workspaces (`python .github/scripts/run_smoke.py`),
  with the new `modeling.py` scripts added to `smoke_tests.txt` if they run
  cleanly under `PYAUTO_TEST_MODE=2` / `PYAUTO_SMALL_DATASETS=1`.
- Every new folder has a `README.md` and `__init__.py`; every parent README's
  `# Files` / `# Folders` list is updated (README ref-drift is CI-gated).
- Notebooks regenerated and the navigator catalogue / `workspace_index.json`
  refreshed via PyAutoHands `generate.py` in both workspaces.
- `group/` and `cluster/` are untouched.
