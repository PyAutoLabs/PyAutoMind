
## magnification-maps-wiring
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/818
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-maps-wiring
- repos:
  - PyAutoArray: feature/magnification-maps-wiring
  - PyAutoGalaxy: feature/magnification-maps-wiring
  - PyAutoLens: feature/magnification-maps-wiring
- prompt: active/magnification_maps_8d_wiring_pretty.md
- epic: cluster-strong-lensing (phase 8d)
- tier: judge — merge mode: human /prm (PyAutoArray → PyAutoGalaxy → PyAutoLens)

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

## likelihood-lifecycle-p4c-runners
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/54
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Science session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p4c-runners
- repos:
  - autolens_inference: feature/likelihood-lifecycle-p4c-runners (4c-0 tooling)
  - autolens_inference: feature/likelihood-lifecycle-p4c1 (4c-1 imaging/interferometer/datacube; worktree autolens_inference_4c1)
  - autolens_inference: feature/likelihood-lifecycle-p4c2 (4c-2 group/multi_galaxy/multi_dataset; worktree autolens_inference_4c2)
  - autolens_inference: feature/likelihood-lifecycle-p4c3 (4c-3 point/cluster/weak; worktree autolens_inference_4c3)
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/55 (4c-0 tooling; MERGED 2026-11-02 20d297dd via human /prm)
- compute-tracking: 4b RAL 413924 (A100 Delaunay, running), 413911 / 413913 (ral cores sweep, queued behind euclid pilots)
- prompt: active/likelihood_lifecycle_p4c_runners.md
- epic: likelihood-lifecycle (phase 4c)
- tier: judge — merge mode: human /prm

## gradient-correctness-sweep
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/517
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/gradient-correctness-sweep
- repos:
  - autolens_profiling: feature/gradient-correctness-sweep
- prompt: active/gradient_correctness_sweep.md
- phase: 0 triage (no code) — table → human approves order; sub-fixes get their own start_dev
- tier: judge — merge mode: human /prm

## latest-per-test-tie
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1758
- issued: 2026-11-02
- session: claude-code desktop (Opus 5.5)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/latest-per-test-tie
- repos:
  - PyAutoFit: feature/latest-per-test-tie
- prompt: active/latest_per_test_tie.md
- tier: judge — merge mode: human /prm
