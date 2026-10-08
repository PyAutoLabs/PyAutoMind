# Objective factory, PoolFactory, JAX fork rule and the run(ctx) bridge (epic search-extensibility, phase A2)

Type: refactor
Target: autofit
Repos:
- PyAutoFit
Themes:
- searches
- jax
Difficulty: large
Autonomy: safe
Consequence: judge
Witness: Emcee on `af.ex.Analysis(use_jax=True)` runs at jitted speed (≤2× the jit per-call time, measured); `grep -rn "Fitness(" autofit/non_linear/search` finds one site besides NSS; Drawer and Nautilus run through `run(ctx)` and pass both A0a conformance layers; a compile-count probe shows one compile per objective kind
Unattended: ready
Priority: high
Epic: search-extensibility
Status: draft
Filed: 2026-10-08

Human launch 2026-10-08: `--auto` for A2, A3, A3b and B3. Plan `draft/research/autofit/search_extensibility_epic_report.md` §4 (phase text quoted verbatim below), architecture §3.3–§3.5, decisions in §8. A0, A0c, A1 and B2 are merged (A1: capability attributes, `Analysis.is_jax`, REQUIRED gate, registry/manifest, `docs/design/run_ctx.md` frozen). Golden identifiers (A0a(i)) are frozen by human ruling: any identifier change stops the item and is flagged. The nine A0 strict xfails are witnesses: flip only the ones a phase names, never add silent ones. Parallel with A3 (which does not touch `Fitness`); A3b follows both.

## Original request (verbatim from the epic plan)

"A2 — Objective factory, PoolFactory, fork rule, run(ctx) bridge (depends on A1; parallel with A3; surveys/01 P2 + surveys/02 P2; D8). Repo: PyAutoFit. Scope: `Fitness.objective(kind)` (lazy jit, `compile=False` escape hatch; D9, D10), ported to every call site except NSS (A3b): Dynesty and BFGS → scalar; Nautilus → batched; Emcee, Zeus, Drawer and the initializer → scalar (fixes eager JAX); MultiStart keeps its transformed-coordinate builder on the shared objective + batching helper; NUTS → scalar log-density (gradient_mode is a separate spike); SMC → batched; `make_fitness(analysis, model, **overrides)` driven by the declared target/invalid-value policy; retire `test_quick_update_wiring.py`; BFGS-on-JAX gets `jac=`, keeping `call_wrap` bookkeeping through a host-side wrapper; deprecation warnings for `use_jax_jit`/`use_jax_vmap`; `PoolFactory` in `parallel/`, owning the EP `number_of_cores` guard, and the one JAX fork rule over search, grid/sensitivity and analysis pools (D11), shipped with the factory so Emcee+JAX+`number_of_cores>1` never regresses to N recompiles; `start_points(model, fitness, n)` calls `plot_start_point` once; the minimal `FitContext`/`run(ctx)` bridge, with Drawer and Nautilus migrated as proofs (D7). Risk: medium-low. Pool paths are where hangs lived (#1442/#1630); keep the semantics byte-for-byte. Verify: a compile-count probe (the `test_fitness_vmap_cache.py` pattern), one compile per kind; an eager-versus-jit timing guard for Emcee+JAX; JAX + `number_of_cores=2` refuses explicitly and `search.summary` records the effective counts; BFGS-JAX `nfev` shows no finite differences; `test_sneaky_map.py`, `test_fork_context.py`; A0a both layers for Drawer and Nautilus via `run(ctx)`; autolens_workspace smoke for Nautilus; workspace_test `{Emcee,Zeus,DynestyStatic,Nautilus,Nautilus_jax,Dynesty_jax}.py` with `number_of_cores=2`. Witness: Emcee on `af.ex.Analysis(use_jax=True)` runs at jitted speed (≤2× the jit per-call time), `grep "Fitness("` under `search/` finds one site besides NSS, and Drawer and Nautilus run through `run(ctx)`."

## Pins (main 2026-10-08)

11 `Fitness(` sites across zeus, nss, emcee, bfgs, dynesty/abstract, nautilus, nuts, smc, multi_start_gradient, drawer. `run(ctx)` signature and `FitContext` members are frozen in `docs/design/run_ctx.md` (any change = a new revision of the note, flagged). `parallel/` holds `context.py`, `process.py`, `sneaky.py`. The `conf.instance` mutations and the Checkpointer are A3's, not here; NSS stays on its own path until A3b. Deprecations are warnings only (one release). `SettingsSearch.search_dict` keeps its shape (A0b ruling).

## Verification

Full `pytest test_autofit` (9 strict xfails unchanged); nojax emulation; the compile-count probe; the Emcee eager-vs-jit timing guard; afT `searches/{Emcee,Zeus,DynestyStatic,Nautilus,Nautilus_jax,Dynesty_jax}.py` with `number_of_cores=2` under `PYAUTO_TEST_MODE=1`; afW `searches/{mcmc,nest,mle}.py`; autolens_workspace Nautilus smoke (`imaging/modeling/start_here.py` under test mode); PyAutoLens/PyAutoGalaxy suites (Fitness is public surface).

## Shape

One PyAutoFit PR (`pending-release`), reviewable commits: objective factory → call sites → make_fitness + deprecations → PoolFactory + fork rule → start_points → FitContext bridge + Drawer/Nautilus migration. Refactor cap safe → ends at PR-open; tier judge, human /prm.
