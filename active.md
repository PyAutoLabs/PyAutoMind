# Active Tasks

## slam-hst-variant-folders-delaunay-1250
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/5
- issued: 2026-09-14
- prompt: active/slam_hst_variant_folders_delaunay_1250.md
- session: claude --resume session_01BtFxjQbaZoXoNH4UTXWxNs
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/slam-hst-variant-folders-delaunay-1250
- repos:
  - autolens_inference: feature/slam-hst-variant-folders-delaunay-1250
- summary: |
    Gives the HST SLaM cell a run-variant level (`results/slam/imaging/hst/slam_base/`
    for the mesh-28x28 base run, `delaunay_1250/` for the new one), commits the four
    completed A100 base rows, and adds the Delaunay-1250 experiment: a `--mesh
    delaunay --mesh-pixels 1250` route with `al.reg.AdaptSplit` (reg.Adapt is not
    jit-traceable on the Delaunay family), its own leaf/cell id
    `imaging/slam/hst_delaunay`, and two A100 submits (dense + sparse, seeds 0-1).
    Ends at submission: job ids recorded on a Cortex task `slam_hst_delaunay_1250`,
    pull and judgment on a later /cortex check-in.

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

## model-figures-rollout-lens
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/542
- issued: 2026-09-13
- prompt: active/model_figures_6b_lens_surfaces.md
- session: claude --resume session_01DLx38vS6F1M7K5LnpVbeZ7
- status: wave 1 MERGED (HowToLens#81, autolens_workspace#543); wave 2 RESUMED 2026-09-14 under a changed prose standard — autolens_workspace PR B on feature/model-figures-rollout-lens-b (sweep + rollout, two commits), HowToLens prose sweep on feature/model-figure-prose-lens
- worktree: ~/Code/PyAutoLabs-wt/model-figures-rollout-lens
- epic: model-figures phase 6b
- release-gate: PyAutoFit
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/81 (merged 635ee49ab155537dcc91dea09237c955408d9431)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/543 (merged c8b7254830da5f4a0908b561296a30654b884ae4)
- repos:
  - autolens_workspace: feature/model-figures-rollout-lens-b
  - HowToLens: feature/model-figure-prose-lens
- standard-change: |
    2026-09-14. The human's verdict is that the per-figure reading commentary this
    rollout writes is information overload and the figure should be self-explanatory.
    Every first-figure prose block — opener, map/legend paragraph and all
    file-specific paragraphs after it — collapses to two fixed paragraphs
    (canonical text on the issue, comment 5669860023). This supersedes the prompt's
    "Pattern" section for the opener block and retires its "lens vocabulary must be
    verified by rendering" requirement, which had nothing left to govern. The short
    one-to-three-line notes at second and third figure sites are unchanged.
- resumed: |
    2026-09-14. Wave 2 was stalled, not in flight: 13 modified scripts under
    scripts/interferometer/ uncommitted in the worktree, last touched 2026-09-13
    22:36, zero commits ahead of origin/main. Their .figure() calls and placement
    are kept; only the prose is rewritten. Branch B was fast-forwarded onto
    origin/main (release Colab-URL bump) with the WIP stashed and popped. HowToLens
    wave 1 is merged, so its sweep runs on a new branch cut from origin/main.
    autolens_workspace ships ONE PR carrying both commits rather than the prompt's
    "two PRs by folder", so the sweep need not wait on a merge to open a third.
    Sibling task model-figure-prose-simplify (autofit_workspace#156) applies the
    same standard to the six unclaimed repos.
- note: "worktree_check_conflict model-figures-rollout-lens autolens_workspace HowToLens exits 0 (2026-09-13, after the stale remove-fits-dataset-plots-yaml claim was closed out). Plan approved in Plan Mode 2026-09-13; SLaM deferred to 6b2; autolens_workspace ships as two PRs (A: guides/imaging/point_source/multi_dataset; B: interferometer/group/multi_galaxy/cluster/weak on feature/model-figures-rollout-lens-b after A merges); release-gate PyAutoFit because guides/modeling/advanced/expectation_propagation.py uses EPResult.factor_graph (merged 6a, unreleased)."

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
  - autofit_assistant: feature/howtofit-mode
  - HowToFit: feature/howtofit-mode
  - autofit_workspace: feature/howtofit-mode
  - PyAutoFit: feature/howtofit-mode
- prompt: active/howtofit_mode.md
- summary: Assistant implementation ready and reviewed; approved README prompt propagation to HowToFit, autofit_workspace and PyAutoFit in progress. Shipping held by Heart YELLOW pending human acknowledgement.
- ship-hold: |
    Workspace validation: 3 failures (cloud#34824535982).
    Manifest drift: organism-map 2; public front-door 2.
    Profiling drift: three matrix_free SLQ fp64 results — delaunay_hpc_a100,
    delaunay_nn_hpc_a100, rectangular_hpc_a100.
- next: Acknowledge these Heart YELLOW reasons before ship_workspace; source remains local and uncommitted.
## model-figure-prose-simplify
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/156
- issued: 2026-09-14
- prompt: active/model_figure_prose_simplify.md
- session: claude --resume session_01LPCvGNHahZqynPyEfMijsb
- status: PRs OPEN (6), awaiting CI + /prm; Heart YELLOW acknowledged by the human 2026-09-14
- worktree: ~/Code/PyAutoLabs-wt/model-figure-prose-simplify
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1627
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/617
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/738
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/158
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/56
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/241
- heart-ack: "workspace validation not passing (3 failed, cloud#34824535982); manifest drift: organism-map blocks (generated) - 2 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: public front-door organ tables (generated) - 2 mismatch(es) vs PyAutoMind/repos.yaml; profiling drift: matrix_free delaunay/delaunay_nn/rectangular hpc_a100 fp64 + mge + mge_mass_jax runtime summaries (+1 more); release validation incomplete: no rehearsal for current source"
- epic: model-figures
- repos:
  - autofit_workspace: feature/model-figure-prose-simplify
  - HowToFit: feature/model-figure-prose-simplify
  - autogalaxy_workspace: feature/model-figure-prose-simplify
  - PyAutoFit: feature/model-figure-prose-simplify
  - PyAutoGalaxy: feature/model-figure-prose-simplify
  - PyAutoLens: feature/model-figure-prose-simplify
- note: "worktree_check_conflict fires on autofit_workspace, HowToFit and PyAutoFit, all claimed by task howtofit-mode (autofit_assistant#42, worktree .worktrees/howtofit-mode). That task's entire scope in those three repos is one uncommitted README.md each with no commits ahead of origin/main; this task touches only scripts/, notebooks/ and docs/cookbooks/, so the file sets are disjoint. Waived in a fresh parallel worktree based on origin/main, the same call recorded for sed-chain-cpu-route and sersic-variants-analysis. Trap: worktree_check_conflict returned a false clean when passed all six repos in one call and only fired when passed them one at a time."
- summary: |
    Human verdict 2026-09-14: the per-figure reading commentary rolled out by the
    model-figures epic is information overload and the figure should be
    self-explanatory. Every map/legend prose block collapses to two fixed
    paragraphs, with all file-specific trailing prose deleted. This task covers
    the six unclaimed repos (41 files); autolens_workspace and HowToLens (100
    files) adopt the same standard by resuming model-figures-rollout-lens
    (autolens_workspace#542), whose wave 2 is stalled with 13 uncommitted blocks
    and ~53 sites unwritten.

## howtofit-tutorials-1-3
- issue: https://github.com/PyAutoLabs/HowToFit/issues/57
- issued: 2026-09-14
- prompt: active/howtofit_tutorials_1_3_fixes.md
- session: claude --resume session_0132v5TNVbbvBBESAefHwnwG
- status: awaiting-merge (both PRs open 2026-09-14; merge is human)
- worktree: ~/Code/PyAutoLabs-wt/howtofit-tutorials-1-3
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/58
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/164
- heart-ack: "workspace validation not passing (3 failed, cloud#34824535982); profiling drift: breakdown/imaging/matrix_free_delaunay_hpc_a100_fp64_matrix_free.json; profiling drift: breakdown/imaging/matrix_free_delaunay_nn_hpc_a100_fp64_matrix_free.json; profiling drift: breakdown/imaging/matrix_free_rectangular_hpc_a100_fp64_matrix_free.json; profiling drift: runtime/imaging/mge/mge_likelihood_summary_hst_v2026.8.17.1.json; profiling drift: runtime/imaging/mge_mass_jax/mge_mass_jax_likelihood_summary_hst_v2026.8.17.1.json; profiling drift: +1 more drifted result(s); release validation incomplete: no rehearsal for current source"
- repos:
  - HowToFit: feature/howtofit-tutorials-1-3
  - PyAutoNerves: feature/howtofit-tutorials-1-3
- note: "worktree_check_conflict exits 1 on HowToFit with two claims. howtofit-mode's scope there is one uncommitted README.md with no commits ahead of origin/main — disjoint, waived (the call already recorded for model-figure-prose-simplify, sed-chain-cpu-route and sersic-variants-analysis). model-figure-prose-simplify (HowToFit#56, open, all checks green) rewrites the same tutorial 1 model-figure paragraphs, so this task does NOT race it: the branch is cut from origin/feature/model-figure-prose-simplify and the PR is opened against that base, so GitHub shows only this task's diff and retargets to main once #56 merges. Merge #56 first. Where the two disagree on the 'identical composition' paragraph, the reader's wording in HowToFit#57 is the newer instruction and wins. PyAutoNerves is unclaimed (exit 0)."
- summary: |
    Reader-reported fixes to HowToFit chapter 1, tutorials 1-3, launched with
    --auto (docs cap, Difficulty medium -> effective level safe; ends at PR-open).
    Tutorial 1 gains the 1D Gaussian dataset figure ahead of the model equation
    (as the RTD python_api page has it), the reader's replacement wording for the
    model-figure "identical composition" paragraph, and a worked 18-parameter
    extensibility example (x2 Gaussian + x4 Exponential, model.info + figure
    only); plus backticked code references and a typo pass. Tutorials 1-3 convert
    `\[ \]` / `\( \)` math to `$$ $$` / `$ $`, which Jupyter and Colab actually
    typeset. Tutorial 3's MLE InitializerParamStartPoints moves closer to the
    truth (50 / 25 / 10) so LBFGS converges reliably.
    The reader's `ModuleNotFoundError: No module named 'emcee'` on Colab is NOT a
    HowToFit bug: emcee and dynesty are real autofit dependencies that the
    PyAutoNerves Colab bootstrap drops because it installs with --no-deps and
    does not name them in _SHARED_EXTRAS. Fixed there as a second PR; it reaches
    users on the next autonerves release.
    Shipped 2026-09-14. The MLE failure turned out NOT to be the start point:
    af.InitializerParamStartPoints was keyed on one af.Model(Gaussian) while a
    freshly built one was passed to search.fit, so no key matched and PyAutoFit
    fell back to random draws (logged, not raised). Fixed in both the LBFGS and
    Emcee blocks; start points 52/23/9 now recover 49.889/25.147/9.847.
    Smoke 18/18 PASS, exit 0. Heart YELLOW acknowledged by the human for the
    exact reason set recorded above.
    Out of scope (follow-ups): tutorials 6, 7 and the optional Bayesian formalism
    tutorial carry the same unrendered math blocks; tutorial 3's __Priors__
    section is dead code whose normalization override (0, 10) excludes the truth
    25 (the fits only work via the config LogUniformPrior fallback).

## howtofit-tutorial-followups
- issue: https://github.com/PyAutoLabs/HowToFit/issues/59
- issued: 2026-09-14
- prompt: active/howtofit_tutorials_followups.md
- session: claude --resume session_0132v5TNVbbvBBESAefHwnwG
- status: awaiting-merge (PR open 2026-09-14; merge is human)
- worktree: ~/Code/PyAutoLabs-wt/howtofit-tutorial-followups
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/60
- repos:
  - HowToFit: feature/howtofit-tutorial-followups
- parent: howtofit-tutorials-1-3 (HowToFit#57 / #58)
- note: "Both follow-ups touch files #56 and #58 already modify (#56: tutorial_7_the_details.py, tutorial_optional_bayesian_formalism.py; #58: tutorial_3_non_linear_search.py), so this cannot branch from main without conflicting. Cut from origin/feature/howtofit-tutorials-1-3 and based on it. Merge order: #56 -> #58 -> this. Same HowToFit claim waiver as the parent task (howtofit-mode README-only, disjoint)."
- summary: |
    The two follow-ups reported out of HowToFit#57. (A) Finish the math sweep:
    tutorials 5, 6, 7 and the optional Bayesian formalism tutorial still carry 13
    `\[ \]` display blocks and 55 `\( \)` inline spans, neither of which Jupyter or
    Colab typeset. (B) Tutorial 3's __Priors__ block is dead AND wrong: it sets three
    priors on a model every later fit discards by re-calling af.Model(Gaussian), and
    normalization Uniform(0, 10) excludes the truth 25 while sigma Uniform(0, 10) puts
    the truth 10 on the boundary. The fits silently run the config defaults
    (centre Uniform(0,100), sigma Uniform(0,25), normalization LogUniform(1e-6,1e6)).
    Design trap: making the block apply changes the parameter space every search
    explores, and the FIRST, uninitialised MLE fit is supposed to fail — that failure
    is the MLE section's whole teaching point, and it only fails reliably today because
    normalization is LogUniform over 12 decades. Decision rule handed to execution:
    prefer real, meaningful priors, but only if the uninitialised MLE still fails 10/10
    runs; otherwise keep the explored space semantically equal to the config defaults
    and make the block honest instead of flaky. Either way the dead code is fixed.
    OUTCOME: branch 2, and the trap was worse than flakiness. af.LBFGS() initialises
    with InitializerBall(0.49, 0.51) - a tight ball on each prior's CENTRE, not a
    random draw - so normalization Uniform(0, 50) has centre 25.0 = the truth and the
    "failing" fit succeeded 10/10 at logL 176.1. Measured: config priors fail 10/10,
    candidate succeeds 10/10, restated defaults fail 10/10 reproducing the baseline
    local max. Shipped the restated defaults, actually applied; 5 dead
    af.Model(Gaussian) re-creations removed. Third fix found en route:
    Analysis.log_likelihood_function in tutorials 3, 4 and 5 read a module-level
    noise_map global instead of self.noise_map - the class readers are told to copy,
    which raises NameError outside the tutorial. Smoke 18/18, CI green on all 7 checks.
    Deferred to draft/bug/howtofit/tutorial_3_uninitialised_emcee_is_flaky.md: the
    uninitialised Emcee fit does not reliably succeed (pre-existing on main, 10
    walkers x 200 steps); fixing it trades tutorial runtime and needs a human call.

## scaling-relation-slam-smoke-frame-cap
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/544
- issued: 2026-09-14
- prompt: active/scaling_relation_slam_smoke_frame_cap.md
- session: claude --resume session_01RbJGue5FwUPbxvCFKwXNam
- status: awaiting-merge (PR open 2026-09-14; merge is human)
- worktree: ~/Code/PyAutoLabs-wt/scaling-relation-slam-smoke-frame-cap
- repos:
  - autolens_workspace: feature/scaling-relation-slam-smoke-frame-cap
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/545
- heart-ack: "workspace validation not passing (3 failed, cloud#34824535982); profiling drift x6; release validation incomplete"
- note: "worktree_check_conflict exits 1 on one claim: autolens_workspace is claimed by model-figures-rollout-lens (feature/model-figures-rollout-lens-b, autolens_workspace#542). Its worktree is clean and its 205-file diff contains no slam.py or slam.ipynb path anywhere; the nearest approach is scripts/imaging/features/scaling_relation/modeling.py and notebooks/imaging/features/scaling_relation/modeling.ipynb, the same directories as this task's two files but not the same files, so the file sets are disjoint at file level and no hunk can collide. Waived on the human's plan approval; this task runs in a fresh parallel worktree cut from origin/main - the same call recorded for sed-chain-cpu-route, sersic-variants-analysis and model-figure-prose-simplify."
- summary: |
    Clears the Heart workspace-smoke failure on
    notebooks/imaging/features/scaling_relation/slam.ipynb (cloud run
    34824535982): under the smoke profile's PYAUTO_SMALL_DATASETS frame cap the
    130x130 @ 0.1" image becomes 16x16 @ 0.6", cropping two scaling-tier
    companions at (5.0, -1.0) and (-1.0, 5.0) out of frame; their MGE
    intensities are solved from noise and use_positive_only_solver clamps a
    non-positive draw to exactly 0.0, tripping the script's own luminosity
    guard. simulator.py passes no noise_seed and dataset/ is gitignored, so the
    clamp is a per-run lottery, not a regression (the same notebook passed in
    runs 33378525604 and 34099198772). Fix is one ENV: full_datasets
    declaration on the script (_declaration_source_path covers the notebook leg
    from the same line) plus a rewrite of the stale guard message, which still
    blames PYAUTO_TEST_MODE and a config/build/no_run.yaml park removed on
    2026-08-29 (883d1e2f). No library edits; galaxy centres and simulator.py
    deliberately untouched.

## emcee-log-prob-alignment
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1628
- issued: 2026-09-14
- prompt: draft/bug/autofit/emcee_zeus_samples_log_prob_misalignment.md
- session: claude --resume session_0132v5TNVbbvBBESAefHwnwG
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/emcee-log-prob-alignment
- repos:
  - PyAutoFit: feature/emcee-log-prob-alignment
- note: "worktree_check_conflict exits 1 on PyAutoFit with two claims, both waived as disjoint: howtofit-mode holds one uncommitted README.md, and model-figure-prose-simplify (PyAutoFit#1627) touches only docs/cookbooks/*.md and docs/features/graphical.md. This task touches autofit/non_linear/search/mcmc/{emcee,zeus}/search.py and test_autofit/ only. Fresh worktree from origin/main."
- summary: |
    Correctness bug found while calibrating HowToFit tutorial 3's MCMC budget
    (HowToFit#59/#60). Emcee's samples_via_internal_from pairs a thinned,
    burn-in-discarded parameter chain with a raw tail slice of the unthinned,
    undiscarded log-probability array (plus a one-element offset), so every
    sample's reported likelihood belongs to a different sample. Zeus has the same
    defect via a silent zip() truncation. Consequence:
    result.max_log_likelihood_instance is the argmax of a scrambled array - a
    random post-burn-in draw, not the MLE - and the "Maximum Log Likelihood" line
    of every Emcee and Zeus result.info is wrong. Nested sampling and the MLE
    searches are unaffected.
    Verified twice in-session: reported 188.9628 vs actual 188.8337 on one fit,
    reported 188.34 vs actual 176.52 on another. The error scales with how much
    post-burn-in samples differ, so a poorly converged chain is punished hardest.
    Fix: request log-probs under the same discard/thin as the chain, bind those in
    both the test-mode and normal branches, assert equal lengths before zip, and
    add a regression test asserting the invariant (reported max-likelihood equals
    the Analysis likelihood recomputed from the reported instance) rather than
    pinning a number - validated by reverting the fix and confirming the test fails.
    Blast radius: moves the reported max-likelihood of every existing Emcee/Zeus
    fit. They were wrong before, so this is a correction, but it will move pinned
    values.
