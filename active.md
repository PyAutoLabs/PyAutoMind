# Active Tasks

## transformed-message-factor-gradient-unpack
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1501 (issued 2026-08-19)
- issued: 2026-08-19
- prompt: active/16_transformed_message_factor_gradient_unpack.md
- status: HOLD — do not start dev. Fix-or-delete hangs off the PyAutoFit#1498 logpdf-contract
  decision (parked #1500 design bundle); dead code (zero production callers), crashes on first
  call if ever exercised.
- external: community PR https://github.com/PyAutoLabs/PyAutoFit/pull/1502 (@trexfr-ops) targets
  this exact unpack — review via /community before any local work; the #1498 adjudication decides
  whether the method should exist at all.
- registered: 2026-08-19 by the wake_up session — the issuing session (claude/autofit-priors-messages-audit-ylvenv)
  filed the prompt + issue but not this entry, tripping Lifecycle Drift on main.
- repos-none-claimed: this entry claims NO repos — one line deliberately, not 2-space bullets.

## reconstruction-noise-map-zeroed-pixels
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/492
- issued: 2026-08-27
- prompt: active/reconstruction_noise_map_solver_mismatch.md
- session: claude --resume session_01Lkq5ww6eLEvJgPFGMgMU1C
- status: ready-to-ship — both branches pushed, no PRs opened yet (awaiting sign-off)
- worktree: ~/Code/PyAutoLabs-wt/reconstruction-noise-map-zeroed-pixels
- repos:
  - PyAutoArray: feature/reconstruction-noise-map-zeroed-pixels (051cfd3e, pushed)
  - autolens_workspace: feature/reconstruction-noise-map-zeroed-pixels (e170560, pushed)
- summary: |
    Implemented in a web-github session directly against fresh clones — the `worktree:` path above
    is a CLAIM on the two repos, not a directory that exists. A local session resuming this will hit
    reference.md's "worktree root MISSING" branch: fetch the two pushed branches rather than
    treating the task as abandoned.

    SHIPPED ON BRANCH, NOT MERGED. Library: `solve_ids_to_keep` is now the single predicate for
    "did the solve subset the system?", read by both `reconstruction` and
    `reconstruction_covariance_matrix`; the covariance is formed on that index set and scattered
    back with NaN at the excluded pixels; three comments mislabelling `mapper_indices` as
    edge-zeroing corrected; `MockMapper` gained the `mesh` accessor it already stored. 10 new tests
    (9 unit + 1 end-to-end invariant). Full suite 1177 passed, 55 skipped. Workspace: documentation
    only, 4 scripts + 4 regenerated notebooks, no code lines changed.

    TWO THINGS THE REVIEWER MUST SEE:
    1. The magnitude of the value change on the SOLVED pixels was NOT measured on a real lens fit —
       this environment has no PyAutoLens. Direction is mathematically guaranteed ([A^-1]_keep >=
       (A_keep)^-1, so noise always drops); a structural proxy gives 0.983–0.992 median, but that is
       the same kind of proxy that understated a related effect 10x in this prompt's own history.
       Measure on a real fit before the release note quotes a number.
    2. Found while editing the workspace, NOT fixed: `imaging` and `interferometer`
       `source_science.py` compute `interpolated_noise_map = griddata(values=reconstruction, ...)` —
       the reconstruction, not the noise map, then plot it as "Source Reconstruction Noise Map".
       `group` and `multi_galaxy` pass `reconstruction_noise_map` correctly. Pre-existing, unrelated
       to this task, and changes a displayed figure, so it needs its own sign-off. Worth an /intake.

    Scope is Defect 2 of the prompt ONLY: `reconstruction_covariance_matrix` inverts the full
    `curvature_reg_matrix` while `reconstruction` solves the `zeroed_ids_to_keep` submatrix and
    scatters back exact zeros. Defect 1's docstring caveat shipped (PyAutoArray#472) and its maths
    stays deferred at `low`; Defect 3 is CLOSED as deliberate (PyAutoArray 84b9ed42); the
    free-lens-mass lambda measurement is deferred as research. The prompt carries a
    "SCOPED FOR DEV 2026-08-27" section recording all of this — read it before the older text,
    which contradicts it.

    Human decisions taken at plan time: excluded pixels report NaN (not 0), and the convention is
    documented in the `reconstruction_noise_map` docstring AND the four autolens_workspace
    `source_science.py` scripts — which is why the workspace repo is claimed too. The workspace leg
    is a second PR behind the library-first merge gate.

    Next step: /start_library.
