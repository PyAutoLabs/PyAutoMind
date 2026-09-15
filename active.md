# Active Tasks

## colab-notebook-release-gate
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/227
- issued: 2026-09-15
- prompt: active/colab_notebook_release_gate.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/colab-notebook-release-gate
- repos:
- summary: |
    Make Heart check F a faithful Colab gate. Today it emulates Colab with
    `pip install autolens jax` WITH deps, so its venv already holds every
    dependency the real --no-deps bootstrap would miss (corner, 2026-09-15).
    New heart/checks/colab_gate.py seeds the sim venv from Google's published
    Colab manifest (googlecolab/backend-info pip-freeze.txt), runs the injected
    setup cell verbatim, walks declared requirements, AST-scans the installed
    libraries for every third-party import (guarded or not) and imports each;
    unguarded miss -> FAIL -> readiness RED. Rung 2 of the prompt's ladder
    (~5 min, release-only verify_install_release lane); rungs 3/4 declined.
    PyAutoHeart only: Nerves + HowTo repos need no edit and are claimed by
    colab-bootstrap-lazy-deps / colab-workshop-dep-stopgap / howtofit-mode.
    EXPECT: first release-integrate after merge is RED until the autonerves
    carrying PyAutoNerves#167 is on PyPI - the gate working, not a regression.

## blackjax-reqs-stopgap-revert
- issue: https://github.com/PyAutoLabs/HowToFit/issues/65
- issued: 2026-09-15
- prompt: active/tutorials_6_7_blackjax_never_installed.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/blackjax-reqs-stopgap-revert
- repos:
  - HowToFit: feature/blackjax-reqs-stopgap-revert
  - HowToGalaxy: feature/blackjax-reqs-stopgap-revert
  - HowToLens: feature/blackjax-reqs-stopgap-revert
- release-gate: PyAutoNerves
- parallel-claim: |
    HowToFit, HowToGalaxy and HowToLens are also claimed by `colab-workshop-dep-stopgap`
    (all three PRs merged 2026-09-15; stale claim awaiting its close-out — this task
    reverts what that task added) and HowToFit by `howtofit-mode` (README/AGENTS
    assistant-prompt propagation, 0 own commits, source uncommitted). Deliberate,
    human-approved override of the conflict guard on 2026-09-15, following the
    `sed-chain-cpu-route` precedent. File sets are disjoint: this task touches
    requirements.txt, the Colab badge lines of README.md and the stopgap cells of
    notebooks/**/*.ipynb + start_here.ipynb (all pure `git revert -m 1` of merged PRs).
- summary: |
    Local-install leg of the tutorials 6/7 blackjax prompt (its Colab leg merged as
    PyAutoNerves#168, unreleased: PyPI autonerves is still 2026.9.15.1) plus, at the
    human's request now the workshop is over, revert of the Colab stopgap: HowToFit
    #63 (1b85e12) and #64 (f4bca40), HowToGalaxy #77 (95eb176), HowToLens #85 (5c3c727).
    Adds blackjax + nautilus-sampler to HowToFit/requirements.txt. One PR per repo.
    MERGE CONDITION: reverting before autonerves > 2026.9.15.1 is on PyPI re-opens the
    Colab gap on every notebook; merge once `pip index versions autonerves` shows a
    newer version, or with the human explicitly accepting the interim gap.

## colab-workshop-dep-stopgap
- issue: n/a — workshop stopgap filed directly as PRs; tracked by PyAutoNerves#167
- issued: 2026-09-15
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/colab-workshop-dep-stopgap
- repos:
  - HowToFit: feature/colab-workshop-dep-stopgap
  - HowToGalaxy: feature/colab-workshop-dep-stopgap
  - HowToLens: feature/colab-workshop-dep-stopgap
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/63
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/77
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/85
- parallel-claim: |
    HowToFit is also claimed by `howtofit-mode` (feature/howtofit-mode). Deliberate,
    human-approved override under workshop time pressure on 2026-09-15, following the
    precedent recorded on `sed-chain-cpu-route`. File sets are disjoint: howtofit-mode
    is propagating README assistant prompts and its source "remains local and
    uncommitted", while this task touches only notebooks/*.ipynb Colab setup cells.
    This task runs in a separate parallel worktree.
- summary: |
    Stopgap for a workshop running 2026-09-15. Adds a second pip install to the Colab
    setup cell of all 100 notebooks carrying one (HowToFit 18, HowToGalaxy 32,
    HowToLens 50), installing corner, optax, xxhash and blackjax with --no-deps
    inside the `else:` (Colab-only) branch. These are autofit dependencies imported
    lazily inside functions, absent from autonerves' _SHARED_EXTRAS and not shipped
    by Colab, so `import autofit` succeeds and the notebook dies partway through a fit.
    --no-deps is load-bearing: with deps, pip would downgrade Colab's GPU jax.
    The anesthetic / nautilus-sampler / dill pins are deliberately untouched.
    REMOVE once autonerves > 2026.9.15.1 is released — the real fix is PyAutoNerves#167,
    which reaches every published notebook retroactively because the setup cell
    pip-installs autonerves unpinned at run time. This exists because the Colab badge
    links point at release tags, not main, so a notebook edit alone cannot reach an
    attendee clicking a README badge.

## colab-bootstrap-lazy-deps
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/167
- issued: 2026-09-15
- prompt: active/colab_bootstrap_missing_lazily_imported_deps.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/colab-bootstrap-lazy-deps
- repos:
  - PyAutoNerves: feature/colab-bootstrap-lazy-deps
- summary: |
    HowToFit tutorial 5 dies on Colab with ModuleNotFoundError: No module named
    'corner', after the search has already completed, in the results update that
    follows it. setup_colab.py installs the stack with --no-deps, so anything
    Colab does not preinstall must be named in _SHARED_EXTRAS; corner==2.2.2 is a
    base autofit dependency and is not there. It hid because corner is imported
    inside corner_cornerpy rather than at module scope, so `import autofit`
    succeeds and smoke at PYAUTO_TEST_MODE=2 never constructs the sampler.
    Third report of the same defect (#166 closed it for emcee/dynesty), so this
    task audits the whole list rather than adding one package: adds corner,
    optax, xxhash, blackjax; corrects two specifiers drifted from
    PyAutoFit/pyproject.toml (anesthetic ==2.8.14 -> >=2.9.0, nautilus-sampler
    ==1.0.4 -> ==1.0.5); adds a specifier-aware test deriving expectations from
    autofit's pyproject rather than restating literals.
    Absorbs the _SHARED_EXTRAS legs of two open prompts (nautilus pin drift;
    tutorials 6/7 blackjax) so one autonerves release closes all of it.
    Out of scope by the human's decision: no PyAutoHands setup-cell change, no
    notebook regeneration (the cell pip-installs autonerves unpinned at run time,
    so the release fixes published notebooks retroactively).
    SHIPPING: merging fixes nothing — an autonerves PyPI release is what ships
    this. Confirm the overnight release run has settled before cutting one.

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

## fixed-light-numba-solver
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/265
- issued: 2026-09-15
- status: workspace-dev
- prompt: active/fixed_light_numba_phase2_source_only_solver.md
- epic: fixed-lens-light-numba-cpu
- phase: 2
- started: 2026-09-15
- worktree: ~/Code/PyAutoLabs-wt/fixed-light-numba-solver
- repos:
  - autolens_profiling: feature/fixed-light-numba-solver
- plan: |
    1. Finish phase 1's close-out so the worktree guard clears.
    2. Issue + active.md registration + worktree fixed-light-numba-solver (workspace-dev, standalone).
    3. Implement (tests + ruff): numpy-path solver-injection seam, factor-reuse NNLS kernel,
       `d_np` route + `--nnls-warm-start` flag in fixed_light_numba.py, and a solver-kernel cell
       fixed_light_numba_solvers.py.
    4. Leg A — the fixed-light speedup on numba with the phase-1 cell (library solver),
       sparse_numba first, then dense; ONE thread only (production runs one single-threaded
       likelihood per process under multiprocessing).
    5. Leg B — solver kernels on the S3 sparse_numba system: library cold / memo-warm /
       certified / factor-reuse / unconstrained floor, --threads 1 only.
    6. Leg C — whole call with the fastest equivalent solver injected, at one thread.
    7. Note results/notes/fixed_lens_light_numba_2026_09.md + speedup breakdown → ship_workspace
       PR (pending-release); PyAutoArray feature prompt filed only if the factor-reuse solver
       earns it.
- scope-decisions: |
    Phase 1's t1/t8 legs were never run; this phase runs them as Leg A. Solver work is scoped from the
    exploration finding that fnnls converges in 0 outer iterations on source-only Delaunay, so the
    lever is factorisation count (LU seed + full Cholesky -> one Cholesky + downdates), not the
    active-set scheme; a fully numba-jitted loop is deferred to the rectangular mesh. Single-threaded
    only (numba 1, BLAS 1): production parallelises across likelihood evaluations with
    multiprocessing, so per-call multi-core gains are not a target; the campaign map's
    thread-scaling phase is retired by this decision. No library edits.
- note: |
    Conflict guard clean (worktree_check_conflict fixed-light-numba-solver autolens_profiling,
    exit 0). Branch based on autolens_profiling origin/main 9285683 (the phase-1 merge).
    The prompt's `Witness:` line and its item 1 still say "one and eight threads" — superseded
    by the single-thread scope decision above, taken by the human 2026-09-15 after filing.

## ep-use-cpu-keeps-jax
- issue: https://github.com/PyAutoLabs/slope_hierarchy_scale/issues/3
- issued: 2026-09-15
- prompt: active/ep_use_cpu_flag_disables_jax.md
- session: claude --resume 32df3fc7-e0cc-4fc7-98c7-0f160dca158c
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/ep-use-cpu-keeps-jax
- repos:

## multi-galaxy-j1011-real-data
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/549
- issued: 2026-09-15
- prompt: active/multi_galaxy_package.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/multi-galaxy-j1011-real-data
- repos:
