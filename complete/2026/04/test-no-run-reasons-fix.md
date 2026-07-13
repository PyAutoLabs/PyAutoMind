## test-no-run-reasons-fix
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/56
- completed: 2026-04-22
- library-pr: https://github.com/PyAutoLabs/PyAutoBuild/pull/57
- note: Two-line assertion fix in `tests/test_result_collector.py::test_parse_no_run_reasons` — the test was asserting `"GetDist" in reasons` but commit `e72a077` ("Rename per-sampler plotter stems to snake_case") had renamed the YAML entry to `get_dist`, so `pytest tests/` was failing on every run. Surfaced while shipping PR #55 (howtofit-register), where the failing test had to be `--deselect`ed. Switched assertions to `get_dist` to match the YAML. No production code or config changed. 40/40 tests now green with no deselects.

## Original prompt

Fix the pre-existing `test_parse_no_run_reasons` test failure in @PyAutoBuild.

## Root cause

Commit `e72a077` ("Rename per-sampler plotter stems to snake_case") renamed
`GetDist` → `get_dist` in `autobuild/config/no_run.yaml`:

```yaml
autofit:
- get_dist # Cant get it to install, even in optional requirements.
```

But `tests/test_result_collector.py::test_parse_no_run_reasons` still asserts
the old CamelCase key at lines 106-107:

```python
reasons = parse_no_run_reasons(config_path, "autofit")
assert "GetDist" in reasons
assert "install" in reasons["GetDist"].lower()
```

Result: the test has been broken on `main` since that rename. Every `pytest`
run on PyAutoBuild fails with:

```
AssertionError: assert 'GetDist' in {..., 'get_dist': 'Cant get it to install, ...', ...}
```

This was surfaced while shipping PR #55 (register-howtofit build target) —
the test had to be `--deselect`ed to keep the ship-library subagent from
stopping on an unrelated pre-existing failure.

## Fix

Update `tests/test_result_collector.py` lines 106-107 to expect the snake_case
key `"get_dist"` (matching what the YAML actually contains). No YAML change
needed — the snake_case stem is the intentional new convention.

## Acceptance

- `pytest tests/` — all 40 tests pass (no deselects needed).
- No change to any production code, only the test assertions.
