# Parked tasks

Tasks that were started or scoped but are not currently in flight. Listed
here so they remain visible across machines instead of disappearing into
unindexed worktrees or stashes. Move an entry back to `active.md` (or to
`planned.md` if re-scoping is needed) when work resumes; on shipping,
write the dated `complete/<YYYY>/<MM>/<slug>.md` record instead.

## interferometer-delaunay-flaky-fitexception
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/640
- status: PHASE 1 COMPLETE (merged) — Phase 1a PyAutoFit#1408 MERGED (TEST_MODE=2 bypass tolerates single-eval FitException = resample-to-reject sentinel -1e99, mirrors fitness.py:256; +2 tests) + Phase 1b autolens_workspace#311 MERGED (un-park interferometer Delaunay + add to smoke; CI green 3.12+3.13). User-facing flake RESOLVED (now tolerated). Worktree removed, branches deleted. REMAINING = Phase 2 ONLY (not claimed): fix the underlying NaN/non-PD producer in PyAutoArray so the fit is CORRECT not merely tolerated — candidates: fnnls.py:134 divide-by-zero (45/250 local draws hit it) and/or degenerate Hilbert-mesh vertices in source_pix_2 (the failing stage). HARD: flake is CI-thread-dependent, not locally reproducible (250 Overlay-stage draws clean); needs source_pix_2 Hilbert-stage repro. NON-URGENT (Phase 1 made it non-fatal).
- worktree: none (Phase 1 shipped+cleaned; Phase 2 will claim PyAutoArray fresh)
- autonomy: supervised
- prompt: active/interferometer_delaunay_intermittent_qhull_nan.md
- note: follow-up to Delaunay cleanup #301/#307 (imaging Delaunay shipped green + smoke-gated; interferometer parked). Consolidates closed autolens_workspace#300/#308/#309. Phase 1 test-mode tolerance helps ALL FitException-prone pixelization scripts, not just this one. Complements PyAutoLens#639 raise_fit_exception (preserves cause).
- repos:
  - PyAutoFit: feature/interferometer-delaunay-flaky-fitexception (Phase 1a SHIPPED #1408)
  - autolens_workspace: feature/interferometer-delaunay-flaky-fitexception (Phase 1b pending)
  - PyAutoLens (not claimed — re-scoped out; issue #640 lives here)
  - PyAutoArray (Phase 2, not yet claimed)
