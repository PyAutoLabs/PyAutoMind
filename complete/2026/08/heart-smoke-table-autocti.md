## heart-smoke-table-autocti
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/172
- heart-pr: PyAutoHeart#173 (merged 2026-08-24; commits 3051f128d42d8bdaa938b0906b9198c5852022a4
  and 732ec63f2d4367cf31eec0a4da31e5374dbef4fd)
- completed: 2026-08-24
- retired-from-draft: 2026-09-09 — filed 2026-08-24 and **never issued**; the work shipped the
  same day from another session. The prompt then sat in `draft/maintenance/ci/` for sixteen days
  rendering as pickable backlog. Retired on evidence by the `ci-smoke` bundle session. This
  record is the retirement, not a re-ship.
- what shipped: all four of the prompt's work items.
  (1) `PyAutoCTI: autocti` added to `smoke.import_names` in `config/repos.yaml`.
  (2) Both workspace entries added with the chain the prompt specified —
  `autocti: {directory: autocti_workspace, chain: [PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoCTI]}`
  and `autocti_test: {directory: autocti_workspace_test, chain: [...same...]}`. The chain
  deliberately excludes autogalaxy/autolens: autolens sits on autogalaxy, autocti does not.
  (3) arcticpy handled by taking TWO of the prompt's three options, because they answer
  different questions. (4) Verified by running it.
- the arcticpy split, worth not re-deriving: WHERE the recipe lives is the shell-script option —
  the composite action's five run-steps were extracted to
  `.github/actions/install-arcticpy/install_arcticpy.sh`; the action calls it via
  `${{ github.action_path }}` (a composite action is downloaded with its whole directory, so
  cross-repo consumers with no PyAutoHeart checkout still work) and `heart/smoke.py` calls the
  same file out of the Heart checkout. WHAT TRIGGERS it is the per-workspace flag option — a
  declared `arcticpy: true` key in the `smoke:` block, mirroring the input the CTI CI callers
  already pass, rather than inferring it from `PyAutoCTI in chain`. Rejected outright: a Python
  leg in `smoke.py` mirroring the recipe — that is the divergence PyAutoHeart#170 was created to
  end. One file, one pin, both consumers running identical bytes.
- pin drift found while extracting: the `2.6` pin had quietly acquired two more copies —
  `action.yml`'s `version` input defaulted to `"2.6"`, and `arcticpy-action.yml` passed
  `${{ inputs.version || '2.6' }}`. The second one mattered: the self-test would have gone on
  proving the OLD version built after a bump. Both now defer to the script's single default and
  no consumer passes `version` at all.
- two traps found by running it rather than reading it. The GSL probe used `ls a b c`, which
  exits non-zero when ANY operand is missing — so on every machine that actually has GSL in
  exactly one prefix it reported the headers absent and refused to build; it now tests each
  prefix independently, overridable via `ARCTICPY_GSL_PREFIXES`. And `pip check` can NEVER pass
  in a CTI environment: arcticpy declares `numpy~=1.21` and is installed `--no-deps` on purpose,
  so the preflight reported the numpy conflict and destroyed every environment immediately after
  building it. The preflight now tolerates exactly that one line, and only for a workspace that
  declared `arcticpy: true`.
- the local leg never runs apt — a dev command must not mutate system packages, and `apt-get`
  does not exist on macOS. It proves the headers are present and fails with the install line.
- the fingerprint hashes the shared script (`files["PyAutoHeart:install_arcticpy.sh"]`), so
  editing the recipe or bumping the pin invalidates the cached environment instead of silently
  reusing a stale one.
- verification, as the prompt demanded: `pyauto-heart smoke autocti_test` on Python 3.12 built
  its environment (arcticpy 2.6 from the shared recipe), passed preflight, and ran 3/3 scripts
  PASS. Not "the config parses".
- tenant-firewall follow-up in the same PR (732ec63f): CI's `repos_sync.py --check --only
  "tenant firewall (organ code)"` failed on three satellite repo names the first commit put into
  organ code. `heart/smoke.py` and `install_arcticpy.sh` are UNLISTED — their two mentions were
  comment prose and were reworded to roles. `tests/test_repo_config.py`'s chain assertion now
  goes through `import_names`, comparing package names instead of repo-name literals, rather
  than growing the allowlist entry.
- context: `complete/2026/08/arcticpy-install-standardisation.md` — why the recipe has one owner.

## Original prompt

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
