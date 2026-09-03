Brought the two-stage CPU route — `vis_lp` under JAX, then `vis_pix` with the Numba sparse
operator and a forked Nautilus pool — out of the private science tree into the public Euclid
pipeline repo, measured whether the process boundary between the two is still needed, and
documented both the CPU and GPU routes with numbers taken on RAL. Phase 4 of the
`euclid-dr1-prep` epic; gates the Cortex science phase `phases/euclid/dr1_prelim_10_lens_science_run`.

## What shipped

euclid_strong_lens_modeling_pipeline PR #50 (`feature/euclid-cpu-two-stage-route`, 9 commits,
merge commit `2412552`), issue euclid#49 closed:

- **`--stage {all,vis_lp,vis_pix}`** in `util.parse_fit_args` and `initial_lens_model.fit`,
  default `all` so existing callers and CI are unchanged. `--stage vis_pix` fails fast naming
  the missing output directory and the `--stage vis_lp` command to run first, instead of
  silently re-fitting `vis_lp` (which could also collide with a `vis_lp` job still running on
  the same lens). `--skip_pix` kept as a deprecated alias.
- **Submission scripts** `hpc/batch_cpu/submit_initial_lens_model_{vis_lp,vis_pix,two_stage}`.
  `two_stage` runs both stages as two consecutive `python3` calls inside one allocation, each
  with its own `env` block — one submission, one queue place, JAX variables from stage 1 unable
  to leak into stage 2, process boundary preserved. `hpc/sync` gains `submit` / `push-submit` /
  `jobs` / `sacct` / `cancel` / `tail` / `logs` / `wait-and-pull` / `du` / `check`; personal
  email and host values scrubbed out of the committed scripts and `sync.conf.example`.
- **`hpc/README.md`** (new) as the single home for route choice — route table with measured
  per-lens times, the `--stage` contract, the process-boundary verdict, the RAL acceptance
  section, cluster setup and the `sync` verbs. `README.md`, `AGENTS.md`, `scripts/README.md`
  and `start_here.py` point at it.
- **`hpc/diagnostics/jax_fork_control.py`** + `hpc/batch_cpu/submit_jax_fork_control` — the
  three-leg control test for the JAX-then-forked-pool question, runnable at the size a
  production `vis_pix` fit actually forks.
- **GPU backend guard** — every `batch_gpu/` script checks `jax.default_backend()` before it
  starts, after a MIG-mode A100 with no instances configured let JAX fall back to CPU and burn
  a 2 h wall on one core while `nvidia-smi` reported a healthy GPU.
- **Sparse-operator correctness fix** — `scripts/initial_lens_model.py` no longer applies
  `apply_sparse_operator()` on the JAX path, and `scripts/full_model.py` (JAX-only, no
  `use_cpu`) no longer applies it at all. The operator is the CPU route's Numba tool; under JAX
  the pixelized inversion uses JAX's own linear algebra on the plain dataset, as the science
  tree does.

## Evidence

- **RAL acceptance, both routes end to end** from this repo's own submission scripts on the
  committed lens `q1_walsmley/102018665_NEG570040238507752998`, `PYAUTO_OUTPUT_DIR` split per
  route so neither could resume against the other's cache: GPU 1 h 14 min (A100 80GB,
  job 342248_0, COMPLETED); GPU re-run after the sparse-operator fix 1 h 44 min (job 342264_0,
  COMPLETED); two-stage CPU 3 h 17 min on 8 cores / 8 pool workers (job 342244_0, COMPLETED).
  The CPU chain's second process logged `Fit Already Completed: skipping non-linear search` for
  `vis_lp` — the new `--stage vis_pix` guard picking up the cached result.
- **The re-run is a node-speed probe, not a regression**: `vis_lp` never touched the operator
  and took exactly 15 quick-update blocks in both runs — 2.01 min per block against 2.51, a 25%
  slower node. `vis_pix` went 3.26 → 4.55 min per block (1.40x); divide out the 1.25 node factor
  and ~1.12 is left, one run against one run on a shared cluster. Quick-update cost unchanged
  (13.8 s vs 13.2 s mean). So `d32d58e` is a correctness fix, not a performance fix, and the gap
  to the documented ~10 min per lens comes from somewhere else.
- **The reset question, measured — boundary kept.** Three legs on two machines, no hang
  reproduced anywhere: `control` (JAX likelihood in-process, then a `use_jax=False` pooled
  Nautilus) 265 s laptop / 216 s RAL; `control_real` (the script's own `fit(stage="vis_lp")`
  then `fit(stage="vis_pix", use_cpu=True)` in one process) 494 s / 378 s; `subprocess` 220 s /
  220 s. PyAutoFit's documented deadlock concerns a forked worker whose *likelihood* touches
  JAX, and the `vis_pix` likelihood under `--use_cpu` is Numba. Untested: production sampler
  size (`n_live` 750/300 against 50) and multi-hour walls — so the process boundary stays as
  the conservative default, which costs nothing with the single-submission chain script.
  `forkserver`/`spawn` are not an option (PyAutoFit pins `fork`, PyAutoFit#1437).
- **CI**: PR #50 green on head `f092efe` — 2 workflow runs, 9 legs (unit, slow, smoke ×
  changes / 3.12 / 3.13), all `success`; `mergeStateStatus` CLEAN. Ship gate: pytest 72 passed,
  smoke 9/9.
- **Heart RED at ship, human-acknowledged and unrelated to this repo**: "PyAutoLens: CI
  failure"; "release validation FAILED (stage integrate)"; "PyAutoArray: open PR 11d old".
  Workspace/pipeline-only change — no library PR, nothing pending release, no freeze window.

## Follow-ups (filed)

- `draft/bug/euclid/gpu_per_lens_time_vs_documented_10_min.md` — re-scoped 2026-09-03: the
  `apply_sparse_operator` drift is fixed here and measured not to be the cause, so the ~7x gap
  to the documented ~10 min per lens stays open against the science `config/`, per-lens JIT and
  visualisation, or the claim's provenance.
- `draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md` — the
  single-process route; the control test found no hang, but production sampler size and
  multi-hour walls are untested, so the boundary was kept.

## Left for a human

`PyAutoCortex/phases/euclid/dr1_prelim_10_lens_science_run` names euclid#49 in its `Gates:`
line. Both gates (`euclid#48`, `euclid#49`) are now closed; no Mind tooling updates Cortex
phase state, so opening that Cortex phase stays a human step.

## Original prompt

# CPU route: keep the two-stage vis_lp (JAX) → vis_pix (numba + multiprocessing) submission, document the GPU route

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- PyAutoLens
Themes:
- euclid
- jax
- hpc
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: euclid-dr1-prep
Phase: 4
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28
Issued: 2026-09-02
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/49 (opened 2026-09-01 as a Cortex gate ref; reuse in start_dev — never open a second)

Phase 4 of the Euclid DR1 preparation epic (3 → 3b on 2026-08-31 when the prose-restoration
phase 3a was inserted ahead of it; 3b → 4 on 2026-09-01 in the Cortex split). **Gate: phase 1.**
Can overlap phase 2. Runs after phase 3, so the documentation this phase writes lands in a repo
whose narrative register has already been restored.
**Gates the 10-lens science run**, which is now `PyAutoCortex` `phases/euclid/dr1_prelim_10_lens_science_run` —
that Cortex phase names this prompt's issue in its `Gates:` line.

User request (verbatim):

"""
3) Science runs I perform for initial_lens_model.py use JAX for the MGE fit (vis_lp) and then numba with python multiprocessing for pixelization
   (vis_pix). The reason I do this is because I have loads of CPUs available and this means this is a much fastest way
to model large sampels. At the moment, I think this requires submission scripts be sumbmitted which run once for vis_lp,
then reset and run for vis_pix, as this avoids a JAX / Python multirprocessing conflict. First, make sure this functionality
is maintained, but also look to see if we can avoid the reset of the script (but its fine if thats not possible). Then,
make sure documentaiton is clear that fully JAX GPU runs are supported, they are typically much faster and recommended if you
are modeling a small subset of Euclid lenses. Retain example batch submission scripts showing these different approaches.
"""

## Why the reset exists

JAX and Python `multiprocessing` conflict once JAX has initialised in a process — this
is the same class of hazard the workspace already knows about (no kernel threading under
nautilus multiprocessing; `Pool` objects bypassing the serial guard). The current
workaround is process-level: submit once for `vis_lp` (JAX, MGE fit), let the process
die, submit again for `vis_pix` (numba + multiprocessing, pixelization). The
requirement is **first preserve this**, then *investigate* removing it. A verdict of
"cannot be removed safely" is an acceptable, shippable outcome.

## Current state (surveyed 2026-08-28)

The pipeline repo's `hpc/` has `batch_cpu/` (`submit_start_here`, `template`, plus
`error/` and `output/`) and `batch_gpu/` (`submit_full_model`, `submit_start_here`), and
a `sync` CLI with `sync.conf.example`.

`Science/euclid/hpc/` is much richer and is the source of truth:
- `batch_cpu/`: `submit_initial_lens_model_q1_sample_first1`,
  `submit_galaxy_sersic_model_cpu`, `submit_build_inspect_cpu`,
  `submit_generate_deblending_fits_cpu`, `submit_generate_magnitudes_cpu`,
  `submit_deduplicate_deblending_fits_cpu`, `submit_audit_sed_outputs_cpu`,
  `submit_build_inspection_bundle`.
- `batch_gpu/`: `submit_initial_lens_model_vis_lp_gpu`,
  `submit_initial_lens_model_vis_lp_gpu_q1_sample_first1`,
  `submit_initial_lens_model_vis_pix_gpu_q1_sample_all`,
  `submit_initial_lens_model_vis_pix_gpu_q1_sample_first1`,
  `submit_sersic_lens_model_gpu`, `submit_galaxy_sersic_model_gpu`.
- Plus `submit_remaining_dr1_grade_ab.sh`, `sync`, `sync_jump`, `sync.conf`.

The `vis_lp` / `vis_pix` split is visible in those GPU submit names — read them to
recover the exact two-stage invocation before changing anything.

## Deliverables

1. **Preserve the two-stage CPU route.** `initial_lens_model.py` runnable as
   `vis_lp` (JAX, MGE) then, in a fresh process, `vis_pix` (numba + multiprocessing),
   with the stage selection exposed cleanly (a CLI flag, not an edit-the-script ritual).
2. **Investigate removing the reset.** Concretely: can the JAX stage be confined to a
   subprocess so one submission does both? Is `forkserver`/`spawn` sufficient? Measure,
   don't reason — a control test that reproduces the conflict first, then the candidate
   fix. Write the verdict down either way. **"No, keep the reset" is a valid result.**
3. **Document the full-JAX-GPU route** as supported and *recommended for small subsets*
   of Euclid lenses, with an honest statement of when the CPU route wins (large samples,
   many CPUs available) — that trade-off is the whole point of the two routes existing.
4. **Retain example batch submission scripts for both approaches** in the pipeline repo's
   `hpc/batch_cpu` and `hpc/batch_gpu`, ported/adapted from the science tree and cleaned
   for public consumption (no personal paths, no DR1-run-specific sample names left
   dangling).

## Acceptance / gate

- Both routes run end to end on RAL for at least one lens, from the pipeline repo's own
  submission scripts.
- The reset investigation has a measured verdict recorded in the PR/issue.
- A reader can tell, from the docs alone, which route to pick for their sample size.
- Gates the 10-lens science run (PyAutoCortex `phases/euclid/dr1_prelim_10_lens_science_run`).
