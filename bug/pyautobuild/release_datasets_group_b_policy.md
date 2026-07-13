# Group B: committed-by-design vs purge policy for the four bare-`dataset/` workspace repos

Type: bug
Target: PyAutoBuild
Repos:
- autofit_workspace
- HowToFit
- HowToGalaxy
- HowToLens
Difficulty: medium
Autonomy: human-required
Priority: medium
Status: formalised

Split from `bug/pyautobuild/release_ships_simulated_datasets.md` (PyAutoBuild#126) after the
2026-07-13 Phase-2 cross-repo audit. #126 handles **Group A** (autolens + autogalaxy, the
allowlist regime). This prompt handles **Group B** — the four repos whose `.gitignore` uses a
bare `dataset/` (ignore-everything, no `!` allowlist), so *all* their committed datasets are
technically `-f`-leaked, but the data is tiny toy/tutorial data that may be committed-by-design.

## The policy question (decide before any edit)

For each of these four repos, is the committed `dataset/` data:
- **committed-by-design** (tutorials/toy examples should run instantly offline with no
  simulate step) → fix = convert bare `dataset/` → `dataset/**` + `!dataset/<dir>/**`
  allowlist so the data is *legitimately* tracked and the Group-A leg-4 guard passes; **or**
- **a leak like Group A** → fix = purge + add self-provision guards.

## Audit facts (2026-07-13, read-only)

| Repo | tracked | size | simulators | loader | guard idiom today |
|------|---------|------|-----------|--------|-------------------|
| autofit_workspace | 409 | 2.6 MB | 3 (`scripts/simulators/`) | `from_json` | **none** |
| HowToFit | 408 | 2.6 MB | 2 (`scripts/simulators/`) | `from_json` | **none** |
| HowToGalaxy | 21 | 2.8 MB | 4 (`scripts/simulators/`) | `from_fits` | none |
| HowToLens | 27 | 0.9 MB | 7 (`scripts/simulator/`) | `from_fits` | none |

Every repo HAS simulators (data is regenerable). But:
- **autofit / HowToFit** load via `af`...`from_json(...)` with **no `should_simulate` idiom
  anywhere** — a purge route needs a new `from_json` auto-simulate guard invented first, and
  the fit-repo dataset dirs (many small 4–6-file `data.json`/`noise_map.json`/`model.json`
  dirs) include aggregator/database multi-realization sets whose simulator coverage is
  unconfirmed.
- **HowToLens / HowToGalaxy** are teaching repos: injecting a `subprocess` simulate-block
  into a tutorial is a **prose/pedagogy change** (tutorial prose stays Opus), not a mechanical
  edit — an argument for the allowlist route (b2) over purge (b1).

## Recommendation

Lean **b2 (allowlist the toy data)** for all four: cheapest, preserves instant-offline
tutorial runs, and makes the Group-A leg-4 guard pass without touching tutorial prose. Confirm
per-repo that the committed dirs are the intended teaching set (no stray smoke-15×15 leftovers)
before writing the allowlist. Revisit b1 only if a repo's committed data is genuinely stale/dead.

## Constraints

Do not blind-purge (no `from_json` guard exists for the fit repos; tutorials need prose edits).
Coordinate with #126 leg 1 (the universal `-f` drop) and leg 4 (the allowlist guard) — this
prompt decides what each Group-B allowlist *is*.

<!-- formalised 2026-07-13 (--auto supervised, split from #126 during Phase-2 audit). -->
