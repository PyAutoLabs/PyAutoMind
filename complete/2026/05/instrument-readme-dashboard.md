## instrument-readme-dashboard
- task-alias: instrument-dashboard  (matches active.md / worktree name during execution; full filename-stem slug here so the z_features audit picks this up as shipped)
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/6
- completed: 2026-05-16
- repo-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/10
- merge-commit: 2bd7fad
- summary: |
    Phase 4 of the autolens_profiling z_feature. Built the public-facing
    instrument-framed dashboard infrastructure that auto-generates the
    headline run-times tables in every section README from versioned
    artifacts under results/.

    What landed:
    - scripts/build_readme.py (270 LOC) — scans results/**/*_summary_v*.json,
      parses (section, sub-folder, script, instrument, version) tuples,
      picks latest version per axis via PEP 440-ish dotted sort, regenerates
      markdown tables between <!-- BEGIN auto-table:NAME --> / <!-- END --> sentinels.
      `--check` mode for CI gate.
    - 7 sentinel region types wired: headline (top-level), likelihood-
      {imaging,interferometer,point_source,datacube}, simulators,
      searches-nautilus.
    - All 7 target READMEs gained sentinel-tagged auto-table regions
      (replacing the "populated by Phase 4" placeholder tables from
      Phases 1-3). Surrounding hand-written prose preserved.
    - Top-level README: new "Latest run-times" section + Roadmap refreshed
      to show Phases 0-4 shipped + new "Future enhancements" subsection
      listing 6 deferred extras (regression-watch indicator, version-history
      PNGs, plotly timeline, flamegraphs, hardware-tier columns, archive policy).

    Design decisions resolved:
    - CPU/GPU split: single column for now (CPU only — every current
      artifact is implicitly CPU). Hardware-tier columns added as a
      Future enhancements entry; renderer change is small once artifacts
      gain a hardware label.
    - Versioning: keep all versions in results/, render latest. Archive
      to results/archive/ is a Future enhancements entry.
    - "Cool extras": ALL deferred to Future enhancements rather than
      landing any in this PR. The dashboard infrastructure is more
      valuable to ship first, and each extra is independently scoped.

    Today every auto-table renders "No data yet — run X to populate"
    because results/ is gitignored per Phase 1's design. Phase 5's CI
    workflow will commit artifacts on release; manual runs work too.

    Smoke: py_compile PASSED; first run populates 7 placeholders; second
    --check run exits 0 confirming idempotence; surrounding prose
    untouched.

## Original prompt

Phase 4 of the `autolens_profiling` z_feature
(see `z_features/autolens_profiling.md` for the full roadmap).

Build the public-facing READMEs (top-level + per-section) so that anyone
landing on `https://github.com/PyAutoLabs/autolens_profiling` immediately
sees the latest run-times framed by *astronomy instrument* (HST, Euclid,
JWST, etc.) rather than just pixel counts or grid sizes. This is the
deliverable the user has been most explicit about: "Framing it in terms
of Astronomy instruments and telescopes, instead of just 'number of
pixels' or other such metrics is way more intuitive."

What the dashboard should surface, in order of importance:

1. A top-level "headline" table on the front-page README: rows are
   instruments (HST imaging, Euclid imaging, JWST imaging, ALMA
   interferometer, …), columns are the supported model compositions (MGE,
   pixelization, Delaunay) plus a "JIT speedup vs NumPy" column. Cells
   show the latest single-likelihood evaluation time. Same table broken
   down further per-section README.
2. CPU / laptop GPU / HPC GPU split: either three columns per cell, or
   three stacked sub-tables, depending on what reads best on GitHub.
3. Version-history graphs: for each instrument × model combination, a PNG
   line plot of run-time vs PyAutoLens release version, generated from
   the versioned JSON artifacts under `results/`. These already exist in
   `_developer/jax_profiling/results/jit/.../*_v<version>.png` form —
   reuse the generation logic.
4. "How to reproduce" footer linking to the script that produced each
   row, so a reader can run it themselves.

Auto-generation:

- The `imaging` package already has instrument options ("hst", "euclid",
  etc.). Check what's actually supported today and lean on that to keep
  this scoped — don't fabricate instrument options that don't exist in
  the underlying simulator.
- Write a small `scripts/build_readme.py` (or similar) that scans
  `results/**/*_summary_v<version>.json`, picks the latest version, and
  regenerates the markdown tables. This is what Phase 5's CI workflow
  will call.
- The script should be idempotent — re-running it on unchanged results
  produces no diff.

READMEs that need authoring or refreshing in this phase:

- `README.md` (top-level) — vision (carry over from Phase 0), headline
  instrument table, JAX-gradient note (carry over from Phase 0), pointer
  to per-section pages.
- `likelihood/README.md` and each `likelihood/<dataset-type>/README.md`
  — instrument table for that section, link to per-script narrative.
- `simulators/README.md` — per-simulator run-time table broken down by
  instrument where applicable (e.g. simulator imaging for HST vs Euclid
  resolutions).
- `searches/README.md` and `searches/nautilus/README.md` — sampler
  run-time table; instrument framing is less natural here, so this
  section may default to "model complexity" rows (n_free_parameters) and
  is allowed to deviate from the strict instrument framing.

Open design questions for the implementer:

- Where do "cool extras" the user asked about live? (The user prompt
  ends with "Do a bit of deep research and thinking about other cool
  ways we can enhance a repo thats all about profiling and run times.")
  Candidates to consider: flamegraph captures alongside the timing
  numbers; a "regression watch" badge that turns red if any cell
  worsens by >X% vs the previous release; a Plotly-rendered interactive
  per-version timeline. Pick one or two, document the rest as future
  follow-ups under a "Roadmap" section in the top-level README.
- Versioning policy: how many historical PyAutoLens versions do we keep
  in the graphs? (Default: last 6 minor releases. Older artifacts can be
  archived under `results/archive/`.)

Out of scope: CI / GitHub Actions automation (that's Phase 5 — but
write `build_readme.py` so Phase 5 can call it).
