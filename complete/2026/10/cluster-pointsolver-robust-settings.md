## cluster-pointsolver-robust-settings
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/436
- completed: 2026-10-22
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/438

- Merged as `c8c9abb3` (2026-10-22); research only (autolens_profiling), Consequence judge, human `/prm`. Pulse campaign `cluster-pointsolver` phase 1.
- Deliverables: `scripts/cluster/image_plane/{robust_settings_sweep,_oracle,_judge,_datasets,_memory,oracle_figure,solver_figure}.py` (+ RAL submit scripts, 14 tests); datasets `simple` (13 components, 3 planes, 2 sources, truth gate) and A2744 synthetic prior-median 191-component model (labelled, not a fitted cluster); ledger `results/notes/cluster_pointsolver_campaign.md`; wiki `wiki/campaigns/cluster_pointsolver.md`; sweep JSON/PNG + 12 figures under `results/breakdown/cluster/`; dashboard/catalogue re-rendered.
- Ground truth: independent oracle (dense multi-plane residual sampling + Newton polish, roots certified < 1e-10″ residual / 1e-6″ stability); calibrated 6/6 at 2.84e-8″ on RAL (1.96e-8″ laptop).
- Result (`simple`, 101 draws, RAL job 412572, CPU fp64, Xeon 8490H): NO setting admissible. Production-extent rows cover 306/306 prior roots, miss 2–6 of 300 stress roots; every miss is a close high-|μ| pair 0.33–0.76″ apart (draws 53/73 tangential, draw 81 radial — missed by every start). Initial scale 0.5″/0.7″ miss 2 at 0.78×/0.75× control speed; production 1.0″ misses 5 (5.29 ms warmed two-source solve); 2.0″ misses 6 (1.30×). Precision 0.01/0.001, MAX_CONTAINING_SIZE 20/40/60 and backend (NumPy/JIT/vmap) change nothing → misses come from the starting grid, not the JAX path. Uncapped containing count ≤ 7 (cap 20 never binds). Eager JAX unusable (row wall over cap). Truth-bbox extents miss 49–63 stress roots. Peak RSS 4.3 GB, live arrays small (retained executables).
- Decision (human, 2026-10-22, chat): DEFERRED — production default stays 1.0″; re-decide after the starting-grid draft and the A2744 pull; 0.5″ is the working answer if forced. No default changed anywhere.
- Checked: the `FitPositionsSource` jacobian-weighting default change (PyAutoLens bdb44a87c) cannot touch this sweep — no sweep script uses `FitPositions*` or a chi-squared. The new cluster `point_solver.png` visualizer (b1754a7ec) is used by `solver_figure.py` (oracle roots as observed circles; a miss = circle without a solved cross).
- Traps: API-gate hook RecursionError on `autolens.plot` → grep-grounded + `PYAUTO_SKIP_API_GATE=1`; `build_catalogue --check` STALE arises from any new cluster setup JSON → full re-render from a clean worktree; `catalogue/script_routes.json` takes no row (legacy aliases only); Heart YELLOW at ship (manifest drift, PyAutoArray rehearsal stale — unrelated), acknowledged by the human at `/prm`.
- Follow-ups: (1) A2744 pilot leg job 412573 (256 GB, 6 h) completed on RAL but NOT pulled — jump host `finan` refused the SSH key 2026-10-22; pull `.out`/JSON/memory_trace and attribute the RSS growth (row-1 live: peak 22 GB, RSS 8.3 GB, live arrays ~0); no resubmission without human go. (2) Pulse PR: paste the Knowledge block from the ledger appendix into `tasks/cluster_pointsolver_speed.md`, `campaigns.yaml` next/updated, check-in, board. (3) Starting-grid / close-member-image question: `draft/research/autolens_profiling/cluster_pointsolver_starting_grid_close_member_image.md`. (4) The human's upcoming Pulse profiling programme may revisit the goal.
- Claim released: `planned.md` `likelihood-lifecycle-p0-profiling` is unblocked.

## Original prompt

# `@autolens_profiling` cluster-pointsolver phase 1: cluster-scale robust PointSolver settings (independent ground truth, CPU fp64 on RAL `ral`)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Epic: cluster-pointsolver-speed
Pulse: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/cluster_pointsolver_speed.md (campaign `cluster-pointsolver`)
Filed: 2026-10-17
Issued: 2026-10-17
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/436
Witness: `results/notes/cluster_pointsolver_campaign.md` carries a supported-settings table where every row has an oracle-verified per-root coverage count, a multiplicity verdict, an overflow verdict and separate compile / first-call / warmed costs with host + SHAs + dataset digest; failing rows are labelled diagnostic/invalid and never substituted into a speed claim.
Review-minutes: 30
Unattended: needs-decision

## Original request (verbatim)

Phase 1 to plan and, once I approve, start via start_dev (one bounded task, judge tier):
"Cluster-scale robust PointSolver settings." Deliverables, in autolens_profiling:
1. Representative cluster data: pick one or two datasets justified against
   autolens_workspace scripts/cluster/ (sources, planes/redshifts, images per source, lens
   components dPIE/NFW/members, the solver grid production fits actually use). The
   gitignored dataset/cluster/simple (13 components, 3 planes, 2 sources) is a starting
   point, not a verdict.
2. Robust-settings sweep on that data, CPU fp64 on RAL `ral` (exclusive node; never `gpu`):
   initial grid scale and extent, pixel_scale_precision 0.01 vs production 0.001,
   containing-size capacity, backend (NumPy / eager JAX / JIT / vmap), per-image coverage
   and multiplicity against an independent numerical reference (reuse 1d's method), overflow
   and unresolved-case detection. Every configuration is its own row; failing configurations
   are labelled diagnostic/invalid and kept, never substituted into a speed claim. Record
   compile, first-call and warmed costs separately with host, SHAs and dataset.
3. A results note with the supported-settings table and tested domain, a campaign wiki
   journal entry, and a Pulse Knowledge draft for tasks/cluster_pointsolver_speed.md.
Out of scope for phase 1: library edits (file findings as bounded Mind prompts instead),
workspace_test CI witnesses (phase 2 distils accepted claims into regressions), A100 rows,
and the observable-overflow API contract (separate task).

Rules: present the plan and wait for my approval before any edit or job; compute needs my
explicit authorization in this chat; no laptop timing; private RAL checkouts only; sessions
end at the deliverable with no background follow-up. After phase 1 ships, update the Pulse
ledger (campaigns.yaml next/updated, task check-in section, board regen) through a PR.

Human, mid-planning (2026-10-17): "Try to make sure you have a good source of ground truth
when making decisions its a hard problem otherwise."

Plan approved by the human in chat 2026-10-17 ("Approve").

## Why

Robust-settings evidence for the PointSolver is single-source only (Source & Cluster 1a–1d,
records `complete/2026/09/point-solver-error-audit.md`, `point-solver-padding-backend.md`,
`complete/2026/10/point-solver-duplicate-policy.md`, `point-solver-image-accuracy.md`,
`pointsolver-extent-sanity-check.md`). 1c/1d are NO-GO: 18 near-cusp rows exceed capacity 20
(uncapped max 87), 10/32 rows miss per-root coverage, a conditioning screen falsely accepts 3
non-converged candidates. The cluster profiling cell solves on 200×200 @ 0.7″ at precision 0.01
with no completeness check, while production cluster fits (`autolens_workspace/scripts/cluster/`)
use 120×120 @ 1.0″ (±60″), precision 0.001, magnification threshold 0.1. No lever may be ranked
until the settings that actually find every image at cluster scale are known.

## Ground truth (design rule, from the human)

Every decision in this task rests on an **oracle independent of the triangle solver**:

1. Oracle = dense fine sampling of the lens equation residual `|θ − α_multi(θ) − β|` over the
   image-plane extent, Newton (or damped Gauss-Newton) polish from every local-minimum basin,
   using the same `Tracer` multi-plane deflections (NumPy fp64). Accept a root only when its
   residual is at round-off (< 1e-10″), it is stable under a 2× finer sampling (position change
   < 1e-6″), and its magnification/parity is finite. Record the Jacobian singular values.
2. Calibrate the oracle first on the analytic isothermal+shear quad from 1a (closed-form
   positions) and on the 1c/1d `angular_roots` fixture; it must reproduce both to < 1e-6″ before
   any cluster row is judged. Record this calibration in the JSON.
3. Never use the production PointSolver, the simulator's own PointSolver output, or a candidate
   grouping rule as the oracle. The `simple` dataset's stored positions are themselves solver
   output; they are compared but are not the truth. A2744 observed positions are a physical
   sanity check only (the best-fit model misfits them at the ~0.5″ noise level), never the oracle.
4. Per-root coverage (each oracle root has exactly one candidate within tolerance), multiplicity
   agreement (distinct at 0.005″) and residual/convergence per candidate are the admissibility
   criteria; image count alone is never evidence. Tolerance is set by the solver's last-step
   triangle side (phase-4a rule), stated per row.

## Datasets (deliverable 1)

| Dataset | Lens model | Planes | Sources × images | Production solver | Role |
|---|---|---|---|---|---|
| `dataset/cluster/simple` (synthetic; regenerated on RAL by the profiling simulator with a pinned seed; gitignored) | 2 dPIE + 10 scaling dPIE + NFW = 13 | z 0.5 / 1.0 / 2.0 | 2 × 3, noise 0.005″ | workspace simulator 800×800 @ 0.1″, 0.001 | known truth tracer; cheap; continuity with carried p1–p3 rows |
| Abell 2744 (`autolens_workspace/dataset/cluster/a2744`, Bergamini+23 inputs; copied into the gitignored profiling `dataset/` by a provenance-stamped producer; FITS/CSV never committed) | 2 BCG dPIE + 188 scaling dPIE + NFW = 191 | lens z 0.308 + 6 source redshifts 1.69–5.66 | 7 × (3–4) = 24, noise 0.5″ | 120×120 @ 1.0″ (±60″), 0.001, mag 0.1 | the real production regime; images span y −52…+6″, x −35…+39″ |

SMACS0723 is excluded (one source, three images, two members). A2744's reference tracer is the
Lenstool best fit mapped through `autolens_workspace/scripts/cluster/lenstool/`; if that mapping
is not runnable, report it and fall back to the workspace model's maximum-likelihood result —
never invented parameters. Draw sets: `simple` truth + 50 seeded prior draws; A2744 best fit +
30 seeded perturbation draws; sizes confirmed by the pilot.

## Sweep (deliverable 2)

New cell `scripts/cluster/image_plane/robust_settings_sweep.py` built from
`scripts/point_source_image/image_plane/solver_config_sweep.py` (phase 4a) and the shared
`scripts/misc/likelihood_breakdown/{timing,provenance,round_bootstrap,family_gates,xla_attribution}.py`,
generalised to per-source `plane_redshift` solves. Axes, each configuration its own
interleaved route and row: extent (production; image bounding box + the PyAutoLens#764 margin
`2·scale + 3σ`; one deliberately over-tight diagnostic row); initial scale 0.5 / 0.7 / 1.0 / 2.0;
precision 0.01 vs 0.001; `MAX_CONTAINING_SIZE` 20 / 40 / 60 patched in-process with the 4a
restore gate, plus uncapped NumPy containing counts per step as the overflow detector; backend
NumPy / eager JAX / JIT / vmap 4 and 16. Neighbor degree stays default. Overflow = uncapped
count > capacity on any step; unresolved = oracle root with no candidate within tolerance or a
candidate that fails residual/convergence. Timing: CPU fp64, `--partition=ral --exclusive`,
nodelist pinned to the Xeon 8490H reference node after `sinfo`, 8 JAX threads (comparability with
carried rows), round-robin routes, 3 warm calls, medians with 2000-sample bootstrap 90 % CI;
compile_s, first-call and warmed recorded separately with host, tag SHAs (library pin
2026.10.17.1 on a private checkout, shared mirror never pulled), dataset digests, thread env,
XLA flags, FLOPs and temp memory. Output
`results/breakdown/cluster/robust_settings_sweep_<dataset>_hpc_ral_cpu_fp64.{json,png}` and
logs under `results/logs/cluster/`. Two RAL jobs, each with explicit human authorization in
chat: a pilot (oracle cost, reference stability, wall sizing) then the full sweep. A row whose
wall exceeds the cap (A2744 at 0.001 is the likely case) is kept as unusable with its reason.

## Deliverable 3

New ledger `results/notes/cluster_pointsolver_campaign.md` (supported-settings table, tested
domain, oracle calibration, unresolved cases); phase-1 row + journal entry in
`wiki/campaigns/cluster_pointsolver.md`; catalogue/dashboard re-rendered from a clean worktree;
`catalogue/script_routes.json` row for the new cell; a Pulse Knowledge draft block for
`tasks/cluster_pointsolver_speed.md`. Library findings → bounded Mind draft prompts only. After
ship, a Pulse PR updates `campaigns.yaml`, the task check-in section and the board.

## Out of scope

Library edits; workspace_test CI witnesses (phase 2); A100 rows; the observable-overflow API
contract; any default/baseline change; laptop timing.
