# Active Tasks

## arxiv-digest-api-retry
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/410
- issued: 2026-09-18
- prompt: active/arxiv_digest_dies_on_api_transport_errors.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/arxiv-digest-api-retry
- repos:
  - PyAutoMind: feature/arxiv-digest-api-retry
- note: "Recovers abandoned branch claude/papers-slack-pyautomemory-39wrt1 (commit 9f5fbab6, written 2026-09-16, never PR'd) and closes its gap: RETRY_STATUSES omitted 406, so _get() re-raised unretried and the fetch step died even though _livecheck() survived. Branch is cut from that branch, not main, to keep its history. Refuted and not to be re-derived: the User-Agent/Accept headers are NOT the cause (all four header combinations returned HTTP 200 when probed live 2026-09-18 from a home IP); cron placement is NOT the cause (complete/2026/09/cron-delivery-headroom.md)."
- parallel-claim:
  - date: 2026-09-18
  - guard: worktree_check_conflict fired — PyAutoMind is claimed by codex-hook-parity (#407)
  - authorization: human approved an own worktree over a fold or a planned.md park
  - basis: file sets are disjoint (#407 touches .codex/hooks.json, scripts/repos_sync.py, repos.yaml, hook workflows; this touches .github/scripts/arxiv_fetch.py, tests/test_arxiv_fetch_retry.py) and #407's worktree is clean
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/412
- implementation: commit 3691aaef on feature/arxiv-digest-api-retry. Red-then-green recorded (2 new 406 witnesses fail on pre-fix source, 8 existing pass; 10 pass after). Both --selftest PASS. arxiv_interests.py coverage proven by execution, not by reading.
- contradiction: the plan expected a live --livecheck PASS from here; it returned SKIPPED (network) after exhausting the full ladder on 406. The 406 is NOT egress-specific and NOT transient — Fastly's edge refuses the request (via: 1.1 varnish, no 1.1 google), so arXiv never sees it, and ten header combinations across urllib.request and http.client all 406 on UNCACHED urls while curl and requests get 200. Leading hypothesis: bot mitigation on the stdlib client fingerprint. #412 is therefore strictly better but possibly insufficient; follow-up filed at draft/bug/pyautomind/arxiv_edge_refuses_the_stdlib_urllib_client.md. Probing trap: repeated urls return cached 200s and hide the effect.
- held: backfill of the four lost digest nights (09-14, 09-15, 09-17, 09-18) needs a manual workflow_dispatch with LOOKBACK_HOURS, which posts to the shared Slack channel — human approval pending, separate from the fix.

## euclid-fields-api
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/89
- issued: 2026-09-18
- prompt: active/fields_api_top1000.md
- status: deployment-pending
- worktree: ~/Code/PyAutoLabs-wt/euclid-fields-api
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-fields-api
- note: Human approved plan, deployment and now submission of the prepared top-1000 vis_lp array (2026-09-18: "let us submit"). Keep fields=field unchanged. Preserve all science outputs and preparation. RAL uses source clones, no PyPI release gate.

- heart-red-override:
  - date: 2026-09-18
  - authorization: User "I approve" to the task-specific development override for issue #89 and merge only with every required CI check green in this session.
  - red-reasons: "release validation FAILED (stage integrate)"
  - yellow-reasons: "manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml"
  - gates: 230 tests PASS; 9/9 smoke PASS; independent review CLEAN (27 focused checks); diff check PASS.
  - scope: commit, push, pending-release PR; merge only on green CI. No release or SLURM submission; modelling-script hold remains.
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/90
- implementation: Pipeline #90 merged 9cdee7b1 after all 9 CI checks passed; source head 7fbdbe5. Local science port complete, RAL deployment pending shared-stack job. Submission hold remains.
- ci-blocker: Both unit matrix legs fail the latent contour test with JAX 0.11.2; isolated third-party-only reproduction confirms the dependency incompatibility. RESOLVED: repair merged as PyAutoGalaxy#623 (90e757d3) + autogalaxy_workspace_test#123 (ae45e490); record complete/2026/09/euclid-jax-contour-compat.md. Pipeline #90 rerun passed all 9 checks and merged at 9cdee7b1.
- deployment: Local selective port committed 2430e4e from d53b9ce, preserving 18 science commits and all data/config/output; model/import validation PASS. RAL unchanged (Lens 7197380); running job 343413 uses shared stack, so refresh and sync held. No submissions. Recheck all jobs, cleanliness/divergence (Fit status incomplete) and preserve editor backups, then HPCPullPyAuto, imports/model verification, hpc/sync and Cortex update. Evidence: tmp/euclid-flat-fields/deployment-state.json; Cortex 3c32bcc.

- current-deployment: RAL stack refreshed (Galaxy 90e757d3, Lens 478213e78); code/config hashes and actual imported model PASS. Data upload in progress; no job submitted. Verify archive checksum and dataset completeness, including interrupted-transfer partial files, before hpc/sync submit. Cortex c37c8f4; tmp/euclid-flat-fields/deployment-state.json.

## codex-hook-parity
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/407
- issued: 2026-09-17
- prompt: active/codex_hook_parity.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/codex-hook-parity
- repos:
  - PyAutoMind: feature/codex-hook-parity
  - PyAutoBrain: feature/codex-hook-parity
  - autofit_assistant: feature/codex-hook-parity
  - autogalaxy_assistant: feature/codex-hook-parity
  - autolens_assistant: feature/codex-hook-parity
  - autocti_assistant: feature/codex-hook-parity
- note: "Preserve user-owned untracked scripts/compose_model_gaussians_exponentials.py in the autofit_assistant main checkout and scripts/cluster_model_composition.py in the autolens_assistant main checkout; implementation is isolated in this worktree."

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
- status: phase-0-gate
- autonomy: supervised (header; no --auto — plan approved in chat 2026-09-18; Phase 0 step 3 is a human-confirmation gate on draft PR #322's red latent leg, and PR-open needs the human's explicit Heart ack)
- worktree: ~/Code/PyAutoLabs-wt/mass-field-workspace-sweep
- repos:
  - autolens_workspace: feature/mass-field-flat-sweep
  - autolens_workspace_test: feature/mass-field-workspace-sweep
- parallel-claim: "worktree_check_conflict mass-field-flat-sweep autolens_workspace autolens_workspace_test (PYAUTO_MAIN=/home/jammy/Code/PyAutoLabs) exits 1 on BOTH repos, claimed by mass-field-workspace-sweep (#559, feature/mass-field-workspace-sweep, LIVE, awaiting-merge). This is deliberate continuity, not a parallel claim: phase 6 is the flat-form follow-up to that task's collection form and REUSES its worktree ~/Code/PyAutoLabs-wt/mass-field-workspace-sweep rather than cutting a conflicting branch. autolens_workspace_test work is folded onto that task's existing branch and its open DRAFT PR #322 (the repo ships the collection form nowhere, so composition_mge.py's identifier pin moves once instead of twice); autolens_workspace branches feature/mass-field-flat-sweep off main, where #560 already merged at c79c8d3, so the two branches never touch the same ref. Waived on the human's plan approval 2026-09-18."
- epic: mass-field (phase 6; draft/feature/autogalaxy/mass_field_epic.md)
- depends-on: PyAutoLens#744 (issue #743) merged 2026-09-18 at 478213e78 — the bare-MassField capability; record complete/2026/09/mass-field-bare-fields.md
- reference-impl: euclid_strong_lens_modeling_pipeline#90 merged 9cdee7b (task euclid-fields-api, euclid issue #89) — already fully flat; mirrored, not edited from here
- release-gate: PyAutoGalaxy
- release-gate: PyAutoLens
- note: Inherits mass-field-workspace-sweep's Heart RED ("release validation FAILED (stage integrate)") + YELLOW ("manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml"). PR-open needs the human's explicit ack, recorded verbatim; merge stays human. GATE before any rewrite: diagnose #322's red latent_integration_smoke_jax.py leg (missing files/latent/latent_summary.json; green on main, red on the draft) and confirm the path with the human.
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

## community-surface-users-vs-dev-flow
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/403
- issued: 2026-09-17
- prompt: active/community_surface_users_vs_dev_flow.md
- session: claude --resume session_01NddWGmJwZfEkZK9WLoxBYg
- status: library-dev
- location: web-github (session clones, no task worktree; branch claude/github-issues-community-migration-512ndl)
- worktree: n/a — web-github session clone (/home/user/PyAutoMind, /home/user/PyAutoBrain)
- repos:
  - PyAutoMind: claude/github-issues-community-migration-512ndl
  - PyAutoBrain: claude/github-issues-community-migration-512ndl
- summary: |
    Decision task shipped as `policy/community_surface.md`: users go to one
    Discussions hub (hosted on `PyAutoLabs/.github`, the org's), the development
    flow stays on per-repo issues, bug reports with a reproducer stay
    issues. The Ears (`pyauto-brain community`) now scan the hub's
    discussions and triage a discussion URL; the Brain board shows
    unanswered threads as triage chips. Migration is the human's native
    "Convert to discussion" clicks (no API can do it — measured); manifest
    of six user-filed feature threads in the policy page, filed as
    `draft/maintenance/community/migrate_user_threads_to_discussions.md`
    with the README/issue-chooser and front-door follow-ups beside it.
    Brain branch needs a human merge (code + skills); Mind branch is mixed
    (policy/ + draft/ + active/) so it waits for a human too.
