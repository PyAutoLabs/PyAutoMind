
## magnification-maps-source-plane
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/673
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-shipped, awaiting-merge (judge → human /prm: Array#674 → Galaxy#691 → Lens#816 → ws#615)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/674
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/691
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/816
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/615
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/674
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/691
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/816
- heart-ack: STALE 'release validation incomplete: no rehearsal for current source' acknowledged live by the human 2026-11-02
- worktree: ~/Code/PyAutoLabs-wt/magnification-maps-source-plane
- repos:
  - PyAutoArray: feature/magnification-maps-source-plane
  - PyAutoGalaxy: feature/magnification-maps-source-plane
  - PyAutoLens: feature/magnification-maps-source-plane
  - autolens_workspace: feature/magnification-maps-source-plane
- prompt: active/magnification_maps_8b_source_plane.md
- epic: cluster-strong-lensing (phase 8b)
- tier: judge — merge mode: human /prm (PyAutoArray → PyAutoGalaxy → PyAutoLens → autolens_workspace)

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

## likelihood-lifecycle-p4a-validation-tooling
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/51
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p4a-validation-tooling
- repos:
  - autolens_inference: feature/likelihood-lifecycle-p4a-validation-tooling
- prompt: active/likelihood_lifecycle_p4a_validation_tooling.md
- epic: likelihood-lifecycle (phase 4a)
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/52 (MERGED 2026-11-02 94ffa86c via human /prm)
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/53 (Optimal-only scope + Delaunay numba seed 0; MERGED 2026-11-02 9bafc6bc via human /prm)
  - autolens_inference: feature/likelihood-lifecycle-p4a-scope-optimal
- tier: judge — merge mode: human /prm

## results-library-p5a-assistant
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/176
- issued: 2026-11-02
- session: claude-code desktop (Opus 5.5)
- status: workspace-shipped, awaiting-merge (judge → human /prm; wiki-currency waits on a PyAutoFit release)
- worktree: ~/Code/PyAutoLabs-wt/results-library-p5a-assistant
- repos:
  - autolens_assistant: feature/results-library-p5a-assistant
- prompt: active/results_library_p5a_assistant.md
- epic: results-library (phase 5a)
- tier: judge — merge mode: human /prm
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/177
- heart-ack: STALE 'release validation incomplete: no rehearsal for current source' (human 2026-11-02)

## howtolens-ch2-explanations
- issue: https://github.com/PyAutoLabs/HowToLens/issues/123
- issued: 2026-11-02
- session: Codex 01a19c86-3bab-7183-a1e1-a04ff3e80c7f
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/howtolens-ch2-explanations
- repos:
  - HowToLens: feature/howtolens-ch2-explanations
- approval: five prose/code blocks approved 2026-11-02; no merge authority

## gradient-campaign-impact
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/515
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/gradient-campaign-impact
- repos:
  - autolens_profiling: feature/gradient-campaign-impact
  - PyAutoPulse: feature/gradient-campaign-impact
- prompt: active/gradient_campaign_impact_of_border_tie_and_centre_singularity.md
- origin: human request during PyAutoArray#671 (record complete/2026/11/rectangular-gradient-rtu-sparse.md)
- compute: any RAL leg needs an explicit human go; private checkout, partition ral
- tier: judge — merge mode: human /prm
