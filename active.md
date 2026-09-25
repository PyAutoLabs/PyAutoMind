# Active Tasks

## pyautoeyes-birth-organ-row
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/437
- issued: 2026-09-25
- prompt: active/eyes_birth_organ_row.md
- session: Claude Code CLI (Fable architect, Opus execution), 2026-09-25; session ID unavailable
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/438
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/44
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/171
- library-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/8
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/415
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/237
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/288
- workspace-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/11
- workspace-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/34
- autonomy: supervised (header); plan approved in-session 2026-09-25 (Fable architect); human-only: gh repo rename, .github row, Heart RED override
- worktree: /home/jammy/Code/PyAutoLabs-wt/pyautoeyes-birth-organ-row
- repos:
  - PyAutoMind: feature/pyautoeyes-birth-organ-row
  - PyAutoBrain: feature/pyautoeyes-birth-organ-row
  - PyAutoHeart: feature/pyautoeyes-birth-organ-row
  - PyAutoHands: feature/pyautoeyes-birth-organ-row
  - pyautolabs.github.io: feature/pyautoeyes-birth-organ-row
  - PyAutoScientist: feature/pyautoeyes-birth-organ-row
  - PyAutoCortex: feature/pyautoeyes-birth-organ-row
  - PyAutoNerves: feature/pyautoeyes-birth-organ-row
  - PyAutoGut: feature/pyautoeyes-birth-organ-row
- resume: awaiting human /prm merge in the Merge order; PyAutoHeart#237 is a DRAFT until the rename (Mind → Cortex/Nerves/Gut → Brain → Heart after rename → Hands → hub → Scientist); human items: `gh repo rename PyAutoEyes -R PyAutoLabs/autolens_visualization`; `.github` org-profile organ row (denied to the agent twice)
- heart-red-override:
  - date: 2026-09-25
  - authorization: live human message 2026-09-25, in the session that built the branches, replying to the phase-0 handover that named issue #437 (item 3 = "Authorize the Heart RED override for issue #437"): "can you do 2 and 3 i authorize RED overrule"
  - red-reasons: "release validation FAILED (stage integrate)" (readiness re-read 2026-09-25T18:54:09.039610+00:00, score 45)
  - yellow-reasons: "workspace validation not passing (4 failed, cloud#35579888156: autolens notebooks/cluster/modeling.ipynb, autolens notebooks/weak/a2744.ipynb, autolens scripts/cluster/modeling.py, +1 more)"; "manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml"; "manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml"
  - passed: Mind pytest 585; Brain pytest 1002 + sphinx docs 0 warnings; Heart pytest 1035; Hands pytest 463; Cortex pytest 63; Nerves pytest 185; Gut none (no tests touched); repos_sync --check organism-map blocks OK; pyauto-brain eyes survey rc=0 on the organ root
  - scope: commit/push/pending-release PRs only; merge not authorized; Heart remains RED for release; the PRs do not fix Heart. Recorded on issue #437 and in every PR body.

## abell-1201-point-mass
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/133
- issued: 2026-09-22
- prompt: active/add_an_abell_1201_central_point_mass.md
- session: Codex (session ID unavailable)
- status: awaiting-input
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/134
- brain-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/414
- merge-order: Brain 414 first, assistant 134 second; assistant declares Brain-ref. Full scientific task remains open after these preparation PRs merge.
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/abell-1201-point-mass
- repos:
- preparation-record: complete/2026/09/abell-1201-preparation.md
- claims-released: Both preparation branches merged; worktree retained for science continuation and ignored plots/reports (4.2 MB).
- repair-plan: Human "go" approved classifying the exact Abell README as domain in Brain and assistant template policy, with regression tests, then retrying shipping. Brain attached to existing task root; fresh Mind has no competing Brain claim (stale canonical claim belongs to merged Brain PR 409).
- summary: Preparation phase merged via human prm on 2026-09-22 (Brain 414 then assistant 134), all four CI jobs green. Full posterior budget and science validation remain checkpoints; no release or posterior execution authorised.
- heart-red-override:
  - authorization: User "continue i suthorize" in direct response to development-only shipping override for issue #133; no release, merge, posterior run or CI bypass.
  - red-reasons: "release validation FAILED (stage integrate)"
  - passed: 129 tests at refreshed head 79854cc; refreshed data preparation, finite coarse likelihood smoke and freeze-check pass.
  - repaired: Clone-boundary now passes with paired Brain classification; 56 clone tests pass. User "go" approved coordinated repair and shipping retry. Separate independent review not required on supervised path; no independent CLEAN verdict claimed.
- latest-shipping-attempt: Assistant f14293d (PR 134), Brain b1c8d89 (PR 414), both pushed with pending-release labels and dependency comments. Publication permission recorded at 79854cc with Nightingale et al. (2023)/HST credit. Heart remains RED for release purposes.
- resume: Preparation PRs are MERGED; do not rerun shipping. Retain issue 133 for full-run budget, posterior/scientific calibration and unresolved absolute photometric units. Approved F390W power-law + shear + point mass with nuisance parameters, cleaned 4 arcsec mask (31417 pixels). No posterior or headless run authorised/executed. Pre-removal originals deferred; RGB retains/discloses cut-out. Worktree retained, artifacts under scripts/scratch/abell_1201; preserve during cleanup. Originals untouched. Re-survey claims and branch before further implementation.

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

## vis-lp-inspection-bundle
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/102
- issued: 2026-09-22
- session: claude (Fable CLI, 2026-09-23; resumed from Codex 2026-09-22)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/vis-lp-inspection-bundle
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/vis-lp-inspection-bundle
- summary: Add an explicit vis_lp-only inspection mode that combines the main normal-model output tree with the 100-lens SED/Sersic tree, without requiring vis_pix or selecting the other 200 main-tree lenses.
- resume: Implemented + committed locally as c6b514d on feature/vis-lp-inspection-bundle (133 tests green, not pushed). Human reviews diff (scratchpad part1_diff.txt) before ship_workspace; then sync tooling to the euclid_dr1 science clone/RAL and submit the 4,922-tile vis_lp-only bundle (OUTPUT_DIR=dr1_full, INITIAL_SEARCH_NAME=vis_lp, DATASET_NAMES_PATH=all, TAR_TO set) as a Cortex run.

## interferometer-mge-breakdown
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/308
- issued: 2026-09-25
- prompt: active/interferometer_mge_breakdown_jax_cpu_gpu.md
- session: Claude Code CLI (Opus 5.5), 2026-09-25
- status: workspace-dev
- autonomy: supervised (header); plan approved in-session 2026-09-25 (research only, no library edits)
- worktree: /home/jammy/Code/PyAutoLabs-wt/interferometer-mge-breakdown
- repos:
  - autolens_profiling: feature/interferometer-mge-breakdown
- parallel-claim: "autolens_profiling is also claimed by certified-solver-phase-c1-lane-rate (feature/certified-solver-phase-c1-lane-rate). Disjoint file sets: that task is imaging/nautilus capture + imaging submits + results/breakdown/imaging/nautilus_batches_*; this task adds scripts/interferometer/likelihood_breakdown/mge.py, hpc/batch_gpu/submit_breakdown_interferometer_mge_*, results/breakdown/interferometer/mge_*, results/notes/interferometer_mge_breakdown_2026_09.md and edits scripts/misc/vram/config.py. Only shared surface is the generated README dashboard (regenerate at ship). Recorded 2026-09-25 per the #177 precedent."
- ral-jobs: RAL worktree /mnt/ral/jnightin/autolens_profiling_wt/interferometer-mge-breakdown @ 0dd0d20 (git bundle, not on GitHub). First A100 pass 351054-351059 INVALID except sma (RAL venv nufftax 0.4.0 < PyAutoArray floor 0.6.1 auto-dispatches fp32 Pallas on GPU; probe 351062: type2 1.05e-4 rel, pure-JAX fp64 2.9e-13 and 13x faster). jvla 351058/9 cancelled.
- resume: BLOCKED on the human running `ssh euclid_jump '/mnt/ral/jnightin/PyAuto/PyAuto/bin/pip install "nufftax==0.6.1"'` (dry-run: only nufftax moves; classifier blocks agents from the shared venv). Then resubmit the 6 hpc/batch_gpu/submit_breakdown_interferometer_mge_a100_* from the RAL worktree (jvla_mp afterok jvla_fp64), pull, set configuration.nufftax_version=0.6.1, lint, commit; then phase C (note + vram/config.py + follow-up prompts incl. RAL venv floor drift: anesthetic/dynesty/psutil/tfp-nightly). Laptop phase A committed 3924280; uncommitted 0.4.0-flagged A100 JSONs in the laptop worktree.
- hpc-cache-cleanup: "hpc-cache-off-home-phase2 (autolens_profiling#310, PR #311; record complete/2026/09/hpc-cache-off-home-phase2.md) removed every NUMBA_CACHE_DIR/MPLCONFIGDIR=/tmp export from main's hpc/ submits and added the cache block to activate.sh; the six hpc/batch_gpu/submit_breakdown_interferometer_mge_a100_* on this branch were excluded — drop their /tmp cache exports before this task merges (activate.sh now sets them under /mnt/ral/jnightin/.cache)."
- summary: Interferometer likelihood campaign 1/3: interferometer MGE breakdown cell on the shared harness (+ exploratory W~ func-list arm), JAX CPU + RAL A100 fp64 (mp on A100) across sma/alma/alma_high(/jvla), VRAM block re-test, ranked lever note + follow-up prompts.
