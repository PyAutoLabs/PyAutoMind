## interferometer-decision-matrix-last-cell
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/369
- completed: 2026-10-04
- epic: interferometer-likelihood-campaign
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/372
- autolens_profiling#372 merged 2026-10-04T20:40Z (head 93a002a9, merge 3a7e633f) via human /prm (Heart RED development override). It fills the last decision-matrix cell, CPU rect 39² alma_high r5.0 (RAL 375978_3), and flips the campaign to phase-4-shipped. Result: numba 75,321 ms, FFT 17,649 ms, gate → FFT, 89× slower than the A100.
- Decision: CPU vs A100 = 1.59e-3 nats, which misses the ≤ 1e-3 bar. The human accepted it on 2026-10-04: it follows the alma_high r3.5 precedent (1.5e-3), the cause is solver/revision, and it is 310× inside the 0.5-nat bar. The miss is recorded in the note. Open fact: the A100 `solver_ab` gives certified == PDIP to 0.0, so the gap may sit in F/D on the older revisions. A post-#595 A100 re-run would settle it; it was not run.
- Wiki: PyAutoArray#582 now reads released in 2026.9.27.2. This is tag-verified; the earlier "2026.10.2.1" came from a lexicographic tag sort.
- Validation: all autolens_profiling lints passed, and pytest gave 1018 passed.
- Post-merge: RAL cleanup of `/mnt/ral/jnightin/autolens_profiling_wt/interferometer-decision-matrix` and `/mnt/ral/jnightin/PyAuto_branch/interferometer-decision-matrix` was done in the /prm close-out, after squeue showed no job from those paths (see close-out report).

## Original prompt

# Interferometer decision matrix: commit the last cell (CPU rect 39² alma_high r5.0) and flip the wiki row to shipped

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- numba-cpu
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: judge
Epic: interferometer-likelihood-campaign
Issued: 2026-10-04

Contract: the PyAutoPulse task `organs/PyAutoPulse/tasks/interferometer_decision_matrix_last_cell.md`
(https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/interferometer_decision_matrix_last_cell.md;
original text after its `---`). This prompt files steps 1-5 of it.

## Human decision (2026-10-04, in-session)

The original request, verbatim: "do the proposed priority order stuff, all of it". The decision
recorded with it: **accept** the CPU-vs-A100 gap of about 1.6e-3 nat. The task's witness bar is ≤ 1e-3 nat.
- Precedent: the r3.5 rect alma_high cell already on main misses by 1.5e-3 nat.
- Cause: the A100 row ran PDIP on revisions from before PyAutoArray#595. The CPU row ran fnnls. This is a
  solver mismatch, not a precision problem.
- The gap is recorded verbatim in the note.
- Consequence is raised from glance to judge because the witness bar is amended by a human
  decision. The PR is left for a human /prm.

## Scope

1. Copy `alma_high/pixelization_numba_hpc_ral_cpu_fp64_r5.0.{json,png}` from the RAL worktree into a task
   worktree off main. Job 375978_3 COMPLETED with wall time 01:11:36.
2. Verify:
   - `inversion_path` is InversionInterferometerSparseNumba;
   - numba vs FFT agree to ≤ 0.5 nat;
   - `source_revisions` match the note.
3. Fill the note:
   - the row, the status line and the blocked-cells table;
   - a recheck of rule 4's range;
   - the RAL jobs line.
4. Wiki updates:
   - flip the `wiki/index.md` interferometer row to shipped;
   - update the campaign page's phase-4 text;
   - fix the stale "PyAutoArray#582 UNRELEASED" wording (it was released in 2026.10.2.1).
5. Regenerate the READMEs and dashboard, run lint, and open the PR.

RAL cleanup (Pulse step 6) is post-merge and stays out of scope here.
