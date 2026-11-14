## What shipped

- autofit_workspace#185 (merged 2026-11-14, 5267644): `scripts/searches/mcmc.py` and `notebooks/searches/mcmc.ipynb` drop the stale `enable_pytrees()` / `register_model(model)` requirement from the `BlackJAXNUTS` example (prose, import and calls). The prose now names `use_jax=True` as the only requirement; `Fitness.__init__` (PyAutoFit `autofit/non_linear/fitness.py:329-333`) registers the model as a pytree automatically.
- The PyAutoFit half (NUTS/SMC error strings) had already landed on main before this task (2026-11-05 re-scope); no library PR.
- Issue: autofit_workspace#184 (closed by the merge).

## Witness (run by the independent close-out session at the PR head)

- `grep enable_pytrees|register_model` over `scripts/searches/` and `notebooks/searches/`: no hits. PyAutoFit main: only internal hits (`jax/pytrees.py`, `jax/__init__.py`, `fitness.py`).
- `BlackJAXNUTS` + `af.ex.Analysis(use_jax=False)`: `SearchException` naming `use_jax=True` only.

## Gate

tests n/a (no library change) / smoke 8/8 scripts + 2/2 notebooks / review CLEAN / heart green (dev-ship --repos autofit_workspace) / witness PASS / adversary (Sonnet) held. CI 7/7 green.

## Left alone

- `autofit/jax/__init__.py:9` module docstring still mentions `enable_pytrees` for calling `jax.jit` by hand. That's the intended library end state, not user-facing advice for searches.

## Original prompt

# Stale enable_pytrees register_model advice in NUTS and SMC errors and searches docs

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: grep -rn enable_pytrees autofit/ autofit_workspace/scripts/searches/ returns no user-facing advice; BlackJAXNUTS with use_jax=False raises an error that names use_jax=True only.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-14 362ee746 (PyAutoFit), 9bdd4e5d (autofit_workspace)
Lane: any

autofit/non_linear/search/mcmc/blackjax/nuts/search.py:270 and autofit/non_linear/search/mcmc/blackjax/smc/search.py:328 tell users to call enable_pytrees() / register_model(model), and the workspace script scripts/searches/mcmc.py lines 244-247 and 283-286 do the same in prose and code. Neither function is exposed on the af namespace and Fitness.__init__ (autofit/non_linear/fitness.py:261-265) already calls them internally; scripts/searches/mle.py:232-235 in the same workspace says the opposite. NUTS was verified to run without them on 2026-09-10. Fix the two error strings and the mcmc.py prose (the workspace half lands in autofit_workspace).

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->

## Re-scoped 2026-11-05 — what is left (draft-queue sweep)

- **Done:** Library advice removed: PyAutoFit now has `enable_pytrees` only in jax/pytrees.py, jax/__init__.py and fitness.py, not in the blackjax nuts/smc searches (commit not pinned).
- **Remaining:** autofit_workspace `scripts/searches/mcmc.py` (and its notebook) still teaches `enable_pytrees()` / `register_model` — fix the workspace leg.

_Evidence from the 2026-11-05 read-only sweep (Mind ledger + GitHub search); remaining items are the live scope of this prompt._
