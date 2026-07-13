## likelihood-jit-mirror
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/1
- completed: 2026-05-16
- repo-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/2
- merge-commit: 7c464c2
- summary: |
    Phase 1 of the autolens_profiling z_feature. Mirrored the JIT
    likelihood profiling scripts and their tracked input datasets from
    autolens_workspace_developer/jax_profiling/jit/ into the new
    autolens_profiling repo at likelihood/ and dataset/. _developer
    stays the source of truth — nothing moved or deleted upstream.

    9 scripts + 1 __init__.py mirrored verbatim (filename-preserving)
    across imaging/, interferometer/, point_source/, datacube/. ~7,400 LOC.
    14 dataset files mirrored (~900K, checksums verified). 5 READMEs
    authored: top-level likelihood/README.md + 4 per-section.

    Path rewrites applied uniformly across all 9 scripts:
      Path("jax_profiling") / "dataset"     -> Path("dataset")
      _script_dir.parents[2]                -> _script_dir.parents[1]
      "jax_profiling" / "results" / "jit"   -> "results" / "likelihood"
      docstring sibling refs                -> new layout
    The if should_simulate(...) block at the top of each script was
    replaced with a clear FileNotFoundError pointing back at
    _developer/jax_profiling/dataset_setup/ for regeneration (Phase 1
    out of scope).

    Decision locked in: dataset/ lives at top-level (shared with Phase 2
    simulators and Phase 3 searches), NOT under likelihood/.

    Smoke (CPU, all 4 produced artifacts at expected results/likelihood/
    paths):
      - imaging/mge.py [hst]: artifacts ✓; regression assertion
        pre-existing drift (constant unchanged from _developer).
      - interferometer/mge.py [sma]: ALL PASSED.
      - point_source/image_plane.py [simple]: artifacts ✓; regression
        assertion pre-existing drift (large: 0.07 → -362, sign change).
      - datacube/delaunay.py [sma × 4]: ALL PASSED (both eager and
        full-pipeline cube regressions).

    Pre-existing drift in imaging/mge and point_source/image_plane is
    upstream science work for _developer — same drift would manifest if
    those scripts ran on PyAutoLens 2026.5.14.2. Worth a separate
    follow-up issue against _developer (especially the point_source one,
    which suggests a real behaviour change rather than fp noise).

## Original prompt

Phase 1 of the `autolens_profiling` z_feature
(see `z_features/autolens_profiling.md` for the full roadmap).

Mirror the JIT-profiling likelihood scripts currently in
`autolens_workspace_developer/jax_profiling/jit/` into the new
`autolens_profiling/likelihood/` directory. `_developer` remains the
source of truth — do not delete the originals.

Scripts to mirror (one-to-one, preserving file names):

- `jit/imaging/{mge,pixelization,delaunay}.py`
- `jit/interferometer/{mge,pixelization,delaunay}.py`
- `jit/point_source/{image_plane,source_plane}.py`
- `jit/datacube/delaunay.py` (+ its `__init__.py`)

Adjustments per-script:

- Update any path references that assume the `_developer` workspace layout
  (e.g. `Path("jax_profiling") / "imaging" / "dataset" / ...`) to the new
  repo's layout (e.g. `Path("likelihood") / "imaging" / "dataset" / ...`).
- Make sure `results/` writes use the same versioned-artifact naming the
  `_developer` repo already uses (`*_summary_v<version>.{json,png}`) so the
  Phase 4 README dashboard can pick them up.
- Keep the printed step-by-step profile narrative each script already
  produces — it is the user-facing documentation. The user has been
  explicit: "make sure you keep that".

Per-section READMEs the implementer should author at the same time:

- `likelihood/README.md` — overview of the section, what "JIT likelihood
  profiling" means, how to read the per-script output, and how the
  versioned result artifacts work.
- `likelihood/imaging/README.md`, `likelihood/interferometer/README.md`,
  `likelihood/point_source/README.md`, `likelihood/datacube/README.md` —
  each with a short narrative on what the profiled likelihood path looks
  like and a table of the most-recent run-times for the scripts in that
  folder. Table population can be a placeholder filled in by Phase 4's
  auto-generation, but the section structure should already be there.

Dataset handling: `_developer/jax_profiling/dataset/` provides the input
datasets these scripts depend on. Decide whether to mirror those files
into `likelihood/dataset/`, symlink, or document a one-time `make
dataset` step. Lean toward mirroring the small simulated datasets so the
new repo is fully self-contained — but check sizes first before
committing binary blobs.

Smoke check before declaring done: run one script from each subfolder
end-to-end from the new repo (`cd autolens_profiling && python
likelihood/imaging/mge.py` etc.) and confirm the JSON / PNG summaries
land under `autolens_profiling/results/`.

Out of scope: anything from `_developer/jax_profiling/gradient/` (still
gated on the JAX gradient story stabilising) or `_developer/jax_profiling/misc/`
(exploratory work, not part of the stable profiling surface).
