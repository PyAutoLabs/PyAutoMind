# Search hygiene and dead code (epic search-extensibility, phase A0b)

Type: refactor
Target: autofit
Repos:
- PyAutoFit
Themes:
- searches
- jax
Difficulty: medium
Autonomy: safe
Consequence: judge
Witness: `grep -rn make_sneakier_pool autofit/` returns zero hits; the two `ROUND_TRIP_XFAIL` strict xfails in `test_autofit/non_linear/search/test_conformance.py` are removed and the round trip passes for BlackJAXNUTS and SMC; a unit test shows an Emcee update computes autocorrelation once; `af.Drawer` runs under `NullPaths`
Unattended: ready
Priority: high
Epic: search-extensibility
Status: active
Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1670
Filed: 2026-10-08

Phase A0b of the search-extensibility epic (`draft/research/autofit/search_extensibility_epic.md`;
plan `search_extensibility_epic_report.md` §4 A0b; source `search_extensibility_epic_surveys/01_search_architecture.md`
§8 and Phase 1). Depends on A0a(i) (merged, PyAutoFit#1667): its conformance suite is the safety net and carries two
strict xfails this phase must flip. Human launch 2026-10-08: `--auto` for every A0 phase. Behaviour-preserving
except where the plan names a repair.

## Original request (verbatim from the epic plan)

"A0b, hygiene and dead code (surveys/01 P1). Repo: PyAutoFit. Scope: delete `make_sneakier_pool` and
`NonLinearSearch.iterations`; dedupe `_log_process_state`; guard Drawer's timer and honour its `search_internal`
argument; stop Nautilus mutating `iterations_per_full_update`; narrow the `samples_from` except to
`(FileNotFoundError, NotImplementedError)`, with a WARNING log; delete Zeus's dead `discard/thin/chain`; fix the
`AbstractNest` `number_of_cores=None` default; add a `self.kwargs` unknown-kwarg warning (not a raise), with
`SettingsSearch` filtering `use_jax_vmap` to the searches that accept it; convert samples once per update; compute
Emcee autocorrelation once per conversion; fix the stale docstrings and `config/non_linear/README.md`; move-only:
`test_autofit/.../optimize/` → `search/mle/`, as its own commit. Dependency: A0a layer (i) merged first; layer (ii)
follows A0b. Risk: low. The narrowed except surfaces hidden errors, which is intended. Verify: A0a,
`pytest test_autofit`, autofit_workspace smoke `searches/{mcmc,nest,mle}.py`, and workspace_test
`searches/{Emcee,Zeus,DynestyStatic,Nautilus,LBFGS}.py`. Witness: `grep make_sneakier_pool` returns zero hits, and an
Emcee update computes autocorrelation once (unit test)."

## Scope, pinned to main 2026-10-08

- `autofit/non_linear/search/abstract_search.py`: delete `make_sneakier_pool` (:1672) and `SneakierPool` if it then has
  no users; delete the unread `iterations` attribute (:262; the updater owns `_iterations`, `updater.py:59-70`);
  `_log_process_state` is defined at :716 and again at `updater.py:339` — keep one; `samples_from` except at :1623
  narrows to `(FileNotFoundError, NotImplementedError)` and logs the fallback at WARNING; `self.kwargs` (:269): log a
  WARNING naming each unknown kwarg (never raise).
- `autofit/non_linear/settings.py` `SettingsSearch.search_dict` (:53-59): pass `use_jax_vmap` only to searches whose
  constructor accepts it (inspect the signature), so the new warning stays silent for the others.
- `autofit/non_linear/search/mle/drawer/search.py`: guard `self.timer` (:147) so `NullPaths` works (bug draft
  `draft/bug/autofit/drawer_crashes_under_nullpaths_timer_none.md`, retire it in this PR), and make
  `samples_via_internal_from` honour its `search_internal` argument (:158-159). Drop the workaround and its
  comment from `autofit_workspace_test/scripts/searches/Drawer.py` as a follow-up note, not in this PR.
- `autofit/non_linear/search/nest/nautilus/search.py` `call_search` (:582-586): compute the effective
  `iterations_per_full_update` locally, never assign to `self`.
- `autofit/non_linear/search/nest/abstract_nest.py:28`: `number_of_cores: int = 1`.
- `autofit/non_linear/search/mcmc/zeus/search.py:288-290`: delete the unused `discard/thin/chain` in `_fit`.
- Emcee: compute the autocorrelation once per samples conversion (today it is recomputed inside the conversion);
  add the unit test the Witness names.
- `SearchUpdater.update`: convert samples once and pass them to `visualize`.
- **Round trip repair (flips the A0a(i) xfails):** BlackJAXNUTS and SMC serialise `inverse_mass_matrix` as a kind
  string their constructors reject; make the constructors accept what `search.json` emits (or serialise what they
  accept), then delete `ROUND_TRIP_XFAIL` from `test_conformance.py`. Identifiers must stay the same: regenerate
  nothing in the golden table; if an identifier changes, stop and flag it on the issue.
- Docstrings: `AbstractNest` (removed "auto-terminate when stuck" feature), `apply_test_mode` base docstring
  ("called during __init__" is false), the NSS docstring block (part 1 fixed the bullet list; check the rest renders).
- Move-only commit: `test_autofit/non_linear/search/optimize/{test_drawer,test_lbfgs}.py` → `search/mle/`.
- Not in scope: `CONFIG_MUTATION_XFAIL` (A3), the `general.yaml` `output.search_internal` duplicate (A3), the
  `isinstance(paths, NullPaths)` capability refactor (A4).

## Verification

`pytest test_autofit` (full, `-x`) with 0 xfails from `ROUND_TRIP_XFAIL` and the three A3 xfails still strict;
emulate the `unittest-nojax` leg (import-hook block of jax/blackjax/optax, not `sys.modules=None`); autofit_workspace
smoke `searches/{mcmc,nest,mle}.py`; autofit_workspace_test `scripts/searches/{Emcee,Zeus,DynestyStatic,Nautilus,LBFGS,Drawer}.py`
under `PYAUTO_TEST_MODE=1`; downstream: PyAutoLens `test_autolens` (SettingsSearch consumer) if `search_dict` changes shape.

## Shape

One PyAutoFit PR (`pending-release`), with the test move as its own commit at the end. Tier judge: the human merges.
