## search-conformance-metadata
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1666
- completed: 2026-10-07
- epic: search-extensibility (phase A0a(i))
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1667
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1667
- merge-commit: PyAutoFit 81bfb8e1fb6b54832c3038e4e6186b3f0b78038d

### Outcome
Tests-only conformance suite, layer (i), over the 15 public searches (`test_autofit/non_linear/search/{conformance_roster,test_conformance}.py`): default construction, family base, `__identifier_fields__` and default-construction identifier against a frozen golden table (generated from main 908ca61a5 with `PYAUTO_TEST_MODE` unset), constructor-argument sets, `search.json` round trip and `conf.instance` unchanged by construction. Classes resolve lazily by class-path string, so the module collects on `unittest-nojax`; only NSS construction skips without blackjax. Five strict xfails, each pinned to one exception type, record later epic work: NUTS/SMC round trip (the serialised `inverse_mass_matrix` kind string is rejected — A0b) and Emcee/NUTS/SMC setting `output.search_internal=True` at construction (A3; the test pushes a `false` override because the test config masks it). No library source or identifier changed.

### Validation and limits
Full `test_autofit` 3066 passed / 2 skipped / 5 xfailed in the task worktree; no-jax leg emulated with an import hook (97 passed, 4 NSS skips, 5 xfails); perturbing one golden identifier fails exactly one case. CI: unittest 3.12, 3.13 and unittest-nojax green on head 886ebb218. `samples_info` key sets deferred to layer (ii), which lands after A0b.

### Traps
- `PYAUTO_TEST_MODE` changes Emcee and Zeus identifiers (apply_test_mode), so golden identifiers are computed with it removed.
- The test config's `output.yaml` has `search_internal: true`, which hides the construction-time mutation; a `false` override is needed to observe it.
- Heart's release-validation freeze (set by pre-build) blocked the library merge until it expired; `pyauto-heart freeze --show` exit 3 = frozen.

## Original prompt

# Search conformance suite, layer (i): metadata and serialization for all 15 searches on every CI leg (epic search-extensibility, phase A0a(i))

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
Priority: high
Epic: search-extensibility
Status: active
Filed: 2026-10-07
Issued: 2026-10-07

Phase A0a(i) of the search-extensibility epic
(`draft/research/autofit/search_extensibility_epic.md`; plan in
`search_extensibility_epic_report.md` §4 A0a, decision D1 in §8.1). Tests
only. It is the safety net every later phase of track A runs against and the
only track-A dependency of B2.

## Original request (verbatim from the epic plan)

"A0a, conformance suite in two layers. Repo: PyAutoFit, tests only. Layer
(i), metadata/serialization, all 15 searches, every CI leg (including
`unittest-nojax`; the module never imports `af.NSS`/`af.SMC` at collection
time): construction, `search.json` round trip and constructor-argument sets,
identifiers against a frozen golden table of all 15 default constructions,
declared capability attributes, and `conf.instance` unchanged by construction
(xfail for Emcee, NUTS and SMC until A3). Risk: none. Verify: `pytest
test_autofit/non_linear` on a full-extras env and with jax/blackjax/optax
uninstalled. Witness: layer (i) green on all legs."

## Scope

Add `test_autofit/non_linear/search/test_conformance.py` (plus a small
`searches_under_test()` helper module beside it) parametrised over every
public search exported from `af`:

- the 15 searches: Emcee, Zeus, NUTS, SMC (mcmc); DynestyStatic, DynestyDynamic,
  Nautilus, NSS (nest); LBFGS, BFGS, Drawer, MultiStartLBFGS/BFGS/Prodigy
  family (mle). Confirm the exact roster from `autofit/non_linear/search/`
  and the `af` exports before freezing the table, and record it in the module
  docstring.
- Collection never imports an optional backend: resolve search classes lazily
  by `class_path` string inside the test (importlib) so the module collects on
  the `unittest-nojax` leg; a search whose backend is absent is **skipped by
  that fact alone for the construction-dependent checks**, never by a
  module-level `importorskip`. Emulate the no-jax leg locally with an
  import-hook block before shipping (memory: nojaxSkip).
- Per search: default construction; `search.json` write → `from_dict`
  round trip equals the original (compare the serialised dicts); the
  constructor-argument set snapshot; identifier of the default construction
  against a **frozen golden table** committed as data in the test module (this
  table is the §3.2 invariant every later phase of the epic must hold);
  declared capability attributes present where they already exist today
  (assert only what exists; A1 adds the full set); `conf.instance` unchanged
  by construction, with `pytest.mark.xfail(strict=True)` for Emcee, NUTS and
  SMC until A3.
- Snapshot the per-search `samples_info` key sets only if obtainable without
  running a backend; otherwise defer to layer (ii).

## Out of scope

Backend execution (layer (ii), after A0b), any source edit under `autofit/`,
the hygiene list (A0b) and the documentation repairs (A0c).

## Verification

- `pytest test_autofit/non_linear` green in a full-extras env.
- The same green with jax/blackjax/optax blocked via an import hook (the
  `unittest-nojax` leg); JAX-only searches skip, the module still collects.
- Golden table: regenerate once, commit, and prove a deliberate identifier
  perturbation fails the test.

## Witness

Layer (i) green on every CI leg; deleting a row from the golden table or
changing a default argument fails exactly one parametrised case.
