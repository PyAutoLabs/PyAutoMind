# jax_delaunay's six-tuple unpacked in imaging/jax_likelihood/delaunay.py, script promoted to the PR gate

autolens_workspace_test#300 → `1f6112ea`, closing autolens_workspace_test#296, merged 2026-09-07. One of six corrective PRs shipped 2026-09-07 under the human-authorised Heart RED corrective-PR exception (reasons: `release validation FAILED (stage integrate)` and `workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)`). Fable session planned; Opus subagents implemented per task; merged via /prm the same day. Validation of the RED clearing is the next scheduled Workspace Smoke and Release Integrate runs on fresh wheels.

- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/296
- completed: 2026-09-07
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/300
- corrective-red: authorization https://github.com/PyAutoLabs/autolens_workspace_test/issues/296#issuecomment-5573411434

## What shipped
- `scripts/imaging/jax_likelihood/delaunay.py`: `_, _, mappings, split_points, split_mappings, _ = jax_delaunay(...)` — PyAutoArray #524 (`46aaac67`) appended `areas` as a sixth return; this was the only five-value consumer in any workspace or library.
- `smoke_tests.txt`: the script is now on the PR-gate allowlist (18.7 s in CI); its absence is why the signature change broke it silently on the weekly/integrate channels only.
- PyAutoArray untouched: `scipy_delaunay` already documents the six-tuple; a named-tuple return would break four correct tuple-unpack sites.

## Key traps / findings
- The prompt's `Target: PyAutoArray` was overridden to autolens_workspace_test (consumer-only fix); the prompt's claim that the script was "disabled on the PR gate" was wrong — it was simply never on the curated allowlist (the disabled sibling is `delaunay_mge.py`).

## Original prompt

# jax_delaunay returns more than the five values imaging/jax_likelihood/delaunay.py unpacks

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Filed: 2026-09-06
Issued: 2026-09-07

Pre-existing on `autolens_workspace_test` `main` (reproduced on a detached
`origin/main` worktree during phase 6 of the ci-timing-fast-tests epic, so it
is not that phase's doing):

```
ValueError: too many values to unpack (expected 5)
  File ".../scripts/imaging/jax_likelihood/delaunay.py", line 384, in interpolated_sum
    _, _, mappings, split_points, split_mappings = jax_delaunay(
```

`jax_delaunay`'s return signature grew and this consumer was not updated. The
script is already disabled on the PR gate for a different reason (the jax-0.7
`pytype_aval_mappings` removal note in `smoke_tests.txt`), so it fails silently
on the weekly channel. Everything before line 384 passes on the phase-6 branch
(vmap literal, poisoned-lane isolation, `jit(fit_from)` round-trip, invalid-mesh
NaN check).

Ask: (1) find the commit that changed `jax_delaunay`'s return tuple and every
in-repo caller of it; (2) update `interpolated_sum` in the workspace script (and
any sibling) to the current signature; (3) re-check whether the gate disable
reason still holds under the installed jax and, if not, re-enable the entry.
