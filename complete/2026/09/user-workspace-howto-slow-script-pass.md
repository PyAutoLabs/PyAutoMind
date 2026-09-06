# User-workspace + HowTo slow-script pass — the surface is import-floor bound; the real levers are library-side

HowToLens#77 → `3d60e73` and HowToGalaxy#73 → `92e1a75`, both merged 2026-09-06 on
branch `claude/ci-test-timing-epic-ke2lul`, closing autolens_workspace#536. Phase 8 of the
`ci-timing-fast-tests` epic (`draft/feature/pyautoheart/ci_timing_fast_tests_epic.md`).
Fable-planned on the issue from the ingested per-script record plus a local probe;
diagnosed and implemented by an Opus subagent from a web session (four workspace clones
with push access; the library clones read-only).

- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/536
- completed: 2026-09-06
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/77
- workspace-pr-2: https://github.com/PyAutoLabs/HowToGalaxy/pull/73

## What shipped

- **Diagnosis of all 14 scripts ≥ 10 s** on the autolens/autogalaxy-stack user surface
  (autolens_workspace 8, HowToLens 3, HowToGalaxy 1, autogalaxy_workspace 2), each split
  into import floor / re-simulation / compile / execution / plot-output with the dominant
  term named (on the issue): 5 are pure import floor (4.3–4.8 s warm), 4 pay the
  `should_simulate` re-simulation subprocess every run (5.2–6.5 s each; interferometer and
  multi_dataset FITS can never corroborate the cap stamp by shape), 3 (+1 sibling) were
  uncapped source meshes under the cap, 1 is `print(model.info)` → a no-op
  `replace_promise` graph walk (6.0 of 10.2 s), 1 (`guides/mappings.py`) is genuine
  full-resolution work under `ENV: full_datasets`, left by design.
- **The three uncapped meshes fixed** in HowToLens (`tutorial_6_borders`,
  `tutorial_4_bayesian_regularization`, `tutorial_3_inversions`: 14.0/10.0/7.7 s →
  4.5/4.2/4.1 s; suite 201 → 182 s, 50/50) and HowToGalaxy (`tutorial_4`: 11.9 → 4.6 s;
  suite 109 → 102 s, 32/32): the mesh shape follows the loaded dataset via the library's
  existing `SMALL_DATASETS_SHAPE_NATIVE` constant — no new env var, no prose, nothing a
  reader sees changes; notebooks regenerated.
- **autolens_workspace and autogalaxy_workspace: no change** — every finding there is
  library work, filed as phase 8c with measured diffs.

## Key traps / findings

- **Measure warm, or do not measure.** The "4–6× slower locally" gap the plan opened with
  was a cold numba cache (86 → 18 s on one script) plus the `should_simulate`
  re-simulation subprocess (18 → 6.5 s), not any script; the `(200, 200)` interpolation-grid
  hypothesis was refuted (never above 0.3 s). Warm, the local HowToLens suite agrees with
  CI per script (182 s vs 219 s over the same 50). Any timing probe in a fresh container
  runs its target twice and reports the second.
- **A cap that reaches the data but not the model is worse than no cap.**
  `PYAUTO_SMALL_DATASETS` shrinks the image to 80 pixels and left 1600–2500-pixel source
  meshes in place, so the capped run solved a harder, more degenerate inversion than the
  real one. Every existing cap lever covers *data*; nothing covered *model size* — the
  library-side fix (`b-lib`) is the systemic form.
- **A `PYAUTO_*` variable honoured in one place is a bug waiting to happen.**
  `PYAUTO_DISABLE_JAX` is read in exactly one function in the stack while two workspace
  guides document it as the global switch; each variable wants a single predicate in
  `autonerves.test_mode`.
- **A subprocess that pays the import floor is never cheap**: the re-simulation costs ~5 s
  of which ~4.5 s is a fresh interpreter importing the stack; the simulation itself ~0.5 s.
- **The import floor is now the floor of the whole user surface** (5 of 14 targets are
  nothing else; both HowTo repos are floor-dominated end to end). Further per-script work
  there has almost no headroom; the remaining wins are the library ones and anything that
  reduces the floor itself (phase 9's census).
- `PYAUTO_SKIP_VISUALIZATION` gates search-time visualization only, by design; a script's
  own `aplt.*` calls are gate coverage of the plotting code, not a category-(a) finding.

## Follow-ups (tracked, not started here)

- Phase 8c, the library leg (issued next): `draft/bug/autofit/replace_promise_no_op_graph_walk.md`,
  `draft/bug/autoarray/small_datasets_cap_stamp_stops_resimulation.md`,
  `draft/bug/autoarray/sparse_operator_ignores_disable_jax.md`,
  `draft/feature/autoarray/mesh_shape_honours_small_datasets_cap.md` (when it lands, the
  four script-level guards become redundant-but-harmless and can be reverted in one pass).
- Phase 8b: `draft/test/autocti_workspace/imaging_ci_start_here_61s.md`.
- `draft/test/pyautoheart/smoke_relevance_gate.md` stays its own Heart prompt.

## Original prompt

# User workspace + HowTo slow-script pass, driven by the ingested timings

Type: test
Target: workspaces
Repos:
- workspaces
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 8
Issued: 2026-09-06

User workspace + HowTo slow-script pass, driven by the ingested timings.

The user-facing repos (autolens_workspace 462 scripts / ~37 smoke entries, autogalaxy
182/16, autofit 39/8; HowTo repos opt-out everything-minus-no_run: HowToLens 57+50nb,
HowToGalaxy 39+32, HowToFit 20+15) run the same reusable smoke workflow with a different
env profile: `PYAUTO_SMALL_DATASETS=1` plus skip vars the _test repos lack
(PYAUTO_SKIP_FIT_OUTPUT, PYAUTO_SKIP_VISUALIZATION, PYAUTO_SKIP_CHECKS). Fast-mode numpy
scripts run 5-12s, mostly the ~5-7s import floor — autolens import time was already
reduced recently, so there is less low-hanging fruit — but the user suspects some big
bottlenecks remain.

Using the phase-1/2 per-script timing surface and the phase-4 digest: identify the slowest
scripts/notebooks per user-facing repo, diagnose each (import floor vs compile vs
execution vs output/plot work the skip vars should already suppress), and fix the genuine
bottlenecks WITHOUT degrading the user-facing prose or realism — these are teaching
surfaces; content changes are conservative and levers are profile/env/dataset-cap side
first. Where a fix belongs in shared machinery (profile yaml, autonerves, PyAutoHands
runner) route it there rather than per-script hacks. Existing adjacent drafts to fold in
or supersede explicitly: `draft/test/workspaces/slowest_smoke_gate_scripts.md`,
`draft/test/pyautoheart/smoke_relevance_gate.md`.
