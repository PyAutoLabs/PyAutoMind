# Search capability declarations, fail-fast gate, lazy registry and the run(ctx) design note (epic search-extensibility, phase A1)

Type: feature
Target: autofit
Repos:
- PyAutoFit
- PyAutoLens
- PyAutoGalaxy
- PyAutoCTI
Themes:
- searches
- jax
- documentation
Difficulty: large
Autonomy: supervised
Consequence: judge
Witness: deleting any entry from `autofit/non_linear/search/registry.py` fails the completeness test; the RTD capability-matrix page renders 15 rows from `python -m autofit search-manifest --json`; a REQUIRED search given a numpy analysis raises `SearchException` with the shared message; `import autofit` imports no optional backend; `docs/design/run_ctx.md` is in the PR
Unattended: ready
Priority: high
Epic: search-extensibility
Status: draft
Filed: 2026-10-08

Phase A1 of the search-extensibility epic (`draft/research/autofit/search_extensibility_epic.md`; plan
`search_extensibility_epic_report.md` §4 A1, architecture §3.1 and §3.3, decisions D2, D3, D7, D12, D18 in §8;
surveys `02_jax_interface.md` §5.1/§5.3/§1.6/§4 and `03_search_docs.md` §5 phase 2). Depends on A0 (all merged
2026-10-08: PyAutoFit#1667, #1672, #1673). Human launch 2026-10-08: `--auto` for A1 and B2. The A0 golden
identifier table must not change (human ruling: identifiers frozen; flag first).

## Original request (verbatim from the epic plan)

"A1 — Declare, gate, registry. Repos: PyAutoFit; downstream PyAutoLens, PyAutoGalaxy and PyAutoCTI docs. Scope:
capability class attributes (§3.1) on all 15 searches, including `objective_target`/`invalid_value`; `Analysis.is_jax`,
replacing the four probes; the `AnalysisFactor` attribute; whole-graph versus per-factor EP backend rules,
`ModelAnalysis`/hierarchical-factor flags, gradient-mode propagation and wrapper serialization (D12); the REQUIRED
fail-fast gate with one shared message (NSS gains the check), placed after the test-mode bypass return (D2); the
Nautilus `force_x1_cpu`+numpy fix (`use_jax_vmap=False`); a declarative, lazy `search/registry.py` plus the
completeness and entry==attributes tests, and the versioned `search-manifest --json` (D3); a design note freezing the
`run(ctx)` signature and `FitContext` members (D7); capabilities surfaced in `search.summary`/`model.info`; generated
`docs/api/searches.rst` plus an RTD capability-matrix page; one canonical citations page; `autodoc_mock_imports` in
`docs/conf.py` (D18); downstream `api/modeling.rst` ×3 collapsed to an intersphinx link. Risk: low to medium. The gate
changes the error type for NUTS, SMC and MultiStart; that is acceptable. Verify: attribute assertions parametrised per
class; `import autofit` imports no optional backend (nojax leg); a REQUIRED search with a numpy analysis raises
`SearchException`; a REQUIRED search with `PYAUTO_DISABLE_JAX=1` + `PYAUTO_TEST_MODE=2` completes; a FactorGraphModel
inherits `use_jax`; a mixed-child EP graph still runs per factor; `Nautilus(force_x1_cpu=True)` runs with numpy; the
docs build in the minimal `[docs]` env and the full-extras env, and a generated-file `--check`. Witness: deleting a
registry entry fails the completeness test, the RTD matrix renders 15 rows from the manifest, and the `run(ctx)`
design note is merged."

## Scope, pinned to main 2026-10-08

1. **Capability class attributes** on `NonLinearSearch` (defaults) and every one of the 15 searches, per report §3.1:
   `jax_use` (`none`/`optional`/`required`), `gradient` (`none`/`uses`), `batched`, `honours_gradient_mode`,
   `posterior_kind` (`chain`/`weighted`/`point`), `produces_evidence`, `resumable`, `warm_start`
   (`provider`/`consumer`/`neutral`), `install_extra`, `upstream_url`, `citation_keys`, `status`, `test_mode_budget`,
   `objective_target` (`log_likelihood`/`log_posterior`/`neg2_log_posterior` + coordinate space) and `invalid_value`.
   Plain class attributes or small enums; string values must round-trip through `search.json` unchanged and must NOT
   enter `__identifier_fields__`. The A0a(ii) roster's `jax_use`/`jax_modules` become derived from the class attributes
   (the roster keeps its golden table).
2. **`Analysis.is_jax`** read-only property; replace every `getattr(analysis, "_use_jax", False)` / `analysis._use_jax`
   probe in `abstract_search.py:429,656`, `dynesty/search/abstract.py:228,249,275`, `bfgs/search.py:298`,
   `multi_start_gradient/search.py:958`, `nautilus/search.py:330`, `analysis/latent.py:159,251`. D12: `AnalysisFactor`
   exposes `is_jax` from its analysis; `FactorGraphModel`/whole-graph fitting requires every child to agree (raise with
   a message naming the disagreeing factors), per-factor EP allows mixed children; `ModelAnalysis` and hierarchical
   factors carry the flag; `gradient_mode` propagates through wrappers; wrapper serialization keeps it.
3. **Fail-fast gate** in `NonLinearSearch.fit`, placed AFTER the test-mode bypass return (`abstract_search.py:830-832`):
   `jax_use == "required" and not analysis.is_jax` → `SearchException` with one shared message (constant in one
   place). NSS gains the same check. Regression tests: REQUIRED + numpy raises; REQUIRED + `PYAUTO_DISABLE_JAX=1` +
   `PYAUTO_TEST_MODE=2` completes. The trace preflight is A3b, not here.
4. **Nautilus** `force_x1_cpu=True` with a numpy analysis: pass `use_jax_vmap=False` (today it crashes).
5. **Registry** `autofit/non_linear/search/registry.py`: declarative, lazy entries (`class_path` string, `lazy`, mirrored
   capability attributes, anchors `example`/`integration_test`); never imports a search module at `autofit` import time
   (keep `_LAZY_ATTRS`, `autofit/__init__.py:212`). Tests: completeness (every `af`-exported search registered;
   deleting an entry fails) and entry == class attributes (skipped per entry when its optional dependency is absent).
   `python -m autofit search-manifest --json` emits a versioned manifest (`search-manifest@1`): the only cross-repo
   format. Static capabilities only; effective capabilities (e.g. SMC evidence needs a prior-sampling initializer) are
   a documented distinction, not fields.
6. **Design note** `docs/design/run_ctx.md` (RTD-visible): freezes the `run(ctx)` signature and the `FitContext`
   members (objective factory handle, model, paths, test-mode level, pool factory, initializer/start points, RNG seed,
   checkpointer slot, updater callback) that A2 ships and A5 migrates to; names what is NOT in the context.
7. **Surface**: capabilities appear in `search.summary` and the `model.info` header.
8. **Generated docs**: `docs/api/searches.rst` and a new RTD capability-matrix page (`docs/searches/index.md` or `.rst`)
   generated from the manifest by a checked-in script with a `--check` mode wired into the docs CI leg; one canonical
   citations page generated from `citation_keys` + `files/citations.bib`; `autodoc_mock_imports` for the optional
   backends in `docs/conf.py` so the minimal `[docs]` env builds.
9. **Downstream** PyAutoLens, PyAutoGalaxy, PyAutoCTI `docs/api/modeling.rst`: replace the hand-maintained search list
   with one intersphinx reference to PyAutoFit's searches page (docs-only PRs, `pending-release`).

Not in scope: `Fitness.objective(kind)` and the `run(ctx)` bridge (A2), the trace preflight and x64 (A3b), the
Hands navigator `--roster`, assistant roster blocks and Brain tier generation (A5), deprecating `use_jax_jit`/`use_jax_vmap`
(A2), any identifier change.

## Verification

Full `pytest test_autofit` (conformance layers (i) and (ii) stay green: 9 strict xfails, none new unless named with its
phase); nojax emulation (`import autofit` must not import jax/blackjax/optax/prodigyopt; registry import-free);
docs build in a minimal env (`pip install -e ".[docs]"`-equivalent) and the full env, zero new warnings; generated-file
`--check`; PyAutoLens and PyAutoGalaxy test suites (public `Analysis` surface changed); autofit_workspace smoke
`searches/{mcmc,nest,mle}.py`; afT `searches/{Nautilus,BlackJAXNUTS,NSS,MultiStartAdam}.py`.

## Shape

One PyAutoFit PR (`pending-release`) in reviewable commits (attributes → is_jax/D12 → gate → registry+manifest → docs
generation → design note), plus three docs-only downstream PRs. Difficulty large → effective `supervised`: under
`--auto` the ship checkpoint is decide-and-flag (at most one flagged decision, PR body states the rejected alternative
and the one-command revert); any second design fork parks on the issue. Tier judge: human /prm.
