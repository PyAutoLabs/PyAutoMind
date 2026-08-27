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
  - PyAutoArray: feature/reconstruction-noise-map-zeroed-pixels (a7703a2e, pushed)
  - autolens_workspace: feature/reconstruction-noise-map-zeroed-pixels (e0484c2e, pushed)
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

    MEASURED ON REAL LENS FITS (PyAutoLens/PyAutoGalaxy/PyAutoFit cloned at main and run against
    this branch). At the evidence-optimal regularization coefficient (lambda*=1, interior to a
    9-point grid): Rectangular 28x28, 108 of 784 zeroed — old/new p50 1.0002, p90 1.069, p99 1.44,
    max 1.81; 21% of solved pixels move >1%, 9% >10%. Delaunay set up as the workspace's own
    delaunay.py does (zeroed_pixels=30) — p50 1.0045, p99 1.90, max 2.37, which answers this
    prompt's "Delaunay untested" caveat. With Delaunay's default zeroed_pixels=0 the property is
    unchanged to the bit. Downstream source flux and magnification through the S/N >= 5 cut moved
    0.00% in every case (lit-pixel counts identical: 7/7, 24/24, 121/121) — the pixels whose noise
    changes most sit at the mesh edge, where there is no flux to move. The earlier structural proxy
    predicted a uniform 1–2% shift and was wrong in shape: the real result is a negligible median
    with a long edge-concentrated tail.

    THE MEASUREMENT ALSO CAUGHT AN OVERCLAIM, now fixed. The first implementation asserted a
    biconditional — reconstruction == 0.0 exactly where the noise map is NaN. False: the NNLS solver
    also pins SOLVED pixels at exactly 0.0. On the 28x28 fit, 603 of 784 pixels read 0.0 while only
    108 are NaN, so 495 well-constrained pixels would have been read as unfitted. NaN => recon == 0
    holds; the converse does not. Library docstring, end-to-end test and all four workspace scripts
    corrected. (The test had passed only because its 3x3 fixture solves a single pixel.)

    The `griddata` bug reported earlier IS NOW FIXED on the workspace branch, per human instruction:
    `imaging` and `interferometer` `source_science.py` interpolated `reconstruction` and plotted it
    as the noise map; they now pass `reconstruction_noise_map`, matching their `group` and
    `multi_galaxy` siblings. All four scripts are consistent.

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
