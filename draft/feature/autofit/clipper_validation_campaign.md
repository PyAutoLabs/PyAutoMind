# Clipper: demonstrate and validate on the profiling search cells

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## What this is

The **validation phase** of the prior-support fix. It produces the evidence that
justifies flipping the default.

> **UNBLOCKED 2026-08-16 — phase 1 has landed.** PyAutoFit#1477 merged as
> `1f4b66a` (tip of `main`), shipping `AbstractClipper` / `ClipperNone` /
> `ClipperPriorBox` in `autofit/non_linear/clipper.py`, wired into both
> `AbstractMultiStartGradient` and `AbstractBFGS`, opt-in, default `ClipperNone`,
> bit-identical under it. Record:
> `complete/2026/08/prior-support-clipper.md`. This task is ready to start.
>
> Three things phase 1 changed for this campaign:
> - **`n_clipped_lane_steps` already exists** — accumulated per-lane at
>   `multi_start_gradient/search.py:863` and written to `search_internal`. Record
>   it as a fourth counter alongside the three below.
> - **The momentum-reset arm is buildable but not built.** `project` returns the
>   clipped mask, which is what a caller needs to zero optimiser momentum, but
>   nothing in PyAutoFit uses it yet. Arm 3 below therefore requires writing that
>   reset in the campaign, not just flipping a flag.
> - The float32 `save_json` crash was not fixed by phase 1 — but has since been
>   fixed, see the handover below.

## SESSION HANDOVER — 2026-08-16, cloud → GPU box

A cloud CPU session did everything this campaign needs except run it. **Three
more PyAutoFit changes landed on `main` after phase 1**, all of them clearing
traps this prompt used to have to work around:

| PR | merge | what it changes for you |
|---|---|---|
| #1477 | `1f4b66a` | phase 1 — the `Clipper` itself |
| #1478 | `bbceff6` | `n_clipped_lane_steps` + `n_constrained_lane_steps` now reported in **`search.summary`** |
| #1479 | `b6e89cd` | `NumpyEncoder` — **the float32 `save_json` crash is fixed** |
| #1480 | *see status* | atomic writes + corrupt-resume recovery — **the poisoned-rerun trap is fixed** |

**All four are UNRELEASED.** They are on `main` and not on PyPI. So this task
**must** run against a PyAutoFit checkout at or after `b6e89cd`, and
`autofit.__file__` must be verified to resolve to that checkout before any
number is trusted. A released wheel has none of this.

**What this means for the traps below.** Two of them are now belt-and-braces
rather than live hazards — but do **not** delete the mitigations:

- The float32 crash cannot fire at `save_json` any more. Still assert the
  recorded step count equals `n_steps` before believing a counter; that
  assertion catches every no-op cause, not just this one.
- A crashed run no longer wedges the next run of the same name. Deleting
  `output/<name>/` between arms is still the cheaper habit than reasoning about
  whether a resume was clean.

### ⚠ THE ARM-COLLISION TRAP — read before running anything

**The clipper does NOT enter the search identifier.** Verified empirically
against PyAutoFit `main` on 2026-08-16:

```
af.MultiStartAdam(name="x")                             -> 2bada4747f74bc46bf812605a762def9
af.MultiStartAdam(name="x", clipper=ClipperNone())      -> 2bada4747f74bc46bf812605a762def9
af.MultiStartAdam(name="x", clipper=ClipperPriorBox())  -> 2bada4747f74bc46bf812605a762def9
```

All three resolve to the **same output directory**. Arms 1 and 2 of this
campaign differ in *nothing else*, so they collide. Stacked with the
`.completed` short-circuit (`is_complete` → `result_via_completed_fit`, which
skips the search entirely), **arm 2 can silently return arm 1's numbers and
look like a clean run** — invalidating the campaign's central comparison while
producing output that looks perfect.

Mitigation — do all three:

1. **Give every arm a unique `name`** (`mge_clip_none_seed0`,
   `mge_clip_priorbox_seed0`, …). Do not rely on the clipper to separate them,
   because it does not.
2. **Delete `output/<name>/` between arms** anyway.
3. **Assert the recorded step count equals `n_steps`** before believing any
   counter. A short-circuited run reports the *previous* run's numbers rather
   than zeros, so a zero-check alone does not catch this.

Not a bug in itself — it is what keeps existing runs' directories stable — but
it is precisely wrong for this campaign. Whether the clipper *should* enter the
identifier is now filed as
`draft/feature/autofit/clipper_in_search_identifier.md`, and phase 3's
re-baseline is the reason it matters.

### Harness traps that already cost a session

From the phase-1 session, which paid for every one of these
(`complete/2026/08/prior-support-clipper.md`):

- **The `.completed` marker short-circuits `fit()`** — a resumed or re-run
  search returns the cached result *without entering `_fit`*. Three successive
  versions of a resume test "passed" while testing nothing. This is the second
  half of the collision above.
- **`fit()` rebuilds `search.paths`**, so an instance-level monkeypatch on
  `paths.save_search_internal` is silently discarded. **Patch at CLASS level.**
- **The `search_internal` folder is deleted on successful completion**, so it
  cannot be read back after the fit. Capture it *as it is written*.
- **Two identically-constructed searches did not resolve to the same identifier
  dir**, so an intended "resume" silently started fresh. The reliable method is
  patching `DirectoryPaths.load_search_internal` at class level.
- **Seed `random` AND `numpy` before every fit** — the initializer draws from
  both, and an unseeded comparison reports a spurious bit-identity mismatch.
  This produced one false alarm on phase 1's bit-identity gate.
- **A box containing the optimum never exercises the clipper.** Phase 1's first
  efficacy attempt measured 0 clips for exactly this reason. Put the truth
  outside the box.

### Arm 3 does not exist yet — do not silently drop it

Phase 1 ships the clipped **mask** from `project`, which is what a momentum
reset needs, but **no reset is implemented** and the search does not touch
`opt_state` on a clip. So arm 3 either gets a small addition written first, or
this campaign runs arms 1–2 and reports the pinned-lane count as the input to
that decision. The prototype's 5/16 pinned lanes are why the arm exists.

### Two phase-1 measurements to carry in as priors

Both CPU/float32 on a toy Gaussian, so directional only:

- With the truth deliberately **outside** the prior box, lane deaths went
  **249 → 0** with 252 clips, and the clipped run pinned `centre` at the upper
  bound. That is "pinning is a result, not a failure" reproducing in miniature,
  and an independent confirmation of the momentum-pinning mechanism.
- **The negative control this prompt asks for already passes at unit level** — a
  `GaussianPrior` coordinate is provably untouched by `ClipperPriorBox`, with a
  regression test guarding it. The cell-level control is still worth running,
  but a failure there would point at the cell, not at bounds extraction.

Also relevant when reading source: the `AbstractMultiStartGradient` class
docstring used to claim the rule steps on the unit-cube parameterization. It
never did — `_broad_starts` maps draws to physical parameters. Corrected in
phase 1, but older checkouts still carry the false sentence.

**The clip count is a validity check, not just a statistic.** Read
`Clipped Lane-Steps` straight out of `search.summary`. **A `ClipperPriorBox`
arm showing no clipping lines at all has not exercised the clipper** — which is
also the signature of the collision above, since arm 1's summary carries no
`Clipper` line. Treat it as a broken arm, not a null result.

**One free finding to reuse.** The #128 mechanism reproduces on a *toy
3-parameter Gaussian* (`autofit.example.Gaussian`, `centre` truth 30 outside a
`UniformPrior(5, 20)`, 4 starts × 200 steps, `learning_rate=1.0`): unclipped
gave `Value-NaN Lane-Steps = 378` (94.5%) and clipped gave `0`, with
`Clipped Lane-Steps = 414` at rate 0.958. That is a seconds-long smoke test for
"is the clipper wired up and firing at all" before spending GPU time on the
`imaging/mge` cell.

**Still owed alongside this**, from `active.md` `mge-lane-death`: the
GPU/float64/multi-seed confirmation of the original result, and the
hazard-index entry for the prior-exit failure mode. Both want the same GPU
session as this campaign, and the confirmation shares its arms.

**Sequencing:** run this campaign first. Then
`draft/research/autolens_profiling/ell_comps_trapping_unmasked.md`, which can
share these arms — it needs `n_constrained_lane_steps` from the *clipped* run,
and explicitly must not re-derive the 27.79% from the prior-neutered diagnostic
arm.

Three phases, three PRs, in this order — do not merge them out of order:

| phase | repo | what |
|---|---|---|
| 1 | `@PyAutoFit` | ✅ **SHIPPED** — `Clipper` class, opt-in, bit-identical by default (PyAutoFit#1477 → `1f4b66a`; `complete/2026/08/prior-support-clipper.md`) |
| **2** | **`@autolens_profiling`** | **this task — demonstrate and validate across the search cells** |
| 3 | `@PyAutoFit` | flip the default to `ClipperPriorBox`, carrying the phase-2 re-baseline |

Phase 2 is where the claim "clipping recovers the lost lanes without changing the
answer" either survives or does not. Phase 3 must not be written until phase 2
has run.

Background and the full root-cause investigation: **autolens_profiling#128**.
One-line version: the objective is `-2 * (log_likelihood + sum(log_prior))`, a
`UniformPrior` is `-inf` outside its box, the search steps in physical space with
nothing holding it there, and a lane that oversteps by ~3% of a box width is
marked dead and never redrawn — while continuing to step and consume full
likelihood-and-gradient cost with its output discarded.

## The truth bar already exists — use it

`results/searches/nautilus/imaging/mge/hst/hpc_a100_fp64.json` is a Nautilus run
on **the same cell, the same 15-parameter model**:

```
max_log_likelihood = 31786.782462488976
log_evidence       = 31690.47079355404
posterior_samples  = 63800          (A100, fp64, n_live 200)
```

Nautilus samples in **unit-cube coordinates**, so it is structurally immune to
this bug. That makes it the reference answer, not merely another data point.

**This is the load-bearing validation.** "Fewer lanes die" is a weak claim on its
own — a change that keeps lanes alive by making them useless would satisfy it.
The claim worth testing is: **does clipped MultiStartProdigy get closer to the
Nautilus maximum log-likelihood than unclipped does?** If lane deaths fall and
best-fit logL does *not* improve toward 31786.8, clipping is cosmetic and phase 3
should not happen.

## Arms

Per cell, at minimum:

1. `clipper=None` / `ClipperNone` — control, must reproduce today's numbers.
2. `ClipperPriorBox` — the candidate.
3. `ClipperPriorBox` **+ momentum reset** on clipped coordinates, if phase 1
   shipped it. The prototype left 5/16 lanes *pinned* to a bound with Prodigy's
   state still pushing outward; this arm is what says whether that matters.

Record for every arm: `n_value_nan_lane_steps`, `n_grad_nan_lane_steps`,
`n_constrained_lane_steps`, **`n_clipped_lane_steps`**, `n_resurrections`,
**`alive N/n_starts` per step**, best-fit log-likelihood, wall time, and the
count of lanes ending pinned to a bound.

`n_clipped_lane_steps` ships with phase 1 and is counted **per-lane, not
per-coordinate** — a lane clipped in three parameters on one step is one clipped
lane-step, matching how the other counters read. Read it from `search_internal`;
it is **not** in `search.summary` yet
(SHIPPED — `complete/2026/08/clipper-usage-in-search-summary.md`, so read it straight
from `search.summary`). It is also the
sanity check on the whole arm: a `ClipperPriorBox` arm reporting **zero** clips
has not exercised the clipper at all, and its "no change" result means nothing.

**At least two seeds per arm.** Single-seed CPU numbers are what this whole
investigation had to go back and re-derive.

## Cells

Start with the characterised one, then widen:

- **`imaging/mge` (hst)** — the reference. ~250s at 16x150 on cloud CPU, so it
  iterates fast. Known baseline: 1446/2400 value-NaN (60.25%), `alive 16/16 ->
  2/16`, 14 lanes dead at steps `[34,36,36,37,38,39,39,40,40,41,41,52,56,125]`.
  Prototype clipping gave 425 (17.71%), 5 dead, `alive -> 11`.
- **The pixelized mesh cells** (`delaunay`, `pixelization`, DelaunayNN) — **GPU
  required**. These are the cells `resurrect=True` was introduced for, so they are
  the strongest test of whether clipping changes the resurrection story. Two prior
  attempts timed out on CPU with zero steps emitted; that is **JIT compile, not
  memory** (`batch_size=1` clears the OOM). Do not shrink the source mesh to make
  them cheaper — the image-plane grid at `mask_radius 3.5` dominates, not the mesh.
- **`point_source`** cells — different model family and different prior structure;
  confirms the fix is not MGE-shaped.
- **A negative control**: a model whose priors are all unbounded (`GaussianPrior`).
  `ClipperPriorBox` must be a *no-op* there. If it changes anything, the bounds
  extraction is wrong.

## What would falsify the fix

Write these down before running, and report them honestly if they happen:

- Lane deaths fall but best-fit logL does **not** move toward the Nautilus
  reference → clipping keeps lanes alive without making them useful.
- Most surviving lanes end pinned to a bound → the wall is absorbing the
  population; momentum reset is mandatory, or projection is the wrong strategy.
- Wall time per step rises materially → a clip on `(n_starts, ndim)` should be
  unmeasurable; if it is not, something is wrong with where it was inserted.
- The pixelized cells get *worse* → clipping and `resurrect=True` interact badly,
  and phase 3 must be scoped per-search rather than globally.

## Pinning is a result, not a failure

Where the likelihood genuinely prefers a value outside the prior, a clipped lane
sitting on the bound is the **correct MAP answer under the declared prior**. In
the reference cell the shear escapes were mixed-sign (`+0.353`, `-0.341`,
`+0.301`, `-0.312`), which reads more like a poorly-constrained parameter
diffusing out than a true value sitting outside — but that is a hypothesis, not a
finding. If clipped runs pin `gamma` at `±0.3` reproducibly, that is evidence the
shear prior is fighting the data and belongs in the write-up as a science finding,
not swept up as a clipping artefact.

## Deliverables

- Results JSONs under `results/searches/` alongside the existing NaN-accounting
  artefacts, following the conventions already there.
- A note under `results/notes/` — the comparison table, the Nautilus-reference
  verdict, and an explicit recommendation for or against phase 3.
- The hazard-index entry for the prior-exit failure mode (owed from #128).

## Environment

- **Python 3.12+** (autonerves). `pip install jaxnnls` is **required** for the JAX
  NNLS solver path and is not pulled in by default. `optax` likewise.
- Install `autolens` with **`--no-deps`** when running editable local
  `autofit`/`autogalaxy`, or the released wheels clobber them. Phase 1 is
  unreleased, so this task **must** run against `@PyAutoFit` `main` (or the phase-1
  branch), not a PyPI wheel — verify `autofit.__file__` resolves to the checkout
  before trusting any number.
- `build_for_cell` **writes into `dataset/`** (rewrites the HST FITS, adds
  `positions.json`, emits `results/simulators/*`). Not read-only.
- Cell scripts honour `SEARCHES_N_STARTS` / `SEARCHES_N_STEPS` /
  `SEARCHES_BATCH_SIZE` / `SEARCHES_DISABLE_VIZ`.
- On A100 set `jax_enable_x64` **explicitly** — it is not inherited under `sbatch`,
  and float32 would understate the quantity under test. All #128 numbers are
  float32 CPU; expect them to move on fp64 and do not treat a difference as a
  regression without checking precision first.

## Traps, all paid for already

- **Grade on the alive-versus-step curve, not the percentage.** `n_value_nan_lane_steps`
  is a *survival integral*: a dead lane keeps counting every subsequent step, so
  the same death curve reports 60% at 150 steps and ~75% at 300. Verified exactly:
  `sum(150 - k_i) = 14*150 - 654 = 1446` = the counter, to the unit. Two arms at
  different budgets cannot be compared on the scalar.
- **A crashed run poisons the next run of the same `name`.** A half-written output
  JSON makes the next search try to *resume* and fail — a 4-second no-op that reads
  as a clean result (zero deaths, because zero steps). Delete `output/<name>/`
  between arms, or use unique names, and **assert the recorded step count equals
  `n_steps`** before believing any counter.
- **`float32` breaks `save_json`.** `autofit/non_linear/paths/directory.py:80`
  raises `TypeError: Object of type float32 is not JSON serializable` at the end of
  a *successful* run. It does not fire when most lanes are dead, so it will start
  firing exactly when the fix works. If phase 1 has not fixed it, capture counters
  independently of the result object.
- **`0` and `null` are different findings.** Read counters with `.get()` and a
  `null` means the search never wrote the key — broken plumbing, not a clean cell.

## Deliberately out of scope

- Flipping any default (phase 3).
- NUTS. It targets the log posterior from a physical start and *diverges* rather
  than dying — a different mechanism needing its own investigation.
- Unit-cube stepping. Rejected for now, with reasons, in
  `complete/2026/08/prior-support-clipper.md` (under `## Original prompt`).
