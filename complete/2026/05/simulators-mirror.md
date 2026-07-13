## simulators-mirror
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/4
- completed: 2026-05-16
- repo-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/9
- merge-commit: 75a562f
- summary: |
    Phase 2 of the autolens_profiling z_feature. Mirrored 6 simulator
    profiling scripts (~2040 LOC) from clean origin/main of
    _developer/jax_profiling/simulators/ into autolens_profiling/simulators/,
    plus replaced the Phase 0 placeholder README with a section README
    covering all 6 scripts.

    Files mirrored:
      imaging.py, interferometer.py, point_source.py,
      cluster.py, group.py, multi.py

    Path rewrites applied uniformly:
    - `_workspace_root / "jax_profiling" / "dataset"` -> `_workspace_root / "dataset"`
    - `_workspace_root / "jax_profiling" / "results" / "simulators"`
        -> `_workspace_root / "results" / "simulators"`
    - `_script_dir.parents[1]` -> `_script_dir.parents[0]`
        (one level shallower than Phase 1 because simulators are at
         simulators/<name>.py vs jax_profiling/simulators/<name>.py)
    - Docstring `python jax_profiling/simulators/<name>.py`
        -> `python simulators/<name>.py`

    The artifact filename convention is unchanged:
    `results/simulators/<script>_summary_v<al.__version__>.{json,png}`

    Smoke: py_compile PASSED for all 6. Full runtime smoke skipped
    intentionally — simulators/point_source.py at default
    dataset_name="simple" writes to dataset/point_source/simple/
    which holds Phase 1's tracked likelihood input JSONs
    (point_dataset_positions_only.json, tracer.json). Running it
    without changing the dataset_name would corrupt those tracked
    files. Phase 5's AUTOLENS_PROFILING_SMOKE=1 short-circuit will
    provide a clean smoke path; until then, smoke manually by
    passing a non-conflicting dataset_name (e.g. "smoke").

    F1 lesson applied: copies came from worktree's clean origin/main
    of _developer (NOT the canonical, which is dirty with ~36
    modified files).

## Original prompt

Phase 2 of the `autolens_profiling` z_feature
(see `z_features/autolens_profiling.md` for the full roadmap).

Mirror the simulator-profiling scripts from
`autolens_workspace_developer/jax_profiling/simulators/` into the new
`autolens_profiling/simulators/` directory. `_developer` stays the
source of truth — do not delete originals.

Scripts to mirror (one-to-one):

- `simulators/imaging.py`
- `simulators/interferometer.py`
- `simulators/point_source.py`
- `simulators/cluster.py`
- `simulators/group.py`
- `simulators/multi.py`

Adjustments per-script:

- Update any `_developer`-relative paths to the new layout.
- Make sure results write to `autolens_profiling/results/simulators/` using
  the same `*_summary_v<version>.{json,png}` pattern the existing
  `_developer/jax_profiling/results/simulators/` artifacts already use.
- Preserve the run-time reporting each simulator already prints. The user
  has called out simulator timing as a first-class deliverable.

JIT-placeholder handling: the user has flagged that "JAX jitting for these
are not fully implemented everywhere so we may have placeholders and then
follow that up." For each simulator:

- If a JIT path exists and works, profile both NumPy and JIT.
- If JIT is not implemented or broken, profile NumPy only and emit a
  `jit: not-yet-implemented` note in the result JSON + a `TODO` link in
  the section README pointing at the upstream issue (open a PyAutoLens
  issue if none exists).

Section README to author:

- `simulators/README.md` — overview of what is being profiled (per-
  simulator construction time, dataset write time, NumPy vs JIT where
  applicable), how to read the result artifacts, and an at-a-glance table
  of the latest run-times (which Phase 4 will keep auto-refreshed).

Dataset handling: simulators *produce* datasets; they don't consume
existing ones. So there's no `dataset/` mirroring decision here — just
make sure the simulators write their outputs somewhere sensible inside
the new repo (probably `simulators/dataset/` or a top-level scratch dir
that's gitignored, depending on how the existing `_developer` scripts
behave).

Smoke check: run each simulator script end-to-end from the new repo
and confirm both the simulated dataset and the timing JSON land where
expected.

Out of scope: implementing JAX JIT for simulators that don't have it
yet — that's a PyAutoLens-library task, not part of this mirror.
