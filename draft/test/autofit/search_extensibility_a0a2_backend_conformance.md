# Search conformance suite, layer (ii): backend execution on the full-extras legs (epic search-extensibility, phase A0a(ii))

Type: test
Target: autofit
Repos:
- PyAutoFit
Themes:
- searches
- jax
- ci
Difficulty: medium
Autonomy: safe
Consequence: judge
Witness: layer (ii) green on the `[optional]` CI legs for all 15 searches; on an emulated no-jax leg NSS, BlackJAXNUTS, SMC and the MultiStart×4 are skipped by declared capability (never by importorskip) and the rest pass
Unattended: ready
Priority: high
Epic: search-extensibility
Blocked-by: search-ext-a0b-hygiene (PyAutoFit, A0b must merge first; implemented stacked on its branch)
Status: planned
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1671
Filed: 2026-10-08

Phase A0a(ii) of the search-extensibility epic (`draft/research/autofit/search_extensibility_epic.md`; plan
`search_extensibility_epic_report.md` §4 A0a layer (ii)). Tests only. Layer (i) is merged (PyAutoFit#1667,
`test_autofit/non_linear/search/{test_conformance,conformance_roster}.py`). Lands after A0b so Drawer/`NullPaths`
is not an xfail. Human launch 2026-10-08: `--auto` for every A0 phase.

## Original request (verbatim from the epic plan)

"Layer (ii), backend execution, Heart full-extras legs only (`lib-tests.yml` installs `[optional]`, `:114`),
explicitly skipped by declared capability on `unittest-nojax`: capability-matched fixtures (numpy `MockAnalysis` for
`jax_use` none/optional, a JAX `MockAnalysis` for required) at `PYAUTO_TEST_MODE=1` with real `DirectoryPaths`; it
asserts the output file set, the completed-path resume, a `NullPaths` fit, the `samples_from(model, None)` fallback
and the `samples_info` key sets. The module docstring states the coverage contract: every backend executes on the
full-extras leg, and `importorskip` may not hide a required backend there. Layer (ii) lands after A0b, so
Drawer/`NullPaths` is not an xfail. Verify: `pytest test_autofit/non_linear` on a full-extras env and with
jax/blackjax/optax uninstalled. Witness: layer (i) green on all legs; layer (ii) green on `[optional]` legs, with
NSS/NUTS/SMC/MultiStart skipped on the no-jax leg by declared capability."

## Scope

- New `test_autofit/non_linear/search/test_conformance_backend.py` reusing `conformance_roster.searches_under_test()`.
  Per search, at `PYAUTO_TEST_MODE=1`: (a) a fit with real `DirectoryPaths` into `tmp_path` asserting the expected
  output file set per search (`search.json`, `model.json`, `samples.csv`/`samples_info.json`, the backend's own
  checkpoint name from survey 01 §8), (b) a second `fit` on the completed path resumes without rerunning (assert via
  the backend's call count or the timer file), (c) a `NullPaths` fit returns a `Result`, (d) `samples_from(model, None)`
  falls back (A0b's narrowed except), (e) `samples_info` key set per family.
- Capability gate: skip by the declared capability attributes A0a(i) introduced (`jax_use` or equivalent), never
  `importorskip`; the no-jax emulation (import-hook block) must show exactly NSS, BlackJAXNUTS, SMC and MultiStart×4
  skipped.
- Fixtures: numpy `MockAnalysis` for `jax_use` none/optional; a JAX `MockAnalysis` (jnp log-likelihood) for required.
- Mark the whole module to run only when `[optional]` extras are installed on CI (the `unittest` legs), skipping
  per-search on `unittest-nojax` by capability.
- Not in scope: any library source. If a search cannot satisfy (a)-(e) without a library change, add a strict xfail
  naming the later phase (A2/A3) and list it on the issue.

## Verification

`pytest test_autofit/non_linear/search -x`; full `pytest test_autofit`; no-jax leg emulated; runtime of the new
module under 90 s on a laptop (reduce budgets via `apply_test_mode`, never by editing searches).

## Shape

One PyAutoFit PR (`pending-release`). Implemented on a branch stacked on `feature/search-ext-a0b-hygiene` with the PR
based on that branch; after A0b merges the human retargets to `main` (or it retargets automatically) and merges.
Tier judge.
