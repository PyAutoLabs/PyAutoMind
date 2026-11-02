
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

## magnification-errors-source-science
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/610
- issued: 2026-10-31
- status: awaiting-merge (judge: Heart-RED-override ship → human /prm)
- pr: https://github.com/PyAutoLabs/autolens_workspace/pull/613
- heart-ack: STALE 'release validation incomplete: no rehearsal for current source' acknowledged live by the human 2026-11-02
- worktree: ~/Code/PyAutoLabs-wt/magnification-errors-source-science
- repos:
  - autolens_workspace: feature/magnification-errors-source-science
- released-claims: PyAutoFit (2026-11-02 by results-library-p2-completeness session — #1751 merged + released in 2026.11.1.1; wt PyAutoFit is detached on main)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1751 (MERGED 2026-10-31 e9d3c6a2 via human /prm; pending-release)
- prompt: active/magnification_errors_source_science.md
- epic: cluster-strong-lensing (phase 7b)
- heart-red-override: authorized live by the human 2026-10-31 ("override heart red, go ahead with 7b"); RED reasons quoted on the issue; development only
- tier: glance — merge mode: auto-merge on green if the Witness passes, post-merge summary

## rectangular-gradient-rtu-sparse
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/671
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/rectangular-gradient-rtu-sparse
- repos:
  - PyAutoArray: feature/rectangular-gradient-rtu-sparse
- witness-harness: autolens_profiling read-only via ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p6c-gradient-walls (6c closed 2026-11-02; that worktree is kept for this harness — do not switch its branch; autolens_profiling is now claimed by likelihood-lifecycle-p6d-gradient-ingest in its own worktree; human ruled PyAutoArray-only 2026-11-02)
- prompt: active/rectangular_fiducial_gradient_wrong_rtu_and_cpu_sparse.md
- tier: judge — merge mode: human /prm
- diagnosis: 1e9 = Isothermal 1e-8 core x mass centre exactly on an odd-grid (141x141, os_pix=1) source point at prior medians — not a mesh bug (posted #671, #509); re-scoped by human 2026-11-02 to the 2–5% autodiff-vs-FD error with MGE-60 lens light
- follow-up (human 2026-11-02): when active work is done, ASSESS whether this issue (centre-on-grid singularity and/or the few-% MGE gradient error) has impacted the PyAutoPulse / likelihood-lifecycle gradient campaign in general — which gradient.json verdicts are affected

## likelihood-lifecycle-p6d-gradient-ingest
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/512
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Science session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p6d-gradient-ingest
- repos:
  - PyAutoPulse: feature/likelihood-lifecycle-p6d-gradient-ingest
  - PyAutoPulse: feature/likelihood-lifecycle-p6d-freeze-gradient
  - autolens_profiling: feature/likelihood-lifecycle-p6d-gradient-ingest
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/87 (freeze --measurement; MERGED 2026-11-02 6d9a8a8d via human /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/88 (freeze day_zero_gradient at autolens_profiling 433bd778; judge, human /prm; merge before #513 lint re-run)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/513 (ingest 73 gradient witnesses; judge, human /prm)
- carried-from-6c: RAL 413890_0 (imaging/delaunay/ao CPU, 512 GB) record + wall + imaging RAL CPU memory value (6c closed 2026-11-02)
- prompt: active/likelihood_lifecycle_p6d_gradient_ingest.md
- epic: likelihood-lifecycle (phase 6d)
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
- tier: judge — merge mode: human /prm

## results-library-p4-package
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1756
- issued: 2026-11-02
- session: claude-code desktop (Opus 5.5)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/results-library-p4-package
- repos:
  - PyAutoFit: feature/results-library-p4-package
- prompt: active/results_library_p4_package.md
- epic: results-library (phase 4)
- tier: judge — merge mode: human /prm
