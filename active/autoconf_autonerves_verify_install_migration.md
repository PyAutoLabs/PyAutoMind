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
