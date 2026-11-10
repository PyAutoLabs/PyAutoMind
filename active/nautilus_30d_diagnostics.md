# Nautilus 30D evidence and output diagnostics

Type: feature
Target: autofit_profiling
Repos:
- autofit_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: workspace-dev
Issued: 2026-11-10
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/12
Filed: 2026-11-10
Consequence: judge
Witness: Copied-checkpoint experiments distinguish exploration reuse from target errors and isolate wrapped output costs with durable bounded receipts; original data stays unchanged and all failures remain visible.
Lane: local-dev
Epic: nautilus-fast-likelihoods
Phase: 0b.2

## Original request

"Continue with the next experimental step—investigate the 30D evidence error and the wrapped timeout. Keep it outside Pulse for now."

Approval: "continue" after presentation of the linked detailed plan. Existing authorization: "Approved. Proceed with phase 0b implementation, the bounded local pilot and development PRs despite Heart RED. Leave merge for human". This next phase-0b member retains that scope and override; no merge or release authorized.

## Approved plan

Proposed next member: nautilus-30d-diagnostics (phase0b.2)
Status: approved by live human "continue", 2026-11-10. Outside Pulse.

HIGH LEVEL
1. Preserve original artifacts; build a diagnostic-only harness using copies of existing checkpoints and the same pinned runtime.
2. Test the exploration-reuse hypothesis using fresh samples from saved fixed bounds; distinguish conditional repeats from independent exploration runs.
3. Replay wrapped final output separately, measuring summary, latents, plotting and finalization without new likelihood calls.
4. Publish every attempt, cap and unresolved result in experiments; validate and open a development PR.
Tier: judge — merge mode: human /prm. No library optimization or merge in this member.

DETAILED IMPLEMENTATION
Repo autofit_profiling. New branch feature/nautilus-30d-diagnostics; new worktree /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-30d-diagnostics/autofit_profiling. Canonical main clean; both earlier retained worktrees remain archives. Mind has no active autofit_profiling claim at survey.
After approval, use start_dev/create_issue/start_workspace to register the member and obtain worktree from current origin/main. Preserve pinned Fit/Nerves and third-party environment from phase0b.1; verify imports, hashes and thread settings. Do not update dependencies.
Add scripts/analytic_gaussian/nautilus/diagnose.py plus focused diagnostic helpers/tests under scripts/misc/profiling. Reuse existing provenance, process-group supervisor and atomic receipt primitives; leave original36-case plan and raw attempts unchanged.
Evidence arm: D5/D10/D30 seed0 copied native checkpoints; explicitly set discard_exploration property True, verify explored state and excluded counts, then seek ESS10000 and minimum100 fresh points per shell. Record constructor/stopping settings, pre/post calls, fresh counts, shell estimates, exact analytic diagnostics and hashes. Report estimates both excluding and including exploration from the same resulting state. D30 gets two additional fixed-seed conditional resampling repeats from the original saved bounds; do not call these three independent full-search seeds. Each child has its own copied checkpoint and output directory. If any cap/failure occurs, retain receipt and stop; no automatic retry or cap escalation.
Output arm: one wrapped replay from a copied30D checkpoint with original output settings, instrumenting entry/exit for samples conversion/summary/CSV, latent draw/computation, visualization and final outputs. Persist events incrementally so timeout retains a useful trace. Assert no likelihood evaluations occur; any additional sampling is an invalid output-only case. This replay measures output cost separately, not full search.fit throughput. Keep original timeout status unchanged.
Caps: at most6 sequential child attempts (5 evidence,1 output),120s and4096MiB perchild;15min aggregate including preflight. Native threads1, one worker, no concurrent timing jobs; same host/load/available-memory guards. Retain every attempt. No60/100/200D, remote compute or production catalogue/Pulse changes.
Evidence destinations: experiments/nautilus_30d_diagnostics/protocol.json, README.md and portable receipts/report. Raw/checkpoint copies under ignored output/nautilus-30d-diagnostics. Human view under this scratch folder or a distinct results child.
Tests: prove original checkpoint hashes unchanged; resumed discard flag is effective; post-exploration count semantics; reject changed target/pins; output replay prohibits likelihood calls; timeout retains stage trace; conditional repeat labeling; missing/capped attempts not promoted to success. Run focused existing/new harness tests, lint and link checks.
Acceptance: explain what the fresh-sample estimates do and do not support; isolate output-stage costs or report bounded incomplete diagnosis. A cap is an experimental result, not permission to increase resources. No fixed accuracy threshold or causal conclusion invented after seeing results. No performance fix in this task; propose separately if warranted.

## Current Heart reasons (verbatim)

```text
Heart: RED — Release RED; monitoring RED · 11/100 · 138 unresolved (updated 1h ago)
  [red] PyAutoGalaxy: CI failure — https://api.github.com/repos/PyAutoLabs/PyAutoGalaxy/actions/runs/42605341827
  [red] PyAutoLens: CI failure — https://api.github.com/repos/PyAutoLabs/PyAutoLens/actions/runs/42605339633
  [red] PyAutoGalaxy: PyAutoGalaxy: CI failure
  [red] PyAutoLens: PyAutoLens: CI failure
  [red] PyAutoGalaxy/Tests: failure
  [red] PyAutoGalaxy/workflows/Tests: failure
  [red] PyAutoHands/workflows/Python Version Matrix: failure
  [red] PyAutoHeart/workflows/Workspace Smoke: failure
  [red] PyAutoLens/Tests: failure
  [red] PyAutoLens/workflows/Tests: failure
  [red] PyAutoGalaxy: PyAutoGalaxy: CI failure
  [red] PyAutoLens: PyAutoLens: CI failure
  [red] autolens_test: red
  [red] Workspace validation: NOT ready — 1399p / 14f / 125s @ cloud#42607741369
  [red] test_run: red
  [red] PyAutoArray: red
  [red] PyAutoGalaxy: red
  [red] PyAutoLens: red
  [red] Worktree drift: 0 orphan / 0 missing / 3 dirty
  [yellow] workspace validation not passing (14 failed, cloud#42607741369: autolens_test scripts/imaging/delaunay.py, autolens_test scripts/imaging/rectangular.py, autole…
  [yellow] PyAutoArray: open PR 7d old — https://github.com/PyAutoLabs/PyAutoArray
  [yellow] PyAutoArray: PR×1 (7d)
  [yellow] PyAutoHeart: CI in_progress
  [yellow] PyAutoBrain/Nightly Release: warn
  [yellow] CI wall-clock: 27 gates · slowest PyAutoBrain Nightly Release 118m · 1 slowed
  [yellow] PyAutoCortex: 1 uncommitted file(s) in canonical checkout
  [yellow] PyAutoPulse: 1 uncommitted file(s) in canonical checkout
  [yellow] magnification-maps-wiring/PyAutoArray: 2 uncommitted file(s) in task worktree
  [yellow] magnification-maps-wiring/PyAutoGalaxy: 2 uncommitted file(s) in task worktree
  [yellow] magnification-maps-wiring/PyAutoLens: 3 uncommitted file(s) in task worktree
  [yellow] PyAutoGalaxy/autogalaxy/3.13: yellow
  [yellow] autogalaxy: yellow
  [yellow] Import timing: 1 imports >1.5× baseline, 11 within
  [yellow] autofit_workspace/features/expectation_propagation.py: EP parked as not release-ready. EP message projection is unstable: a truncated per-factor search project…
  [yellow] autofit_workspace_test/graphical/analytic_gaussian_priors.py: moments projection (PyAutoFit#1656) passes the gaussian and truncated scatter families (16/16 eac…
  [yellow] autofit_workspace_test/graphical/ep.py: EP not release-ready: the per-factor searches are truncated (maxcall/maxiter=1000), so each search projects an ESS=1 po…
  [yellow] autofit_workspace_test/graphical/ep_deterministic.py: EP parked as not release-ready alongside graphical/ep.py. Passes today, but shares the EP machinery whose…
  [yellow] autofit_workspace_test/graphical/ep_exact.py: EP parked as not release-ready alongside graphical/ep.py. Passes today, but shares the EP machinery whose message…
  [yellow] autofit_workspace_test/graphical/ep_parity.py: EP parked as not release-ready alongside graphical/ep.py. Passes today, but shares the EP machinery whose messag…
  [yellow] autogalaxy_workspace/imaging/features/shapelets/modeling: real-search JAX shapelet fit exceeds the 1800s mode=release cap (>30min); speedup tracked by the Prof…
  [yellow] autogalaxy_workspace_test/multi_dataset/jax_likelihood/delaunay.py: quarantined: TIMEOUT 1805s at the release cap in TWO CONSECUTIVE release-integrate runs (34…
  [yellow] autogalaxy_workspace_test/multi_dataset/jax_likelihood/rectangular.py: re-quarantined: hung 1805s at the release cap in release-integrate run 33244320906 with …
  [yellow] autolens_workspace/cluster/start_here: hits the full 1800s mode=release cap in workspace-validation (PyAutoHeart run 29912642195). Script-specific, not a shard…
  [yellow] autolens_workspace/guides/modeling/advanced/expectation_propagation.py: EP parked as not release-ready. EP message projection is unstable: a truncated per-fact…
  [yellow] autolens_workspace/multi_galaxy/features/advanced/shapelets/modeling.py: hit the 1800s mode=release cap in the 2026.10.7.1 release smoke job (PyAutoHands run 3…
  [yellow] autolens_workspace/multi_galaxy/start_here: blocked two consecutive release runs after autolens_workspace#554 (2026-09-17) swapped it off the simulated `simple…
  [yellow] autolens_workspace/weak/features/strong_lensing/a2744: hits the full 1800s mode=release cap in workspace-validation (PyAutoHeart run 29912642195). Script-speci…
  [yellow] autolens_workspace_test/cluster/visualization: per-plane critical-curve + caustic computation on the required full-extent 250x250 viz_grid (multi-plane marchin…
  [yellow] autolens_workspace_test/imaging/subhalo_recovery_evidence.py: evidence-grid acceptance test of PyAutoLens#672 (156-point one-shot + 25-point iterative-to-conve…
  [yellow] autolens_workspace_test/imaging/visualization/modeling_visualization_delaunay_jit: now FAILS its own JIT-cache assertion at 52s (cached 2.45s not < 0.5x compil…
  [yellow] autolens_workspace_test/imaging/visualization/modeling_visualization_jit: re-measured: times out at the 300s cap; JIT + full visualization pipeline
  [yellow] autolens_workspace_test/imaging/visualization/modeling_visualization_rectangular_jit: now FAILS its own JIT-cache assertion at 36s (cached 2.21s not < 0.5x com…
  [yellow] autolens_workspace_test/interferometer/visualization/modeling_visualization_jit: historically >300s cap; local re-measurement OOM-killed (SIGKILL) at 132s - me…
  [yellow] autolens_workspace_test/misc/database/scrape/multi_analysis_jax: re-measured: times out at the real 300s cap (full search, no test mode)
  [yellow] autolens_workspace_test/misc/database/scrape/slam_general_jax: re-measured: times out at the real 300s cap (full search, no test mode)
  [yellow] autolens_workspace_test/misc/database/scrape/slam_multi_one_by_one_jax: re-measured: times out at the real 300s cap (full search, no test mode)
  [yellow] autolens_workspace_test/misc/database/scrape/slam_pix_jax: re-measured: times out at the real 300s cap (full search, no test mode)
  [yellow] autolens_workspace_test/multi_dataset/jax_likelihood/delaunay.py: hung 1805s in release-integrate run 33177898708 (second vmap call, post-compile) with XLA_FLA…
  [yellow] autolens_workspace_test/multi_dataset/jax_likelihood/delaunay_mge.py: hung twice in 30 min with XLA_FLAGS=--xla_cpu_multi_thread_eigen=false in force: 1805s at…
  [yellow] autolens_workspace_test/multi_dataset/jax_likelihood/shared_preloads.py: hung 1805s in release-integrate run 33220882817 (vmap trace at shared_preloads.py:211 …
  [yellow] Skipped-script census: 13 SLOW (5 unmeasured) / 14 NEEDS_FIX / 52 permanent across 10 workspaces
  [yellow] PyAutoArray: PyAutoArray: open PR 7d old
  [yellow] Release readiness: workspace validation not passing (14 failed, cloud#42607741369: autolens_test scripts/imaging/delaunay.py, autolens_test scripts/imaging/rec…
  [yellow] HowToFit:behind: behind: 2
  [yellow] PyAutoEyes:behind: behind: 1
  [yellow] PyAutoHands:behind: behind: 8
  [yellow] PyAutoHeart:behind: behind: 2
  [yellow] PyAutoInsight:behind: behind: 1
  [yellow] PyAutoMemory:behind: behind: 2
  [yellow] PyAutoPulse:behind: behind: 1
  [yellow] autocti_workspace:behind: behind: 2
  [yellow] autofit_workspace:behind: behind: 2
  [yellow] autogalaxy_workspace:behind: behind: 2
  [yellow] autolens_workspace:behind: behind: 2
  [yellow] PyAutoArray/test_autoarray/inversion/inversion/test_log_det_sparse.py::test__log_det_regularization_matrix_term__vertex_coincident_adapt_split__numpy_matches_j…
  [yellow] PyAutoArray/test_autoarray/inversion/plot/test_inversion_plotters.py::test__inversion_subplot_of_mapper__is_output_for_all_inversions: yellow
  [yellow] PyAutoGalaxy/test_autogalaxy/interferometer/model/test_plotter_interferometer.py::test__visualizer__matrix_free_route[True]: yellow
  [yellow] PyAutoGalaxy/test_autogalaxy/interferometer/test_fit_interferometer.py::test__fit_figure_of_merit__sparse_operator__pixelization_only__jax_jit_matches_numpy: y…
  [yellow] PyAutoNerves/test_autonerves/test_default.py::test_keep_first: yellow
  [yellow] Unit-test timing: 6 tests >1.5× baseline, 279 within
  [yellow] URL hygiene: 2 forbidden pattern(s) in 2 repo(s) (swept 2026-11-04T13:58:45.284480+00:00)
  [yellow] PyAutoCortex: yellow
  [yellow] PyAutoPulse: yellow
```

## Development handoff — 2026-11-10

- PR: https://github.com/PyAutoLabs/autofit_profiling/pull/13; issue12 remains open for human merge.
- Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-30d-diagnostics/autofit_profiling; branch feature/nautilus-30d-diagnostics; head168f3c6bf0176e2f46d4a195a025f43d8fecc308.
- Measurements at3cf17eab18ead7fff72d3bf0de394c8c22188303, original pins preserved. Added diagnose.py, diagnose_report.py, diagnostic helpers/tests, experimental protocol/evidence.
- 5D/10D completed fresh-only logZ errors +0.012717/−0.017798, versus −0.057994/−0.147382 originally.
- First30D fresh case timed out at120.07s. Read-only partial checkpoint: error−0.049803, ESS2633.6/10000,118900newcalls. Ineligible as success. Other2repetitions and wrapped output replay unrun; stopped per plan; no retries/cap escalation.
- Charged159.24s including5.14s preflight. Original checkpoint/result hashes unchanged. ~93MB raw output retained under output/nautilus-30d-diagnostics; earlier worktrees untouched.
- Incremental native checkpoint writes omit the changed discard flag. Timed output copy retained inconsistent old flag; partial inspection setTrue in memory only. Final harness fully writes mode before sampling.30D copied-checkpoint reload smoke passed with zero added calls. No timed rerun after correction.
- Evidence/report in experiments/nautilus_30d_diagnostics; all statuses and unrun cases visible. No Pulse registration/catalogue changes; whole phase0b incomplete.
- Validation:78toolingtests, Ruff, runtime preflight restores3original posterior hashes, discard leaves0selected, native mode roundtrip, original integrity, catalogue and9local report links pass. Log:output/nautilus-30d-diagnostics/validation/tests.log. Author review only.
- Exact-head CI: pull_request run42836078590, lint job129898505755, every step successful including lychee. All configured runs for this head verified.
- Authoritative Heart RED at2026-11-10T14:30:29.649657+00:00: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure". Live phase0b development override and plan approval remain recorded. No merge/release authority.
- Human view: /mnt/c/Users/Jammy/Workspace/Science/scratch/nautilus_30d_investigation_2026-11-10/results/evidence/report.html.
- Next: human review/merge ofPR13. A later bounded output-only replay remains needed; do not automatically resume the halted matrix or promote the partial30D result.

## Approved output-only continuation — 2026-11-10

Human: "Continue the wrapped-output investigation" after explicitly choosing it instead of merge. Reuse the approved output replay arm with exactly one case in a separately frozen plan, fresh copied original30D checkpoint, pinned runtime, zero new likelihood calls and durable stages. Add --output-only preparation and scope validation so no evidence case can restart;120s/4096MiB child cap,180s aggregate including preflight, no retries. Preserve the original halted pilot. Update this same issue/PR after validation; remain outside Pulse and leave merge human.

## Output continuation handoff — 2026-11-10

- Live instruction: "Continue the wrapped-output investigation"; merge explicitly not selected.
- PR13 updated at c13f420aea67289d7ce921806bf50d5d638477c3; output measurement code e701a77f83d7c58ba49a534e4aa180f8db28395c; same worktree/branch/issue12.
- Added --output-only frozen scope with exactly1case,120s/4096MiB child cap and180s aggregate, rejects evidence cases. Both native and wrapper likelihood calls blocked.
- Attempt timed out at120.0616s inside SearchUpdater.visualize. Samples conversion9.9016s, summary10.5721s, CSV5.2632s; enclosing _save_samples25.7716s. Latent stage0.01646s. Nested times overlap. Later profile/summary and post-fit output not reached.
- Charged123.1886s including2.9483s preflight. Sampled peak526MiB. Durable trace captures visualize entry and no exit. Cold Matplotlib font-cache setup occurred in the visualization stage; no isolated rendering duration or exact original interruption location claimed.
- Native run returned in0.00629s without sampling. Copied checkpoint byte-identical after timeout; originals unchanged. No completed-fit receipt. No retries/cap escalation; original halted six-case pilot remains unchanged.
- Source inspection: weighted-search full-corner enabled, compact above10parameters, full plot skipped only above30; this30D model still eligible. Plot-subset/config comparison is a possible later separately scoped experiment; no library/default changes.
-81tests, Ruff, catalogue and15report links passed; regression covers output-only scope admission, both likelihood entry points, and unfinished-stage rendering. Tests log:output/nautilus-output-only/validation/tests.log.
- Raw output:output/nautilus-output-only (~45MB) retained in addition to earlier~93MB and original archives. Committed portable receipts:experiments/nautilus_30d_diagnostics/output_evidence.
- Current authoritative Heart RED at2026-11-10T14:52:02.458296+00:00: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure". Existing live phase0b development override and specific output continuation authority recorded. No merge/release authorization.
- Human view:/mnt/c/Users/Jammy/Workspace/Science/scratch/nautilus_30d_investigation_2026-11-10/output_replay/output_evidence/report.html.
- Next:human review/merge PR13; no automatic further experiments. Full phase0b incomplete; remains outside Pulse.

- Latest exact-head CI:run42838953442/job129908636691 for c13f420; every configured step passed, including lychee. PR13 remains open/unmerged.

## Approved plot comparison continuation

Nautilus visualization comparison — proposed bounded continuation

Status: approved live "I approve" on2026-11-10.
Issue12 / PR13 / feature/nautilus-30d-diagnostics; PR remains unmerged. Outside Pulse.

New read-only findings
The pinned runtime enables corner_anesthetic and permits the full plot through30parameters. It uses compact lower-triangle histograms plus diagonal KDE above10parameters. D30 therefore has465panels and30diagonal twin axes. figsize_per_parammeter=4 makes a120x120inch figure. Live Matplotlib settings: figure.dpi=100, savefig.dpi=figure, implying a12000x12000 raster (144million pixels;576MB for one RGBA buffer before other overhead). This is a theoretical export size, not a measured allocation. The capped replay produced no search plot; current broad-stage trace cannot distinguish axis construction, data plotting or rendering. No new timed experiment or source edit was made to obtain these facts.

High-level plan
1. Preserve both halted experiments and add a separately named three-case visualization comparison on the same original30D checkpoint and pinned environment.
2. Compare no search corner plot, a six-parameter compact corner, and a smaller-canvas full30D compact corner. Keep the fitted model, posterior and all non-plot output identical.
3. Trace axis construction, data plotting and PNG export separately, including incomplete stages and unexpected plot errors.
4. Publish timings, exact settings, figure receipts and limits in the existing experimental PR; do not change library defaults or claim full phase0b complete.
Tier: judge — merge mode: human /prm.

Detailed implementation
Continue in /home/jammy/Code/PyAutoLabs/.worktrees/nautilus-30d-diagnostics/autofit_profiling on feature/nautilus-30d-diagnostics, updating issue12/PR13 and Mind's active record after approval. No new library branch or Pulse task.
Extend scripts/misc/profiling/nautilus_diagnostics.py and diagnose.py with a separately frozen plot-comparison scope; retain validation of the original six-case and single output-only protocols unchanged. Extend diagnose_report.py and focused tooling tests.
All three cases use copied original seed0/D30 checkpoint, unchanged original stopping settings and all34100likelihood calls already stored. Native and direct-wrapper likelihood entry points remain forbidden; verify input and posterior hashes. Intercept only the search plotting callable in child-local context, restoring it afterwards. Do not disable sample/latent output or change source libraries.
Fixed order and exact variants:
A: no search corner plot; all other wrapped output remains enabled. Establish whether full finalization completes without the corner.
B: one six-parameter corner of indices[0,6,12,17,23,29], explicit compact style (diagonal kde_1d, lower hist_2d, upper=False), figsize=(12,12), dpi=100. Use every sample and its original weight; no thinning.
C: one full30D corner with the same explicit compact style, figsize=(12,12), dpi=100. This keeps panel count but reduces canvas dimensions from the earlier default. The small full30D figure is a diagnostic variant, not a proposed readable default.
Use one declared font-cache state established during charged preflight and shared by the sequential cases; record it and avoid presenting these as matched warm/cold comparisons to the earlier cold-cache timeout.
Durable entry/exit events: wrapped stages plus anesthetic.make_2d_axes, NestedSamples.plot_2d, and matplotlib.figure.Figure.savefig (or the exact callable used by the installed pinned implementation). Record actual figure inches, DPI, axis count, PNG dimensions and file hash. No profile-based monkeypatch optimization. A caught plotting exception or missing required output is a failed case, not success.
Caps: at most3sequential attempts,120s and4096MiB perchild,420s aggregate including runtime/font preflight. Existing host memory/load guard, native threads1, no concurrent timing jobs. Stop on first failure/cap, no retry/escalation. No fresh sampling, evidence resampling, HPC or library optimization.
Witnesses: A has no search corner and completes full wrapped output; B/C each produce exactly the requested PNG and retain unchanged posterior/calls. Reports must distinguish completed cases, caps and unrun cases; nested timings cannot be summed. Checkpoint hashes unchanged before/after. Test scope cannot admit evidence cases, wrong dimensions/indices, or larger caps; stage patches restore; swallowed plot errors are detected; missing images are failures.
Commit measurement code before preflight; retain exact producer/runtime pins. New raw directories under output/nautilus-plot-comparison; portable evidence under experiments/nautilus_30d_diagnostics; figures/viewing copy in a new child of this scratch task. Existing measurements, raw inputs, halted states and their reported coverage stay unchanged.
Acceptance is causal diagnostic evidence, not a prespecified speedup: determine which stages scale with panel count/canvas and whether non-plot output completes. Single realizations cannot establish stable speedups. No production-default or full-accuracy claim. On completion validate, update PR13 and stop for human review; no merge.

Why approval is required
Workspace AGENTS.md says: "Present a plan and wait for explicit user approval before editing any source, workspace script, notebook, test, or release file." This is a new three-case experiment beyond the completed one-case continuation. The existing phase0b Heart RED development override remains recorded; this request is for the new experimental scope, not a repeat Heart override.

## Plot-comparison implementation checkpoint — approval clarification pending

- Approved three-case harness implemented but not committed/run: diagnose.py and diagnostic helpers extend plot-comparison scope; new nautilus_plot_comparison.py hooks af.Nautilus.plot_results, anesthetic.make_2d_axes, NestedSamples.plot_2d and Figure.savefig; new plotting tests and portable PNG/stage reporting. Original library sources/defaults untouched.
- 93 tooling tests pass; Ruff clean. Log:output/plot-comparison-precheck.log. No timed plot-comparison attempt or runtime preflight has started. Existing PR13 headc13f420 remains unchanged/unmerged.
- Source preflight found an incompatible constraint: pinned PyAutoFit SearchUpdater._profile_and_summarize (updater.py:380) unconditionally calls fitness.call_wrap once to time the best point before save_summary. The approved zero-likelihood-call guard would reject the no-corner control after visualization, halting the entire plan.
- Asked human: allow exactly one final-summary timing evaluation percase (native sampling remains forbidden, separately counted), or keep zero calls and omit that timing stage (changes non-plot output). Await answer; do not infer approval or run the known failure.
- If one call is allowed, scope it only to _profile_and_summarize, cap at1, retain native evaluate_likelihood guard, record sampler calls0 and summary calls1 separately, verify posterior/call invariance and test extra/out-of-stage calls are rejected. Update frozen protocol/issue before committing measurement code. If zero, document the skipped stage explicitly instead of inventing timing data.

## Timing clarification approved

Human: "Allow one final-summary timing call per case". Plot comparison only: exactly1target evaluation inside final-summary timing, native sampling forbidden. Count separately; reject extras/out-of-stage calls and verify stored max-likelihood point/value. Earlier zero-call protocols unchanged. Proceed with original3case caps and stop rule; no merge.


## Plot continuation outcome — 2026-11-10

Measurement code frozen at51663d11fc6a873d9681899608bd352a294293e5. Runtime/checkpoint/font-cache preflight passed in6.4377s. Driver halted before launching any child with `RuntimeError: host load exceeds guard` (eight-CPU affinity gives threshold2.0; rejected exact load was not persisted). All3cases remain unrun. Total charged6.4379s; no target evaluations, figures or new timing comparisons. Stop rule honored with no retry. Full phase0b incomplete; outside Pulse.

Report/tests head9dbc272a1bb498d0d2b6d4e904484c3d84e7914f pushed to PR13, open and unmerged.98tests, Ruff, catalogue and18local report links pass; new exact-head CI run42843360212 attempt2 failed only on unchanged Brain standards link HTTP503; tests/lint/format/catalogue passed. Plotting path has no end-to-end runtime witness. Summary timing guard tests reject zero/two-call plan changes, extra/out-of-scope calls and preserve old zero-call scopes. Measurement code stayed clean during preflight/guard check; report display/test added afterward.

Published plot_evidence contains halted state, all-unrun coverage and portable plan; raw20KiB plan/state retained under output/nautilus-plot-comparison, previous~93MB+45MB and original archives retained. Human view: /mnt/c/Users/Jammy/Workspace/Science/scratch/nautilus_30d_investigation_2026-11-10/plot_comparison/plot_evidence/report.html.

Heart remains RED at2026-11-10T14:52:02.458296+00:00: "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure". Live phase0b development override, plot-plan approval and "Allow one final-summary timing call per case" recorded in issue, PR and ledgers. No merge/release authorized. Next: human may authorize a fresh bounded attempt after host load settles, with a new plan/output identity retaining this halt, or review/merge the existing diagnostic work. No automatic retry.

Exact-head CI final: run42843360212 attempts1and2 both failed only on lychee receiving503from https://github.com/PyAutoLabs/PyAutoBrain/blob/main/docs/standards.md (unchanged AGENTS.md link). Attempt2 job129925246485; all code/test/catalogue checks passed. One CI-only retry, no experiment retry. CI is not green; no merge. Logs retained in output/plot-ci-failure.log and output/plot-ci-retry-failure.log.

## Fresh plotting attempt authorized

Live human: "I approve, continue" after the host-load halt. Authorizes one fresh three-case comparison with unchanged 120s/4096MiB per-child and420s aggregate caps, same stop-on-first-failure rule and exactly one final-summary timing call per case; native sampling forbidden. Original halted plan/state retained. New identity: output/nautilus-plot-comparison-02, producer9dbc272; no source changes before measurement. Entry host load0.434 below2.0 guard, available memory about13.6GiB. Outside Pulse; no merge or release.

## Corrected comparison authorized

Attempt02 at9dbc272: no-corner child failed18.982s due to timed_summary bound argument `instance` colliding with PyAutoFit instance keyword; charged22.364s, two cases unrun, checkpoint byte-identical, no target calls. Fixab896cd renames bound argument updater;99tests plus Ruff/catalogue/22links pass. After this concrete fix human selected "Run corrected comparison once". New raw identity output/nautilus-plot-comparison-03, same3cases and120s/4096MiB/420s caps, same stop rule and exactly1scoped summary call; native sampling forbidden. Both prior halted runs retained. Outside Pulse; no merge.


## Corrected attempt03 results — 2026-11-10

Human selected "Run corrected comparison once". Measured cleanab896cdc36061b33998bae9c214d6a47c7773b5d; report259c62ee0c90c95d975a5c2e5288d6c82a24fbed. Same3cases,120s/4096MiB child,420s aggregate; spent242.321s including4.518preflight. No-corner success54.054s and six-small success62.278s. Both completed normal finalization, unchanged posterior/n_like34100 and exactly1scoped summary call,0new sampler calls. Six-small verified1200x1200PNG,27axes,all33984samples/weights,indices0,6,12,17,23,29; visually inspected. Original library labels allaxes x.

Full30D small-canvas timeout120.092s, axes9.997s, posterior plotting74.739s, PNG export entered at trace109.261s then killed; noPNG, nofinalsummary/postfit.495axes at12x12in/100dpi. All3checkpointcopies byte-identical; original hashes passed. RSS sampled peaks347/365/526MiB. Inclusive stage times overlap; process times include imports/provenance/checkpoint and posterior checks. Single realizations do not establish speedups; prior large-canvas replay used different cache state. Shrinking canvas alone did not complete full30D within cap; plotting fewer parameters did. No automatic retry.

Raw output/nautilus-plot-comparison-03 ~156MiB retained; attempt02 ~45MiB and every previous archive retained. Portable plot_evidence_03 plus figure/integrity receipts; previous plot_evidence and plot_evidence_02 preserved. Human view /mnt/c/Users/Jammy/Workspace/Science/scratch/nautilus_30d_investigation_2026-11-10/plot_comparison_03/plot_evidence_03/report.html.

99tests,Ruff,catalogue,26local links passed. Exact-head CI42845740473 failed (output/plot-03-ci-failure.log retained); current HeartRED at2026-11-10T15:27:23.643729+00:00 exact reasons "PyAutoGalaxy: CI failure"; "PyAutoLens: CI failure". Live development override persists, merge remains human. Fullphase0b incomplete/outside Pulse. Next human review/merge onceCIgreen; new experiments or optimization need separately scoped decision.

Final CI detail: run42845740473/job129932586557 code checks all passed; only lychee failed with HTTP503 from unchanged Brain docs/standards.md and Mind draft/research/autofit/search_extensibility_epic.md links. No more CI reruns after repeated service failures across heads; overall CI remains red.
