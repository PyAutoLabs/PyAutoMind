# Physical + fast rebuild of the autogalaxy_workspace_test smoke gate — coarser shared datasets, models that match their data

autogalaxy_workspace_test#117 → `0f69588`, closing autogalaxy_workspace_test#116,
merged 2026-09-06 on branch `claude/ci-test-timing-epic-ke2lul`. Phase 5 of the
`ci-timing-fast-tests` epic (`draft/feature/pyautoheart/ci_timing_fast_tests_epic.md`)
— the rehearsal repo; phase 6 applies what generalises to autolens_workspace_test.
Fable-planned on the issue, implemented by an Opus subagent under the Brain's
delegation ladder from a web session (no task worktree; the full PyAuto stack
was pip-installed from source in the container so the gate ran locally).

- issue: https://github.com/PyAutoLabs/autogalaxy_workspace_test/issues/116
- completed: 2026-09-06
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/117

## What shipped

- **Coarser shared datasets, set by what the models resolve**: imaging
  180×180 @ 0.2″ → 100×100 @ 0.3″ (PSF 21×21 σ0.2″ → 11×11 σ0.35″, a 0.8″
  FWHM seeing kernel that is well sampled); interferometer real-space grid
  256×256 @ 0.1″ → 128×128 @ 0.2″ (same 200 visibilities, same seed);
  multi-wavelength 150×150 @ 0.1″ → 80×80 @ 0.2″ (PSF σ0.25″). Every
  intensity, sky level, exposure and seed unchanged.
- **Every model matches its data**: each family's simulator also writes a
  `jax_test_group` dataset holding the two extra galaxies the `mge_group.py`
  scripts fit (`SersicSph` at `(1.2, 1.2)` and `(-1.0, 1.5)`, inside the 3.0″
  mask); the three `mge_group.py` scripts read it with matching centres.
  Before, they fitted two to five galaxies no simulator produced, some outside
  the mask.
- **Levers, coverage preserved**: over-sampling 4 → 2 (imaging
  `rectangular.py`, `delaunay.py`), radial bins `[4,2,2]` → `[2,2,1]`,
  `aggregator/fit_imaging.py` 5 → 2; MGE bases 30×2 → 20×2 and extras 10 → 8
  in the two `mge_group.py` scripts; vmap `batch_size` 50 → 10 in six
  imaging/interferometer scripts. Every `# ENV:` line, `smoke_tests.txt`,
  `config/build/profile_smoke.yaml`, every assertion tolerance, the
  inline-simulator scripts, and the multi-dataset composite two-band
  `FactorGraphModel` vmap structure (the Eigen-pool reproducer, `batch_size = 3`)
  untouched. Dataset-constant sweep across all 64 scripts (the 25 non-gate
  scripts read the same FITS).
- **Measured**: 39/39 green before and after; gate total 515.1 s → 438.4 s
  (−15%) cold in one 4-core container. Largest rows: `visualization.py` 40.1 →
  24.5 s, `imaging/jax_likelihood/rectangular.py` 23.5 → 14.1 s, both
  `mge_group.py` −37%. The full 39-row table is on #116's Shipped comment.
- **CI acceptance**: both smoke legs green (~10 min wall each) on a cold JAX
  cache and a cold dataset cache — the first run under the phase-7 epoch-1
  keys, which it seeded (22 JAX entries / 7 MB; 30 dataset entries / 1 MB).

## Key traps / findings

- **Coarsening the data can under-determine an inversion that was fine
  before.** `imaging/jax_likelihood/rectangular.py` failed its JAX-vs-NumPy
  `rtol=2e-2` at 2.44% on the first after-run. Not the over-sampling lever
  (backing it off reproduced the numbers to every digit): the 3.0″ mask holds
  316 image pixels at 0.3″/px against 716 at 0.2″/px while the mesh stayed
  28×28 = 784 source pixels, a 2.5× under-determined fit. Mesh → 17×17 (289 ≤
  316, the largest square mesh the data constrains — a rule, not a tuned
  number). The tolerance is untouched. **Phase 6 rule: check every
  pixelization mesh against the masked pixel count after coarsening.**
- **The mixed-precision JAX-vs-NumPy gap grows on small data and is
  mesh-independent**: ~15 nats on the new imaging data against 5.8 on `main`'s
  (14.99 / 26.73 / … / 14.98 nats across meshes 12–28). The mesh fix restores
  the relative margin by increasing `|log_L|`, not by shrinking the gap. Filed
  for the source repo: `draft/bug/autoarray/mixed_precision_inversion_jax_numpy_gap_small_data.md`.
- **The interferometer `_group` extras are below this family's noise** at the
  spec's `intensity=0.25` (aggregate S/N 0.17; `noise_sigma=1000` puts the
  primary at S/N ~20). Left as specified — raising them enough to detect would
  make the satellites brighter than the galaxy; the dataset still structurally
  contains what the model fits.
- **Where the time is**: the dataset levers moved the compute-bound rows
  (visualization, pixelization inversions, `_group` fits); the ±10% rows on
  3–10 s scripts are container noise on the ~5–7 s per-process import floor
  (~230 s of the gate across 39 entries). That floor is phase 8/9's; the
  compile share is what the phase-7 JAX cache removes on CI, not on a cold
  local run.
- **Absolute-pin doctrine is autolens_workspace_test's, not this repo's**:
  autogalaxy_workspace_test has only relational JAX-vs-NumPy assertions, so
  no pin-regeneration wave was needed here. Phase 6 is the first wave that
  regenerates literals.

## Follow-ups (tracked, not started here)

- Phase 6: `draft/test/autolens_workspace_test/physical_fast_rebuild.md` —
  one simulator per family writing the single-object and `_group` datasets
  from one galaxy definition; mesh-vs-masked-pixel check; one
  pin-regeneration wave from the new sims; its PR appends the `fast-tests`
  epoch boundary to PyAutoHeart `timings/epochs.jsonl`.
- Hot-vs-cold cache numbers from `timings/scripts/` once this repo has its
  second run on `main` (the first, cold, landed with this PR).
- `draft/bug/autoarray/mixed_precision_inversion_jax_numpy_gap_small_data.md`.

## Original prompt

# autogalaxy_workspace_test physical + fast rebuild (rehearsal repo)

Type: test
Target: autogalaxy_workspace_test
Repos:
- autogalaxy_workspace_test
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 5
Issued: 2026-09-06

autogalaxy_workspace_test physical + fast rebuild (the rehearsal repo before autolens).

Two coupled changes across the repo's 39 smoke-gate scripts (64 scripts total), done as ONE
wave because both force regenerating every pinned likelihood literal:

1) PHYSICAL REALISM: every script uses physical, realistic galaxy models with
simulator↔model consistency and high-likelihood solutions. Where the simulator and the
fitted model mismatch, fix it. Sensible physical inputs throughout (intensities,
background sky, sizes resolvable at the chosen pixel scale). Rationale: when a user
inspects a _test failure, a physical setup is interpretable.

2) SPEED: make the scripts as fast as possible without losing coverage. The ~50s class is
`ENV: jax full_datasets` scripts (compile ~12-18s + full-resolution vmap + ~5-7s import
floor; `config/build/profile_smoke.yaml:22-43` records mge_group.py at 54-63s). Ranked
levers from the 2026-08-31 survey: coarser simulated datasets (e.g. 180x180@0.2" mask 3.5"
-> ~100x100@0.3", shrinking both compile graphs and execution quadratically — 0.3" still
resolves the structure); over-sampling reduction (over_sample_size_lp=4 + radial [4,2,2]
-> [2,2,1]/uniform 2); fewer MGE gaussians / smaller vmap batch sizes (20+30-gaussian
bases dominate graph size). TEST_MODE=2 already bypasses samplers on the smoke gate, so
search settings are not the lever; keep n_like_max philosophy for the weekly/release
channels — better-conditioned physical models are how those get faster.

Constraints: regenerate every pinned `fitness._vmap` literal once, at the end, from the
new sims (pins are deliberately absolute — `scripts/CLAUDE.md`); keep the
`--xla_cpu_multi_thread_eigen=false` workaround and do NOT shrink the
`multi_dataset/jax_likelihood/*` scripts in ways that stop reproducing the Eigen-pool bug
class (jax-compile-stall epic); library unit tests + developer/profiling workspaces are
the independent validation that likelihood-value changes stayed local. Record before/after
per-script seconds against the phase-4 legacy snapshot. Patterns proven here are the
template phase 6 applies to autolens_workspace_test.
