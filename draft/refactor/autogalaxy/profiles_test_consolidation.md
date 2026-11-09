# Profiles test consolidation

Type: refactor
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- hygiene
- mge
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Filed: 2026-11-09
Epic: profiles-unified-api
Phase: 4
Consequence: notify
Witness: a script in the PR extracts every `(profile class, quantity, grid point, expected value, tolerance)` tuple asserted under `test_autogalaxy/profiles/` before and after and the two sets are identical; `pytest test_autogalaxy/profiles -q` green; the PR reports test-function and test-line counts before and after (target: the 66 parity tests gone, test lines down by at least 1,500)
Review-minutes: 1
Unattended: ready
Lane: any

Phase 4 of the profiles-unified-api epic (`draft/refactor/autogalaxy/profiles_unified_api_epic.md`;
report §1.5, §7 phase 4; ruling D5: in). Depends on phases 0–3 being merged. Test-only: no file
under `@PyAutoGalaxy/autogalaxy/` changes.

## Change

1. Delete the 66 hand-written cross-variant parity tests (27 in
   `@PyAutoGalaxy/test_autogalaxy/profiles/test_light_and_mass_profiles.py`, 39
   "elliptical vs spherical" tests across `profiles/light/standard/test_*.py` and
   `profiles/mass/**/test_*.py`); the phase-0 contract tests cover every one of them for every
   class, not only the hand-picked ones.
2. Convert the per-profile pinned-value tests (~430 functions of the shape "construct one profile,
   evaluate one quantity at one point, `pytest.approx` one number") into `pytest.mark.parametrize`
   tables — one table per quantity per test module, rows of `(kwargs, grid, expected, rel)`. The
   extraction script in the witness is written first and run on `main` so the row set is pinned
   before any test moves. Keep as ordinary functions anything that is not that shape (xp-forwarding
   spies, `monkeypatch` tests, JAX-free tracer tests, `test_deflections_memo.py`, `test_mge.py`,
   `test_validate.py`, `test_model_constraint.py`, `test_model_figure_semantics.py`).
3. Drop tests that only re-assert what the golden file pins (argument names, defaults, class of
   `lp_instance_from` output), citing the golden-file key in the commit message for each.

## Gotchas

Keep tolerances identical per row (several files mix `1e-2`, `1e-3`, `1e-4`); `pytest.approx` on
autoarray wrappers compares `.array` — keep whichever form each test used; do not "fix" a pinned
number that looks wrong — file it via `/bug` instead.

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-0/-home-user/cd6c1ec3-dd35-55c4-a663-eb8c309de811/scratchpad/intake_raw/p4.md -->
