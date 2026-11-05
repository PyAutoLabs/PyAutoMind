# Likelihood lifecycle phase 4e: ingest the phase-4 wall-time validation rows, publish walltime-validation@1, and lay out parity for human rulings

Type: research
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- profiling
- inference
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/59
Issued: 2026-11-05
Consequence: judge
Witness: autolens_inference main carries the phase-4 validation rows for every completed GPU and CPU leg (413924, 413966–413982, 414141–414189, 414362), excluding 414150's failed delaunay_nn rows. dashboard/walltime_validation.json gives every Optimal setup that has a row its ratio_measured_over_predicted, and the rectangular/hst numba cores sweep its parallel_efficiency curve (1/2/4/8/16/32). The 414189 rows (pin 2026.10.25.1 + PyAutoArray#677) are marked as such in the exporter's limitations. A backend-parity table at mass_total[1] (max log L per setup per likelihood) is laid out for human rulings, with no parity verdict computed. Lint and tests are green, and the Pulse lens-walltime instance refreshes after merge.
Review-minutes: 20
Unattended: never
Epic: likelihood-lifecycle
Phase: 4
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-05

## Context

- Phase 4 (epic): inference wall-time validation on RAL. Phases 4a (tooling, #51/#52/#53) and 4c (runners for all 20 likelihoods, #54/#55–#58) are closed; 4b/4d compute is in the epic ledger.
- Compute as of 2026-11-05 21:30 GMT:
  - GPU batch: all 34 legs COMPLETED, plus the A100 Delaunay legs 413924.
  - CPU batch 414141–414180: completed legs all have rows.
  - 414150 (delaunay_nn numba CPU) failed on GNU OpenMP fork. It was fixed by PyAutoArray#677 and rerun as 414189 on the pin plus that fix.
  - 414160 (multi_galaxy MGE JAX CPU) timed out and was resubmitted as 414362 (24 h).
  - 13 numba legs are still running: datacube, group delaunay/rectangular, multi_dataset, multi_galaxy delaunay/rectangular, interferometer rectangular seed 1.
- Exporter preview on the pulled rows (scratch, 241 records):
  - Pixelized A100 ratio 1.2–1.4 (interferometer sparse 2.4–2.7; multi_dataset 0.41 is odd, so check the predicted basis).
  - Cheap likelihoods (weak, point source, cluster, MGE on A100) are sampler-overhead bound at 5–10 ms/eval.
  - Cores sweep parallel efficiency is 0.68/0.62/0.55/0.36/0.28 at 2/4/8/16/32 cores. The 1-core implied cost is 601 ms/eval against 566 ms profiled.
- Exporter facts:
  - `parity_status` stays `not_assessed` unless `PARITY_RULINGS` names the run (human rulings only).
  - `ADOPTED_PIN` marks the 56 adopted 2026.10.17.1 rows.
  - The Pulse reference is `catalogue/pulse_lens_runtime_reference.json`.
- Open observation: the A100 Delaunay max log L is about 86 below the adopted numba rows from light[1] on (different pins). It belongs in the parity table, not a verdict.

## Plan sketch

1. Pull every completed leg's `results/**/validation/**` rows from the RAL checkout (`/mnt/ral/jnightin/inference/autolens_inference`) into the branch. Exclude `results/archive/2026-10-19_numba_thread_oversubscription` (not phase 4) and anything from 414150; 414189 overwrote those paths, so verify by slurm job id.
2. Exporter: mark the 414189 rows (patched-library note in the limitations, keyed by slurm job, the way `ADOPTED_PIN` marks adopted rows), then regenerate `dashboard/` (summary, catalogue, walltime_validation) and pass `--check`.
3. Backend-parity table at `mass_total[1]` across setups per likelihood (`build_readme`'s parity view, or a wiki page), handed to the human for rulings. Any ruling goes into `PARITY_RULINGS` only on the human's word.
4. Wiki: update `wiki/project/state.md` with the phase-4 findings (ratios, overhead floor, cores curve, the 6 h estimate miss on multi_galaxy MGE CPU).
5. Add the remaining legs as they complete (same branch), then PR (human /prm), then dispatch the Pulse refresh so `lens-walltime` picks up main.

## Original request (verbatim, 2026-11-05)

"Continue" (after the 21:30 phase-4 check-in; the epic's next step is the 4e ingest).
