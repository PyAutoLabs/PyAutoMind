# Time the cluster tutorial and simulator stage by stage, and name the bottleneck

Type: research
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
Themes:
- cluster
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: an autolens_workspace_developer PR adds `cluster_tutorial_timing/` whose README tables give seconds per stage for `start_here.py` and `simulator.py` (cold and cached runs, with dataset, backend and CPU recorded) and names each script's largest stage; a `Phase: 4b` draft proposes its fix
Review-minutes: 20
Unattended: ready
Lane: local-dev
Epic: cluster-usability
Phase: 4a
Filed: 2026-11-26

## Why

Ledger: `draft/feature/autolens/cluster_usability.md`, item 4 of "Proposed work in priority order" ("Measure and improve the slow paths"). Items 2 and 3 (figures) are complete on all three tiers: Simple, Pandora and MACS J0416 are live on PyAutoEyes and the panels are taught in autolens_workspace#687 (record `complete/2026/11/cluster-family-fit-figures.md`). Item 1's remaining malformed-CSV validation and the first Simple profiling baseline are in flight in autolens_profiling#536 / PR #537. This phase is independent of that PR: it touches neither autolens_profiling nor the cache guard.

The ledger's words:

> Time `scripts/cluster/start_here.py` and `scripts/cluster/simulator.py` separately. For the tutorial, distinguish first download, cached load, first useful figure and fit time. For the simulator, distinguish setup, first JAX compilation, synchronised warm execution and file output. Record dataset, backend and hardware. Optimise the measured bottleneck, then repeat the timings and compare outputs on the same inputs.

This phase does the measurement and diagnosis only (slice 4a). The optimisation, and the before/after comparison on the same inputs, is slice 4b, filed by this phase once the bottleneck is known. That split keeps one unattended run bounded and lets the human choose the fix.

## What to do

1. Plan first (start_dev): post the plan on the issue before any edit.
2. Add `autolens_workspace_developer/cluster_tutorial_timing/` with a harness that runs the two workspace scripts from an autolens_workspace main checkout **without editing them**. Instrument from outside (e.g. `runpy` with wrapped/patched entry points, `time.perf_counter` around stage boundaries, `jax.block_until_ready` for synchronised warm timings). If a stage boundary cannot be timed from outside, record that and time the nearest enclosing span.
3. Tutorial stages: first download (empty cache dir), cached load (second run), first useful figure (first saved/opened figure that contains data), `search.fit` wall clock. Run headless (`MPLBACKEND=Agg`) with test-mode settings off for the fit; if the full fit would exceed ~30 minutes on the laptop, stop it at the first Nautilus checkpoint and report the extrapolation instead of running on.
4. Simulator stages: setup, first JAX compilation, synchronised warm execution (median of ≥ 5), file output.
5. Record dataset, backend, FP precision, CPU/GPU model, Python/JAX versions and the commits used. Write the tables and the named bottleneck with its cause to the folder README. Put any plots in `Science/scratch/cluster_usability_timing/`.
6. File the 4b draft prompt (Phase: 4b, same Epic) describing the proposed optimisation of the largest stage, which repo it lands in, and the same-inputs output comparison it must pass, and moving the post-fix run times into autolens_profiling.
7. Ship via ship_workspace to an open PR. Update the ledger's item 4 with the measured table link.

## The human's decision on where timings live (2026-11-26)

> I think so, with fast run times once sorted then in autolens_profiling

The timing harness lives in `autolens_workspace_developer/cluster_tutorial_timing/` while the
slow paths are being found and fixed. Once 4b has made the tutorial and simulator fast, their
run times move into autolens_profiling (and Pulse) as a tracked entry; the 4b draft this phase
files must include that step.

## Rules

- Plan-first; no edits to autolens_workspace scripts or any library in this phase (measurement only). The optimisation waits for 4b and human approval.
- No multi-hour runs on the laptop; no RAL submission.
- Do not touch autolens_profiling in this phase (Simple profiling, PR #537, merged 2026-11-28).
- Merge and issue close stay human.
