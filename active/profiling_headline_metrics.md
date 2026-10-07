# Profiling headline metrics

Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/30
Target: @PyAutoPulse
Type: feature

Expose selection-specific headline measurements immediately below Instrument / Device / Configuration in the setup detail view. Simplify configuration labels to e.g. `1500 source pixels - float64`, removing Runtime. Distinguish missing measurements from inapplicable metrics; preserve evidence identity and units. No campaign execution or invented multiprocessing correction.

## Original user request

At the moment, the "headline figurs" I would want to know for profiling are hiden in drop down menus.

When I click something like Delaunay and open a new tab, I think Under the Instrument / Device / Configuration thing
I should immediately see (and it should update when I change the configuration):

Likelihood Run Time Total: ### s
Likelihood Run Time Batched: #### s (probably not applicable to numba, but maybe numba should have a multiprocessing correction here?)
JAX Compile Time: #### s (Not on Numba)
VRAM Use: #### GB (not on Numba)
Memory use: #### GB

In Confiuguration I think we should use 1500 source pixels - float64, but not have the RunTime word, which feels like bloat.

Some runs wont have numbers yet, soon I will do a "Day Zero" run to fill in everything when we complete a major PyautoPulse campaign.

## Approved implementation plan

- Add always-visible headline metrics directly below the selectors, refreshing on every instrument, device or configuration change.
- Show full single-likelihood runtime, per-likelihood batched runtime with batch-size context, JAX compile time, measured device memory and measured host memory. Use seconds and GB; preserve measurement provenance and distinguish peak/current semantics where supplied.
- Hide JAX compile and VRAM fields for Numba; show batched timing as not applicable unless supported measured evidence exists. Do not estimate multiprocessing speedup by dividing by core count.
- Show `Not measured yet` for applicable absent measurements, with distinct loading/error states. Never substitute component sums or static compiler estimates for full runtime or measured memory.
- Label configurations `1500 source pixels - float64` where applicable, omitting Runtime; preserve underlying setup identities and deep links, and disambiguate any resulting duplicate labels with meaningful configuration attributes.
- Exercise the browser flow, asynchronous selector changes, missing data and Numba handling, then run the repository's required checks and open one PR.

Tier: undeclared — merge mode: human /prm

### Detailed change and validation scope

Primary repo: PyAutoPulse. Classification: library workflow (Brain decision), direct single phase.
Suggested branch: feature/profiling-headline-metrics.

1. `pulse/measurement_presentation.js`: add explicit headline selection helpers grounded in producer metric keys, axes, units and matching setup/device/backend/precision/run identity. Select full-likelihood runtime and batch per-call evidence; do not conflate batch wall time, instrumented totals or partial timings. Preserve ambiguity rather than arbitrarily selecting conflicting runs. Expose only trustworthy measurements; absent unsupported fields remain explicit.
2. `pulse/setup_browser.js`: simplify `configurationLabel`; insert a headline container immediately after selectors and before `metadata(setup)`. Populate it from the existing verified shard/record path in `display`; clear it on selection and loading, respect stale-request protection, and preserve error/no-setup paths. Retain existing evidence disclosures.
3. `pulse/setup_browser.css`: style accessible metric labels/values with existing theme sizing tokens, wrapping on narrow screens; no shared Brain component change anticipated.
4. Extend `tests/measurement_presentation.cjs`, `tests/browser_setup.cjs` and their fixtures as needed for actual matching evidence, JAX/Numba applicability, missing/ambiguous data, unit conversion, selection updates, shard failures and asynchronous stale response protection. Confirm headlines visible without opening details and no horizontal overflow on mobile.
5. Run browser harness, Python suite, ruff checks and `bin/pyauto-pulse check --offline`; regenerate affected board output through the existing offline render procedure if required by repository checks, without starting a campaign or refreshing scientific measurements.

### Initial survey

- Mind: clean main before adding this prompt; origin fetched, no behind commits reported.
- Pulse: clean main, behind origin/main by one generated dashboard refresh commit (`17d1115`); implementation should start from current origin/main.
- No active registry conflict reported for PyAutoPulse. Conflict helper warns of an unregistered `feature/organism-map-regen-486` worktree; leave it untouched and inspect overlap during approved worktree setup.
- Heart gate: STALE (exit 1), planning permitted. Ship-time verdict remains required.
- No source edits or issue creation performed before approval.
