# Memoise `prior_count` inside `AbstractPriorModel.parameterization` (O(N·depth) walk)

Type: refactor
Target: autofit
Repos:
- PyAutoFit
Themes:
- performance
- hygiene
Difficulty: medium
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Filed: 2026-09-10

`AbstractPriorModel.parameterization`
(`autofit/mapper/prior_model/abstract.py:2069`) walks every prefix path of every
prior/constant and calls `obj.prior_count` on each node. `prior_count` →
`unique_prior_tuples` → `attribute_tuples_with_type` → `path_instances_of_class`
is itself a **full recursive subtree walk**, so the whole thing is O(N·depth) and
the cost lands on any script that prints a model `.info`.

## Measurement

Found by `/ci_speedup` (2026-09-10) while auditing the slowest CI smoke scripts.
Measured on `autogalaxy_workspace_test`
`scripts/multi_dataset/jax_likelihood/mge_group.py`, smoke profile, warm JAX cache:

| phase | s | share |
|---|---|---|
| `print(model.info)` | 1.72 | 9% |
| `print(factor_graph.global_prior_model.info)` | 5.53 | 28% |
| **both `.info` prints** | **7.25** | **37% of a 19.4s warm run** |

Call counts on that model:

- `model.info` — 1,498 `prior_count` calls driving **763,555** recursive
  `path_instances_of_class` calls.
- `global_prior_model.info` — 3,497 `prior_count` calls driving **2,438,255**.

All of that produces ~25 lines of `(N=k)` annotation text.

cProfile attributes ~99% of the `.info` time to `parameterization`.
`parameterization` is already memoised per object (`_parameterization_cache`), so
a caller cannot pre-warm it — the blowup happens *within a single call*.

A/B, prints commented out and nothing else changed: warm **19.3 → 12.7s**,
cold **26.8 → 19.8s**.

## Why this is worth doing centrally

**25 of the 39 entries** in `autogalaxy_workspace_test/smoke_tests.txt` print a
`*.info`, so this is a standing cost across most of that gate, not one script.
The same pattern appears in the autolens test workspace.

## The fix

Memoise `prior_count` bottom-up across a single `parameterization` walk: compute
each node's count once from its children instead of re-walking the subtree per
node. Behaviour-preserving by definition — the rendered `.info` text must be
byte-identical before and after, which is the acceptance test.

## Explicitly NOT the fix

Deleting or trimming the `.info` prints in the smoke scripts. That text is those
lines' deliverable; removing smoke output is a coverage decision for a human, and
`/ci_speedup` forbids it as a speed-up. The scripts were left pristine.
