## ci-actions
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/7
- completed: 2026-05-16
- repo-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/11
- merge-commit: e18685b
- summary: |
    Phase 5 (final) of the autolens_profiling z_feature. Wired up two
    GitHub Actions workflows + threaded AUTOLENS_PROFILING_SMOKE=1 into
    every profile script so the lint workflow's smoke step is cheap.

    What landed:
    - ruff.toml at repo root (conservative E/F/W/I/UP/B selection;
      E501/E402/F401/B008 ignored for scientific code patterns)
    - .github/workflows/lint.yml — PR + push-to-main gate, <5min target,
      CPU-only ubuntu-latest. Steps: ruff check, ruff format --check,
      build_readme.py --check (dashboard idempotence), lychee link-rot,
      smoke one script per section with AUTOLENS_PROFILING_SMOKE=1.
    - .github/workflows/profile.yml — workflow_dispatch (with sections
      filter) + on release:published. Runs every profile script
      continue-on-error per section, runs build_readme.py, commits diff
      back to main as github-actions[bot] with [skip ci]. Skips
      simulators/point_source.py in the loop (default dataset_name
      overwrites Phase 1 tracked JSONs).
    - .github/workflows/README.md documenting both + design decisions.
    - AUTOLENS_PROFILING_SMOKE=1 threaded into 17 scripts (likelihood/*,
      simulators/*, searches/nautilus/*) via AST helper at the first
      non-import top-level statement. Each script exits 0 in <1s with
      "[smoke] ... imports + module setup OK" when the env var is set.

    Design decisions resolved:
    - CPU-only github-hosted runners (self-hosted GPU additive later)
    - workflow_dispatch + release-only (no weekly cron)
    - github-actions[bot] with [skip ci] subject
    - continue-on-error per section (single regression -> ERR cell,
      not blocked dashboard refresh)
    - ruff.toml standalone (no pyproject.toml because this isn't a
      Python package)

    Smoke: yaml.safe_load PASSED on both workflows; py_compile PASSED on
    all 17 SMOKE-instrumented scripts; the SMOKE flag verified working
    on 3 representative scripts locally; build_readme.py --check still
    exits 0 after the SMOKE insertions (Phase 4 idempotence preserved).

    First real CI run will be against any PR after this lands — local
    yaml parse is necessary but not sufficient; any GitHub Actions
    runtime issues get follow-up PRs.

## Original prompt

Phase 5 of the `autolens_profiling` z_feature
(see `z_features/autolens_profiling.md` for the full roadmap).

Wire up GitHub Actions for the new `autolens_profiling` repo. There are
two distinct workflows here that should be designed and committed
together but kept in separate `.yml` files.

## Workflow 1 — Lint / format / smoke on PR

Standard "did the contributor break anything" check that runs on every
PR and on push to `main`. Should be cheap (CPU-only, no JAX needed) and
fast (<5 minutes).

Things to check:

- Python syntax + basic linting (`ruff check` is the obvious choice,
  matching other PyAutoLabs repos — confirm by looking at how
  `PyAutoLens/.github/workflows/` is set up and copy the same config).
- `black` / `ruff format --check` formatting parity.
- Markdown link-rot check on all `README.md` files (use `lychee` or
  similar; cheap to run).
- A *smoke* import / dry-run of one script per section to catch obvious
  breakage (the smallest pixelization profile script, the cheapest
  simulator, the smallest Nautilus run with `n_live=10`). Should not
  produce real result artifacts — set an `AUTOLENS_PROFILING_SMOKE=1`
  env var the scripts can read to short-circuit to a tiny problem size.

## Workflow 2 — Re-run profiles + refresh README dashboard

`workflow_dispatch` (manual trigger) and `release`-triggered workflow
that re-runs the real profile scripts, regenerates the JSON / PNG
artifacts under `results/`, runs the `scripts/build_readme.py` from
Phase 4 to refresh the tables in every README, and commits the result
back to `main`.

Open decisions the implementer needs to make:

- **CPU only on GitHub-hosted runners**, *or* **self-hosted runners for
  GPU runs?** GitHub-hosted = free + simple but CPU-only. Self-hosted
  GPU = expensive operationally but produces the laptop-GPU / HPC-GPU
  numbers the front-page table promises. Recommend: start with
  GitHub-hosted CPU-only; structure the workflow so a future
  self-hosted GPU job can append its numbers without touching the
  workflow shape.
- **Cadence**: every release? weekly cron? manual only? Lean toward
  "manual + on release tag" so we don't burn CI minutes on noise.
- **Bot identity**: which GitHub Actions identity commits the
  refreshed README back to `main`? Probably `github-actions[bot]` with
  a `[skip ci]` tag on the commit message to avoid loops.
- **Failure handling**: if one profile script crashes, does the whole
  workflow fail or do we mark that cell `ERR` in the tables and
  continue? Recommend the latter so a single regression doesn't block
  the dashboard refresh.

## Files to produce

- `.github/workflows/lint.yml` (Workflow 1)
- `.github/workflows/profile.yml` (Workflow 2)
- `pyproject.toml` (or `setup.cfg`) holding the `ruff` config that the
  lint workflow references — copy what PyAutoLens uses.
- A short `.github/workflows/README.md` documenting which workflow is
  for what and how to trigger Workflow 2 manually.

## Pre-flight

This phase depends on Phase 0 (repo exists) and benefits from Phase 4
(dashboard build script exists). If Phase 4 hasn't shipped yet,
Workflow 2's "refresh README" step can be a TODO stub that just
commits the new JSONs; flip it on once `build_readme.py` lands.

## Out of scope

- Cross-platform matrix (macOS, Windows) — lens-modeling profiling is
  Linux-only in practice.
- PyPI / conda packaging — the repo isn't a Python package.
- Coverage reporting — there are no unit tests in this repo, by design.
