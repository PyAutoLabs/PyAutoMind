# Single-process CPU route: JAX vis_lp then Numba + pool vis_pix without a process boundary

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoFit
Themes:
- euclid
- jax
- hpc
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Epic: euclid-dr1-prep
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-09-02

Follow-up spawned by Mind phase 4 of the euclid-dr1-prep epic
(`euclid_strong_lens_modeling_pipeline#49`). Phase 4's control test,
`hpc/diagnostics/jax_fork_control.py`, measured whether a forked Nautilus pool
started from a process that already has a CPU XLA backend initialised hangs —
and it did not, on either machine tested:

- Laptop (WSL2, 4 workers): `control` 265 s, `control_real` 494 s, `subprocess`
  233 s — all PASS.
- RAL (`euclid-ral-compute-1`, 16 workers, `n_like_max=2000`): `control` 216 s,
  `control_real` 378 s, `subprocess` 220 s — all PASS, 0 tracebacks.

The `control_real` leg is the pipeline's own `fit(stage="vis_lp",
use_cpu=False)` followed immediately by `fit(stage="vis_pix", use_cpu=True,
number_of_cores=N)` in the same process — i.e. exactly the single-process
route this prompt asks for, but only exercised at diagnostic sampler sizes.

What phase 4 shipped instead was the conservative default: the two-stage route
kept as two separate processes (a single-submission chain script
`hpc/batch_cpu/submit_initial_lens_model_two_stage` plus separate vis_lp and
vis_pix jobs), documented in `hpc/README.md` as conservative because
production sampler sizes (`n_live` 750/300, `n_like_max` 200000/100000) and
multi-hour wall times were never measured for the fork-survives-XLA-init
behaviour — only the short diagnostic runs above were.

The ask: add a mixed mode to `scripts/initial_lens_model.py` so one process
runs `vis_lp` under JAX (CPU backend) and `vis_pix` under Numba with the CPU
sparse operator and a forked pool, in sequence, without a process boundary
between them. Concretely: a new flag (name to be decided at plan time, e.g.
`--pix_cpu`; the existing `--use_cpu` must keep meaning "no JAX anywhere in
this process") that sets `use_jax=True` for the vis_lp analysis and
`use_jax=False` plus `apply_sparse_operator_cpu()` plus `number_of_cores` for
the vis_pix analysis. Add a `hpc/batch_cpu/submit_initial_lens_model_single_process`
submission script alongside the existing two-stage one, with per-stage thread
pinning resolved for a single process — threads-equal-cores is fine while JAX
runs vis_lp alone, but the forked pool then oversubscribes unless BLAS thread
count is dropped to 1 before the pool starts; investigate `threadpoolctl` or
setting the relevant env vars right before the vis_pix search launches.

Validate at production scale on RAL before trusting this beyond the
diagnostic: run one lens through the new single-process route with the real
sampler settings, compare wall time and result against the same lens run
through the existing two-process route, and re-run `jax_fork_control.py` at
production `n_like_max` to see whether the survives-fork result still holds
at that scale.

Acceptance: a production-scale single-process run completes and its result
matches the two-process route's result for the same lens within sampler
noise; `hpc/README.md` gains a route-table row for the single-process option
and its "conservative default" paragraph is rewritten to state the measured
position instead of the untested caveat. A measured verdict either way is
shippable — if the single-process route hangs or degrades at production
scale, record that finding and close the task; the two-process route stays
the default.

Note two things that constrain the design: `forkserver`/`spawn` remain off
the table because PyAutoFit pins the `fork` start method
(`PyAutoFit#1437`), so this has to work within a forked pool, not around it;
and PyAutoFit's documented deadlock concern is specifically about a forked
worker whose own likelihood touches JAX, which the Numba vis_pix likelihood
does not — the risk being tested here is the surrounding process having
touched JAX before the fork, not the worker doing so after it.
