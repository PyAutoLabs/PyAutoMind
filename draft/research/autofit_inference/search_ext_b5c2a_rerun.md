# `@autofit_inference` B5c-2a-rerun: re-pilot the 80 Emcee/Zeus rows lost to the harness bug…

Type: research
Target: autofit_inference
Repos:
- autofit_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: medium
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md
Status: formalised
Consequence: judge
Witness: the 8 cells each have 10 valid attempts per backend accounted for; `results/calibration/correlated_nd_wave1.json` carries their timeouts from real walls; the probe-first set shrinks accordingly; no scored run exists; B5c-2b (`draft/research/autofit_inference/search_ext_b5c2b_scored_wave_submit.md`) is updated to depend on this task.
Review-minutes: 25
Unattended: needs-slicing

Why: in the `correlated_nd` pilot (RAL 410866) all 80 Emcee and Zeus rows on `corr_gaussian_d20` and `rosenbrock_d20` (2 searches × 2 datasets × 2 backends × 10 seeds) failed because of a harness bug in this repo — chain diagnostics were relabelled by `g0.centre` after the search finished. The bug is fixed in autofit_inference#18, but those 8 cells have no valid pilot evidence: A2 marks them provisionally probe-first and their timeouts/bands rest on no rows. Human ruling 2026-10-16: rerun them cleanly before the scored wave rather than carry the gap.

Shape:
1. Build a manifest of exactly those 80 runs from `hpc/batch_cpu/correlated_nd/pilot.tsv` (same seeds, same cells) and submit them on RAL `--partition=ral` ONLY from the PRIVATE copy `/mnt/ral/jnightin/inference/autofit_inference_b5c` at the pilot pin df6d218f10cd (PyAutoNerves 7f3055b7), with the fixed harness delivered to the private copy (sha256-verified), 8 G, the 4 h process cap; never the shared mirror, never touching another campaign's jobs. Cortex `## Runs` line with the job id.
2. Pull `results/` only; the rerun rows replace the 80 failed attempts in the accounting (record the replacement explicitly: the failed rows stay in history as `harness-bug`, a new attempt class or a reason field — decide-and-flag).
3. Judge under `correlated_nd@1`; recalibrate those 8 cells' timeouts and, if any band would move under the §7 ≥ 20-row rule, write amendment A3 (bands may move only by the §7 rules; frozen `@2` values change only via A3 and before any scored row). Remove the provisional probe-first flag where evidence now exists; rebuild catalogue/README/accounting/rates.
4. Cortex Log entry (newest-first) + Insight pilot row + campaign next → B5c-2b.

Witness: the 8 cells each have 10 valid attempts per backend accounted for; `results/calibration/correlated_nd_wave1.json` carries their timeouts from real walls; the probe-first set shrinks accordingly; no scored run exists; B5c-2b (`draft/research/autofit_inference/search_ext_b5c2b_scored_wave_submit.md`) is updated to depend on this task.

Review-minutes: 25
Unattended: needs-slicing

<!-- formalised by the Intake (Conception) Agent on 2026-10-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/525f7109-4545-4825-9b1b-2bdb3d87fac1/scratchpad/intake_b.md -->
