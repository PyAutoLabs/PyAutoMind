# Remaining code consumers move to the flat `fields=` form: profiling, inference, JOSS benchmarks, Reduce prototypes

**2026-09-19 update:** This four-repo survey is now historical context. PyAutoReduce#77 and the independent autolens_inference simulator PR #8 merged; the inference SLaM runner has its own draft. The user confirmed the deleted local `autolens_jax_joss` checkout is outside this sweep. The 47 live non-chaining profiling calls shipped in `complete/2026/09/mass-field-profiling-live.md`; `mass_field_pipeline_resume.md` retains the 5 staged calls, and 5 inline witnesses remain historical. Do not issue this broad prompt as a single task.

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
- autolens_inference
- autolens_jax_joss
- PyAutoReduce
Themes:
- cluster
- profiling
- hygiene
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Consequence: glance
Witness: an AST re-walk (never a grep — memory `ASTwitness`) over each repo's live script set reports zero `af.Model(al.Galaxy, ..., shear=...)` and zero `al.Galaxy(..., shear=...)` model builders outside the named exclusions, and every migrated builder composes `fields=field` with `field = af.Model(al.MassField, redshift=..., shear=af.Model(al.mp.ExternalShear))`; one runnable script per repo executes end to end; `autolens_profiling` lint (`build_readme.py --check`) passes with regenerated dashboards.
Review-minutes: 10
Unattended: needs-slicing
Epic: mass-field
Superseded-by: `complete/2026/09/mass-field-profiling-live.md` and `draft/maintenance/autolens_profiling/mass_field_pipeline_resume.md`; helper merged in PyAutoGalaxy#625 / PyAutoLens#745, publication pending
Filed: 2026-09-18

## The trap, stated first

These four repos returned **zero `fields=` hits**. That is **not** because they are
clean — it is because they were **never migrated**. They sit at the **pre-epic,
galaxy-attached** form: `af.Model(al.Galaxy, ..., shear=af.Model(al.mp.ExternalShear))`.
Reporting "0 hits, nothing to do" would be exactly wrong, and is the reading this
prompt exists to prevent. Zero-hit ≠ done.

Target idiom (the flat form shipped by epic phase 6):

```python
field = af.Model(al.MassField, redshift=<lens z>, shear=af.Model(al.mp.ExternalShear))
model = af.Collection(galaxies=af.Collection(lens=lens, source=source), fields=field)
# prior paths read fields.shear.gamma_1, not fields.field.shear.gamma_1
```

## Dependency on the chaining helper

`al.util.chaining.mass_from` / `chaining_util.mass_from` takes **no `fields`
argument**, so a chained stage that carries galaxies forward and omits `fields=`
**silently drops the external field** — no error, no log line. That is why this prompt
is `Blocked-by` the helper prompt. Do not migrate any staged pipeline here by hand
before the helper lands; a text replace across a chained file is the documented way to
produce a wrong model that still runs.

## Per repo

### `autolens_profiling` — 52 live runnable model builders under `scripts/`

- **No archive directory exists** in this repo. Experiment snapshots are *inline*,
  which means the usual "everything outside `archive/` is live" rule does not apply.
  **EXCLUDE from any rewrite** — these are recorded measurements, not live code:
  - `fixed_light_numba_s4_witness.py`
  - `*_levers_l{2,3}_witness.py`
  - `fixed_light_draws.py`
  - `fixed_light_trace.py`
  - `results/hazards/component/profile_registry_coverage.json` (generated tripwire)
- **READMEs are generated.** Lint runs `build_readme.py --check` (memory `READMEgen`),
  so anything that touches `results/` rows needs the regenerated dashboards in the same
  PR.
- **Claim conflict:** the repo is currently claimed by `hst-gpu-residue-p2` and
  `fixed-light-numba-s4b`. A parallel-claim waiver plus a fresh worktree is needed, and
  the waiver recorded on `active.md` the way the euclid/sersic rows do it.

### `autolens_inference` — 3 live files, one of them the risk

- `scripts/misc/simulators/imaging.py`, `scripts/misc/simulators/interferometer.py` —
  live simulators with galaxy-attached `ExternalShear` instances.
- `scripts/misc/slam/_runner.py` — **a LIVE staged SLaM pipeline**, chaining
  `Isothermal + ExternalShear` into `PowerLaw` via
  `al.util.chaining.mass_from(..., unfix_mass_centre=True)` (module docstring lines
  15-20, builder at lines 713-742). **This file is precisely why the helper prompt
  blocks this one.** Migrate it last, with a per-stage witness that the field survives
  into every stage's model.

### `autolens_jax_joss` — 7 benchmark files

`benchmarks/{group,imaging,imaging_and_interferometer,imaging_and_point_source,
interferometer,multi_band,point_source}.py`. All galaxy-attached, all live runnable
benchmarks, no open PRs. Note this repo is **absent from `repos.yaml`** — see
`draft/maintenance/pyautomind/autolens_jax_joss_manifest_gap.md`; adding it there is
independent of this migration but should land first so the repo is visible to the next
manifest-driven sweep.

**Update 2026-09-18 (PyAutoBrain#389):** this repo's **local checkout was removed** as
dead weight. The 7 benchmark files still exist on GitHub at `6bce65e` and still need
the flat-`fields=` migration, but they are **no longer locally sweepable** — this
member now requires a fresh clone, so sequence it accordingly (or drop it from the
local sweep and raise it as a PR against the remote). The remote is deliberately
retained: it is the citable artefact behind the JOSS paper's benchmark claims.

### `PyAutoReduce/prototypes` — 2 files

Smallest of the four; prototypes, no chaining.

## Sequencing

Four repos, so `Unattended: needs-slicing` — this is a slice-per-repo task, not one
sitting. Suggested order: `PyAutoReduce` (2 files) → `autolens_jax_joss` (7) →
`autolens_profiling` (52, needs the claim waiver and the README regeneration) →
`autolens_inference` (3, the SLaM runner last, after the helper). Each repo is its own
PR; the `mass-field` epic table should gain a row once the human rules on scope.

Filed 2026-09-18 from the flat-`fields=` adoption sweep's follow-up audit
(issue autolens_workspace#561).
