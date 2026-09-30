# EP cortex check-in clean-up (2026-09-30) — clear the small issues, then relaunch runs

Type: maintenance
Target: PyAutoCortex
Repos:
- PyAutoCortex
- PyAutoFit
Themes:
- ep
- hpc
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: `cortex.py` census shows zero `open` runs for ic50_workspace and slope_hierarchy_scale; `projects.yaml` loads with a duplicate-key check passing (one row per key); the analytic_gaussian ledger carries astra's criterion-2 opinion as a `note`; and each of the four ledgers' `## Now` names a concrete next submission or a named blocker.
Review-minutes: 3
Unattended: needs-slicing


The 2026-09-30 Cortex check-in of the four active EP projects (ep_toy_gaussian,
analytic_gaussian, ic50_workspace, slope_hierarchy_scale) found a set of small
issues standing between us and a new wave of runs. Work through them one by
one, in this order, then stop at a go/no-go for new submissions. Every ledger
write is a `cortex.py` verb; a `result`/`lesson` entry is the human's words only.

## 1. Cortex bookkeeping

1a. **Close stale ledger runs.** These are listed `open` but their SLURM logs
    show they ended long ago (the project `hpc/sync sacct` only covers today, so
    exit codes were not confirmed from the cluster — confirm via the logs /
    a dated sacct, then record with `cortex.py done`):
    - ic50_workspace: 342408, 342409 (N=5 parity, completed), 342412 (graphical
      ladder, all rungs passed, finished 2026-09-09 22:48), 342411 (EP ladder,
      finished 2026-09-09 23:19 but **rung N=50 FAILED** → `--failed`).
    - slope_hierarchy_scale: 342348_[0-24] (one_by_one, ended 2026-09-08
      20:37), 342350_0 (joint NUTS, ended 2026-09-09 13:06), 342351_0 (EP arm,
      superseded by 342410 / 343299 — output parked as ep_dead_342351).
1b. **Refresh `## Now`** for ic50_workspace (still says the ladder is
    "submitted") and slope_hierarchy_scale (still lists the three runs as open)
    in the human's words.
1c. **De-duplicate `PyAutoCortex/projects.yaml`.** Several project rows are
    repeated up to three times (e.g. analytic_gaussian at lines 118/292/452,
    ep_toy_gaussian 132/306/466, slope_hierarchy_scale, ic50_workspace,
    autolens_inference, profiling, cowls_diana, subhalo_simulations,
    slope_hierarchy, concr). YAML keeps the last duplicate silently. Find the
    commit that introduced the repetition, keep one canonical row per key
    (diff the copies first — keep any field that differs), re-render the
    dashboard, and add a duplicate-key check so it cannot recur.
1d. Check-in could not push because the Cortex checkout had an unrelated
    uncommitted edit to `projects/euclid_dr1.md` — find its owner session and
    get it committed or discarded (do not discard blind), then run
    `pyauto-brain cortex checkin --apply`.

## 2. ep_toy_gaussian — prepare wave 2 (collapse question at N=50 unanswered)

- Wave 1 failed on infrastructure only: NUTS 342639 OOM at the 8 GB SBATCH cap
  in window adaptation; EP x3 342640_[0-2] EMFILE (fixed by PyAutoFit#1632/#1634,
  RAL mirror a73684012 contains both).
- Raise the NUTS SBATCH memory above 8 GB (size it from the N=50 model).
- Re-verify the RAL PyAutoFit mirror still contains #1632/#1634 and dependency
  floors (see RAL dep-floor lesson: diff pip freeze vs floors).
- Choose a NEW sample name (e.g. `n50_seed42_w2`) — never rerun into an
  existing sample directory.
- Ready to submit; submission itself waits for the human go.

## 3. analytic_gaussian — settle criterion 2 before any rerun

- Open question (planned, never run): is criterion 2's mu threshold wrong, or
  is the minimal-EP control wrong? Task archive:
  `archive/tasks/analytic_gaussian/minimal_ep_legb_mu_threshold.md`.
- Wave 1 baseline (342413, 200 seeds N=5): EP exact on Gaussian leg, leg B
  sigma misses as pre-registered 78/200, collapse 0/200, witness 7 met / 4 miss.
- **Ask astra (Codex GPT-6-astra) for an independent opinion** on the question:
  hand it the pre-registered criteria, the wave-1 aggregate (analytic_gaussian
  b44390d), and the minimal-EP control code; ask whether the threshold, the
  control, or neither is at fault and why. Record its answer verbatim as a
  `note` and bring it to the human — the human rules, not astra.
- Then run the planned check if the human agrees, and only then decide whether
  the N=25 rung (written, not submitted) goes out.

## 4. ic50_workspace — the EP N=50 rung failure

- 342411 rung N=50 failed with `AssertionError: assert np.isfinite(suff_stats).all()`
  in `autofit/messages/abstract.py` `project` (see
  `hpc/batch_cpu/error/error.342411.err`). Rungs 5/10/25 completed; graphical
  ladder (342412) passed all rungs including N=50.
- Diagnose: which factor/message produced non-finite sufficient statistics,
  and whether the RAL mirror at the time predated a relevant fix. If it is a
  library bug, file it through /intake (bug, autofit) rather than fixing inline.
- Then decide the next ladder: rerun N=50 (fixed/current mirror) and/or try the
  `ep_lbfgs_jax` scale lever; report EP cost and hill_coef width vs N from the
  completed rungs.

## 5. slope_hierarchy_scale — the moment-matching gate

- 343299 showed the hierarchical factor never updates under the Laplace
  projection (0/50 SUCCESS: 27 BAD_PROJECTION + 23 FAILURE); parent = prior.
- Human decision needed: go/no-go on
  `draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md`. Surface
  its current size and status; do not start it inside this task.
- Record the per-lens (342348) and joint NUTS (342350_0) outcomes that were
  never logged, so the graphical baseline for the EP comparison is on file.

## Done when

Every stale run is closed, every `## Now` is current, projects.yaml has one row
per key with a guard, and each project has a concrete, human-approvable next
submission (or a named blocker). New runs themselves are the follow-up.

<!-- formalised by the Intake (Conception) Agent on 2026-09-30 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/50609e83-4b82-4c6e-bdb9-2bf59891e997/scratchpad/ep_checkin_cleanup.md -->
