# Heart's local smoke runner cannot run any CTI workspace — no autocti entry

Type: maintenance
Target: pyautoheart
Repos:
- @PyAutoHeart
Themes:
- ci-smoke
- cti
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-24

`PyAutoHeart/heart/smoke.py` is the local smoke runner — "one isolated
environment per workspace, prepared from the workspace-owned installer", the
local mirror of what CI does. Which workspaces it can prepare is declared in
`config/repos.yaml` under the `smoke:` block, and **the CTI repos are absent
from it entirely**:

```yaml
smoke:
  import_names:
    PyAutoNerves: autonerves
    PyAutoFit: autofit
    PyAutoArray: autoarray
    PyAutoGalaxy: autogalaxy
    PyAutoLens: autolens          # <- no PyAutoCTI
  workspaces:
    autofit: {directory: autofit_workspace, chain: [...]}
    autogalaxy: {...}
    autolens: {...}
    autolens_test: {directory: autolens_workspace_test, chain: [...]}
    euclid: {...}
    howtolens: {...}              # <- no autocti, no autocti_test
```

So `pyauto-heart smoke autocti` cannot work, and neither can a local smoke run of
`autocti_workspace_test` — the only way to exercise CTI smoke is to push and let
CI do it. That is a slow loop for the repo group that has just acquired two smoke
suites.

## Why it matters now

As of 2026-08-24 there are **two** CTI smoke surfaces:

- `autocti_workspace_test` — its long-standing suite (3 scripts, ~20 s).
- `autocti_workspace` — new as of autocti_workspace#28 (3 curated scripts,
  ~132 s cold), the repo's first CI.

Both run in CI through PyAutoHeart's reusable `smoke-tests.yml`. Neither can be
run through Heart's *local* runner, so the Brain/Heart local loop has a blind
spot exactly where new coverage just landed.

## Work

1. **Add `PyAutoCTI: autocti` to `smoke.import_names`.** The block's docstring
   calls it "the repo -> import-package map the preflight proves", so the
   preflight cannot currently prove a CTI environment at all.
2. **Add the two workspace entries** with the correct chain
   (`[PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoCTI]` — matching what both
   repos' CI callers declare; autocti does **not** depend on autogalaxy/autolens):
   ```yaml
   autocti:      {directory: autocti_workspace,      chain: [PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoCTI]}
   autocti_test: {directory: autocti_workspace_test, chain: [PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoCTI]}
   ```
3. **Handle arcticpy.** This is the real design question, and the reason this is
   not a two-line config edit. `import autocti` hard-requires arcticpy, which is
   not a pip dependency: source-only C++ sdist, needs `libgsl-dev` + a toolchain,
   and its own requirements downgrade numpy below 2.0. In CI this is solved —
   `PyAutoHeart/.github/actions/install-arcticpy` owns the canonical recipe and
   the single `arcticpy==2.6` pin, and the workspace callers pass `arcticpy: true`.
   A **composite action cannot be invoked from `heart/smoke.py`**, so the local
   runner needs an equivalent. Decide deliberately between:
   - factoring the recipe into a shell script that both the action and
     `smoke.py` call (keeps one owner, adds a file);
   - a small Python leg in `smoke.py` that mirrors it (risks the exact
     divergence the action was created to end — the recipe had drifted into four
     copies before 2026-08-24);
   - a per-workspace `arcticpy: true` flag in the `smoke:` block that
     `smoke.py` honours.

   **Whatever is chosen, there must remain exactly one place the recipe and the
   `2.6` pin live.** Re-creating a second copy would undo PyAutoHeart#170.
4. **Verify by actually running it** — prepare a CTI environment through the
   local runner and run both suites, not just "the config parses".

## The recipe, for reference (verified 2026-08-24 by building it)

```bash
sudo apt-get install -y libgsl-dev
pip install --upgrade pip setuptools wheel   # BUILD deps: --no-build-isolation
pip install numpy cython                     #   will not supply these
pip install scipy matplotlib                 # RUNTIME deps --no-deps suppresses
pip install arcticpy==2.6 --no-build-isolation --no-deps
python -c "import arcticpy; from importlib.metadata import version; print(version('arcticpy'))"
```

Two traps that cost time if rediscovered: `--no-deps` suppresses arcticpy's
*runtime* imports too (`arcticpy/read_noise.py` imports `scipy` **and**
`matplotlib`, and `__init__.py` imports it), and **arcticpy exposes no
`__version__` attribute** — `arcticpy.__version__` raises `AttributeError` on a
perfectly healthy install.

## Context

`PyAutoMind/complete/2026/08/arcticpy-install-standardisation.md` — why the
recipe has one owner and what breaks when it does not.
