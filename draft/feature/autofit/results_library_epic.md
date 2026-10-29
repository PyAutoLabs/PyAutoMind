# Results library — index, complete, export and ship thousands of PyAutoFit results

Type: feature
Target: autofit
Repos:
- PyAutoFit
- autofit_workspace
- PyAutoLens
- autolens_assistant
- euclid_strong_lens_modeling_pipeline
- PyAutoCortex
Themes:
- hpc
- euclid
- results
- aggregator
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: campaign map — phases route through /start_dev one at a time; this file is never issued itself and nothing here is bulk-issued
Consequence: judge
Witness: phase 0 — a fixture tree holding one corrupt result zip aggregates with `agg.errors` of length 1 instead of raising, and an unknown AggregateCSV column path raises instead of writing None; phase 1 — `python -m autofit.results status` over a fixture of completed, interrupted and corrupt results prints one line per state class with the right counts
Review-minutes: 30
Unattended: needs-slicing
Epic: results-library
Filed: 2026-10-07

## Scope

This epic covers everything that happens **after** modelling runs complete:
indexing, status, completeness, reading, exporting, packaging, distributing
and reconciling a library of thousands of PyAutoFit results. The work is
generic and lives in PyAutoFit; Euclid DR1 is the pilot. Building the DR1
catalogue (Sept 9 – Oct 7, 2026) needed about 4.2k lines of hand-written
project tooling over the aggregator. Nine producers each re-walked and
re-extracted every result zip (about 16 min per 100 lenses, 27 h serial). The
final build took about 26 h from launch to verified zips against a 4-5 h
estimate. The released catalogue still carried wrong-cutout fits, duplicate
objects and 941 missing A+B lenses. Completeness, provenance and incremental
export were the missing primitives. The lessons, with session and timestamp
citations, are in `draft/feature/autofit/results_library_epic_report.md`,
cited below as "report Pn".

PyAutoLens appears in Repos only for the COOLEST/FITS hooks a lens result
exposes to the exporter. No lensing science changes are in scope.

## Original request (verbatim)

> Bringing together the euclid_dr1 catalogue became a bit of a nightmare, and we are still recnonciling issues now. Managing all the .zip files, the output folder build, large file sizes and many other things has been complex and slow. Do a review of the claude logs where we did this work, and file in PyAutoMind a task or an epic which will learn from what we did sub optimally and improve the PyAutoFit infrastructure for managing large results libraries. Note that we have already filed a similar prompt which looked at how when modeling runs we could have more outputs to track live progress and monitor what runs worked or not. This is more the follow up of that which focuses on the catalogue building side once modeling runs are complete.

## Boundary

**With hpc-campaign** (`draft/research/autofit/hpc_campaign_epic.md`, the
"similar prompt" already filed; report in
`draft/research/autofit/hpc_campaign_epic_report.md`):

- hpc-campaign owns **run time**: the per-fit `status.json` written by the
  running fit, failure records, resource measurement, the USR1 checkpoint
  flush, `campaign.yaml` submit/plan/resubmit, the Slurm adapter and carbon.
- results-library owns **post-run**: the results index, completeness over a
  declared grid, robust and lazy aggregator reads, incremental exports,
  chunk/merge of exports, packaging and distribution, identity and provenance,
  diff and parity.
- **Phase 0 is owned here and shared with hpc-campaign** (ruling F1,
  2026-10-28): one PyAutoFit issue, two PRs (0a artefact integrity, 0b honest
  reads). hpc-campaign records its phase 0 #A as issued here and does not
  re-issue it. The `fit()` failure record moved to hpc-campaign phase 1.
- Each epic may consume the other's artefacts. When hpc-campaign's
  `status.json` exists, the phase 1 index reads it as its status source. When
  it does not, the index classifies from disk.

**With `draft/feature/euclid/upstream_dr1_final_catalogue_tooling.md`**: that
prompt ports the DR1 science-clone scripts into
`euclid_strong_lens_modeling_pipeline` as they are, fragilities included.
This epic does **not** block it. Phase 5 later shrinks those scripts to the
Euclid-specific grade joins and product choices on top of the library.

## Phases

Library first in every phase. One issue per repo per phase, and each phase
ships on its own behind the ordinary `start_dev` → `ship_library` /
`ship_workspace` gates. Line references are PyAutoFit `main` @ `710f4b343`
(2026-10-07).

### Phase 0 — Integrity and honesty primitives (PyAutoFit) — no dependencies

Shared-with: hpc-campaign

One PyAutoFit issue, two PRs in sequence (review §D.1, ruling F1). The `fit()`
failure record is not part of this phase: moved to hpc-campaign phase 1.
Line references below are from 2026-10-07; the search-extensibility A-series
(`FitContext`/`run(ctx)`, `Checkpointer` + `internal_state.py`, `open_atomic`,
archive-before-`.completed`, paths capability flags; released 2026.10.26.1)
moved them — hook those, not the old lines.

**PR 0a — artefact integrity**

- **Atomic result zip.** `zip_directory` (`@PyAutoFit/autofit/tools/util.py`)
  writes `<path>.zip.tmp`, then `os.replace`. `.png`, `.fits` and `.hdf5`
  members are `ZIP_STORED` (incompressible, about 95% of a result's bytes);
  text stays DEFLATED.
- **`restore()` is non-destructive**
  (`@PyAutoFit/autofit/non_linear/paths/abstract.py`): extract to a temp dir and
  swap; never delete the zip unless the caller owns the result (`remove_files`
  and this search's identifier). A `BadZipFile` is quarantined as
  `<hash>.zip.corrupt_<utc>`, not left to fail every rerun. A read-only
  `open_result()` reads without restoring.
- **`is_complete` for a zipped result** checks `.completed` inside the zip
  plus `zipfile.testzip()`, cached (`@PyAutoFit/autofit/non_linear/paths/directory.py`).
- **Checkpoint validity probe before resume** in `Checkpointer.load`, for
  Nautilus and dynesty. Open with h5py and catch `OSError`, `ValueError`,
  `RuntimeError` and `KeyError`. On failure, or on a sampler exception
  (`LinAlgError`), move `search_internal/` aside to
  `search_internal.failed_<utc>/` and start fresh with a logged warning.
- **Timer moves to `files/`** behind the `has_timer` paths capability.
- Tests: a killed-mid-zip fixture resumes; two processes restore one zip
  concurrently; truncated-HDF5 and poisoned-checkpoint fixtures start fresh
  with the old state moved aside.

**PR 0b — honest reads**

- **`Aggregator.from_directory(..., on_error="skip"|"raise")`**
  (`@PyAutoFit/autofit/aggregator/aggregator.py`). Bad results are collected in
  `agg.errors` (path and exception) instead of one `BadZipFile` aborting the
  walk. An **empty** aggregator logs a loud warning naming the searched path
  and filters. Reporting moves from `print` to `logging`.
- **AggregateCSV strict by default**
  (`@PyAutoFit/autofit/aggregator/summary/aggregate_csv/__init__.py`).
  `strict=True` becomes the default, so an unknown column path raises and
  never writes `None`. The header becomes the union of all rows (today the
  first row). Atomic save. Labels join by key, not row index. `save()`
  reports blank columns.
- **Regression tests for `row.py`** sigma-1, sigma-3 and max_lh using an
  asymmetric latent PDF fixture. The bugs were fixed in PyAutoFit#1598; this
  adds the non-vacuous tests (report P11).
- Fix the inverted `post_fit_output` docstring
  (`@PyAutoFit/autofit/non_linear/search/abstract_search.py`).

Retires: report P1, P2, P11 (residual), P12 (partly), P13 (bad zip abort).
Gaps (report §4): 6, 7 (zip), 8, 17.
Done: a killed-mid-zip fixture resumes cleanly; a truncated-HDF5 and a
poisoned-checkpoint fixture both start fresh with the old state moved aside;
a tree with one corrupt zip aggregates with `agg.errors` of length 1; an
unknown CSV column raises; `autolens_workspace_test` smoke green.
Depends on: nothing. hpc-campaign phase 1 merges after PR 0a (both touch
`abstract_search.py`).

### Phase 1 — Results index, status classes, identity and lazy reads (PyAutoFit) — depends on 0

- **Incremental index** `.autofit_index/` per output root (ruling F2):
  per-result JSON records are the truth (rsync-friendly); a local SQLite
  cache is built by `python -m autofit.results index <root>` and is always
  rebuildable, never truth on NFS. The CLI is the writer; the fit writes only
  `status.json` and `dataset_identity.json`. Keyed on (zip path, size, mtime)
  so only new or changed results are opened.
- **State vocabulary imported, never redefined**: state classes come from
  `autofit/non_linear/status/states.py` (hpc-campaign phase 1). If that lags,
  this phase defines the enum and hpc-campaign adopts it; one owner either way.
- **Reads `status.json` when present** (hpc-campaign phase 1) as the status
  source; classifies from disk when absent.
- **One record per result**: dataset name and path, `unique_tag`, search name,
  identifier hash, state class, `completed_at`, products present (samples,
  latent, `image/`, `files/*`), library versions, and a schema stamp. State
  classes: `completed`, `running`, `interrupted_valid_ckpt`, `corrupt_ckpt`,
  `corrupt_zip`, `failed`, `superseded`, `never_started` (the last needs the
  phase 2 grid).
- **`dataset_identity.json`** written at fit start: user-supplied `object_id`
  (and optional external ids), input file paths, SHA256 of each input (on by
  default with a config off switch, ruling F10), and cutout centre where the
  dataset exposes one. Lives in `autofit/non_linear/status/identity.py`, in
  the same `FitContext` hook family as the status writer. Duplicates and wrong-input
  fits become detectable by join (report P5).
- **Sibling-hash policy**: `agg.latest_per(key=("unique_tag", "name"),
  by="completed_at")`, replacing the two mtime-based "latest zip" rules in
  the DR1 scripts. `completed_at` comes from the index, never zip mtime.
- **Lazy zip-member reads**: `SearchOutput`
  (`@PyAutoFit/autofit/aggregator/search_output.py`) reads `files/*.json`,
  `image/*` and summaries straight through `zipfile` with no extraction.
  `Aggregator.from_index(root)` replaces the eager `extractall` at
  `aggregator.py`:254-295. `search_output.open_member(path)` is public.
  `value(name, kind=...)` stops a bare name resolving JSON before FITS
  (the `tracer.json`/`tracer.fits` trap, report P15).
- **Follows custom output folders.** The user's words: "it will become
  common place for me to split results using custom output folders"
  (report P25). The index covers any number of roots and is
  layout-agnostic (flat or nested sample levels).
- Aggregator reporting moves from `print` to `logging`
  (`aggregator.py`:374-387, 504).
- **CLI**: `python -m autofit.results {index,status,count}`.

Retires: report P3 (post-run half), P4, P5, P6, P13, P15, P16 (dedup), P22.
Gaps: 1, 2, 3, 4, 5 (scan cache), 17 (print).
Done: a synthetic 15k-result fixture indexes in minutes and re-indexes
after 10 new results in seconds; "how many completed, how many corrupt" is
one command; aggregate over the index with zero bytes extracted to disk.
Depends on: phase 0.

### Phase 2 — Completeness over a declared grid, and enrich (PyAutoFit, autofit_workspace) — depends on 1

- **Declare the expected library**: datasets × searches (and per-product
  requirements) in `library.yaml` or by API (`af.ResultsLibrary(expected=...)`).
  `library.yaml: from_campaign: <campaign.yaml>` derives the grid from the
  hpc-campaign manifest, so the campaign file is the single declaration of
  what is expected; this epic never keeps a second manifest.
- **Completeness report**: expected / done / missing / incomplete, with
  **per-product** completeness. A zip that exists is not complete if
  `image/`, the latent summary or a named product such as `model.fits` is
  missing (the Tile102015606 pattern: 20 lenses QA-complete without a VIS
  magnitude row). Writes `<name>.missing.csv` with a reason per row.
- **`Aggregator.enrich(fn, name=..., overwrite=False)`** writes a new product
  into existing zips atomically from the saved result, sharded by index
  (`--shard i/N`). It replaces the `force_pickle_overwrite` toggle and SLURM
  reload pass used for `coolest.json` and `wcs.json` (report P7).
- **autofit_workspace**: a `results/` guide example (declare, index, check,
  enrich) on the gaussian example.

Retires: report P12 (wrong tree becomes "expected 0 found"), P17, P21
(implicit stage gates), P7.
Gaps: 9.
Done: on a fixture library with deliberate holes, the report lists every
missing (dataset, search, product) with its reason; `enrich` adds a member
to 100 zips with sha256 of all other members unchanged; workspace smoke green.
Depends on: phase 1.

### Phase 3 — Incremental, honest exports and chunk/merge (PyAutoFit) — depends on 1

- **AggregateCSV / AggregateFITS refresh**: per-result cached rows keyed by
  identifier and index state; a rebuild only touches new or changed results.
  Atomic writes (temp then `os.replace`, today a plain `open(path, "w")` at
  `aggregate_csv/__init__.py`:138). Per-row error capture.
- **Every expected lens gets a row or a reason**, never a silent drop
  (`status_reason`: `no_result`, `not_completed`, `missing_latent_summary`,
  `prior_edge` …). Labels join **by key**, not by row index
  (`add_label_column` today).
- **`<name>.columns.json`** sidecar: source path, kind (parameter / latent /
  derived), unit, bound type (`quantile_1sigma`, not ±err), n_blank (report
  P18). Optional prior-edge flag columns from the samples summary.
- **Plain-JSON view of typed outputs** (`search_output.plain(name)`),
  replacing hand decoders such as `build_wcs_package.plain_from`.
- **Scheduler-agnostic chunk/merge runner**: split the index into N shards,
  export each, merge with header agreement and key dedup. Usable from SLURM,
  a laptop pool or anything else; it generalises `merge_catalogue.merge_csv`.

Retires: report P14, P16 (labels), P17 (rows with reasons), P18, P20 (most
of the generic code).
Gaps: 5, 7 (CSV), 10, 11, 13, 15.
Done: on the 15k fixture, a refresh after 50 new results rewrites only those
rows; killing an export mid-write leaves the previous CSV intact; a 4-shard
export merges to a CSV byte-identical to the serial one.
Depends on: phase 1 (not phase 2; may run in parallel with it).

### Phase 4 — Packaging, distribution and parity (PyAutoFit) — depends on 3

- **`af.export.package(...)`**: size-capped parts, `parts_manifest.csv`,
  `SHA256SUMS`, STORED media / DEFLATED text, optional `include_dataset`
  (inputs and segmentation travel with the results, report P24), delta or
  atomic rebuild of one part, a `verify` step (members non-empty, CSVs parse,
  row counts match the manifest), and a README/KNOWN_ISSUES template with
  provenance (git revs, index hash, counts). Pure Python (`zipfile`), no `tar`
  dependency. It generalises `merge_catalogue.distribute` (`:571-728`).
- **Library diff/parity tool**: generalise `compare_catalogues.py` (1094
  lines) to identity / exact / tolerance-by-sigma columns, with duplicate-key
  detection and an error floor.
- **Run-to-run scatter helper** `af.agg.scatter_between(a, b, paths)`. Two
  Nautilus runs with the same code and data differed by a median z of 15.4,
  so "within 3σ" is the wrong parity test (report P19).

Retires: report P8 (packaging side), P19, P23, P24, P26 (fewer, larger files).
Gaps: 12, 14, 16 (packaging side).
Done: package a fixture library into 3 parts, rebuild one part after a
change with the other two byte-identical, `verify` catches an injected empty
member; the parity tool on two reruns of a fixture reports scatter, not FAIL.
Depends on: phase 3.

### Phase 5 — Organism integration and the DR1 census witness (autolens_assistant, pipeline, Cortex, hpc/sync) — depends on 2, 3, 4

- **autolens_assistant**: skill and wiki page "build and ship a results
  library" (declare → index → completeness → export → package → verify →
  reconcile), plus CRLF-safe readers for user manifests (`newline=""`, strip
  `\r`).
- **euclid_strong_lens_modeling_pipeline**: the ported scripts shrink to the
  grade joins and product choices over the library API.
- **hpc/sync**: pull the index and `inspect/` only; never the whole `output/`.
- **PyAutoCortex**: the ledger records the library index hash and counts for
  each release.
- **Witness: read-only census of the DR1 v1.0 standardised release (v5 tree)**
  on the 500-lens collaborator sample (ruling F8: 500 datasets, DR1 is fine):
  index, state classes and completeness against the manifest, reproducing the
  known excluded tiles, plus `package verify` on the 500-lens sample package.
  The DR1 release itself keeps its current tooling. ("DR1 v1.1" is retired; it
  existed only in this ledger.)

Retires: report P20, P22, P23 (CRLF), P25, P26, P32.
Done: the 500-lens DR1 census reports zero unexplained gaps (every exclusion
reproduced with a reason), `package verify` passes on the 500-lens sample, and
the Cortex ledger line carries the index hash. Pipeline legs wait until DR1
v1.0 has shipped.
Depends on: phases 2, 3 and 4.

## Non-library lessons

About half the pain was not PyAutoFit's (report §2, layers "project
scripts", "HPC-sync" and "agent workflow"). Those lessons are recorded in
report §6 as candidate prompts with proposed paths. They route as **separate
Brain, assistant and pipeline prompts**, not as phases of this epic:
agree distribution contents before building; reconcile the object funnel
before building; test at about 1% scale and dry-run the merge at full size;
do not scale walltime linearly from a tiny test; cap SSH retries with
backoff; record state durably before a hand-off claims it; never run
producers silently against an empty tree; commit fixes before release; a
subagent never submits on a relayed "continue".

## Rulings (human, 2026-10-28)

Replaces the open questions. Review: `Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/REVIEW.md` §F.
Human's words, verbatim: "F1 your recommendations, F2 ok, F3 yes, 4. yes do the 50 task thing, F5 ok, F6 ok, F7 ok, F8 ok as long as its 500 datasets i dont mind us using dr1 but whatever seems easiest, F9 ok F10 ok F11 ok F12 should be Claude and codex. F4a yes, F4b yes"

- **F1 (Phase 0 home):** owned here, PRs 0a/0b; failure record → hpc-campaign phase 1.
- **F2 (index store and writer):** per-result JSON sidecars as truth + local SQLite cache built by the CLI; the fit writes only `status.json` (+ identity).
- **F7 (PNG render-on-demand):** deferred until after the paper; keep PNGs, STORED.
- **F8 (pilot witness):** DR1 v1.1 retired; read-only census of DR1 v1.0 (v5 tree) on the 500-lens sample + `package verify`; DR1 release keeps its tooling.
- **F10 (`dataset_identity.json` scope):** `object_id` + sha256 of every input at fit start, default on, config off switch.
- **F11:** two concurrent PyAutoFit worktrees allowed, each plan stating review §D.4 file ownership.

## How to start

Issue phase 0 via `/start_dev` as a **single PyAutoFit issue** with two PRs
(0a then 0b); DONE 2026-10-29 — record `complete/2026/10/results-library-p0-integrity.md`. Issue one phase at a time, never
the whole map. Library first in every phase. Workspace and organism repos
follow only after the library PR merges.

## Ledger

- 2026-10-28 — STARTED, concurrent with hpc-campaign (human decision). Final scoping review `Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/REVIEW.md` adopted; human ruled F1–F12 (see Rulings). Amended: Phase 0 owned here and split into PR 0a (artefact integrity) and PR 0b (honest reads), `Shared-with: hpc-campaign`, failure record moved to hpc-campaign phase 1; phase 1 imports `states.py`, reads `status.json`, index = JSON truth + SQLite cache (F2); phase 2 `library.yaml: from_campaign:`; phase 5 witness = 500-lens DR1 v1.0 census + `package verify` (F8). Next: phase 0 via `/start_dev`.
- 2026-10-28 — phase 0 ISSUED: PyAutoFit#1734 (task `results-library-p0-integrity`, branch `feature/results-library-p0-integrity`; PRs 0a then 0b). hpc-campaign phase 1 issued in parallel (PyAutoFit#1735, PyAutoNerves#206), merging after PR 0a.
- 2026-10-29 — phase 0 SHIPPED to PR: PR 0a PyAutoFit#1736 (artefact integrity; suite 3,953 green, smoke 47/47) and PR 0b PyAutoFit#1737 stacked on 0a (honest reads; suite 3,969 green, smoke autofit+autolens_test+euclid 56/56). **#1737 HELD:** the new `AggregateCSV(strict=True)` default breaks `euclid_strong_lens_modeling_pipeline` `tests/test_catalogue_missing_assets.py::test_bundle_reaches_later_stages_with_missing_assets` (351/352): `source_sersic` asks for `galaxies.source.bulge.centre.centre_0` on fits without it → `KeyError`. Options for the human: (a) explicit `strict=False` in the euclid catalogue scripts (works on released and new PyAutoFit; euclid PR merges first), or (b) keep `strict=False` as the library default. hpc-campaign phase 1 (#1738) merges after #1736.
- 2026-10-29 — PHASE 0 COMPLETE (human /prm): PyAutoFit#1736 (0a) and #1737 (0b) MERGED, pending-release. Human ruled option (a) on the strict default: euclid_strong_lens_modeling_pipeline#112 (explicit `strict=False`, 17 calls) merged first; euclid tests 352/352 against 0b. Issue #1734 closed; record `complete/2026/10/results-library-p0-integrity.md`. hpc-campaign phase 1 (#1738) merged after 0a. NEXT: phase 1 (results index; imports `autofit.non_linear.status.states`) via `/start_dev`.
