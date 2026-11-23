
## autonomous-orchestrators-p4c
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/574
- issued: 2026-11-04
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: human-ops (pilot run; no worktree — briefs land in PyAutoMind/batches/ by the human)
- prompt: active/autonomous_orchestrators_p4c_pilot_run.md
- epic: autonomous-orchestrators (phase 4c of 4a–4c)
- pre-check: open shadow tick on system python3.10, minimal env — 6 notify proposals, 0 spawns (2026-11-04)
- tier: judge — merge mode: human /prm

## pyautolens-ii-case-studies
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/147
- issued: 2026-11-12
- session: OpenAI Codex desktop
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/pyautolens-ii-case-studies
- repos:
  - autolens_workspace_developer: feature/pyautolens-ii-case-studies
- prompt: active/pyautolens_ii_case_studies.md
- coordination: human approved PyAutoLens/paper_jax/paper.md-only edits alongside magnification-maps-wiring; no library code changes
- next: validate JWST PSF/noise and export calibrated ALMA visibilities, then joint gradient check and bounded pilots
- tier: judge — merge mode: human /prm

## sed-waveband-search-cap
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (79ac305d-a450-40fe-b02b-8b0ccf4e159a)
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1793
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/140
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1793
- resumed: 2026-11-22, Codex desktop, Q17 option 1
- worktree: /home/jammy/Code/PyAutoLabs-wt/sed-waveband-search-cap
- repos:
  - PyAutoFit: feature/sed-waveband-search-cap
  - euclid_strong_lens_modeling_pipeline: feature/sed-waveband-search-cap
- question: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136#issuecomment-7034635460
- prompt: active/sed_chain_waveband_fit_can_spin_forever.md
- validation: PyAutoFit 936b073d4 passed the timeout and conformance checks, including a real sampler and empty-posterior recovery. Euclid 89b7f7c passed 511 fast tests and all nine smoke scripts. Two sequential synthetic plateau fits hit a reduced call budget and wrote QA markers.
- next: Human review of PyAutoFit #1793 first, then Euclid #140. The maintainer will run the original tile on RAL after merge and report on Euclid #136.
- tier: judge — supervised, human review and /prm

## numba-wtilde-validation-legs-stall
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/73
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (da579b3a-de74-4060-a9fc-d5b17ae8c5c4)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/autolens_inference/issues/73#issuecomment-7035552262
- verdict: https://github.com/PyAutoLabs/autolens_inference/issues/73#issuecomment-7035547161
- prompt: active/numba_wtilde_validation_legs_stall_nautilus.md
- note: research, no claim/worktree. Rectangular SMA: zero source after source_pix[1] makes mass_total[1] flat on BOTH routes (A100 + numba seed 0 "converged" rows invalid). Datacube: ~50% not-PD evaluations, in-run values don't reproduce serially (+106 nat outlier). Remedy pick parked
- tier: supervised — merge mode: human /prm

## likelihood-lifecycle-p5a-nerves
- issue: https://github.com/PyAutoLabs/PyAutoNerves/issues/222
- issued: 2026-11-23
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5 orchestrator)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/likelihood-lifecycle-p5a-nerves
- repos:
  - PyAutoNerves: feature/likelihood-lifecycle-p5a-nerves
- prompt: active/likelihood_lifecycle_p5a_nerves_environment.md
- epic: likelihood-lifecycle (phase 5A of 5A–5H)
- tier: judge — merge mode: human /prm

## plot-utils-critical-curves-docstrings
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/747
- issued: 2026-11-23
- session: shift worker 2026-11-23-am2 (codex:bdcf6dbbd92948e69d9dd55313e27d37)
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/748
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/748
- worktree: /home/jammy/Code/PyAutoLabs-wt/plot-utils-critical-curves-docstrings
- repos:
  - PyAutoGalaxy: feature/plot-utils-critical-curves-docstrings
- prompt: active/plot_utils_critical_curves_default_docstring_drift.md
- tier: notify
