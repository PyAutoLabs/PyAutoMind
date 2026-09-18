# Active Tasks

## mass-field-workspace-sweep
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/559
- issued: 2026-09-17
- prompt: active/mass_field_workspace_sweep.md
- session: Fable CLI background job 281b9756 (local-dev)
- status: awaiting-merge
- autonomy: supervised (header; default launch, no --auto — plan approved in chat 2026-09-17; PRs will open as DRAFTS labelled pending-release and merge only after the PyAutoGalaxy + PyAutoLens release is on PyPI)
- worktree: ~/Code/PyAutoLabs-wt/mass-field-workspace-sweep
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/560 (MERGED 2026-09-18, c79c8d3)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/322
- note: Human lifted PyPI release hold on 2026-09-18. autolens_workspace#560 merged after all 7 checks passed; workspace_test#322 remains draft with both Python smoke legs failing latent_integration_smoke_jax.py (missing latent_summary.json). Task and worktree retained until sibling is green and merged.
- release-gate: PyAutoGalaxy
- release-gate: PyAutoLens
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/742
- heart-ack: "install verification FAILED (testpypi; checks F)"; "release validation FAILED (stage integrate)"; yellow "manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml" — acknowledged by the human 2026-09-18 (chat) for commit/push/DRAFT PR-open only; none concern the workspace repos; merge stays human and release-gated
- repos:
  - autolens_workspace: feature/mass-field-workspace-sweep
  - autolens_workspace_test: feature/mass-field-workspace-sweep
- summary: |
    Phase 3 of the mass-field epic (draft/feature/autogalaxy/mass_field_epic.md),
    re-scoped 2026-09-17 on the human's ruling that the user-facing API is
    `fields=` everywhere: every galaxy-attached ExternalShear / MassSheet /
    ExternalPotential in autolens_workspace (217 files) and autolens_workspace_test
    (87 files) moves to al.MassField in its own fields= slot; one legacy regression
    script kept in workspace_test. Absorbs former phase 4 (group/). Started ahead
    of the release to validate the library with real workspace runs; local smoke
    subset against library main, then draft PRs held for the release.

## mass-field-flat-sweep
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/561
- issued: 2026-09-18
- prompt: active/mass_field_flat_sweep.md
- status: awaiting-merge
- autonomy: supervised (header; no --auto — plan approved in chat 2026-09-18; Phase 0 step 3 is a human-confirmation gate on draft PR #322's red latent leg, and PR-open needs the human's explicit Heart ack)
- worktree: ~/Code/PyAutoLabs-wt/mass-field-workspace-sweep
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/562 (DRAFT, pending-release; c8a1283f on feature/mass-field-flat-sweep, 262 files +630/-728, off main c79c8d36)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/322 (DRAFT, pending-release; UPDATED by 8c1a82a1, fast-forward from 63c3323, 64 files +110/-103 — this task's commit folds onto the phase-3 branch)
- repos:
  - autolens_workspace: feature/mass-field-flat-sweep
  - autolens_workspace_test: feature/mass-field-workspace-sweep
- parallel-claim: "worktree_check_conflict mass-field-flat-sweep autolens_workspace autolens_workspace_test (PYAUTO_MAIN=/home/jammy/Code/PyAutoLabs) exits 1 on BOTH repos, claimed by mass-field-workspace-sweep (#559, feature/mass-field-workspace-sweep, LIVE, awaiting-merge). This is deliberate continuity, not a parallel claim: phase 6 is the flat-form follow-up to that task's collection form and REUSES its worktree ~/Code/PyAutoLabs-wt/mass-field-workspace-sweep rather than cutting a conflicting branch. autolens_workspace_test work is folded onto that task's existing branch and its open DRAFT PR #322 (the repo ships the collection form nowhere, so composition_mge.py's identifier pin moves once instead of twice); autolens_workspace branches feature/mass-field-flat-sweep off main, where #560 already merged at c79c8d3, so the two branches never touch the same ref. Waived on the human's plan approval 2026-09-18."
- epic: mass-field (phase 6; draft/feature/autogalaxy/mass_field_epic.md)
- depends-on: PyAutoLens#744 (issue #743) merged 2026-09-18 at 478213e78 — the bare-MassField capability; record complete/2026/09/mass-field-bare-fields.md
- reference-impl: euclid_strong_lens_modeling_pipeline#90 merged 9cdee7b (task euclid-fields-api, euclid issue #89) — already fully flat; mirrored, not edited from here
- release-gate: PyAutoGalaxy
- release-gate: PyAutoLens
- heart-ack: "release validation FAILED (stage integrate)"; yellow "manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml" — RELEASE READINESS RED score 60, both pre-existing and unrelated to these two workspace repos; the human was asked "Do you authorize pushing the two commits and opening/updating the PRs despite the RED?" and answered "Yes — push and open/update PRs" (chat 2026-09-18). Scope is push + PR-open/update ONLY: nothing was merged, no PR marked ready, nothing released or tagged; merge and release stay human-only. Second ruling: autolens_workspace#562 opens DRAFT with pending-release because the flat form needs PyAutoLens#744 (478213e78), merged but not yet on PyPI.
- note: Both PRs are OPEN and DRAFT, labelled pending-release, pending the PyAutoGalaxy + PyAutoLens PyPI release; merge stays human. Phase 0 gate CLEARED: #322's red latent_integration_smoke_jax.py leg was bisected to a JAX 0.11.2 x unfixed-PyAutoGalaxy regression (TypeError: functools.partial ... is not a valid JAX type in the zero-contour solver via the effective_einstein_radius latent), NOT the field sweep — the unmodified main script fails identically in a CI-matching venv, and PyAutoGalaxy 90e757d3 (merged ~10.5 h after that CI run) fixes it, so a CI re-run should clear it; the script PASSES under the flat form (56.4 s). Evidence: 8/8 equivalence, bit-identical log_likelihood -37796.54513586828, autolens_workspace smoke 38/38 + 2/2 notebooks, workspace_test smoke 32/32, notebook AST witness 0 mismatches. Identifiers change BY DESIGN (fields.field.* -> fields.*): old output/ trees are orphaned, nothing aliased or renamed; composition_mge.py pin b99831e66dd27eee314113e8e58235b6 -> 29f82bd3de24984b94657c328b64c3be, galaxy_attached_legacy.py pin 35ebe9353118bcc0c7b2d577ce2639ee UNCHANGED. Also carries two behaviour fixes: the subhalo sensitivity hasattr guards (the old guard silently skipped a deliberate shear prior re-centring under the flat form) and a SEPARATE pre-existing bug in multi_dataset/features/one_by_one/modeling.py whose Second Dataset Offset stage dropped fields= and fitted with no external shear. Next human step: gh pr ready both + re-run #322 CI once the release is on PyPI, then /prm.
- summary: |
    Phase 6 of the mass-field epic. PyAutoLens#744 made the fields= model slot
    accept a bare MassField; this is the requested adoption sweep that moves
    autolens_workspace (143 single-entry sites in 130 files) and
    autolens_workspace_test (66 sites across 65 files) from
    fields=af.Collection(field=field) to fields=field, so prior paths read
    fields.shear.gamma_1 rather than fields.field.shear.gamma_1. Witness is an
    AST re-walk, never a grep — chaining is shape-transparent. Identifiers change
    by design: flat scripts write to new output/ directories and old trees are
    not resumed; composition_mge.py's pin is recomputed once and
    galaxy_attached_legacy.py's 35ebe935... must not move. HowToLens,
    autolens_workspace_developer, profiling, inference, joss, assistant and
    markdown/ are deliberately out of scope with follow-ups filed.

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
- session: https://claude.ai/code/session_01LfJojDFow4pxPzuwRHqMt2 (web-github resume 2026-09-17; planned 2026-09-12 in session_01KTGhZacWuxrxYkXXWXJbBx)
- status: workspace-dev
- worktree: n/a — web-github session clone (/home/user/euclid_strong_lens_modeling_pipeline); the local ~/Code/PyAutoLabs-wt/sersic-variants-analysis worktree named on 2026-09-12 never pushed feature/sersic-variants-analysis, so the branch of record is the session's
- repos:
  - euclid_strong_lens_modeling_pipeline: claude/sersic-variants-analysis-3iqibr
- resume: "IMPLEMENTED 2026-09-17 (web-github; Fable planned, Opus executed): claude/sersic-variants-analysis-3iqibr pushed at 480c107 — scripts/analysis/{sersic_variants.py,README.md,__init__.py}, tests/test_sersic_variants_analysis.py (8 tests), one config/build/no_run.yaml entry. Verified locally: the new tests + test_repo_invariants + test_compare_catalogues, 26 passed; the rest of the fast suite needs astropy/autolens (absent in the container) — CI runs it. FLAGGED on issue #76 comment 5715176814: the W1-W4 thresholds are transcribed into the module's WITNESSES constant (plan page rev 3 unreachable from the session) and need the human's confirmation. NEXT = /ship_workspace (PR) then /prm; nothing here imports --variant, so PR #75's merge order is not a gate."
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

## hst-gpu-residue-p2
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/273
- issued: 2026-09-16
- prompt: active/hst_gpu_residue_p2_vmap_vs_jit_and_batched_callback.md
- session: claude --resume 51243072-d1a4-437b-b5a6-edf3bff12db4
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/hst-gpu-residue-p2
- repos:
  - autolens_profiling: feature/hst-gpu-residue-p2
- parallel-claim: "autolens_profiling was also claimed by fixed-light-numba-levers (#267, COMPLETE 2026-09-16, merged and closed out; worktree removed): its files are fixed_light_numba*, fixed_light_numpy_solvers.py, the lever submits/results and fixed_lens_light_levers_2026_09.md; this task touches fixed_light_trace.py, a new host_callback_probe.py, library_solver_injection.py, a new vmap submit + results + note — disjoint, own worktree beside it exactly as phase 1 (#268) did."
- note: "Phase 2 of hst-gpu-non-solver-residue, STEP 1 ONLY (matched vmap-vs-jit A100 experiment + policy; PyAutoArray batch-aware callback deferred to phase 2b via /intake if the numbers warrant). Fable session plans, Opus executes. A100 submit -> wait -> harvest is a human resume point. Heart RED (install verify testpypi F; release integrate) at start; PR-open needs the human's ack. Phase-1 worktree ~/Code/PyAutoLabs-wt/hst-gpu-residue-p1 still awaits the human's cleanup (3 untracked .err -> worktree_remove -> branch -d)."
- hpc: "A100 array 343376 tasks 0-4 SUBMITTED 2026-09-17 00:10 BST from RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/hst-gpu-residue-p2 @ bf52147 (B16 distinct fb-on / B16 fb-off / B8 / B4 / B16 identical control); all 5 RUNNING on euclid-ral-gpu-1/2 at submit. HUMAN RESUME POINT: when done, harvest = commit the 5 results/breakdown/imaging/fixed_light_trace_delaunay_vmap*_hpc_a100_fp64_*.{json,png} in the RAL worktree, fetch locally (git fetch euclid_jump:/mnt/ral/jnightin/autolens_profiling_wt/hst-gpu-residue-p2 feature/hst-gpu-residue-p2), check AUTOTUNE_ENTRIES count=0 + unjoined 0 + lane pins PASS in hpc/batch_gpu/output/output.343376_*.out, then Phase C (note + errata + README + ship). Phase A on the issue: #273 comment 2026-09-17."

## grid-offset-prior
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/88
- issued: 2026-09-17
- prompt: active/datasetmodel_grid_offset_prior_0_2_clips.md
- session: claude --resume 7bff8610-4b84-413a-a994-d72484c4c14c
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/grid-offset-prior
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/grid-offset-prior
- note: "worktree_check_conflict grid-offset-prior euclid_strong_lens_modeling_pipeline exits 1 on five claims (sed-chain-cpu-route PR #70, sersic-variants PR #75, sersic-variants-analysis #76, simulator-from-result-linear #77 parked, witt-wynne-catalogue #84). Code file sets are disjoint; catalogue/README.md shares one hunk with witt-wynne-catalogue: one-hunk resolution on whichever merges second. Waived on the human's plan approval 2026-09-17; fresh parallel worktree off origin/main."
- note: "PAUSED 2026-09-17 17:10 BST, resumable. DONE on feature/grid-offset-prior (3 local commits d50eb52 prior ±0.5\" / 3563a98 prior_edge_y-x columns + header pin + tests / e58a1be README + eight producers; 208 fast tests green; NOT pushed, no PR). Witness done: sep1 Tile102008165 nir_j x 0.1906 [.., 0.2000] flagged → 0.2727 [0.167, 0.387] unflagged under ±0.5"; nir_h of that tile spins in Nautilus exploration (second case of 343381_8). RESUME: cd ~/Code/PyAutoLabs-wt/grid-offset-prior/euclid_strong_lens_modeling_pipeline; source ../activate.sh; pytest tests -q; /ship_workspace (Heart RED release-side → human ack); /prm; README one-hunk overlap with witt-wynne-catalogue #84. Full state on issue #88 comment."

## oneshot-benchmark-harness
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/126
- issued: 2026-09-17
- prompt: active/oneshot_benchmark_harness.md
- session: claude --resume session_01YTzjiXh2fLocc6dNqLQ66d
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/380
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/127
- autonomy: supervised (header; launched on the human's "Go / continue" in-session — plan on the issue, shipped to PR-open 2026-09-17, merge is human; Brain PR first, it is the assistant PR's `Brain-ref:`)
- location: web-github (session clones /home/user/autolens_assistant + /home/user/PyAutoBrain, no task worktree)
- worktree: n/a — web-github session clones
- repos:
- note: "PyAutoBrain PR #380 and autolens_assistant PR #127 merged; issue #126 is closed. Both repo claims are released. The entry remains active only for the first real headless runs noted below; do not fully close it as part of codex-hook-parity."
- summary: |
    One-shot, machine-scored assistant benchmarks: headless `benchmark.py run`
    (harnesses.yaml adapters, private workdir without benchmarks/truth, compute
    shims), computed-score contract (common gates × card metrics → score.json,
    RESULTS.md medians), prompt freeze (prompt_sha256 + VERSIONS.lock), first
    one-shot card `oneshot-smoke`, 2026-07 cards retired to prompts/conversational/,
    Brain clone VALIDATION_PLAN/partition update. Cards
    benchmark_positions_initialised_inference / benchmark_forward_model_consistency
    stay in draft/, Blocked-by this task. Real headless runs need a laptop with
    the agents installed — the human's first step after merge.

## workspace-smoke-shim-bootstrap
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/416
- issued: 2026-09-18
- prompt: active/workspace_smoke_shim_bootstrap.md
- status: workspace-dev
- autonomy: supervised (plan approved in chat 2026-09-18; staged Mind implementation then coordinated rollout)
- worktree: ~/Code/PyAutoLabs-wt/workspace-smoke-shim-bootstrap
- repos:
  - PyAutoMind: feature/workspace-smoke-shim-bootstrap
- note: First stage edits Mind only. Rollout to the twelve consumers is gated on resolving existing lens workspace and Euclid pipeline claims. No overlap waiver or phase-3 move authorized. Preserve canonical Mind's pre-existing staged draft deletion.
