## parameterization-prior-count
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1635 (closed completed 2026-09-17)
- completed: 2026-09-17
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1637 (merged 7c0e79a)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1637
- session: https://claude.ai/code/session_01TSJ72sveM7GrTcddMXzUkb (web-github; Fable planned, Opus executed; /start_dev → /prm in one session)
- summary: |
    `AbstractPriorModel.parameterization` (the `(N=k)` block of every `model.info`)
    resolved every prefix of every leaf path and asked each model node for its own
    `prior_count`, itself a full recursive subtree walk, so the root and every
    ancestor were re-walked once per leaf beneath them: O(leaves x subtree). A
    module-private `_subtree_unique_priors(obj, memo)` now computes each node's
    distinct-prior set once, bottom-up, memoised by object identity for one call,
    mirroring the `path_instances_of_class(obj, Prior, ignore_children=True)`
    traversal behind `prior_count`. Leaf listing, prefix enumeration and the order
    handed to `find_groups` are untouched, so the text is byte-identical; each
    unique prefix is resolved once. Synthetic 561-prior model: 6.2 s / 3,244,174
    `path_instances_of_class` calls -> 0.012 s / 2,374.
- witness: |
    In-session: the pre-change algorithm kept verbatim as `_reference_parameterization`
    and compared byte-for-byte over eight model shapes; a shared prior counts once at
    the parent; `path_instances_of_class` calls during `parameterization` equal one
    leaf walk (118 = 118). Full `test_autofit/` 2813 passed / 48 skipped; CI green on
    97a92e6 (unittest 3.12 / 3.13 / nojax, docs-build). Run identifiers verified
    unchanged: `model.identifier` byte-identical on main vs branch for six model
    shapes, before and after touching `.info` (the identifier hashes `__dict__`
    skipping underscore keys; the change adds no attribute). DEFERRED to the human:
    the prompt's timing witness on `autogalaxy_workspace_test` `mge_group.py`
    (763,555 -> per-node calls; warm run 19.3 s -> <= 14 s) — that workspace is not
    in a web session.
- traps: |
    - The helper duplicates the traversal rules of `path_instances_of_class` for the
      `Prior` case rather than calling it (that function cannot share work across
      nodes); the oracle test is what pins the two together. Its `except` returns the
      partially accumulated result, mirroring the original, not an empty dict.
    - Cyclic references: the memo hands out the still-filling dict where
      `DynamicRecursionCache` hands out a back-patched promise; models are DAGs, so
      no test exercises it, but it is the one place the mirror is not provably exact.
    - `prior_count` itself and `model_tuples_with_type` (one `prior_count` per model)
      are deliberately unchanged; a later pass could memoise the same way if they
      ever show up in a profile.
    - `PyAutoMind/scripts/ledger_merge.py classify --base ...` blocks forever in the
      Claude Code web harness: it prefers stdin whenever stdin is not a TTY, and the
      harness stdin is a socket that never closes. Pass explicit paths instead.
    - Two sessions filed `active.md` entries at the same spot minutes apart; the
      first `mind_ledger_merge` run conflicted, a merge commit briefly landed conflict
      markers on `main` (run 282 passed `lifecycle.py check` with them present), and a
      follow-up commit removed them. `lifecycle.py check` does not detect conflict
      markers.
- autonomy: |
    Prompt header `Autonomy: safe`, `Unattended: ready`, refactor cap safe. Ran the
    safe flow with no plan-approval hold (plan on the issue at start, unmodified);
    merge on the human's typed `/prm`. Heart unreachable in the session (no
    `pyauto-heart`); the full suite stood in as the gate. Review faculty not run.
    Shadow row appended at close-out (tier notify, stage 1, merged-unchanged: the PR
    merged as the single reviewed commit 97a92e6 with nothing changed after PR-open;
    the human was not asked the one question — the session ran unattended).

## Original prompt

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
Consequence: notify
Witness: `model.info` and `factor_graph.global_prior_model.info` on `autogalaxy_workspace_test` `mge_group.py` are byte-identical before and after; `path_instances_of_class` calls under `model.info` drop from 763,555 to at most one per node; the warm smoke run of that script drops by at least 5 s (19.3 -> <= 14 s).
Review-minutes: 0
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-17

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
