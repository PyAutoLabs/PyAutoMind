# Give the Profiling Agent a compile-time axis — the arc

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: planned (arc — execute via the three child prompts below)
Filed: 2026-07-14 (backfilled from git)

> **RE-SCOPED 2026-08-10.** This prompt was filed 2026-07-14 asking the Profiling
> Agent to *measure JAX compile/eval time of the release-validation heavy scripts
> so we can speed them up*. Both halves of that framing are now spent: the
> speed-up shipped, and the release-script half belongs to a different conductor.
> What survives — and is still unbuilt — is **regression surveillance**. The
> original text is preserved under § What the prompt originally said.

## Why the original framing no longer holds

**The speed-up already shipped.** The `#71 → #74 → #77` arc
(`autolens_profiling/scripts/misc/jax_compile/README.md`) settled the question
this prompt opened, with controlled A/Bs:

| lever | effect | status |
|---|---|---|
| persistent compilation cache | 117.0 s → **2.3 s** (CPU MGE `vag`, 51×); 5517.8 s → **937.1 s** (A100 pixelized Nautilus end-to-end) | shipped |
| `--xla_gpu_autotune_level=0` | FD probe 498 s → **29 s** (17×); full 300×16 Adam fit −40 %; likelihoods bit-identical | shipped |
| source jit-boundaries | ruled out by evidence — "**Do not restructure**" | closed |

The prompt's own candidate root causes are likewise resolved: `lax.map` is
innocent (every batched-gradient structure compiles in the same ~105–125 s band),
the >30-min repeated-fusion observations were host-load contention plus a
re-firing alarm banner, and the tracing floor is 58 % jax-internal with no PyAuto
lever.

**So the durable risk is no longer slowness — it is silent regression.** Both wins
are *settings*. A config drift, a `jax` version bump, or a wrapper that clobbers
`XLA_FLAGS` (exactly what PyAutoNerves#127 fixed, and what invalidated the
2026-07-15 "autotuning ruled out" A/B for two months) puts the 70-minute
worst case straight back without anything failing. Nothing watches for that today.

This is precisely the handoff the research left open — `jax_compile/README.md`
Verdict item 4: *"should track **warm** compile times per cell so cache
regressions are caught"*, and `probe.py`'s own docstring: *"industrializes this
across the full cell grid once the research settles the method."* The method has
settled.

## Why the release-validation-scripts leg is dropped

The original prompt asked profiling to cover the release-validation heavy scripts
(`jax_grad/imaging_pixelization.py` et al. blowing the 300 s cap). That crosses a
boundary both conductors already document:

- `agents/conductors/profiling/AGENTS.md` — profiling owns "the product's
  modelling / compute speed (likelihood on the science grid, GPU tiers, A100)".
- `agents/conductors/hygiene/AGENTS.md` — hygiene owns "the *developer loop's*
  cost (unit tests, `PYAUTO_TEST_MODE` / `PYAUTO_SMALL_DATASETS` integration
  scripts, import time)", and "Hunting generally-slow functions flagged by
  integration tests is hygiene's `perf` mode (**moved here from profiling's staged
  future modes**)".

Script-suite cost was deliberately moved *out* of this agent once already. Pulling
it back in would re-open a settled boundary to serve a motivation (the 300 s cap)
that PyAutoHeart#72 has since handled. Decision 2026-08-10: **out of scope here**;
if release-script cost needs an owner, it is a `/hygiene` `perf` prompt, filed
separately.

## The gap, confirmed against current main

- `agents/conductors/profiling/AGENTS.md` still lists *"JAX compilation-time
  profiling of likelihood functions"* under **Future modes**.
- `agents/conductors/profiling/_profiling.py` (353 lines) contains **zero**
  occurrences of "compile". `campaign` / `ingest` / `triage` read only
  `results/runtime/`.
- The workspace instrument exists and is already producing data — 93 records under
  `scripts/misc/jax_compile/results/<hardware>/<model_type>.json`.

So this is a **wiring** task, not an instrument-building one. The agent cannot see
a tree that is already full.

## The three blockers the child prompts exist to clear

Measured against the 93 committed records, 2026-08-10:

1. **Coverage is 2 of 21 grid cells.** Every record is `hst`; there is **no
   interferometer, no datacube, no `jwst`, no `ao`** row, and only `local_cpu` is
   meaningfully populated (A100 has 9 rows, all `pixelization`/`mge` × `jit`/`vag`).
   Two model types present (`knn`, `delaunay_matern`) are mesh variants that are
   not in the runtime `CELLS` grid at all. → **child prompt 1**.

   *(Corrected 2026-08-10 once phase 1 computed it: the grid is 21 cells, not the
   24 first written here, and only `imaging/mge/hst` + `imaging/pixelization/hst`
   are on-grid — 11 of 147 cell×transform runs on the local tier, 3 on A100.)*
2. **Warm rows are not machine-identifiable.** "Warm" is encoded only in a
   free-text `tag` — ~40 distinct ad-hoc values across the corpus
   (`census-warm`, `census-warm2`, `prodigy-census-warm-retry`, `cache-warm`,
   `a100-census-warm`, `mb_homo_cold`, `idle-check`, `smoke`, `matrix`, …).
   A dashboard that must track *warm* compile literally cannot tell which rows are
   warm. `cache_dir` is recorded but as a machine-specific path, so it answers
   "a cache was configured", not "this row hit it". → **child prompt 2**.
3. **Compile rows have no pin.** Runtime results carry `pinned_expected`, which is
   what `ingest` and `triage` are built around. Nothing equivalent exists for
   compile, so there is no baseline to regress against. → **child prompt 2**, used
   by **child prompt 3**.

Also present and needing a decision rather than a fix: **4 malformed records** with
`hardware`, `dataset_class` and `instrument` all `null`.

## The constraint any design must carry

**Compile timings are host-load-sensitive and cross-host comparison is invalid.**
The README records the first measurements being wrong by up to **7×** (851 s vs
117 s for the same compile) purely from host load, and those rows are retained
"only with their original tags for provenance". The corpus already contains
`prodigy-census-ral32-*` rows taken on a different core count from the
`local_cpu` rows filed beside them.

So comparability is a **key**, not a nicety:
`(hardware, jax_version, mixed_precision, cache_state)` — plus an explicit
idle/loaded provenance signal. An agent that compares across that key will report
regressions that are only a busy laptop, which is worse than no surveillance at
all.

## Phasing

| # | Prompt | Repos | Size |
|---|---|---|---|
| 1 | `compile_axis_campaign_coverage.md` | PyAutoBrain | small |
| 2 | `compile_warm_baseline_dashboard.md` | autolens_profiling + PyAutoBrain | medium |
| 3 | `compile_axis_triage_drift.md` | PyAutoBrain | small–medium |

Strictly sequential: 2 needs 1's cell-resolution logic, 3 needs 2's pins.

`draft/feature/autolens_profiling/jax_compile_time_profiling.md` (already
re-scoped 2026-07-28 to "the recurring cell-grid compile dashboard") is the
workspace half of child prompt 2 and is **absorbed** into it — see its header.

## Acceptance (arc)

- `pyauto-brain profiling <mode> --axis compile` answers all three modes.
- The compile axis never compares rows across the comparability key.
- `AGENTS.md` moves compile-time profiling from **Future modes** to **Modes**.
- A cache regression (warm compile reverting toward cold) is *detected*, which is
  the surveillance function the whole arc exists for.

---

## What the prompt originally said

<details>
<summary>Original text, filed 2026-07-14 (superseded — kept for provenance)</summary>

Extend the **PyAutoBrain Profiling Agent** (`agents/conductors/profiling/`, workspace
`autolens_profiling`) scope to track **JAX compile-time and eval-time** of the
release-validation heavy scripts, so we can speed them up.

The 2026-07-13 release-validation tail (PyAutoHeart#72,
[[project_release_2026_07_13_blocked_3bugs]]) is largely **PERF**: real-search +
finite-difference JAX scripts blow the 300s per-script cap under `mode=release`
(`jax_grad/imaging_pixelization.py` >400s, `jax_grad/interferometer.py`,
`imaging/features/shapelets/modeling.py`, group/slam chaining, `jax_likelihood
multi/shared_preloads`). We are upping the release `BUILD_SCRIPT_TIMEOUT` to unblock
now (see PyAutoHeart#72); the **durable fix is to speed them up**.

Extend the Profiling Agent's `campaign` / `ingest` / `triage` scope so it measures,
for these scripts, the **`jax.jit` compile time** + **per-eval time** (CPU, and the
FD-gradient full-run cost), records baselines, flags regressions, and emits a
**ranked slowest-JAX-scripts report** that `/hygiene` can act on. Candidate root
causes to look for (see [[project_jax_gradient_audit_shipped]] and
[[feedback_jax_closure_cache_busts]]): recompilation / JIT cache-busting (fresh `f`
per call), finite-differences where `jax.grad` would work but a `custom_jvp` is
missing (Delaunay), and oversized problems under the real-search release profile.

Deliverable: a Profiling-Agent scope extension (compile/eval-time coverage of the
release-validation JAX scripts) + the ranked report driving a hygiene/perf backlog.
Large — expect to phase at start_dev time. Cross-ref the mode=release timeout/scope
policy question on PyAutoHeart#72.

</details>

<!-- formalised via the Intake (Conception) Agent on 2026-07-14 from user-intake; target hand-corrected PyAutoHeart -> PyAutoBrain (Profiling Agent is a Brain conductor) -->
<!-- re-scoped 2026-08-10 via the Feature Agent (pyauto-brain feature): motivation moved
     from speed-up to regression surveillance against the shipped #71/#74/#77 verdicts;
     release-validation-scripts leg dropped to the hygiene boundary; split into three
     child prompts; absorbed the workspace-side dashboard prompt. -->
