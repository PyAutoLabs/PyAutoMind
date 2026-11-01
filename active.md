
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## r2-pages-function-access
- issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4
- issued: 2026-10-29
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/r2-pages-function-access
- repos:
  - ECLIPSE_lens_catalogue: feature/r2-pages-function-access
- tier: judge — merge mode: human /prm

## hpc-campaign-p5a-assistant
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/172
- issued: 2026-10-30
- session: claude-code desktop (WSL), PyAutoLabs session (background fork)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/hpc-campaign-p5a-assistant
- repos:
  - autolens_assistant: feature/hpc-campaign-p5a-assistant
- prompt: active/hpc_campaign_p5a_assistant.md
- epic: hpc-campaign (phase 5)
- heart-red-override: authorized live by the human 2026-10-30 ("Override + approve") for hpc-campaign phase 5; RED reasons quoted on the issue; development only, merge via /prm
- tier: judge — merge mode: human /prm
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/173 (MERGED 2026-10-31)
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/174
- resume: 2026-10-31 — #173 merged; #174 (feature/hpc-campaign-p5a-v2, retargeted to main) green on boundary + colab, RED on wiki-currency only because it audits RELEASED PyAutoFit, which lacks autofit.campaign (pending-release) — /prm #174 after the next PyAutoFit release (rerun wiki-currency first); then close out p5a

## sky-orientation-p2
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/115
- issued: 2026-10-31
- session: claude-code desktop (WSL), PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/sky-orientation-p2
- repos:
  - euclid_strong_lens_modeling_pipeline: (no branch; next sub-phase 2c)
- prompt: active/sky_orientation_euclid_dr1_and_library.md
- epic: sky-orientation (phase 2: 2.0 land v5 branch → 2a catalogue fix → 2b–2e)
- heart-red-override: extended live by the human 2026-10-31 to phase 2 ("Yes, extend it"); development only, merge via /prm
- merged: euclid#116 (2.0 land v5 branch) 2026-10-31
- merged: euclid#117 (2a catalogue frame fix) 2026-10-31
- run: RAL 413687 sky_frame_bundle MODE=dry over inspect/dr1_catalogue_v5 (private code /mnt/ral/jnightin/active/euclid_dr1_p2c_code @910e5c8; submitted via scratch hpc/sync copy) → NEXT read dry report, MODE=live, re-package; then re-render pilot (~50, human review), 2b docs
- tier: judge — merge mode: human /prm

## magnification-errors-source-science
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/610
- issued: 2026-10-31
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-errors-source-science
- repos:
  - autolens_workspace: feature/magnification-errors-source-science
  - PyAutoFit: feature/magnification-errors-source-science
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1751 (MERGED 2026-10-31 e9d3c6a2 via human /prm; pending-release)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1751
- prompt: active/magnification_errors_source_science.md
- epic: cluster-strong-lensing (phase 7b)
- heart-red-override: authorized live by the human 2026-10-31 ("override heart red, go ahead with 7b"); RED reasons quoted on the issue; development only
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary

## likelihood-lifecycle-p6c-gradient-walls
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/509
- issued: 2026-11-01
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p6c-gradient-walls
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p6c-gradient-walls
- prompt: active/likelihood_lifecycle_p6c_gradient_runs.md
- epic: likelihood-lifecycle (phase 6c)
- compute: RAL submit checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2dg @ 97cdc88; human go per batch (batch 0 probe: go given 2026-11-01)
- tier: judge — merge mode: human /prm

## simulate-if-needed-workspace-sweep
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/268
- issued: 2026-11-01
- session: claude-code remote (cloud), https://claude.ai/code/session_016nhQ8NyQo2s3YUk8eUrrB3
- location: cloud session clones (no local task worktree)
- status: workspace-dev
- repos:
  - autogalaxy_workspace: claude/pyautoarray-simulate-helper-yuqd16
  - autolens_workspace_test: claude/pyautoarray-simulate-helper-yuqd16
  - autogalaxy_workspace_test: claude/pyautoarray-simulate-helper-yuqd16
  - autolens_workspace: claude/pyautoarray-simulate-helper-yuqd16
  - HowToLens: claude/pyautoarray-simulate-helper-yuqd16
  - HowToGalaxy: claude/pyautoarray-simulate-helper-yuqd16
  - autocti_workspace: claude/pyautoarray-simulate-helper-yuqd16
  - euclid_strong_lens_modeling_pipeline: claude/pyautoarray-simulate-helper-yuqd16
  - PyAutoBrain: claude/pyautoarray-simulate-helper-yuqd16
- prompt: active/simulate_if_needed_workspace_sweep.md
- tier: glance — merge mode: human /prm, after the PyAutoArray release carrying PyAutoArray#670
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/269
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/353
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/132
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/612
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/120
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/99
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/39
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/118
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/549
- resume: 2026-11-01 — sweep complete: 7 workspace sweep PRs (536 blocks) + euclid#118 (invariant token) + PyAutoBrain#549 (hygiene lever). Workspace sweep PRs merge after the PyAutoArray release; euclid#118 and Brain#549 can merge any time. No rewrite needed: autofit_workspace (intentional raw guards), autolens_workspace_developer + autolens_profiling (non-standard: extra argv/cwd)
- blocked-repos: none
- shared-claims: autolens_workspace (also magnification-errors-source-science), HowToLens + HowToGalaxy (also howto-chapter2-format) , euclid_strong_lens_modeling_pipeline (also sky-orientation-p2) — swept on human instruction 2026-11-01 despite the claims; neither task's branch was on the remote, overlap noted in each PR

## howto-prose-format
- issue: https://github.com/PyAutoLabs/HowToLens/issues/119
- issued: 2026-11-01
- session: Codex desktop, current chat
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs-wt/howto-prose-format
- prompt: active/howto_prose_format.md
- repos:
  - HowToLens: feature/howto-prose-format
  - HowToGalaxy: feature/howto-prose-format
- merge-authorization: User requested PR, prm, merge and local pull in this session.
- resume: User authorized audit-based recovery. Restore missing runtime/plot/evidence outputs and compactness demonstration within existing tutorials; repair Galaxy notebook prose loss. Fresh Heart STALE 2026-11-01T18:43:28Z (release rehearsal absent only), after clean library fast-forwards. Existing formatter changes preserved.
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/122
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/100
