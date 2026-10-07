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
