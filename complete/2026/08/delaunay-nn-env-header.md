# delaunay-nn-env-header

Follow-up from #499 close-out. `misc/jax_assertions/delaunay_nn.py` / `delaunay_nn_caps.py`
declared `ENV: jax full_datasets` but CI ran them with JAX off and small datasets.

## Shipped
- autolens_workspace_test#285 — added the `__Env__` header AND moved the docstring summary line
  off the opening `"""`: `read_env_declaration()`'s delimiter regex only matches a bare `"""` line,
  so a prose-on-opener docstring inverts the block parity and the whole declaration is skipped.
  These were the only 2 of 92 `__Env__` scripts with a non-bare opener. Now resolves
  `PYAUTO_DISABLE_JAX=None`, `PYAUTO_SMALL_DATASETS=None`; smoke runner 28.1 s / 50.6 s vs 300 s cap.

## Open (not filed here)
- `validate_env_profiles.py` is clean before and after: it detects neither a headerless `ENV:`
  line nor a non-bare docstring opener swallowing a valid declaration. Candidate PyAutoHands task.

## Original prompt

# delaunay_nn jax_assertions carry a dead ENV declaration (no __Env__ header)

Type: bug
Target: workspaces
Repos:
- autolens_workspace_test
- workspaces
Difficulty: small
Autonomy: safe
Priority: normal
Issued: 2026-08-28
Status: formalised

# delaunay_nn jax_assertions carry a dead ENV declaration (no __Env__ header)

Type: bug
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: normal

## Problem

`scripts/misc/jax_assertions/delaunay_nn.py` and `delaunay_nn_caps.py` carry an
`ENV: jax full_datasets` line but no `__Env__` docstring header, so
`read_env_declaration()` returns `None` and the declaration is dead. Both are registered in
`smoke_tests.txt`, so CI has been running them with `PYAUTO_DISABLE_JAX=1` and
`PYAUTO_SMALL_DATASETS=1` — the opposite of what they ask for. `validate_env_profiles.py`
did not flag it.

## Fix

- Add the `__Env__` header to both (convention: the other `jax_assertions` scripts, e.g.
  `fit_interferometer_sparse_operator.py`).
- Verify with `build_env_for_script` that `PYAUTO_DISABLE_JAX` and `PYAUTO_SMALL_DATASETS`
  resolve to `None`; run both under the smoke runner and confirm runtime stays inside the smoke
  timeout budget with JAX + full datasets on. If it does not, decide whether `full_datasets` is
  really needed rather than dropping the script.
- Sweep this repo (and, if cheap, the sibling test workspace and the user workspaces) for any other
  `ENV:` line lacking the `__Env__` header. Optionally propose the missing check for
  `validate_env_profiles.py` as a separate follow-up in the build tooling repo — do not widen this task into it.

## Context

Found 2026-08-28 during the close-out of the array library's issue #499.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b766a19b-260c-4b56-8d19-072fa9a34b28/scratchpad/intake_dead_env.md -->
