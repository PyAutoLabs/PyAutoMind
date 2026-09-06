# replace_promise runs only when a recursion promise actually escaped — model.info halved

PyAutoFit#1564 → `cab17a3ee`, closing PyAutoFit#1563, merged 2026-09-06 on branch
`claude/ci-test-timing-epic-ke2lul`. Phase 8c (library leg) of the `ci-timing-fast-tests`
epic, from the phase-8 user-workspace diagnosis. Fable-planned on the issue from the
phase-8 executor's measured diff; implemented by an Opus subagent from a web session.

- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1563
- completed: 2026-09-06
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1564

## What shipped
- `autofit/mapper/prior_model/recursion.py`: `RecursionPromise` gains a `used` flag
  (`__slots__`), set when `DynamicRecursionCache` hands the placeholder back to a caller;
  `replace_promise` (the recursive `setattr` walk over every object reachable from the
  result) runs only when the promise escaped. For a non-recursive model it never does.
- Tests compare the two implementations via a `force_traversal` fixture and a traversal
  counter: a self-referential `Collection` (traversal still runs, graph and `model.info`
  intact) and a flat model (count 0). 2421 passed / 25 skipped.
- Measured: `autolens_workspace multi_galaxy/features/advanced/shapelets/modeling.py`
  under the smoke profile, warm, 10.58 → 6.73 s, stdout byte-identical.

## Key traps / findings
- `print(model.info)` appears in nearly every modeling script in every workspace at
  0.5–1.3 s each; this is the single largest systemic win on the user-facing surface.
- Phase 9's CI census confirms from the third side: `replace_promise` no longer appears in
  PyAutoFit's CI top 25 on this head.

## Follow-ups
- Release: PyAutoFit release outstanding (`pending-release`).

## Original prompt

# replace_promise walks the whole model graph even when no promise escaped (model.info cost on every modeling script)

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-09-06
Epic: ci-timing-fast-tests
Phase: 8c
Issued: 2026-09-06

Library leg of phase 8 (autolens_workspace#536): a shared-machinery finding from the
user-workspace slow-script diagnosis, traced to the unguarded call in the library and written
up as a diff there rather than patched per script. The measurement and the diff below are the
phase-8 executor's; nothing was applied to the library. Library-first gate: this lands before
any workspace script relies on it. Validation: the library unit tests plus a before/after of
the named workspace scripts under the smoke profile.

## (a1) PyAutoFit — `replace_promise` walks the whole model graph even when no promise escaped

**File** `autofit/mapper/prior_model/recursion.py`
**Functions** `RecursionPromise`, `DynamicRecursionCache.__call__.wrapper`
**Consumers** `autofit/mapper/model.py:338` `path_instances_of_class`,
`autofit/mapper/prior_model/abstract.py:1389`

`DynamicRecursionCache` hands out a `RecursionPromise` placeholder for the duration of a
decorated call and then calls `replace_promise(...)` unconditionally, which recursively
`setattr`s its way through **every object reachable from the result** looking for that promise.
For a non-recursive model the promise is never handed to anyone, so no object can possibly
contain it and the entire traversal is provably a no-op — but it is still paid, once per
decorated call, over a graph that grows with the model. `model.info` on a shapelet basis makes
hundreds of such calls.

**Measured**: `multi_galaxy/features/advanced/shapelets/modeling.py` **10.1 s -> 5.4 s** with
`replace_promise` neutralised at runtime, and `model.info` byte-identical. On a small synthetic
model `model.info` is 0.17 s -> 0.01 s, again byte-identical. `print(model.info)` appears in
nearly every modeling script in every workspace, at 0.5–1.3 s each, so this is the single
largest systemic win available on this surface.

```diff
--- a/autofit/mapper/prior_model/recursion.py
+++ b/autofit/mapper/prior_model/recursion.py
 class RecursionPromise:
-    pass
+    # ``used`` records whether this placeholder was ever handed back to a caller.
+    # If it never was, no object in the result can hold a reference to it and the
+    # ``replace_promise`` traversal below is provably a no-op.
+    __slots__ = ("used",)
+
+    def __init__(self):
+        self.used = False
@@ def wrapper(item, *args, **kwargs):
             if item_id in self.cache:
-                return self.cache[item_id]
+                promise = self.cache[item_id]
+                promise.used = True
+                return promise
             recursion_promise = RecursionPromise()
             self.cache[item_id] = recursion_promise
             result = func(item, *args, **kwargs)
-            result = replace_promise(recursion_promise, result, result)
+            if recursion_promise.used:
+                result = replace_promise(recursion_promise, result, result)
             del self.cache[item_id]
             return result
```

Note `__slots__` also removes the `try: obj.__dict__` branch cost when a promise *is* live.
A regression test should assert `model.info` is unchanged for a genuinely self-referential model
(the case the cache exists for) as well as for a flat one.
