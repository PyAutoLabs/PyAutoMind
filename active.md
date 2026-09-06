# Active Tasks

## physical-fast-rebuild-autolens
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/293
- issued: 2026-09-06
- prompt: active/physical_fast_rebuild_autolens.md
- session: claude --resume session_0151gQm9fk3XGLi5f18Urdba
- status: workspace-dev
- epic: ci-timing-fast-tests (phase 6 of 9)
- worktree: none — cloud session; branch `claude/ci-test-timing-epic-ke2lul` in the autolens_workspace_test clone
- repos:
  - autolens_workspace_test: claude/ci-test-timing-epic-ke2lul
- summary: |
    Phase 6 of the ci-timing-fast-tests epic: the physical + fast rebuild of the
    autolens_workspace_test smoke gate (27 entries, 434.7 s legacy CI / 396 s local
    cold), applying the phase-5 template plus the one pin-regeneration wave this
    repo needs. Coarser shared datasets (imaging 100x100@0.3", interferometer
    128x128@0.2", multi 80x80@0.2", with_lens_light 60x60@0.3"), every model
    matched to its data (lens light in the imaging models, shear where the truth
    has shear, a lens_sersic_light multi-wavelength dataset for the lens-MGE
    scripts, priors whose medians are the truth), mesh <= masked pixels, batch /
    over-sampling levers, delaunay_nn timing block to one repeat. Fable plan on
    the issue (per-script inventory taken first); implementation + local
    before/after timing delegated to Opus with the source stack installed in the
    container. After merge: PyAutoHeart `fast-tests` epoch line + compile-stall
    ledger note. Next: /prm.

## retire-gpu1-mig-exclusion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/220
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/222
- heart-ack: 2026-09-05 in-session, single reason "release validation FAILED (stage integrate)" — organism-scope (PyAutoHeart Release Integrate run 33951278577); nothing in this branch is in the release chain
- issued: 2026-09-05
- session: claude --resume session_0117cr7VQNhHL2HzkGwQCDun
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/retire-gpu1-mig-exclusion
- repos:
  - autolens_profiling: feature/retire-gpu1-mig-exclusion
- parallel-claim: autolens_profiling also claimed by delaunay-nn-breakdown (#219); "file sets disjoint (hpc/batch_gpu submits, hpc/README.md, activate.sh vs _profile_cli.py + scripts/imaging/likelihood_breakdown/delaunay.py); prompt out-of-scope note says merge order does not matter; own worktree taken under --auto safe"
