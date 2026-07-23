# Purge the autoconf-era legacy surface from PyAutoNerves

Type: refactor
Target: PyAutoNerves
Repos:
- PyAutoNerves
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Why

After the `autoconf` → `autonerves` rename (PyAutoNerves#135), the repo still
carries a legacy surface from the pre-rename era. Three distinct problems are
tangled together and were separated by survey on 2026-07-23:

1. **Untracked rename leftovers.** `autoconf/`, `test_autoconf/`,
   `autoconf.egg-info/`, `build/` and `bad/` sit in the working copy but are
   **not tracked** — `git grep -ril autoconf` over tracked files returns nothing.
   `autoconf/` and `test_autoconf/` contain only `__pycache__`, yet still resolve
   as a namespace package (`import autoconf` →
   `_NamespacePath(['.../PyAutoNerves/autoconf'])`), so they shadow imports
   rather than sitting inert.

2. **A test that litters the repo root.** `bad/` is regenerated on every test run
   by `test_autonerves/test_config.py` (`BAD_PATH = "bad/path"`, `os.makedirs`
   into CWD, never cleaned up). Deleting it without fixing the producer is a
   no-op.

3. **Dead one-shot tooling.** `scripts/` holds four drivers from the original
   config bootstrap, years dormant, wired into no CI and referenced from no
   workspace. Two are already broken on their own imports:
   - `edenise.py` imports `autofit.tools.edenise`, **removed from PyAutoFit** —
     `ImportError` on run.
   - `convert_prior_configs.py` imports `oyaml`, not a declared dependency.
   - `convert_config.py` is the `.ini` → YAML migration, long since run.
   - `generate_priors.py` is a CLI over `autonerves/json_prior/generate.py`,
     whose only other consumer is its own test.

## Scope

Five steps, each independently shippable.

**Step 0 — local cruft (no PR).** Remove the untracked `autoconf/`,
`test_autoconf/`, `autoconf.egg-info/`, `build/`, `bad/` from the working copy.

**Step 1 — stop `bad/` regenerating.** Move `test_path_does_not_exist` and
`test_path_empty` in `test_autonerves/test_config.py` onto `tmp_path`; delete the
`BAD_PATH` constant and the `remove_path()` helper.

**Step 2 — remove dead EDEN tooling.** Delete `PyAutoNerves/eden.yaml` and
`scripts/edenise.py` — the PyAutoNerves leg of
`draft/refactor/pyautofit/remove_eden_packaging_tooling.md`.

`PyAutoFit/eden.yaml` is **descoped** from this task: the branch survey on
2026-07-23 found PyAutoFit claimed by the `testmode-env-drift` worktree
(`feature/testmode-env-drift`, PRs open awaiting merge). `autofit.tools.edenise`
is already gone from PyAutoFit main, so only the orphan `eden.yaml` remains
there — a one-file follow-up once that claim releases. The eden draft stays open
until then.

**Step 3 — remove the one-shot config-migration tooling.** Delete
`scripts/convert_config.py`, `scripts/convert_prior_configs.py`,
`scripts/generate_priors.py`, `autonerves/json_prior/generate.py`,
`test_autonerves/json_prior/test_generate.py`, and the orphan
`priors/subconfig.json` (a stray output artifact of `generate_priors.py`). Both
`scripts/` and `priors/` disappear.

**Step 4 — sort PR #136.** Force-push with only the test-fixture re-anchor,
reverting `autonerves/__init__.py` to `2026.7.9.1`.

## Guardrails

- **`autonerves/json_prior/config.py` is NOT in scope** — it is the live half,
  imported by `autonerves/conf.py` and re-exported from `autonerves/__init__.py`
  (`default_prior`, `make_config_for_class`, `path_for_class`,
  `JSONPriorConfig`). Only the sibling `generate.py` goes.
- **Do not bump `__version__` on any library main.** The release model is
  wheels+tags-only (PyAutoBuild#118/#120); main's `__version__` is deliberately
  stale and hand-bumping it rebuilds the cascade engine #120 deleted. This is
  precisely why PR #136 is being trimmed rather than merged as-is.
- `generate.py` is an import surface. Confirmed clean before deletion: no
  consumer in any PyAuto library, workspace, or doc outside its own script and
  test. Re-run `grep -rn "json_prior import generate\|json_prior.generate"`
  before deleting; if a live consumer surfaces, re-scope.
- Run the full `test_autonerves` suite (151 tests at survey time) before each
  push.
- Library-only; no downstream workspace impact expected.

## Related

- Ships the PyAutoNerves leg of
  `draft/refactor/pyautofit/remove_eden_packaging_tooling.md`; that prompt stays
  open for its one remaining file (`PyAutoFit/eden.yaml`).
- Separately: PyAutoNerves#100 is fully shipped (5 library + 7 workspace PRs all
  merged; ledger at `complete/2026/04/workspace-version-config-check.md`) and was
  simply never closed on GitHub. Close it as part of this pass.
