# subhalo_recovery smoke test: iterative dkappa correlation collapsed (0.032 vs 0.3)

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

`autolens_workspace_test` **main** smoke gate is RED (since ~2026-07-17 13:39,
after the dpie-lenstool-default release): `scripts/potential_correction/
subhalo_recovery.py` fails its iterative assertion —

    AssertionError: iterative dkappa correlation 0.032 below threshold 0.3
    (subhalo_recovery.py:166)  # assert corr_iter > 0.3

19/20 smoke scripts pass; only this one. The ONE-SHOT correction still passes
(corr > 0.5, line 133), but the ITERATIVE correction (`iter_fit`, line 155)
recovers essentially zero correlation (0.032, ~10x below threshold — not
marginal/flaky, a hard collapse). Reproduced identically on main run
29597679558 and on an unrelated PR branch (env-scrubbed-baseline #180), so it
is a real main regression, not PR-specific or seed noise.

**Not caused by** the build-chain env-profile work (#161 step 3) — that change
is a no-op for PYAUTO_ vars on CI and autofit/autogalaxy smoke passed; it
merely SURFACED this because its PR smoke gate ran. **Blocks** merging Phase 3
step 3's autolens leg (alwt#180) until green.

Investigate: what changed in the iterative potential-correction path between
the last green autolens_workspace_test main smoke and 13:39 2026-07-17 — a
PyAutoLens library change, a dpie-lenstool workspace change, or a regularization
/ pixelization default. Bisect the iterative `pair_dpsi_data_obj` / dkappa
metric path. The one-shot passing while iterative collapses points at the
iterate loop, not the base correction.

<!-- filed 2026-07-17 from the build-chain Phase 3 step-3 smoke gate (alwt#180); regression pre-exists on main -->
