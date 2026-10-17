# Point-source source-plane gradient-search admission measurement (MultiStartAdam, 2026.10.17.1)

Type: research
Target: autolens_inference
Repos:
- autolens_inference
- autolens_profiling
Themes:
- point-source
- inference
- jax
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: active
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/25
Consequence: judge
Review-minutes: 20
Epic: point-source-cpu-speed
Filed: 2026-10-17
Pulse-task: organs/PyAutoPulse/tasks/point_source_source_plane_chi_squared_speed.md (campaign point-source-source, parked)
Related: organs/PyAutoPulse/tasks/runtime_cell_single_jit_gpu_warmup.md (autolens_profiling#371)

## Request (human, 2026-10-17, via the parallel-array dispatch; verbatim authorisation "Do all that, I authorise all")

Run the admission measurement the point-source source-plane campaign is blocked on: does a
gradient-based search on the source-plane chi-squared likelihood find the right answer, and at
what cost, on the released 2026.10.17.1 stack? Record hardware (A100 vs CPU, host), software
SHAs/versions, dataset, model config, precision, compile vs execution, steps/evaluations to
convergence, correctness vs truth/reference. Report against the inference repo's admission bar as
evidence only — never conclude "admitted"/"accepted" (human's call). If the runtime cell runs,
capture the median headline fields (#408/#412) so #371's fresh-median gap gets evidence. RAL
compute authorised (A100 and/or CPU); merge stays human. Blackjax stays parked unless the
inference setup names it (the point-source setup names only Nautilus).

## Scope

- One gradient search: `af.MultiStartAdam` — the library's gradient search that honours
  `AnalysisPoint.gradient_mode = "forward"` (PyAutoFit#1649/PyAutoLens#752). BlackJAX NUTS/SMC
  (`honours_gradient_mode = False`) stay parked.
- Same model, priors and dataset as the Nautilus leaf (`scripts/misc/searches/_point_runner.py`:
  L5 Isothermal + PointSolved, FitPositionsSourceSolved, `simple`, θ_E ~ U(0.5, 4)).
- Legs: RAL CPU (`--partition=ral`, 8 cores) and A100 (`--gres=gpu:1 --exclusive`), seeds 0-4,
  plus a same-stack Nautilus control on RAL CPU (seeds 0-4); private RAL venv of the released
  wheels (autolens==2026.10.17.1, resolved jax 0.11.2), never the shared PyAuto mirror.
- autolens_profiling: the source-plane runtime cell (`likelihood_runtime_solved.py`) on the same
  stack/hosts for the #371 median fields + a campaign-note section.
- No library edits; no speed-up levers.
