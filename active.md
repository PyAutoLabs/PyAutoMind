# Active Tasks

## witness-campaign
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/398
- issued: 2026-09-10
- prompt: active/witness_campaign.md
- session: claude --resume session_018ip88yepHJjM1VjjFMMmuP
- status: library-dev
- location: web-github (session clones, no task worktree; branch claude/witness-campaign-feature-h21cq4)
- worktree: n/a — web-github session clone (/home/user/PyAutoMind)
- repos:
  - PyAutoMind: claude/witness-campaign-feature-h21cq4
- summary: |
    Campaign, not a one-shot: ~6 passes of ~15 prompts over the 89 unwitnessed
    `Unattended: ready` drafts. Each pass proposes candidate witnesses for the
    human to accept/edit/strike, then writes three header fields per accepted
    prompt — `Witness:`, `Consequence:`, `Review-minutes:`. The three-field
    rewrite is load-bearing: 74 of the 89 already declare `Consequence: judge`
    (a cached derivation from intake's hygiene set), and the precedence rule
    lets that stale value beat the witness, so a witness written alone moves
    nothing. Baseline 2026-09-10, derived over the 110 ready prompts:
    5 notify / 12 glance / 93 judge; fully witnessed the same set grades
    28 notify / 74 glance / 8 judge.
    Pass 1 (`workspaces`, 15) SHIPPED 2026-09-10: 15 judge -> 7 notify /
    8 glance / 0 judge, 300 seed review-minutes -> 24. Backlog now 109 ready,
    36 witnessed, derived 12 notify / 19 glance / 78 judge.
    Next: `autoarray` (10), then autolens (9), autofit (8),
    autolens_workspace (6), autolens_profiling (5), tail pass (~26 singletons).
    Pass-by-pass counts are in the prompt's `## Campaign log`.

## sed-chain-cpu-route
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/69
- issued: 2026-09-11
- prompt: active/sed_chain_cpu_route_jax_cpu_backend.md
- session: claude --resume session_01AELxUSfSPRz2SDnnVJHohi
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/sed-chain-cpu-route
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sed-chain-cpu-route
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/70
- note: worktree_check_conflict flagged euclid_strong_lens_modeling_pipeline as claimed by remove-fits-dataset-plots-yaml, whose PR #63 merged and issue #62 closed on 2026-09-10 without a close-out. Stale claim, waived on the human's plan approval; the file sets are disjoint (hpc/ submit scripts and README here, config/visualize/plots.yaml there) and this task runs in a fresh parallel worktree.
- summary: |
    The SED chain (Sersic VIS + per-band waveband fits) gets a CPU submit script,
    hpc/batch_cpu/submit_sersic_waveband, which pins JAX to the CPU backend exactly as
    stage 1 of submit_initial_lens_model_two_stage does for vis_lp (no --use_cpu: both SED
    analyses are use_jax=True and --use_cpu would flip them to Numba). It becomes the
    documented default; the GPU script stays as the optional route. README route table,
    hpc/sync comments and usage text, the sersic_lens_model.py batch_size docstring and the
    PyAutoCortex "Where to look" line are repointed. GPU job 342648 is untouched.

## sersic-variants
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/74
- issued: 2026-09-12
- prompt: active/sersic_variants_prior_edge.md
- session: claude --resume session_01KTGhZacWuxrxYkXXWXJbBx
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/sersic-variants
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sersic-variants
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/75
- note: "worktree_check_conflict sersic-variants euclid_strong_lens_modeling_pipeline exits 1 on two claims. remove-fits-dataset-plots-yaml is stale (PR #63 merged, issue #62 closed 2026-09-10, no close-out). sed-chain-cpu-route is LIVE (PR #70 open) and its file set genuinely overlaps: hpc/README.md route table (both add rows to the same table — a one-line resolution expected on whichever merges second) and scripts/sersic_lens_model.py (its only hunk there is a two-line batch_size docstring edit at ~250, clear of the model block extracted here). Waived on the human's plan approval, in a fresh parallel worktree — the same call sed-chain-cpu-route itself recorded against remove-fits-dataset-plots-yaml."
- summary: |
    --variant for the Sersic stage: four variants (baseline, wide_n,
    central_noise, sersic_point) on the same 100 euclid_sersics core lenses, to
    explain the lens-light Sersic index pile-up at the n = 5 prior edge. The
    inline model block in fit_sersic is extracted into a pure sersic_model_from
    helper; variant=None stays byte-for-byte today's behaviour and any other
    variant writes to unique_tag sersic_lens_model_<variant>. util gains a pure
    Gaussian noise-inflation helper (A = 9, sigma = 0.17") plus a keyword-only
    noise_inflation on load_vis_dataset, and parse_fit_args(with_variant=True).
    New hpc/batch_cpu/submit_sersic_variants runs the four variants sequentially
    inside one array task per lens, because all four restore the same vis_lp zip
    and PyAutoFit's restore() deletes it. Science-clone submit and the analysis
    script (PR 2) are follow-ups.

## sersic-variants-analysis
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/76
- issued: 2026-09-12
- prompt: active/sersic_variants_analysis.md
- session: claude --resume session_01KTGhZacWuxrxYkXXWXJbBx
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/sersic-variants-analysis
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/sersic-variants-analysis
- note: "worktree_check_conflict sersic-variants-analysis euclid_strong_lens_modeling_pipeline exits 1 on three claims. remove-fits-dataset-plots-yaml is stale (PR #63 merged, issue #62 closed 2026-09-10, no close-out). sed-chain-cpu-route (PR #70) and sersic-variants (PR #75) are live, but neither file set intersects this one: this task adds only scripts/analysis/** (new tree), tests/test_sersic_variants_analysis.py (new) and one line in config/build/no_run.yaml, which neither touches. Its documentation deliberately goes in a new scripts/analysis/README.md rather than scripts/README.md or catalogue/README.md, which belong to PR #75's diff. Waived on the human's plan approval, in a fresh parallel worktree based on origin/main - the same call sed-chain-cpu-route itself recorded against remove-fits-dataset-plots-yaml."
- summary: |
    PR 2 of the euclid_sersics variants work: scripts/analysis/sersic_variants.py
    reads the four lens_sersic_<variant>.csv scrapes that PR #75's --variant
    produces and emits the per-variant comparison production needs - N, median n,
    fractions above 4.5/4.9/9.5 (and 5.0 for wide_n), paired dn and dR_eff against
    baseline with 16-84 % bands, June-vs-baseline dn from sample/lens_map.csv, and
    the four witness readings W1-W4 printed as numbers beside their pre-registered
    thresholds, never as a verdict word. Four-panel shared-bin histogram PNG plus a
    markdown report. Pure functions split from the CLI; a synthetic four-CSV
    fixture with a variant missing two tiles pins the inner join and its reporting.

## simulator-from-result-linear
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/77
- issued: 2026-09-13
- prompt: active/simulator_from_result_linear_intensities.md
- session: claude --resume session_01EehLEWoRRsmnLys4aHj5W4
- status: blocked
- worktree: ~/Code/PyAutoLabs-wt/simulator-from-result-linear
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/simulator-from-result-linear
- note: "worktree_check_conflict simulator-from-result-linear euclid_strong_lens_modeling_pipeline exits 1 on three claims (sed-chain-cpu-route PR #70, sersic-variants PR #75, sersic-variants-analysis #76). No file set intersects this one: this task touches scripts/simulator.py (none of the three edits it), tests/test_simulator_from_result.py (new) and the --from-result bullet of scripts/README.md at ~line 63 — PR #75's only scripts/README.md hunk is four lines at ~line 22 in the fitting-scripts list, a different hunk that merges cleanly. Waived in a fresh parallel worktree based on origin/main, the same call sed-chain-cpu-route recorded against remove-fits-dataset-plots-yaml and sersic-variants-analysis recorded against both live tasks."
- parked: "2026-09-13. The fix is COMPLETE and pushed: feature/simulator-from-result-linear @ 85f6dfd6bf33b9f19418abbe42afb9f90fd96a21. Ship parked at the autonomous-ship gate leg 4 — pyauto-heart readiness is RED, reason verbatim 'release validation FAILED (stage integrate)'. AUTONOMY.md: Heart RED forbids PR-open at every autonomy level, and the corrective-PR exception never fires under --auto (and would not apply — that RED is organism-scope release validation, nothing in this branch is in the release chain). Legs 1-3 PASS: tests 128 fast + 6 slow, smoke 9/9, review CLEAN with the lifted claim basis-cited. Witness met: mock VIS peak/median-RMS 72.3 vs 81.1 real on tile Tile102008855RA0680593469007DECNEG0634007351862, truth.json lens intensity 0.008437 / source 8.180 (3.9 before the fix). Unblock = a human running /ship_workspace once Heart is green, or explicitly authorising the PR. The branch is usable as-is by the science clone meanwhile. Evidence on the issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/77#issuecomment-5653294402"
- autonomy: "--auto launch; effective level = min(prompt safe, bug cap supervised) = supervised, so the ship checkpoint resolves to decide-and-flag (AUTONOMY.md, extended 2026-09-07). Plan approval of record is the human's launch instruction 'im going out so autonomously get these sersic things simulated and their vis_lp runs going'; both plan levels written to issue #77. Ends at PR-open."
- summary: |
    simulator.py --from-result rebuilt the tracer from files/model.json plus the
    max-log-likelihood vector, but every profile this pipeline fits is linear
    (al.lp_linear.*), so the rebuilt profiles carry no intensity and the mock is
    noise (tile 0 of dr1_sep1_sersics: mock VIS peak SNR 3.9 vs 81 real). The
    solved-intensity tracer is already on disk as files/tracer.json, written by
    AnalysisDataset.save_results from fit.model_obj_linear_light_profiles_to_light_profiles.
    Read that instead, under the same resolve_files_path hash, guard that no
    lp_linear profile survives, and add tests/test_simulator_from_result.py —
    --from-result had no test at all.
## howtofit-mode
- issue: https://github.com/PyAutoLabs/autofit_assistant/issues/42
- issued: 2026-09-14
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtofit-mode
- repos:
  - HowToFit: feature/howtofit-mode
  - autofit_workspace: feature/howtofit-mode
  - PyAutoFit: feature/howtofit-mode
- released-repo: autofit_assistant — PR #43 merged; issue #42 closed; remaining repo claims retained.
- prompt: active/howtofit_mode.md
- summary: Assistant implementation ready and reviewed; approved README prompt propagation to HowToFit, autofit_workspace and PyAutoFit in progress. Shipping held by Heart YELLOW pending human acknowledgement.
- ship-hold: |
    Workspace validation: 3 failures (cloud#34824535982).
    Manifest drift: organism-map 2; public front-door 2.
    Profiling drift: three matrix_free SLQ fp64 results — delaunay_hpc_a100,
    delaunay_nn_hpc_a100, rectangular_hpc_a100.
- next: Acknowledge these Heart YELLOW reasons before ship_workspace; source remains local and uncommitted.
- parallel-claim: |
    RESOLVED 2026-09-14: the parallel task `howtofit-tutorial-4-6-feedback`
    (HowToFit#61 / PR#62) merged and closed out, so HowToFit is no longer shared
    and this claim stands alone again. Kept as a record of a deliberate,
    human-approved override of the conflict guard, not drift. Evidence at the
    time: this task's `feature/howtofit-mode` had 0 commits of its own and 0
    changed files against origin/main (9 behind, working tree clean) — the
    HowToFit claim was registered but never used. File sets were disjoint:
    howtofit-mode is README/AGENTS assistant-prompt propagation; the other task
    touched scripts/, notebooks/ and markdown/ under chapter_1_introduction only.
    NOTE: `feature/howtofit-mode` is now 9+ commits behind origin/main and the
    merged tutorial work landed there — rebase before editing HowToFit here.

## fixed-light-numba-phase1
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/263
- status: workspace-dev
- prompt: active/fixed_light_numba_phase1_whole_call.md
- epic: fixed-lens-light-numba-cpu
- phase: 1
- started: 2026-09-14
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-numba-phase1
- repos:
  - autolens_profiling: feature/fixed-light-numba-phase1
- plan: |
    Phase 1 of the numba CPU campaign, and the first phase of it to be issued. Measure the
    whole AnalysisImaging.log_likelihood_function on PyAutoArray's numba path - the
    production CPU route the completed GPU epic never touched - and produce a decomposition
    of where that call goes, measured in ONE process rather than attributed across two.
    Three new files, zero library edits: call_accounting.py (an access-counting harness that
    wraps ~35 library descriptors for one instrumented pass and reports inclusive time,
    exclusive time and n_calls per site), fixed_light_system.py (the jax-free half of
    active_set_steps.py, extracted so a numba cell can build the S3 system without dragging
    JAX into the process), and the cell fixed_light_numba.py (routes a/b/c x {dense,
    numba-sparse} = six rows). Gates: a three-layer sparse-operator parity pin, a coverage
    contract (unattributed/call <= 5 %), an instrumentation-overhead ceiling of 1.03.
    Three legs on the 8-core laptop: smoke (N=484), t1, t8.
- scope-decisions: |
    Two, taken with the human before planning. (1) The campaign map's original phase 0
    (numba kernel measurement) is FOLDED into this phase - GPU phase 2 already measured the
    CPU kernel rows and concluded a CPU assessment "should score the library's fnnls path,
    not the certified active set", so a kernel phase would re-answer a settled question.
    (2) S3 is measured on dense numpy AND on a re-baked numba-sparse dataset with a parity
    pin - the S3 subtraction rebuilds the dataset and drops the sparse operator, so without
    the re-bake this leg would measure a path nobody runs. The campaign map was amended in
    the same breath: five phases, not six, and phase 3 repurposed from certified pass
    budgets to the fnnls memo warm start.
- design-finding: |
    The re-bake is PROVABLY identity-preserving, which turns the one genuinely risky part of
    this phase into a cheap assert. The JAX sparse class reads a weight map baked at
    apply_sparse_operator time (PyAutoArray .../imaging/sparse.py:64) - which is what made
    re-baking look dangerous - but the NUMBA class does not: it recomputes psf_weighted_data
    from the live data every evaluation (.../imaging_numba/sparse.py:94-101), and
    SparseLinAlgImagingNumba is built purely from noise_map.native, psf.kernel.native and the
    mask (dataset.py:652-716), none of which the subtraction touches.
- trap: |
    Inversion.curvature_reg_matrix is a PLAIN @property (abstract.py:358-370) that rebuilds
    an (n,n) sum on every access, and it is accessed >= 3x per call (:613/:647, :397); under
    edge zeroing two of those add a further full fancy-index copy. The existing numba
    decomposition (delaunay_numba.py:596-672) is a sequential-touch walk and therefore
    silently loads those rebuilds into its "solve" and "log det" rows - anyone reading them
    today is over-attributing to the solver. That is why this phase counts accesses instead,
    and why a test asserts n_calls >= 2 so a future PyAutoArray fix fails loudly.
- note: started 2026-09-14; plan approved by the human before any edit. Conflict guard clean (worktree_check_conflict fixed-light-numba-phase1 autolens_profiling, exit 0).
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/264 (MERGED 2026-09-15, main 9285683)
- status-detail: |
    IN FLIGHT, mechanism merged, MEASUREMENT OUTSTANDING. PR #264 merged with lint green on
    every run and leg and the branch proved an ancestor of main. The issue was deliberately
    NOT closed and the prompt deliberately NOT moved to complete/: phase 1's deliverable is a
    measurement, and recording a research phase complete having produced no numbers would
    corrupt the ledger. Outstanding: leg 1 (t1), leg 2 (t8), and the verdict note
    results/notes/fixed_lens_light_numba_2026_09.md. Both land as a FOLLOW-UP PR; /prm then
    closes the task out properly.
    The worktree ~/Code/PyAutoLabs-wt/fixed-light-numba-phase1 and its branch are KEPT ON
    PURPOSE - worktree_remove would refuse anyway while active.md claims the task, which is
    the correct behaviour here. Resuming needs no start_dev, just the two run commands on an
    idle machine.
- note: |
    PR #264 opened 2026-09-15 with the MECHANISM AND ITS GATES; the timing legs are
    deliberately NOT in it. call_accounting.py (407), fixed_light_system.py (491), the cell
    fixed_light_numba.py (2081), 42 new tests; full scripts/misc/test/ suite 440 passed and
    test_active_set_steps.py 22/22 UNCHANGED (the gate proving the extraction moved no pin
    across the five shipped GPU phases); ruff clean.
    Smoke leg gates all PASS on real HST data: P1 re-baked operator 3/3 arrays bitwise
    identical, P2 D 1.31e-15 / F(mapper) 3.39e-15 at rtol 1e-9, P3 2.18e-11 nats with ZERO
    passive-set differences, S3==S0 mapper-block log-dets rel 0.0. COVERAGE - the phase's
    contract - is 0.08-0.36 % unattributed on every row against a <= 5 % requirement.
    Indicative magnitudes only (smoke, N=484, wiring not measurement): sparse-numba is ~4.4x
    dense on S0 (452 vs 1981 ms) and S0->S3 is ~1.66x on the sparse-numba path (452 -> 272 ms)
    against 1.31x on the A100. Route c costs +12.889 nats with 2 negative entries, the same
    order as the GPU epic's +8.4 at N=500 HST - an independent corroboration on a different
    backend.
- deferred: |
    LEGS 1 (t1) AND 2 (t8) NOT RUN - they ARE the measurement and the laptop was
    oversubscribed (load average 8.41 on 8 cores, another session running a 4-way parallel
    suite, two other claude sessions live). Leg 2 is the thread-scaling comparison, which
    oversubscription makes actively misleading rather than merely noisy. Human decision
    2026-09-15: land the code, run the legs on an idle machine. They land as a follow-up
    commit on the SAME branch plus the verdict note
    results/notes/fixed_lens_light_numba_2026_09.md; the worktree and branch stay in place, so
    no start_dev is needed to resume - just run the two commands when the machine is quiet.
    The committed artifact is the smoke leg, stamped timing_status: wiring_only_not_measured
    with peak load recorded, carrying no pins (pinned_drift empty) so it enters no drift
    surface.
- methodology: |
    A sequential clean-vs-instrumented overhead ratio is DRIFT-DOMINATED on this hardware:
    0.71/0.98/1.10/1.11/1.24/1.37 across rows, including instrumented apparently FASTER than
    clean - physically impossible as an overhead, and the tell that the estimator was broken
    rather than the instrumentation. Replaced with a steady-state warm-up plus an ABBA
    COUNTERBALANCED estimator, which cancels linear drift: instrumentation costs ~0.8 % (mean
    1.0085, median 1.0071). The 1.03 gate threshold was NOT loosened - the estimator was
    replaced. A 2.9x decaying sequence in one early run did not reproduce (15 consecutive
    clean calls flat, first/last 0.942, +-15 % scatter): queueing, not warm-up, now pinned by
    a test so nobody re-derives it as a ramp.
- spawned: |
    PyAutoArray bug filed from this work - draft/bug/autoarray/curvature_reg_matrix_rebuilt_every_access.md:
    curvature_reg_matrix is a plain @property rebuilding an (n,n) sum on EVERY access, reached
    >= 3x per evaluation, and its docstring's stated reason for not caching describes an
    in-place implementation the code no longer has. HANDSHAKE: this phase's test asserts
    n_calls >= 2 on that property, so if the fix lands a cache that test is MEANT to fail,
    forcing the decomposition to be updated deliberately rather than shifting underneath a
    published number.
- scope-addition: |
    likelihood_breakdown/__init__.py made lazy (PEP 562), beyond the approved plan and flagged
    in the PR body: it eagerly imported `timing`, which imports jax at module level, so ANY
    likelihood_breakdown.* import pulled JAX into the process and the cell's no-jax guarantee
    was unreachable. Every consumer imports submodules; the 440-test suite covers it.

## experimental-colab
- issue: https://github.com/PyAutoLabs/autofit_assistant/issues/44
- issued: 2026-09-15
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/experimental-colab
- repos:
  - autofit_assistant: feature/experimental-colab
- prompt: active/experimental-colab.md
- summary: Experimental Colab notebook and README implementation prepared; isolated installation and full Gaussian validation in progress.
- ship-hold: |
    Heart RED: PyAutoFit: 1 commit(s) behind origin
    PyAutoGalaxy: 1 commit(s) behind origin
    PyAutoLens: 1 commit(s) behind origin
    Stale: release validation incomplete: no rehearsal for current source
