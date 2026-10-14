# Codex gpt-6-astra adversary review — A4 stack (PyAutoFit#1685 → #1686 → #1687), pre-merge, 2026-10-14

Read-only review from the task worktree root over `8437a3b76 → d37280e2b → 27e77474c → 946835f2a`; inputs: A4 prompt, the three PR bodies, epic report §3.2/§3.3/§3.5/§8.3/§8.5/§8.6, review 05. Human rulings supplied: MultiStart explicit-seed re-key accepted; #1500 out of scope; SneakyPool and pool shims stay until A5. Verdict FINDINGS (4). Enacted on the stacked branches before /prm; see the A4 completion record.

## §1 Verdict — FINDINGS

**Four confirmed findings: three in PR 2 (#1686), one in PR 3 (#1687).** No must-fix regression confirmed in PR 1 (#1685).

Reviewed `8437a3b76484 → d37280e2bd06 → 27e77474c866 → 946835f2ab61`. The checkout remains unchanged.

**Validation:** 266 focused tests passed using a restricted, serial harness. Normal pytest initialization was blocked because even `/tmp` is read-only; the harness loaded the test configuration, disabled filesystem-cleanup conftests, and stubbed `NullPaths` temporary-directory allocation. Another 15 cases stopped at filesystem-fixture setup. These results do **not** establish full-suite or disk-backed compatibility.

I also loaded actual baseline search classes from `origin/main` in a separate process, compared their identifiers/serialization, and unpickled their searches under HEAD.

## §2 Witness falsification

| Clause / claim | Disposition and evidence |
|---|---|
| `abstract_search.py ≤600` | **Holds:** HEAD has 585 lines. Lifecycle remains there; extracted method groups have distinct responsibilities rather than another oversized lifecycle class. |
| BFGS/LBFGS reduced `maxiter` | **Holds:** both construct with `maxiter=10` at levels 1–3; normal construction retains 15000. Backend forwarding inspected. |
| Two `Emcee(seed=1)` fits produce identical CSV | **Holds in memory:** two real 30-step fits produced identical **25,109-byte** output through the real CSV writer. Two unseeded controls differed. Filesystem writing remains unverified. |
| All 15 default identifiers and hash lists | **Holds:** compared against actual main constructions, independently of the new golden fixture. |
| `Nautilus().hash_list` unchanged | **Holds:** included in that baseline comparison. |
| Explicit-None and explicit-seed cases | **Holds for the specified table:** all 15 identifier cases passed. Accepted NUTS/SMC and MultiStart explicit-seed re-keys retained. |
| Conditional seed hashing; no base identifier field | **Holds:** conditional walk at `mapper/identifier.py:151`; no `"seed"` in the base fields. Nautilus/NSS retain their static fields. |
| `to_dict`/`from_dict`: null versus absent | **Holds:** checked all 15. Explicit null remains null; absent uses constructor defaults, including NSS’s 42. |
| Old default NUTS/SMC JSON loads without re-keying | **Fails:** both search identifiers and aggregator IDs change. **Finding 1.** |
| Old incomplete output folders | **Holds only for fresh default reconstruction:** all 15 path checks pass. Reconstructing NUTS/SMC from their old JSON instead selects a different identifier. |
| Nautilus/NSS aliases; NUTS/SMC backend default 42 | **Holds:** constructor and backend dispatch inspected. |
| Emcee/Dynesty backend stream 1; Zeus initial points only | **Holds for ordinary constructions:** helper tests and Emcee fits pass. Existing Dynesty subclasses encounter **finding 2**. |
| Grid children use independent streams | **Fails for several actual backends:** helper streams differ, but raw-seed backends and MultiStart ignore child keys. **Finding 3.** |
| Spawn key never hashed or serialized | **Holds for identifiers and `search.json`.** The broader wording needs qualification: ordinary search pickle state retains `_seed_spawn_key`. |
| Serialized constructor-argument sets | **Holds for intended metadata changes:** comparison with main found seed additions where previously absent and SMC’s removed auto-correlation field. Drawer retains serialized `clipper`. Positional compatibility nevertheless fails—**finding 4**. |
| `samples_cls` class paths | **Holds:** all 15 checks pass; Samples classes were not moved. |
| #1493 clipper tripwire | **Holds:** nested-search exclusion, six BFGS/MultiStart identifier cases, and Drawer’s clipper-independent identifier passed. |
| Deprecated family subclass warnings | **Holds:** distinct classes, `FutureWarning`, literal `stacklevel=3`. Actual warning attribution is `<frozen abc>:106`, rather than the subclass declaration. |
| Family defaults and public MRO | **Holds for tested construction:** public searches exclude family bases; initializer, clipper, auto-correlation and samples-class checks pass. |
| SMC weighted plotter | **Holds:** dispatch test passes; it selects WEIGHTED/anesthetic and drops chain auto-correlation settings. |
| Test-mode equivalence | **Holds for inspected built-in reductions:** generic budgets pass; NUTS with one chain and SMC with three particles retain those smaller values. Full bypass/output equivalence remains unverified. |
| EP inheritance and adapter | **Holds by inspection:** `AbstractFactorOptimiser` inheritance, path replacement, updater invalidation, visual switches and release semantics remain. **Two-step EP execution unverified independently.** |
| Paths/runtime settings preserve disk output | **Holds by inspected transformation; disk execution unverified.** Built-in timer/checkpoint capability values reproduce the former type checks. |
| Grid cores and paths | **Holds in construction probe:** outer two-core grid forces child searches to one core, assigns `(0,)`/`(1,)`, and retains the existing child-path construction. |
| Pool shims and JAX fork protection | **Holds:** shims remain. Direct Nautilus `_fit` with JAX and two requested cores receives `is_jax=True`, effective cores **1**. |
| Overrides, monkeypatching and pickles | **Partially holds:** tested search-method patching works; all 15 baseline search pickles deserialize. NUTS/SMC pickle identifiers change—**finding 1**. Historical Result pickle execution remains unverified. |
| Developer-tier searches still run | **Construction holds:** UltraNest, PySwarmsGlobal and PySwarmsLocal import and construct. Fits unverified independently. Developer NSS directory is absent, as reported. |
| Workspace smoke / graphical scripts | **Unverified as complete suites; graphical compatibility fails:** the existing seeded Dynesty helper reaches a new `TypeError`. **Finding 2.** |
| Docs | **Generated content holds:** all three generated pages match the current manifest; in-process manifest CLI returns 15 searches. Sphinx’s ≤30 warnings remains unverified. No family-base references found in searched RST files. |
| A5 / Prior–Message exclusions | **Holds by diff inspection:** no remaining-backend `run(ctx)` migration, pool-shim deletion, `FitLifecycle` extraction or Prior/Message redesign found. |

The review-05 fixes survived the inspected transformations:

- Legacy eager/JIT/vectorized Fitness state and resolved preflight regression tests passed.
- Injected archive failure left completion unset; successful ordering was `archive → completed`.
- Context updates called checkpoint `save`.
- Success/failure/idempotent pool-cleanup tests passed.
- Diagnostic forwarding and sentinel-mutation rejection tests passed.
- Direct bridge JAX protection passed as described above.

## §3 Findings ranked by severity

### 1. P1 — Historical default NUTS/SMC artifacts acquire new identities

**PR:** #1686. **Confirmed empirically**, including actual main-created search pickles.

**Locations:** [identifier.py:151](PyAutoFit/autofit/mapper/identifier.py:151), [execution.py:115](PyAutoFit/autofit/non_linear/search/execution.py:115), downstream consumer [search_output.py:320](PyAutoFit/autofit/aggregator/search_output.py:320).

**Input → wrong output:** deserialize main’s default `search.json`, which records `seed: 42`.

| Search | Original search identifier | Loaded identifier |
|---|---|---|
| BlackJAXNUTS | `2a6f5217539f82fab8ea42eda9bf3441` | `b120de220578c303f72789456b54e9fc` |
| SMC | `3baa494f2ca7b37a8c4b85884cadd1f7` | `933c180e80f42e17a24f9a4dcf271cb1` |

The PR’s justification—identifiers already exist on disk—does not cover the actual consumers:

- `SearchOutput.id` **recomputes** the identifier from the loaded search/model/tag.
- Database scraping uses that recomputed ID at `database/aggregator/scrape.py:82`, while reading existing parent identifiers separately.
- A deserialized search’s paths likewise compute the new identifier when reused.

Thus historical default outputs change aggregator/database identity, and reconstructing an incomplete run from its saved search selects another folder. Baseline NUTS/SMC **pickles** exhibit the same identifier change.

[test_seed.py:158](PyAutoFit/test_autofit/non_linear/search/test_seed.py:158) explicitly expects this wrong legacy identity; its passing result does not establish compatibility.

**Required correction:** preserve persisted legacy identity during hydration/loading. Keep the separately accepted explicit-constructor seed re-key.

### 2. P2 — New Dynesty seed injection breaks an existing graphical subclass

**PR:** #1686. **Confirmed empirically at the real sampler-construction call.**

**Locations:** [static.py:189](PyAutoFit/autofit/non_linear/search/nest/dynesty/search/static.py:189), equivalent dynamic/pooled calls; existing consumer [analytic_autofit.py:206](autofit_workspace_test/scripts/graphical/analytic_autofit.py:206).

`SeededDynestyStatic(seed=0)` already supplies:

```python
search_kwargs["rstate"] = np.random.default_rng(self.seed)
```

PR 2 now passes both `**self.search_kwargs` and `**self._rstate_kwargs()`.

**Input → wrong output:**

```text
Existing SeededDynestyStatic(seed=0), starting a fresh sampler
→ TypeError: dynesty.dynesty.NestedSampler() got multiple values
  for keyword argument 'rstate'
```

I executed the exact downstream class declaration and the actual `search_internal_from` method, intercepting only live-point generation and the pool-marker write.

This is a new failure mechanism, contradicting the assertion that graphical failures are unchanged from main. The listed companion changes omit this consumer.

**Required correction:** resolve `rstate` once with defined override precedence, and update the downstream helper to the supported seed interface.

### 3. P2 — Grid child streams do not reach several backends

**PR:** #1686. **Confirmed empirically for seed material; backend call sites inspected.**

**Locations:** [grid_search/__init__.py:329](PyAutoFit/autofit/non_linear/grid/grid_search/__init__.py:329), [MultiStart search.py:1961](PyAutoFit/autofit/non_linear/search/mle/multi_start_gradient/search.py:1961), [NSS search.py:395](PyAutoFit/autofit/non_linear/search/nest/nss/search.py:395).

**Input → wrong output:** two children of a search with `seed=9`, assigned spawn keys `(0,)` and `(1,)`.

- Nautilus, NSS, NUTS and SMC still receive backend seed **9 in both children**.
- MultiStart’s `_seed_for(0)` produces identical broad-start random sequences in both children; its resurrection stream also ignores the child key.
- NSS generates its actual initial population directly from that raw JAX key; the generic `start_points` test does not exercise this path.

The new helpers distinguish child streams, but these execution paths bypass them. NUTS/SMC initializer points can differ while backend randomness remains shared.

**Required correction:** incorporate child provenance into those backend seed paths. Preserve existing standalone seeded behavior when no child key exists. This does not require reversing the accepted MultiStart identifier re-key.

### 4. P2 — Family-base removal shifts existing positional constructor arguments

**PR:** #1687. **Confirmed empirically; prior signatures inspected.**

**Locations:** [Drawer search.py:49](PyAutoFit/autofit/non_linear/search/mle/drawer/search.py:49), [SMC search.py:102](PyAutoFit/autofit/non_linear/search/mcmc/blackjax/smc/search.py:102).

**Concrete Drawer input:**

```python
Drawer(None, None, None, 50, None, 12, 34, True)
```

| Attribute | Before PR 3 | After PR 3 |
|---|---:|---:|
| Full-update cadence | 12 | 34 |
| Quick-update cadence | 34 | 1 |
| `silence` | True | False |
| `clipper` | `ClipperNone` | integer `12` |

Adding `clipper` in the middle silently rebinds valid calls. Constructor-argument **set** comparisons cannot catch ordering changes.

SMC has the corresponding removal problem: an old positional `AutoCorrelationsSettings` argument now occupies the quick-update slot and raises:

```text
TypeError: float() argument must be a string or a real number,
not 'AutoCorrelationsSettings'
```

Popping the deprecated keyword only protects keyword/JSON callers.

**Required correction:** add Drawer’s explicit clipper without shifting existing positional slots, and provide compatibility handling for SMC’s removed positional slot.

## §4 PR-body claims not independently verified

- Full-suite, Python-version, no-JAX, workspace-smoke and Sphinx-warning totals.
- Disk-backed historical aggregator imports, interrupted-output recovery, HDF resume, zipped output and exact file inventories.
- The complete two-step EP witness and developer-backend fits. UltraNest’s reported NumPy ABI failure and baseline comparison were not independently reproduced.
- Arbitrary historical Result pickles and every external override/monkeypatch pattern.

The companion survey found **no family-base imports** in the searched PyAutoLens, PyAutoGalaxy, PyAutoCTI or assistant Python/Markdown/RST sources. The named consumers remain unchanged here:

- [Brain sampler guidance:129](PyAutoBrain/skills/sampler_pipeline/reference.md:129)
- [UltraNest:14](autofit_workspace_developer/searches/ultranest/search.py:14)
- [PySwarms:48](autofit_workspace_developer/searches/pyswarms/abstract.py:48)

Their proposed replacements are broadly consistent with the new API, but companion delivery is not demonstrated by this checkout. The list also needs the graphical Dynesty consumer from finding 2.

The global-random survey found the relevant initializer-seeding reliance in `analytic_autofit.py:229`; other hits inspected concern simulation/data generation or NumPy randomness. PySwarms still calls `samples_from_model` directly without passing the search RNG.

## §5 PR-body decisions I would overturn

1. **Treating old default NUTS/SMC JSON re-keying as harmless.** The aggregator recomputes identity; finding 1 disproves the justification.
2. **Keeping identical raw backend seeds across grid children.** This contradicts the independent-child-stream requirement. Preserve standalone compatibility while deriving child-specific backend seeds.
3. **Inserting/removing constructor slots without positional compatibility.** Preserve serialization changes without silently rebinding callers.
4. **Treating the companion list and graphical baseline comparison as complete.** The existing seeded Dynesty subclass is a concrete missed consumer.

I would retain the human-accepted MultiStart explicit-seed re-key, deprecated pool shims, `SneakyPool`, SMC’s weighted plotter, construction-time chain defaults, and the deferred A5 scope.