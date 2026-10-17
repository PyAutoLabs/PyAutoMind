Point-source source-plane gradient-search admission measurement for the PyAutoPulse campaign
`point-source-source` (issues autolens_inference#25, autolens_profiling#428). Merged 2026-10-17:

- https://github.com/PyAutoLabs/autolens_inference/pull/29 (MERGED): `af.MultiStartAdam`
  leaves (`multi_start_adam.py`, 300-step default; `multi_start_adam_n3000.py`) on the L5
  source-plane solved target, released 2026.10.17.1 wheels in a private RAL venv, RAL CPU
  (`ral`) + A100 (exclusive), seeds 0–4; runner gradient-admission bar and MAP-vs-truth in
  Nautilus σ; 20 result rows (jobs 412494/412495/412498).
- https://github.com/PyAutoLabs/autolens_profiling/pull/432 (MERGED): source-plane runtime
  median refresh on 2026.10.17.1 (A100 0.233 ms, RAL CPU 0.147 ms; first release-stamped
  median rows for #371), `PYAUTO_VENV` override in the two submit scripts, campaign ledger +
  wiki section recording the admission evidence.

Evidence, not a verdict: at 3000 steps every seed converges in 259–1432 steps to the Nautilus
log-L range with all parameters ≤ 0.80σ; at the 300-step default 4/5 seeds stop on budget.
Likelihood+gradient is 0.8–3.7% of search wall on CPU, 0.3–2.3% on A100 (fixed per-fit cost
and per-step optimiser overhead dominate). Human decision 2026-10-17: point-source gradient
work is filed as research; the BlackJAX admission call stays with the human.

## Original prompt

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
