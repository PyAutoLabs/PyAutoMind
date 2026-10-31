
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

## howtogalaxy-chapter2
- issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/94
- issued: 2026-10-31
- session: Codex; session ID unavailable
- status: awaiting-ci
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/96
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtogalaxy-chapter2
- repos:
  - HowToGalaxy: feature/howtogalaxy-chapter2
- approval: approved chapter restructure, independent Galaxy adaptation and explicit Heart RED development override in current chat
- heart-red-override:
  - authorisation: "Yes, proceed with the full HowToGalaxy implementation despite Heart RED, validate it and get the PR up. Do prm if the required checks and shipping gates pass."
  - exact-red-reasons: "PyAutoFit: 2 commit(s) behind origin"; "release validation FAILED (stage integrate)" (2026-10-31T17:02:52.103664+00:00)
  - passed-gates: 31/31 scripts smoke; 32/32 notebook generation; 25 tutorial completeness; navigator/catalogue/search-memory/whitespace; independent review; full-size CPU JAX likelihood/gradient/batch finite
  - scope: development shipping only; current-turn prm conditional on all required checks, no release or failed-check bypass

## howto-chapter3
- issue: https://github.com/PyAutoLabs/HowToLens/issues/111
- issued: 2026-10-31
- session: Codex chat 01a19297-ff24-7bb0-87ce-437076a9d0a9
- status: awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howto-chapter3
- repos:
  - HowToLens: feature/howto-chapter3
  - HowToGalaxy: feature/howto-chapter3
- prompt: active/chapter_3_pixelizations_restructure_checkpoint.md
- approval: approved blocks and both Chapter 3 adaptations; explicit Heart RED implementation/validation override
- conflict-exception: human authorized separate Chapter 3 worktree alongside howtogalaxy-chapter2; no Chapter 2 edits
- tier: judge — merge mode: human /prm
- heart-red-override:
  - authorization: "Open both PRs despite Heart RED" (live human, 2026-10-31; development shipping only)
  - reasons: "PyAutoFit: 2 commit(s) behind origin"; "release validation FAILED (stage integrate)"
  - passed-gates: Lens smoke 44/44; Galaxy smoke 29/29; notebook generation, schema/code parsing, completeness, navigation, search-memory lint, catalogue reproducibility, whitespace and independent review
  - evidence: https://github.com/PyAutoLabs/HowToLens/issues/111#issuecomment-6546499778
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/112
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/95
- next: human /prm after required CI; adaptive Lens continuation remains pending five-block review
