# autonerves-verify-install — release-fidelity harness migrated autoconf → autonerves

**Shipped 2026-07-20.** Issue [PyAutoHeart#97](https://github.com/PyAutoLabs/PyAutoHeart/issues/97), PR [#98](https://github.com/PyAutoLabs/PyAutoHeart/pull/98) (merged, squash `3c65577`).

## Problem
The `autoconf → autonerves` package rename (PyAutoConf → PyAutoNerves, merged into the libraries 2026-07-19/20) was not propagated to PyAutoHeart's release-fidelity / verify-install harness. The nightly publishes the `autonerves` wheel now, but Stage-3 still did `pip install autoconf==<today's dev>` from TestPyPI → `No matching distribution found for autoconf==2026.7.20.1.dev66901`. This broke **both** `nightly-release` (Stage 3, run 29719984654) and `workspace-validation` overnight 2026-07-20.

## Fix
Surgical 6-file migration in PyAutoHeart:
- `heart/checks/verify_install.sh` — current-build install list (Check C/F `$TARGET_VERSION`), import checks (B/D), Colab `setup_colab` bootstrap.
- `.github/workflows/workspace-validation.yml` — `autoconf[optional]` → `autonerves[optional]`.
- `heart/checks/import_time.py` `DEFAULT_PACKAGES`; `tests/test_validate.py` expectation (39 passed).
- `.github/workflows/{docs-build,lib-tests}.yml` — cosmetic help text.

## Traps / notes (carry forward)
- **NOT a blind rename.** Check A/E installs the *historical yanked release* `autoconf==2026.2.26.4` (predates the rename; no `autonerves` at that version) — that block must stay `autoconf`.
- The `docs-build`/`lib-tests` case statements keep accepting `autoconf` as an **input alias** → `repo=PyAutoNerves` (back-compat), so `autoconf` legitimately survives there.
- `autonerves` exposes both `[optional]` and `[jax]` extras (1:1 with the old `autoconf` extras).
- Filed from `/wake_up` overnight-failure triage; the same rename also motivated the local dir renames PyAutoConf→PyAutoNerves / PyAutoBuild→PyAutoHands.

## Validation
`bash -n` clean; `pytest tests/test_validate.py` → 39 passed; PR CI green (pytest 3.12/3.13). Next nightly Stage-3 + workspace-validation expected green.

## Original prompt

# Migrate PyAutoHeart release/verify-install harness from `autoconf` to `autonerves`

Type: bug
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised

The `autoconf` → `autonerves` package rename (PyAutoConf → PyAutoNerves, merged
into the libraries on 2026-07-19/20) was not propagated to PyAutoHeart's
release-fidelity and verify-install harness. The nightly release now publishes
the `autonerves` wheel, but the harness still asks pip for the old `autoconf`
package name at the new version, so the install cannot resolve.

## Evidence

Overnight 2026-07-20:
- `nightly-release` (PyAutoBrain) failed at **Stage 3 (release-fidelity
  integration)** → PyAutoHeart run 29719984654.
- `workspace-validation` (PyAutoHeart) failed with the **same** root cause.

Stage-3 install step log:

```
pip install autolens==2026.7.20.1.dev66901 ... autoconf==2026.7.20.1.dev66901 ... jax
ERROR: No matching distribution found for autoconf==2026.7.20.1.dev66901
```

TestPyPI's latest `autoconf` is `2026.7.19.1.dev66601` (frozen at the rename);
today's build published `autonerves` instead. Every `run_scripts` matrix job and
`verify_install_release` fail identically at "Install TestPyPI wheels".

## Fix locus (PyAutoHeart, harness only — no library-source or workspace change)

Migrate the hard-coded `autoconf` package name to `autonerves` in:
- `heart/checks/verify_install.sh` — pip install lists and import checks
  (approx. lines 226, 231, 306, 309, 473–475, 486, 492, 535, 539–540, 546, 574,
  588, 593, 597, 637). Note the `from autoconf import setup_colab` import and the
  `pip install autoconf --no-deps` Colab-emulation path.
- `.github/workflows/workspace-validation.yml:264` — `"autoconf[optional]==$TESTPYPI_VERSION"`.
- `heart/checks/import_time.py:57` — `DEFAULT_PACKAGES`.
- `tests/test_validate.py:22` — expected package list.
- Sweep `heart/` for any remaining `autoconf` package references (docs-build.yml
  and lib-tests.yml `description:` strings are cosmetic help text — migrate for
  consistency but they do not affect the failure).

Verify the `autonerves` distribution name matches what PyAutoHands publishes
(package name on PyPI/TestPyPI and the import module) before finalising.

## Validation

Re-run the release-fidelity leg (or `verify_install` A–E against TestPyPI wheels)
and confirm the `autonerves==<dev>` install resolves and the import checks pass;
`nightly-release` Stage 3 and `workspace-validation` should return green.

<!-- filed from /wake_up overnight-failure triage on 2026-07-20 -->
