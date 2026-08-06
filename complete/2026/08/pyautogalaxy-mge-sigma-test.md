The two `*_default_sigma_list_is_bitwise_unchanged` guards added with
PyAutoGalaxy#549 compared the implementation's per-element scalar power
(`gaussian.sigma = 10 ** log10_sigma_list[i]`, `autogalaxy/analysis/model_util.py`
:190 and :271) against a vectorised `10 ** np.linspace(...)` in the test. numpy
does not guarantee its scalar and SIMD power loops agree bit for bit, so the
tests failed on AVX-512 hosts. Fix builds the expected ladder element-wise so
both sides take the same numpy code path — test-only, no library source touched.

## PRs

- PyAutoGalaxy#551 → `b8988200`, merged 2026-08-05T21:40Z (issue
  PyAutoGalaxy#550 closed as completed). Branch
  `claude/pyautogalaxy-mge-sigma-test-3neq07` (fix commit `91eb878a`).

## What was established (beyond the fix)

- **Reproduced, not assumed**: the cloud runner was itself AVX-512
  (avx512f/bw/cd/dq/vl/vnni) with numpy 2.4.6 — pytest failed on the unmodified
  tree exactly as reported and passed after.
- **Footprint wider than the report**: the prompt named one index
  (mask_radius=3.0/n=20 → 18); mge also drifts at 3.5/30 index 8, and the POINT
  test drifts at 0.1/10 indices 4 and 9 and 0.05/5 index 3. Both tests were
  broken.
- **Guarantee NOT weakened** (explicit human instruction): `pytest.approx`
  deliberately not used; docstrings keep the exactness reasoning verbatim and
  now carry a PORTABILITY TRAP note so a later tidy-up does not re-vectorise
  the expectation.
- **Control test**: perturbing the implementation defaults by a relative 1e-7
  still fails BOTH tests, so the element-wise expectation is not vacuous;
  implementation restored, only the test file changed.
- Validation at ship time: `test_autogalaxy/analysis/test_model_util.py` 29
  passed; full `test_autogalaxy/` 1004 passed, 3 skipped (Python 3.11 cloud
  sandbox; change is pure-Python test code).
- Neighbouring `pytest.approx(..., 1.0e-8)` assertions at L129/L237 are
  tolerance-based by design and were deliberately untouched.

## Loose-end closure (2026-08-06)

The active.md entry said "NO PR opened" — stale: PR #551 was opened and merged
2026-08-05. This record retires the entry; the merged remote branch was deleted
as part of the same cleanup.

## Original prompt

# Bug in PyAutoGalaxy: the MGE bitwise sigma-ladder tests fail on

Type: test
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised

Bug in PyAutoGalaxy: the MGE bitwise sigma-ladder tests fail on AVX-512 hardware. In PyAutoGalaxy, test__mge_model_from__default_sigma_list_is_bitwise_unchanged and test__mge_point_model_from__default_sigma_list_is_bitwise_unchanged in test_autogalaxy/analysis/test_model_util.py assert exact equality between two different numpy code paths. The PyAutoGalaxy implementation builds each sigma with a per-element scalar power, gaussian.sigma = 10 ** log10_sigma_list[i] at autogalaxy/analysis/model_util.py line 190, while the test builds its expectation with a vectorised 10 ** np.linspace(...). numpy does not guarantee the scalar and SIMD power loops agree bit for bit; on an x86-64-v4 / AVX-512 CPU they differ by 1 ULP at index 18, exactly the index pytest reports. Reproduced in isolation with numpy 2.4.6. The effect is cosmetic, not functional: the run identifier quantizes at RESOLUTION 1e-8 and this drift is ~1e-16 relative, so no identifier moves and no archived fit is orphaned. But the tests are green on GitHub runners and red on AVX-512 developer machines, so the regression guard added with PyAutoGalaxy#549 is not portable. Fix in PyAutoGalaxy by building the expected ladder element by element the way the implementation does, or by comparing with a tolerance far below the 1e-8 identifier resolution.

<!-- formalised by the Intake (Conception) Agent on 2026-08-05 from user-intake -->
