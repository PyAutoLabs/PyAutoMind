# Move the Witt–Wynne SIEP solver/projection into PyAutoLens once the two copies have settled

Type: refactor
Target: autolens
Repos:
- PyAutoLens
- autolens_workspace
- euclid_strong_lens_modeling_pipeline
Themes:
- point-source
- euclid
Difficulty: medium
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: `al.witt_wynne.*` exists with the pipeline's `tests/test_witt_wynne_util.py` ported and passing; on the DR1 catalogue inputs the library gives bit-identical solver output to `catalogue/scripts/witt_wynne_util.py` at the commit it was ported from; the guide and the pipeline import the library (the pipeline keeping a thin producer), with the pipeline change held behind the PyAutoLens release that carries it.
Review-minutes: 3
Filed: 2026-09-17

## Original request (verbatim)

> (deferred decision from the Witt–Wynne catalogue plan, 2026-09-17) Solver home: pipeline-local
> copy, with the guide fixed in parallel. The pipeline must not import the workspace, and the
> numerics just changed — freezing them into PyAutoLens is a follow-up refactor once both copies
> have settled.

## Context

- Two byte-identical-in-behaviour copies exist: `euclid_strong_lens_modeling_pipeline/catalogue/scripts/witt_wynne_util.py`
  (canonical, tests in `tests/test_witt_wynne_util.py`) and the reusable span of
  `autolens_workspace/scripts/guides/misc/witt_wynne.py` (identity-checked 2026-09-17).
- Candidate home: `autolens/point/witt_wynne.py` (pure numpy; `LensCalc`-based projection).
- Blocked on: the compiled Zenodo C++ round-trip (never re-run since the fixes), and any further
  numerics changes from real-data use (DR1 shows verdict 9/10, positions 10–40 % of b).

## Deliverables

1. Library module + unit tests (port the pipeline's tests), public API `al.witt_wynne.*`.
2. Guide and pipeline import the library; pipeline keeps a thin producer only.
3. Release-gate note: the pipeline change waits for the PyAutoLens release that carries it.
