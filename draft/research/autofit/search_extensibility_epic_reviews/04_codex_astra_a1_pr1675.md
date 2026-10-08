# Codex gpt-6-astra adversary review — A1 (PyAutoFit#1675), 2026-10-08

Independent-adversary leg over branch `feature/search-ext-a1-declare-gate` at c03f027a1 (`codex exec --sandbox read-only -c model_reasoning_effort=high`, run from the task worktree root). Enacted the same day; see the PR and `complete/2026/10/search-ext-a1-declare-gate.md` once closed.

## §1 Verdict — FINDINGS

Six defects need resolution or explicit judgement: three in the D12 graph contract and three in the published capability declarations.

Sandbox-adapted checks produced **288 passing tests**. I disabled filesystem-writing pytest fixtures and replaced `NullPaths` temporary-directory creation in memory. Additional checks requiring writes were blocked, as detailed below. No files changed.

## §2 Witness falsification

| Clause | Disposition and evidence |
|---|---|
| Deleting any registry entry fails completeness | **Holds.** Removed each of the 15 entries individually in memory and invoked the [completeness assertion](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/test_autofit/non_linear/search/test_registry.py:74). All 15 deletions were detected. |
| Capability matrix renders 15 rows from the manifest | **Holds locally; deployed RTD unverified.** Executed the CLI entry point in-process: 15 manifest entries. The generator reproduced all three committed pages. Docutils rendered the capability table with 15 data rows and no warnings, using a substitute for Sphinx’s `class` role. This does not establish a complete RTD build. |
| REQUIRED search plus NumPy analysis raises the shared `SearchException` | **Holds.** All seven REQUIRED searches passed the [shared-message tests](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/test_autofit/non_linear/search/test_jax_required_gate.py:57), including backend-not-reached assertions. The disable-JAX/test-mode-2 cases also passed. |
| `import autofit` imports no optional backend | **Holds.** Fresh-process import of this checkout, followed by manifest construction, loaded none of the listed optional backends. Registry lazy-module checks also passed. |
| `docs/design/run_ctx.md` is in the PR | **Holds.** Commit `c03f027a1` adds the [design note](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/docs/design/run_ctx.md:1), including the frozen signature, context members and lifecycle rules. |

## §3 Findings, ranked by severity

### 1. P1 — Legacy graph pickles silently change backend and cannot flatten

**Location:** [collection.py:72](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/graphical/declarative/collection.py:72), [collection.py:54](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/graphical/declarative/collection.py:54).

**Input → wrong output:** A graph constructed by `origin/main` with JAX children and explicit `use_jax=False` stores `_use_jax=False`. Loading that pickle on this branch produces `is_jax=True`. Calling `tree_flatten()` then raises:

```text
AttributeError: Analysis has no attribute _explicit_use_jax
```

The new descriptor ignores the old dictionary field, while flattening assumes the new field exists.

**Empirically confirmed:** Loaded the actual `origin/main` class definition in memory, pickled its instance, restored the branch class, and unpickled. This was not merely a fabricated legacy dictionary. A state migration must preserve the old explicit choice.

### 2. P1 — Backend inference rejects a valid all-JAX hierarchical graph

**Location:** [collection.py:75](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/graphical/declarative/collection.py:75).

**Input → wrong output:**

```python
h = af.HierarchicalFactor(
    af.GaussianPrior,
    mean=af.GaussianPrior(mean=0, sigma=1),
    sigma=1.0,
    use_jax=True,
)
h.add_drawn_variable(af.GaussianPrior(mean=0, sigma=1))
graph = af.FactorGraphModel(h)
```

The generated factor reports `is_jax=True`, but `graph.is_jax` is **False**. `graph.check_backend_agreement()` rejects that same factor.

Inference reads unflattened `_model_factors`, including the `HierarchicalFactor` container; agreement checking instead reads flattened factors. The container lacks the required `is_jax` property, and the outer probe masks the resulting attribute failure as False.

**Empirically confirmed.** The existing hierarchical test checks the generated children, not inference through their containing graph.

### 3. P2 — `ModelAnalysis` bypasses whole-graph agreement

**Location:** [abstract_search.py:863](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/search/abstract_search.py:863).

**Input → wrong output:** Create a graph containing one NumPy and one JAX factor. Passing the graph directly raises the intended `SearchException`. Passing `ModelAnalysis(graph, graph.global_prior_model)` reaches `_fit` instead.

The check only recognizes a directly supplied `FactorGraphModel`. The wrapper forwards the likelihood but is excluded by `isinstance`.

**Empirically confirmed:** Substituted a backend that raises `BackendReached`; the bare graph raised `SearchException`, while the wrapped graph raised `BackendReached`. D12 validation needs to survive supported wrappers.

### 4. P2 — NSS declares the wrong sampling coordinates

**Location:** [NSS search.py:211](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/search/nest/nss/search.py:211).

NSS declares `objective_target.space="unit_cube"`, although the capability definition describes coordinates proposed by the backend.

**Input → wrong output:** For a `UniformPrior(10, 20)`, an initial unit coordinate `0.5` becomes physical parameter `15` before entering `algo.init`. The NSS likelihood calls `instance_from_vector`, and the sampler receives a physical-space prior density. The manifest nevertheless publishes `unit_cube`.

**Confirmed by inspection:** [initial transformation at line 440](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/search/nest/nss/search.py:440) and subsequent `algo.init(initial_samples)` establish this. Initializing through a unit cube does not make the sampling coordinates unit-cube coordinates.

### 5. P2 — Minimizer `invalid_value` declarations misdescribe returned objectives

**Location:** [BFGS search.py:51](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/search/mle/bfgs/search.py:51), [MultiStart search.py:63](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/search/mle/multi_start_gradient/search.py:63).

**Input → wrong output:** A likelihood returning NaN, evaluated with BFGS’s actual Fitness settings, returns **`+inf`**. The declaration, manifest and generated documentation say **`-inf`**.

Fitness replaces NaN with `-inf`, then [multiplies by −2](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/fitness.py:503). Conversely, its early `FitException` return remains `-inf`. Therefore simply flipping the declaration is insufficient: the existing invalid-value behavior is conditional.

**Empirically confirmed for the BFGS Fitness configuration; MultiStart uses the same settings by inspection.** The runtime inconsistency predates A1, but the newly published unconditional contract is incorrect. Describe that limitation without silently expanding A1 into sentinel normalization.

### 6. P2 — Emcee’s `resumable=False` contradicts its HDF resume implementation

**Location:** [Emcee search.py:40](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/search/mcmc/emcee/search.py:40).

**Input → wrong output:** An interrupted Emcee run with an HDF backend is reported as non-resumable by the manifest and summary. Its implementation opens that backend, [loads the last sample and iteration count](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/search/mcmc/emcee/search.py:183), and samples the remaining iterations.

**Confirmed by inspection, not an interrupted-run experiment.** The declared meaning is “an interrupted run resumes from its own checkpoint,” not “an exact optimizer/kernel state is restored.” Literal adherence to the report’s table does not make this value accurate.

## §4 Claims not independently verified, and remaining audit results

**Not independently verified:**

- The reported full-suite, no-JAX, downstream-suite and workspace-smoke totals.
- Full minimal/full-extras Sphinx builds, the 30-warning baseline, and deployed RTD inventory resolution.
- End-to-end mixed-factor EP: its test reached a directory-output write and failed on the read-only filesystem. This is an environment limitation, not evidence of a branch regression.
- Live GitHub CI conclusions or clean-runner dependency installation. Ordinary CLI subprocesses also encountered the sandbox’s temporary-directory restriction; CLI/generator checks used their entry points in-process.

**Verified or inspection-supported:**

- **A0 goldens unchanged:** the golden table has no diff; identifier, constructor-field and search-JSON round-trip tests passed. No capability enters `__identifier_fields__`. Both claims lifted by the review surface concerning unchanged identifiers therefore have a cited basis in [the conformance tests](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/test_autofit/non_linear/search/test_conformance.py:112).
- **Gate placement correct:** test-mode bypass precedes both gates at [abstract_search.py:851](/home/jammy/Code/PyAutoLabs-wt/search-ext-a1-declare-gate/PyAutoFit/autofit/non_linear/search/abstract_search.py:851).
- **Probe migration:** no old `_use_jax` consumer probes remain in PyAutoFit searches/Fitness/latent machinery. Storage, forwarding descriptors and the central probe remain intentionally. Downstream libraries still contain their pre-existing direct probes.
- **Exception consumers:** searched `ValueError` handlers across all seven requested repositories/workspaces; found no handler wrapping the old REQUIRED construction/fit gate.
- **Budgets:** all 15 budget tests passed. NUTS/SMC values are caps; MultiStart reductions live in its convergence object. BFGS/LBFGS/Drawer correctly declare empty current budgets.
- **Nautilus:** its NumPy `force_x1_cpu=True` regression test passed.
- **Summary consumers:** the header changes file content, but I found no affected positional parser in the searched consumers. External parsers remain unverified.
- **CI wiring:** `generated-search-docs` is a separate ordinary job alongside Heart’s reusable workflow; that structure is valid. Its generator requires no Sphinx installation.
- **Downstream links:** all three load intersphinx, define the `autofit` mapping, and reference the generated label correctly. Actual resolution still depends on the upstream inventory publication.
- **Scope:** no executable `run(ctx)` bridge, objective factory, trace preflight, x64 enforcement or NSS-to-Fitness migration leaked into A1.

## §5 Flagged decisions and judgement values

- **Keep** the gates after the test-mode bypass.
- **Keep the intent** of `use_jax=None` inheritance, but reject the implementation as complete until findings 1–3 are addressed.
- **Correct the migration advice:** explicit `FactorGraphModel(use_jax=False)` does not force JAX children onto NumPy; agreement checking can reject them.
- **Overturn Emcee `resumable=False`** under the published definition. Correct the design table alongside the implementation.
- **Keep NUTS `batched=True`:** its warmup and sampling operate through chain-wise `vmap`.
- No evidence warrants overturning the four experimental statuses, mode-finder `warm_start="provider"`, reverse-mode fallback for mixed gradient declarations, or deferring `checkpointer` to A3.
