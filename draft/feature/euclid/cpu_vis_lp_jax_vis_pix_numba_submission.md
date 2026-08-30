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
Phase: 3
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28

Phase 3 of 10 in the Euclid DR1 preparation epic. **Gate: phase 1.** Can overlap phase 2.
**Gates phase 4** — the 10-lens science run uses this CPU route.

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
- Gates phase 4.
