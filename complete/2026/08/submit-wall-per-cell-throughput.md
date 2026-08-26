## submit-wall-per-cell-throughput
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/176
- completed: 2026-08-26
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/179 (merge commit b4b30ee0, commit 7b2d716)
- summary: |
    An MGE step rate can no longer be quoted as the basis for a pixelized cell's
    wall clock. `submit_phase8b_bijector_a100` had set --time=0:30:00 and justified
    it in its own header with an MGE rate, for an array of 20 delaunay_adapt_split
    arms, 15 knn arms and 4 mge controls; RAL job 340576 was killed at ~12% of
    budget on 35 of its 39 arms, losing an overnight A100 block. The 4 that
    finished were the mge controls -- the only cells the citation described.

    LANDED (56 files, +1594):
    - scripts/misc/wall/rates.py -- curated per-cell step-rate table mirroring
      vram/config.py. Keyed (dataset, cell, instrument, device, precision,
      n_lanes, batch_size); batch_size is IN THE KEY because unbatched lane rows
      and batch_size=4 pixelized rows are different configurations of one cell.
      step_rate_for() RAISES UnmeasuredCellError -- no nearest-neighbour
      fallback, because that fallback IS the defect. Seeded with the three rates
      recovered from 340576's truncated arms (mge 0.117, knn 2.23 = 19x,
      delaunay_adapt_split 4.83 = 41x, at 16 lanes / batch_size=4 / A100 fp64)
      plus the three already-measured MGE lane rows (0.05@16, 0.19@64, 0.77@256,
      unbatched).
    - scripts/misc/wall/check_submits.py -- requires ONE `# WALL-BASIS:` row per
      cell a submit actually RUNS. Cells are read from the real
      python3 scripts/.../<cell>.py invocation, resolving ${CELLS[$I]} arrays,
      case arms and variable indirection, and ignoring commands merely MENTIONED
      in comments. Also checks a declared cell is one the submit runs, that
      `source: rates` matches the table within 5%, and that --time clears
      headroom x the SLOWEST row.
    - 48 submits retrofitted; submit_phase8b_bijector_a100 --time 0:30:00 ->
      7:00:00, set by the delaunay row.
    - Wired into .github/workflows/lint.yml; contract stated in hpc/README.md and
      scripts/misc/wall/README.md; loss written up in
      results/notes/inference/phase_08_regularization/wall_clock_340576.md.
    - test_wall_check_submits.py (23 tests) reconstructs the submit exactly as it
      went out and asserts the checker refuses it.

    DECISIONS worth keeping:
    - Three headroom floors by evidence quality: rates 1.5x, measured-wall 1.25x,
      unmeasured 3x. The 1.25x floor exists because
      submit_search_nss_imaging_delaunay_a100_hst_fp64_mainline runs a measured
      29,720 s under a 12 h budget = 1.45x, which a flat 1.5x would have failed
      on a submit that has run fine.
    - `unmeasured` stays LEGAL and needs no wall estimate. Requiring one would
      have meant inventing ~40 numbers to satisfy the linter -- inventing numbers
      is the disease. The row's value is the per-cell admission that this cell's
      wall clock rests on nothing.
    - Required by PATH PREDICATE (submit_search_* / submit_phase8b_*), never an
      allowlist: an exemption list would hide the very leak class this closes.
    - The n128 MGE tier is deliberately ABSENT from the table -- its ~0.38 s/step
      is interpolated, not measured. That submit declares measured-wall instead.
    - --time is 7:00:00, not the 6:00:00 in the approved plan: the plan used 1.4x,
      the gate's floor for a rates row is 1.5x = 22,185 s, past six hours.

    SCOPE LIMITS (open, deliberate):
    - 34 submits carry NO wall basis -- submit_runtime_* / submit_breakdown_* /
      probe submits run a single cell and cannot mis-cite across cells. Gap: if
      one ever grows a second cell it inherits the requirement only if renamed
      into the searches family.
    - The table has 6 rows. Every pixelized cell other than knn and
      delaunay_adapt_split, and every non-hst instrument, is `unmeasured` today.
    - hpc/batch_cpu is scanned but nothing there is required to carry a header.

    PROCESS: sibling of #175 from the same 340576 post-mortem. autolens_profiling
    was claimed by #175 mid-session after this task's branch survey read clean;
    human-approved fold into its worktree, then #175 re-branched off origin/main
    and shipped independently in PR #178. Branch and worktree were renamed off the
    #175 name before shipping -- worktree_remove derives its path from the TASK
    NAME, so the mismatch would have stranded this close-out. Heart was RED at
    ship time on two reasons unrelated to this repo (autogalaxy_workspace_test
    smoke on main; release validation stage integrate); push + PR-open were
    human-authorized against those exact strings, merge was not, and merge waited
    for this /prm.

## Original prompt

# Submit scripts quote an MGE step rate for pixelized cells and get…

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Filed: 2026-08-26
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/176 (issued 2026-08-26)
Issued: 2026-08-26
Worktree: ~/Code/PyAutoLabs-wt/log-det-multistart-tag (SOLELY this task's since 2026-08-26 —
  log-det-multistart-tag #175 shipped in PR #178 and moved off; nothing else is uncommitted there)

# Submit scripts quote an MGE step rate for pixelized cells and get killed

`autolens_profiling/hpc/batch_gpu/submit_phase8b_bijector_a100` set
`--time=0:30:00`, justified in its own comment as "16 starts x 3000 steps at
the #117-validated pixelized throughput is ~5 min including compile per task
(matches the diagnostic_theta_e submit's citation); --time below gives it 6x
headroom."

That citation is an MGE-cell throughput and does not transfer. Measured on
RAL 2026-08-25:

  mge                  0.117 s/step   (3000 steps ~ 350 s)  — matches the citation
  knn                  2.23  s/step   (3000 steps ~ 1.9 h)  — 19x
  delaunay_adapt_split 4.83  s/step   (3000 steps ~ 4.0 h)  — 41x

So the "6x headroom" was ~8x short for knn and ~16x short for delaunay. 35 of
39 arms in job 340576 were killed at roughly 12% of budget, losing an entire
overnight A100 block. Only the 4 mge control arms — the ones the citation
actually described — completed.

FIX: a per-cell throughput reference that submit scripts must cite, and/or a
guard, so an MGE step rate can never be quoted as the basis for a pixelized
cell's wall clock. The numbers above are the first measured rows.

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cc3c117a-bb7b-499c-aa8c-f3e8f65d1bb5/scratchpad/prompts/p3.md -->
