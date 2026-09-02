# Restore the narrative prose: `start_here.py` as the end-to-end guide, `scripts/` as its chapters

Type: docs
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
- autolens_workspace
Themes:
- euclid
- hygiene
- pixelization
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 30
Unattended: needs-slicing
Epic: euclid-dr1-prep
Phase: 3
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-31
Issued: 2026-08-31

Phase 3 of the Euclid DR1 preparation epic (was 3a — inserted 2026-08-31, renumbered to a
plain 3 on 2026-09-01 in the Cortex split) and **the next phase to
run**. **Gate: phases 1 and 2** (both shipped). Runs before phase 4
(`cpu_vis_lp_jax_vis_pix_numba_submission.md`, was 3b), because phase 4 adds documentation about
submission routes and should be written into a repo whose narrative register has already
been restored.

User request (verbatim):

"""
ok, we have a Euclid epic task on going which has been rebuilding
euclid_strong_lens_modeling_pipeline in advance of large scale DR1 modeling. Can you add a
new phase, which will be the next phase we run, which will put all this prose back into
the exiswting project and restore start_here.py to be the fully documented new user end to
end guide it should be. Note that for things in "scripts" the idea we generally assume the
user has read start_here.py and thus things which repeat whats there should just point to
start_here.py, but things which are not covered there (e.g. Source Pix) are explained
again. Note also that some of the docs from 4 months ago will be old / drifted and thus
this task also needs to compare to autolens_workspasce where appropriate.
"""

## The finding this phase acts on (audited 2026-08-31, read-only)

The repo's in-script narrative — the `__Section__` prose blocks between code that make a
PyAuto script read as a walkthrough — has been substantially lost. Markdown docs
(`README.md`, `scripts/README.md`, `catalogue/README.md`, `dataset/README.md`) are
thorough and current; **this phase does not touch them**. The gap is in the `.py` files.

Prose density at `main` (`361e83b`), measured as `__Section__` header count and share of
lines inside module-level triple-quoted blocks:

| File | Lines | Sections | Inline prose |
|---|---|---|---|
| `workflow/fits_make.py` | 220 | 13 | 53% |
| `workflow/png_make.py` | 272 | 14 | 47% |
| `workflow/csv_make.py` | 342 | 18 | 45% |
| `scripts/initial_lens_model.py` | 382 | 9 | 22% |
| `scripts/full_model.py` | 657 | 10 | 16% |
| `scripts/sersic_lens_model.py` | 185 | 2 | 7% |
| `scripts/mge_lens_only.py` | 313 | **0** | 2% |
| `scripts/lens_model_waveband.py` | 302 | **0** | **0%** |
| `catalogue/scripts/*.py` (6 files) | 863 | **0** | **0%** |
| `preprocess/*.py` (4 files) | 1074 | **0** | **0%** |
| `start_here.py` | 63 | **0** | 0% |

`workflow/*.py` is imported near-verbatim from `autolens_workspace/scripts/guides/results/workflow/`
and is the in-repo reference for the correct register.

### Where it went — and where it did NOT

**The Aug-2026 `Science/euclid` port (phase 1) is not the cause.** `db09e3b` was net
**+147** prose lines and `593318b` (the `catalogue/` tree) net **+368**. What the port did
do is dilute — it added ~82 lines of code to `initial_lens_model.py` with zero new prose,
landed `catalogue/scripts/` at zero sections by design (its own commit message: "the
unrelated 'Results: Fits/Png Make' boilerplate docstrings are gone, replaced by ones
stating what each producer emits"), and reduced `start_here.py` to a shim.

**The loss event is `355b309` (2026-04-02), "Visualization cleanup, remove old datasets and
legacy pipelines": −812 prose lines net**, the largest in the repo's history. It deleted
the `pipelines/` tree:

| Deleted at `355b309` | Sections | Successor at HEAD |
|---|---|---|
| `pipelines/full_model.py` | 23 | `scripts/full_model.py` — 10 |
| `pipelines/lens_model_waveband.py` | 17 | `scripts/lens_model_waveband.py` — **0** |
| `pipelines/mge_lens_only.py` | 16 | `scripts/mge_lens_only.py` — **0** |
| `pipelines/sersic_lens_model.py` | 14 | `scripts/sersic_lens_model.py` — 2 |

Earlier, `fc43be0` (2025-11-05) deleted `pipelines/groups.py` (17 sections) and
`pipelines/point_source.py` (14 sections) with **no successor anywhere** — while
`README.md` today says point-source and group pipelines "will be added to this repository
in future releases". They were in it, documented, and were removed.

**The pattern to reverse:** rationale short enough for one sentence was compressed into
module docstrings and survived (e.g. "The Sersic profile diverges at the galaxy centre, so
this pipeline uses a higher-order over-sampling scheme"); rationale that needed a
paragraph was deleted. The result reads as reference documentation, not a guide — the
*what* is present throughout, the *why* is largely gone.

Recovery source: `git show 355b309~1:pipelines/<file>.py` and
`git show fc43be0~1:pipelines/<file>.py`.

## The doctrine this phase establishes (user direction, do not re-derive)

1. **`start_here.py` is the fully documented, end-to-end new-user guide.** It is currently
   a 63-line shim (`db09e3b`) over `scripts/initial_lens_model.fit`. That was an approved
   phase-1 decision made to kill code drift — **the code-drift fix must be preserved, the
   documentation decision is being reversed here.** `start_here.py` must become the
   narrative entry point a new user reads front to back. Its lineage peaked at 21 sections
   / 295 prose lines (`25437a5`, 2025-03-18); that is the register to aim at, not the line
   count.
2. **`scripts/*.py` assume the reader has read `start_here.py`.** Anything `start_here.py`
   already explains is **not** repeated — point back to it by name. Anything
   `start_here.py` does not cover **is** explained in full, in place. The named example is
   **Source Pix**: `scripts/initial_lens_model.py:239` carries an *empty* `__Source Pix__`
   header, and the 147 lines below it — the entire pixelized-source stage, the
   conceptually hardest part of the pipeline — carry no prose at all.
3. **The recovered prose is 4+ months stale. Verify every claim before restoring it**, and
   compare against `autolens_workspace` where the concept is a library concept rather than
   a Euclid one. Restoring text that is now wrong is worse than leaving the gap.

## Known drift in the recoverable prose (verified 2026-08-31 — non-exhaustive)

Every cross-reference in the deleted prose is stale:

- `github.com/Jammy2211/...` → the org is **`PyAutoLabs`** (both the pipeline repo and
  `autolens_workspace` links).
- `features/multi_gaussian_expansion.ipynb`, `features/pixelization`,
  `features/pixelization/adaptive`, `linear_light_profiles.py` — all **GONE** from those
  paths. They now live under `autolens_workspace/scripts/imaging/features/…` (and
  parallel `interferometer/`, `group/`, `multi_galaxy/` trees). Pick the `imaging/` one.
- `guides/modeling/chaining` → `autolens_workspace/scripts/guides/modeling/chaining.py`
  (exists; the `.ipynb` reference does not resolve from this repo).
- `import slam_pipeline` / `from start_here import fit` — the `slam_pipeline/` tree was
  deleted at `3e6be0b` and no longer exists.
- `mask_radius: float = 3.0` as a function/CLI argument — **removed**. `README.md` is
  explicit: "`mask_radius` is **not** an argument — it is always read from the dataset's
  `info.json`." Any restored prose describing it as a knob is wrong.
- `__JAX & Preloads__` describes `al.Preloads` / `source_pixel_zeroed_indices` against a
  **Rectangular** mesh. Phase 1 moved both pixelized stages to **Delaunay +
  `reg.AdaptSplit`**; `Preloads` and `source_pixel_zeroed` now return zero grep hits in
  the repo. This section must be **rewritten against the Delaunay path**, not restored.
  See `autolens_workspace/scripts/imaging/features/pixelization/delaunay.py` — the epic's
  agreed Delaunay referent (user decision 2026-08-28) — and note the repo deliberately
  uses `Hilbert(pixels=500)` where that script uses 1000, because Euclid VIS cut-outs are
  small.
- `conf.instance["visualize"]…` direct indexing vs the current
  `from autolens import conf` + `conf.instance.push(...)` surface (changed at `8e5a0fd`).

## Scope

### In scope

- **`start_here.py`** — restore to a full end-to-end narrative guide while keeping it a
  thin functional shim over `scripts.initial_lens_model.fit` (no re-forked implementation;
  that drift is what `db09e3b` fixed). Installation, what the pipeline does, what a
  dataset must contain, how to read `output/`, where to go next (`scripts/`, `workflow/`,
  `catalogue/`), and the SLaM concepts a new user needs. This is the file that carries the
  concepts; everything else defers to it.
- **`scripts/initial_lens_model.py`** — fill the empty `__Source Pix__` block and document
  the 147-line pixelized stage (Delaunay mesh, Hilbert image mesh, `AdaptImages`, the
  circle-edge points, `AdaptSplit` and why `reg.Adapt` cannot JIT on the Delaunay family).
  Trim anything that now duplicates `start_here.py` down to a pointer.
- **`scripts/lens_model_waveband.py`** (0 sections / 302 lines) and
  **`scripts/mge_lens_only.py`** (0 sections / 313 lines) — the two worst gaps among
  user-facing fitting pipelines. Predecessors at `355b309~1` had 17 and 16 sections.
  Recover, verify, de-duplicate against `start_here.py`.
- **`scripts/sersic_lens_model.py`** (2 sections) and **`scripts/full_model.py`** (10) —
  restore the *why*. `full_model.py`'s 115-line SLaM introduction (`__Black Box
  Description__`, `__Preqrequisites__`, `__Overview__`, `__Pipeline Structure__`,
  `__Design Choices__`, `__This Script__`) is the single largest recoverable block; the
  `__Design Choices__` reasoning (Source First → Image Positions → Adapt Images → Lens
  Light Before Mass → Mass Model Last) is still substantively correct and is exactly the
  "why is it ordered like this" a new user needs. Cross-check against
  `autolens_workspace/scripts/guides/modeling/slam_start_here.py` before restoring —
  note that script uses `RectangularBilinearAdaptImage`, not Delaunay (epic ground-truth
  surprise #3), so do not import its mesh claims wholesale.
- **`catalogue/scripts/*.py`** (6 producers, 0 sections) — lift toward the register of
  `workflow/example/csv/lens_mass.py`, which produces the *same* `lens_mass.csv` in 201
  lines with 9 sections. Also **cross-link the two trees**: `catalogue/README.md` never
  mentions `workflow/`, `workflow/README.md` never mentions its own `example/` folder, and
  `workflow/csv_make.py:24` points at "`workflow/examples`" — a path that does not exist
  (the folder is `workflow/example`, singular). Fix that ref.
- **Empty section headers** — `scripts/initial_lens_model.py:239` `__Source Pix__`, and
  `scripts/simulator.py` `__Tracer__` (795), `__Write The Dataset__` (1021),
  `__Positions__` (1058). Also `simulator.py` lines ~200–795 (~595 lines) with no sections
  at all.

### Explicitly out of scope

- **All `*.md` files.** The READMEs are current and good; do not rewrite them. The one
  exception is the `workflow/examples` → `workflow/example` ref fix above and any
  cross-link additions named in scope.
- **`preprocess/*.py`** (4 files, 0 sections). Verified: these **never** had narrative —
  0 sections at every commit since they appeared at `1bd6c7d`. That is a pre-existing gap,
  not a regression, and it is not on the DR1 critical path. Leave it; file a follow-up
  prompt if the reviewer wants it.
- **Resurrecting `groups.py` / `point_source.py`.** Their prose is good and recoverable
  (`fc43be0~1`) but restoring them means restoring *pipelines*, which is a feature phase,
  not a docs one. If the reviewer wants them back, that is a separate prompt. **Do**
  check whether `README.md`'s "will be added in future releases" line should be softened
  given they were previously present and removed.
- **Any behaviour change.** This phase adds and edits prose only. The one permitted code
  touch is the `workflow/examples` string fix. If a restored explanation turns out to
  describe behaviour the code no longer has, the prose is corrected to match the code —
  **not** the other way round; file a separate bug prompt if the code looks wrong.

## Acceptance

- `start_here.py` reads end to end as a new-user guide and still delegates execution to
  `scripts.initial_lens_model.fit` with no duplicated fitting logic.
- No `__Section__` header anywhere in the repo is empty.
- `scripts/lens_model_waveband.py` and `scripts/mge_lens_only.py` are no longer at zero.
- Every restored cross-reference resolves: no `Jammy2211` org links, no
  `features/<x>` paths, no `slam_pipeline`, no `mask_radius`-as-argument claims, no
  `Preloads` / Rectangular-mesh description of the Delaunay stage.
- `python -m pytest -q -m "not slow"` and `python3 .github/scripts/run_smoke.py` still
  pass (`tests/test_repo_invariants.py` will fail on any new `.py` not registered in
  `smoke_tests.txt` / `config/build/no_run.yaml` — this phase should add no new scripts).
- A reviewer who has read only `start_here.py` can open any script in `scripts/` and not
  hit an unexplained concept that is neither in `start_here.py` nor explained in place.

## Notes for whoever runs this

- **Prose authorship is Opus-tier work** ([[tutorial-prose-opus]] / `WORKFLOW.md`) — do
  not delegate the writing to Sonnet. Recovery of the old text, drift-grepping and the
  mechanical de-duplication sweep are fine to delegate.
- Read the recovered prose *before* deciding what to keep. Roughly: the SLaM design
  reasoning and the dataset/waveband explanations are still true; anything naming a mesh,
  a preload, a config-access idiom, a workspace path or a CLI argument is suspect.
- The repo has no `notebooks/` tree — this prose is read in the `.py` files themselves,
  so it must read well as source, not only as generated markdown cells.

## Addendum — 2026-08-31 batch review (euclid member, decision: structure-ok)

The human's review of the phase-2 retrospective (packet
`batches/packets/2026-08-31-am.html`) adds the following structural/docs items to
this phase, verbatim:

"""
The ### Simulating a lens section is too long in README.md and should be moved below
CLI arguments. Make this literally one paragraph pointing to the python file,
describing it and thats it, but do give the CLI prompt too.

We dont need ### The `WORST_BAND` / `WORST_PSF_*` header contract in README.md, I
think all docs should just be in the python scripts so I guess this can be fully
covered in util.py which I think it already is.

Move ## Documentation above the "Fitting Pipelines" section.

I want scripts which run lens models to be separate to stuff like
"diagnose_latent.py", "build_inspect.py" and "diagnose_latent_vis_pix.py". Can you
move these to a scripts/tools folder.

I don't think we should have a start_here.py, seems pointless.

AGENTS.md is way too long and can be significantly shortened lots of stuff feels too
much info (CI, how to run scripts) also look for clearer mirroring with other
workspace repos where possible.
"""

Two scope amendments this implies:

- **README.md is no longer fully out of scope**: the three structural edits above
  (Simulating-a-lens trim+move, WORST_* contract section removal, ## Documentation
  reorder) are in scope. The rest of the READMEs stay untouched.
- **`scripts/tools/` move**: `diagnose_latent.py`, `build_inspect.py`,
  `diagnose_latent_vis_pix.py` move out of the model-running script tree
  (update `smoke_tests.txt` / `config/build/no_run.yaml` registrations and the
  bundle `.sh` accordingly — `tests/test_repo_invariants.py` enforces the lists).

**RESOLVED — human ruled 2026-08-31 (batch close-out):** **keep `start_here.py`**
and update it with the docs — it becomes the fully documented new-user end-to-end
guide this phase describes. The batch review's "seems pointless" remark applied to
the current 63-line shim, not to the documented guide this phase turns it into;
the delete option is closed. Do not re-present this choice at plan time.
