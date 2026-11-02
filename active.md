
## magnification-maps-image-plane
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/689
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/magnification-maps-image-plane
- repos:
  - PyAutoGalaxy: feature/magnification-maps-image-plane
  - PyAutoLens: feature/magnification-maps-image-plane
  - autolens_workspace: feature/magnification-maps-image-plane
- prompt: active/magnification_maps_8a_image_plane.md
- epic: cluster-strong-lensing (phase 8a)
- tier: judge — merge mode: human /prm (PyAutoGalaxy → PyAutoLens → autolens_workspace)

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

## rectangular-gradient-rtu-sparse
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/671
- issued: 2026-11-02
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: library-shipped, awaiting /prm
- worktree: ~/Code/PyAutoLabs-wt/rectangular-gradient-rtu-sparse
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/672 (pending-release; judge, human /prm)
- root-cause: border relocator max(|y'|) tie gradient unstable under jit (fixed in #672); 1e9 HST = Isothermal core at grid-point centre (profiling-side, #509)
- heart-ack: STALE "release validation incomplete: no rehearsal for current source" — acknowledged by human at ship 2026-11-02
- repos:
  - PyAutoArray: feature/rectangular-gradient-rtu-sparse
- witness-harness: autolens_profiling read-only via ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p6c-gradient-walls (6c closed 2026-11-02; that worktree is kept for this harness — do not switch its branch; autolens_profiling is now claimed by likelihood-lifecycle-p6d-gradient-ingest in its own worktree; human ruled PyAutoArray-only 2026-11-02)
- prompt: active/rectangular_fiducial_gradient_wrong_rtu_and_cpu_sparse.md
- tier: judge — merge mode: human /prm
- diagnosis: 1e9 = Isothermal 1e-8 core x mass centre exactly on an odd-grid (141x141, os_pix=1) source point at prior medians — not a mesh bug (posted #671, #509); re-scoped by human 2026-11-02 to the 2–5% autodiff-vs-FD error with MGE-60 lens light
- follow-up (human 2026-11-02): when active work is done, ASSESS whether this issue (centre-on-grid singularity and/or the few-% MGE gradient error) has impacted the PyAutoPulse / likelihood-lifecycle gradient campaign in general — which gradient.json verdicts are affected

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
