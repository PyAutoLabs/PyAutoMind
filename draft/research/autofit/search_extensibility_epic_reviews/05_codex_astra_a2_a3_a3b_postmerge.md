# Codex gpt-6-astra adversary review — A2/A3/A3b (PyAutoFit#1679/#1680/#1681), post-merge, 2026-10-08

Independent read-only audit of `0dbf258c4..7d056728c`, with HEAD verified as `7d056728c4427cb8c831dc5c56d05309022d5755`; reviewed the supplied decisions, completion records, frozen design and A1 review; no files changed.

## §1 Verdict — FINDINGS

Seven findings: a cross-version pickle regression, an unresolved completion/checkpoint ordering defect, and five preflight, pool, context-contract or validation gaps.

**220 focused tests passed.** One additional test could not initialize its filesystem fixture. In-memory checks reproduced the findings below, replayed all five golden fixtures, and exercised interrupted atomic writes. The two already-filed findings are excluded.

## §2 Witness falsification

**A2**

| Phase clause | Disposition and evidence |
|---|---|
| Emcee JAX evaluation costs ≤2× the jitted call | **Holds locally.** The committed timing guard passed with actual JAX compilation and synchronized evaluations. |
| One `Fitness(` construction site besides NSS | **Holds.** The merged range leaves exactly one construction site under `search/`, in `make_fitness`; NSS now uses it too. |
| Drawer and Nautilus run through `run(ctx)` | **Holds.** Drawer’s bridge tests passed. A real reduced-budget Nautilus fit invoked `run` once and returned 100 samples. |
| Shared JAX fork protection | **Fails for direct bridge entry.** Direct Nautilus `_fit` selects a two-worker multiprocessing path for a JAX analysis; finding 4. |

**A3**

| Phase clause | Disposition and evidence |
|---|---|
| Constructing Emcee leaves `conf.instance` unchanged | **Holds.** Compared the complete configuration before/after construction with `output.search_internal=False`; also verified NUTS and SMC. |
| Golden samples remain byte-identical | **Holds locally.** Serialized all five fixtures through the real table writer into memory; every CSV matched its fixture byte-for-byte. Numeric/header checks and the committed `samples_info` comparisons also passed. |
| Goldens protect D13’s diagnostic preservation | **Fails.** Every checked NUTS ESS/R-hat value can become `-999` without failing the test; finding 7. |
| A pre-A3 output folder loads in the aggregator | **Unverified end-to-end.** The supplied record reports success. I independently replayed pre-adapter sample fixtures and tested an actual A1-created Fitness pickle; the latter exposes finding 1. |

**A3b**

| Phase clause | Disposition and evidence |
|---|---|
| NSS fits `gaussian_x3_blend` with ordered-centre assertions under JAX | **Unverified independently.** The supplied completion record reports successful 10-parameter runs with 50 MCMC steps at `a98312308`, but a harness verdict of `not_assessed`. The smaller committed assertion-bearing NSS fit passed here. |
| Non-traceable likelihood fails with its original error chained | **Holds for the intended compiled path.** Preflight tests passed; it also rejects supported runtime configurations incorrectly—finding 3. |
| D2 bypass remains intact | **Holds.** The REQUIRED-search and disable-JAX/test-mode bypass tests passed. |
| Dynesty no longer swallows runtime failures during sampling | **Holds in focused tests.** The sentinel tests passed, including propagation of errors after pool creation. |

## §3 Findings, ranked by severity

### 1. P1 — Loading an old Fitness pickle silently enables JIT

**Location:** [fitness.py:965](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/fit/PyAutoFit/autofit/non_linear/fitness.py:965).

**Input → wrong output:** Loaded the actual `Fitness` class source from `0dbf258c4` in memory, constructed it with `use_jax_jit=False`, and pickled its instance. Its JAX analysis used `float(np.asarray(instance.centre))`, which is valid eagerly.

```text
A1 evaluation:                 50.0
Unpickle under merged code:   compile=True
Restored evaluation:          TracerArrayConversionError
```

`__setstate__` discards the old JIT flag and defaults `compile` to `True`. This changes persisted execution semantics and can break backend checkpoints containing that Fitness. Setting the current search’s eager option does not repair the restored object.

**Fix:** Preserve the legacy dispatch when migrating state: scalar `use_jax_jit=False` must remain eager; legacy vectorized execution should retain its previous compiled behavior. Add an actual old-state round-trip regression.

### 2. P1 — A failed archive write leaves an unrecoverable “completed” fit

**Location:** `autofit/non_linear/search/abstract_search.py:966`, [abstract_search.py:1215](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/fit/PyAutoFit/autofit/non_linear/search/abstract_search.py:1215); NSS also discards its resume state at `nest/nss/search.py:541`.

**Input → wrong output:** Ran a real Drawer fit with in-memory paths that retain samples and the completion marker. Its retained archive strategy raised `OSError("simulated disk full")` during finalization.

```text
Archive failure:   OSError
Completion marker: True
Rerun backend calls:             0
Archive attempts across both fits: 1
```

The rerun reports completion and never retries the missing archive. The marker is written before `post_fit_output` finalizes the archive. NSS compounds the failure window by deleting its checkpoint before final result processing.

**This ordering predates the reviewed range**, but remains unresolved by A3’s checkpoint guarantees.

**Fix:** Successfully finalize required retained state before committing `.completed`; retain resume state until that transaction succeeds. Recover incomplete finalization on an already-marked folder when the required archive is missing.

### 3. P2 — Preflight validates a different execution configuration from the backend

**Location:** [preflight.py:147](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/fit/PyAutoFit/autofit/non_linear/search/preflight.py:147), `preflight.py:181`.

**Input → wrong output:** Reproduced two false rejections:

- `DynestyStatic(use_jax_jit=False)` successfully evaluates the eager likelihood from finding 1 as `50.0`, but preflight raises `SearchException`, chained to `TracerArrayConversionError`.
- An analysis declares forward differentiation, while `MultiStartAdam(gradient_mode="reverse")` explicitly overrides it. A likelihood using `jax.custom_vjp` evaluates and differentiates successfully in reverse mode, but preflight attempts forward differentiation and raises: `can't apply forward-mode autodiff (jvp) to a custom_vjp function`.

The throwaway Fitness ignores runtime overrides; kinds come from class-level declarations. The eager-option regression also contradicts the constructor warning promising that `use_jax_jit=False` retains its meaning for one release.

**Fix:** Resolve execution settings once and share them between preflight and sampling. Respect explicit eager execution, the search’s gradient override, and its actual batching selection.

### 4. P2 — Direct Nautilus bridge entry bypasses the JAX fork rule

**Location:** [abstract_search.py:1487](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/fit/PyAutoFit/autofit/non_linear/search/abstract_search.py:1487), `abstract_search.py:2012`, `nest/nautilus/search.py:395`.

**Input → wrong output:** Called:

```python
Nautilus(number_of_cores=2)._fit(model, jax_analysis)
```

Intercepted the two backend helpers before any process creation. The bridge selected:

```text
fit_multiprocessing
pool.is_jax = False
effective cores = 2
```

Outside `start_resume_fit`, `_pools()` constructs `PoolFactory(self)` without the available analysis. Nautilus now branches on that factory’s flag, whereas its previous implementation inspected the analysis itself.

Normal `fit()` initializes the factory correctly. The defect affects direct `_fit` callers and permits the forbidden fork/JAX combination; I did not launch a potentially hanging worker.

**Fix:** When the bridge has no active factory, construct `PoolFactory(self, analysis)`. Add a direct-entry regression asserting that no fork constructor is reached.

### 5. P2 — Successful `run(ctx)` fits leak context-created pools

**Location:** [fit_context.py:139](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/fit/PyAutoFit/autofit/non_linear/search/fit_context.py:139).

**Input → wrong output:** Extended the committed toy search to call `ctx.pool()` and then complete normally. Used the real `PoolFactory`, substituting only the process-pool constructor with a recording double.

```text
Pools created: 1
close calls:   0
terminate calls: 0
join calls:    0
```

`ctx.close(failed=False)` returns immediately, and `start_resume_fit` subsequently drops the factory. A new search following the frozen contract does not receive the promised cleanup. Existing Nautilus’s private context manager masks this omission.

**Fix:** Close and join context-owned pools on successful exit; terminate and join on failure. Keep cleanup idempotent and independent of backend-specific ownership assumptions.

### 6. P2 — `ctx.update` does not save the promised checkpoint

**Location:** [fit_context.py:125](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/fit/PyAutoFit/autofit/non_linear/search/fit_context.py:125).

**Input → wrong output:** Ran the committed toy search with a recording strategy serving as both archive and resume state. Its backend called the real `ctx.update(internal)` and then raised `InterruptedError`.

```text
Checkpoint save calls:     0
Checkpoint finalize calls: 0
```

The update reaches sample conversion/output, but neither it nor `SearchUpdater` persists internal state. A new resumable search following the frozen member table loses its progress. Native backend checkpoints hide this omission in the migrated proofs.

**Fix:** Save the appropriate strategy during `ctx.update`, using `save`, not completion finalization that discards resume state. Native strategies can retain their documented no-op behavior.

### 7. P2 — Shape-only golden diagnostics accept arbitrarily wrong convergence results

**Location:** [test_golden_samples.py:104](/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2c1be2d0-f973-4cfa-aad7-5881727d6579/scratchpad/astra/fit/PyAutoFit/test_autofit/non_linear/samples/test_golden_samples.py:104).

**Input → wrong output:** Converted the real NUTS fixture, replaced every present key in `BACKEND_DIAGNOSTIC_KEYS` with shape-preserving `-999` values, and invoked the committed `test_samples_info_is_unchanged("nuts")`.

**The test passed.** Scalar diagnostics have shape `()`, so their values receive no protection whatsoever. This can conceal incorrect ESS/R-hat wiring or values even when CSV preservation remains perfect.

**Fix:** Separately test diagnostic ownership using deterministic mocked backend outputs and exact forwarding assertions. For real diagnostic calculations, compare against the installed backend’s reference calculation or versioned expectations, plus sensible validity checks. Preserve the portable CSV tolerance.

## §4 Claims not independently verified

- Full-suite, Python 3.13, no-JAX, downstream, CI and documentation-build totals in the supplied records.
- Real disk kill-and-resume, HDF interruption, zipped restoration, complete pre-release aggregator folders, and filesystem durability. An in-memory filesystem exercise confirmed that a partial pickle dump preserves the previous archive and removes the temporary file; corrupt content raised `UnpicklingError`.
- The full 10-parameter NSS campaign witness and its scientific acceptance thresholds.
- A real deadlock from finding 4 or leaked operating-system workers from finding 5; process creation was intercepted deliberately.

**A1 follow-through:** The graph pickle-migration, hierarchical inference and wrapper-agreement regression tests passed. NSS declares physical coordinates and Emcee declares resumability. The minimizer sentinel inconsistency remains explicitly documented as conditional behavior; it is not reported again here.

**Compatibility evidence:** All 15 default identifier and current search-JSON round-trip cases passed. This does not establish compatibility for every historical JSON or backend pickle.

**Remaining duplicated lifecycle work:** Drawer still writes its dill through paths, Nautilus manages its own pool context, and NSS deletes its checkpoint inside `run`. These explain why the migrated proofs do not expose all defects in the general context contract.

## §5 Flagged decisions I would overturn

- **Shape-only diagnostic equivalence:** it does not protect D13’s values or diagnostic ownership.
- **Backend-owned successful pool cleanup:** the frozen context contract promises that responsibility to new search authors.
- **Preflight based solely on declarations:** it must validate the resolved runtime configuration.

I would retain the relaxed CSV tolerance: all fixtures were byte-identical locally, and cross-CPU roundoff is a reasonable reason for numerical comparison.

## §6 Recommended resume actions

1. **[blocker-for-release]** Preserve eager execution when migrating old Fitness pickles; add the actual A1 pickle reproduction.
2. **[blocker-for-release]** Make preflight respect eager, gradient and batching overrides; cover both false-rejection reproductions.
3. **[blocker-for-release]** Finalize retained archives before completion and delay resume-state deletion; add failure injection and rerun recovery.
4. **[blocker-for-release]** Pass the analysis into factories created by direct bridge entry; assert no JAX fork.
5. **[before-A4]** Complete `FitContext` pool cleanup and update checkpointing, with a resumable toy search testing both exit paths.
6. **[before-A4]** Restore value-sensitive diagnostic ownership tests and require the `-999` mutation to fail.
7. **[blocker-for-release]** Run disk-backed historical-output, interruption and restore checks in a writable environment.
8. **[later]** Consolidate remaining backend-specific lifecycle paths after the shared contract is enforced.