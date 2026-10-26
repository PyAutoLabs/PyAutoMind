# Matrix-free interferometer inversion, phase 5b/5c: profiling note (Pulse) and workspace example

Type: research
Target: autolens_profiling
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_profiling
- autolens_workspace
Difficulty: large
Autonomy: supervised
Priority: medium
Parent: active/matrix_free_interferometer_inversion.md
Community: https://github.com/PyAutoLabs/.github/discussions/39
Status: formalised
Consequence: judge
Witness: a results note under autolens_profiling/results/notes/ with a dense-vs-matrix-free table (time, peak memory, evidence difference) at 50², 64², 128², 192² on one synthetic and one real interferometer dataset, ingested by PyAutoPulse, plus a workspace example running under the smoke harness
Review-minutes: 20
Unattended: needs-slicing
Filed: 2026-10-21
Blocked-by: none for the profiling leg (runs against checkouts; phases 1-4 on main) — only the workspace example waits for the release. Part of the human's PyAutoPulse profiling programme (anchor Pulse#62); not to be started before that programme.

## What

1. Wiring: DONE 2026-10-26 as phase 5a — `complete/2026/10/matrix-free-interferometer-wiring.md` (PyAutoArray#657 → #658 + Galaxy#670, pending release; an `InversionInterferometerMatrixFree` class behind `Settings(interferometer_route="matrix_free")`). 5b = item 2 below, 5c = item 3; both depend on 5a.
2. Profiling campaign in autolens_profiling (laptop CPU + RAL `ral` partition CPU legs; A100 only if a JAX leg exists by then): dense sparse-path vs matrix-free (unconstrained and positive) at 50², 64², 128², 192²; record time, peak RSS, evidence difference; note with decision rules for the assistant ([[AssistantReadsProfiling]]); summary in the Pulse `profiling-summary` contract.
3. Workspace: `interferometer/advanced/matrix_free.py` example + docs.
4. Thread update with the table; this is the human's lead-in to the full PyAutoPulse profiling programme.
