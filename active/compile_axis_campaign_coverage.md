# Profiling Agent phase 1 — `campaign --axis compile`: what compile coverage do we actually have?

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

Phase 1 of `profiling_agent_jax_compile_time_scope.md` (read that first — it
carries the re-scope, the evidence and the comparability constraint).

## Why this leg first

It is the cheapest of the three, it is pure-read, and it produces the number that
justifies the other two. Right now nobody can say how much of the science grid the
compile corpus covers, because nothing cross-references the two trees.

Measured by hand 2026-08-10 — this is what the mode should compute automatically:

- **93 records**, all under `scripts/misc/jax_compile/results/<hardware>/<model_type>.json`.
- Distinct `(dataset_class, model_type, instrument)` touched: **`imaging/mge/hst`,
  `imaging/pixelization/hst`, `imaging/delaunay_matern/hst`, `imaging/knn/hst`**,
  plus two synthetic multi-band classes (`datacube_img`, `datacube_img_hetero`).
- The runtime grid (`scripts/misc/likelihood_runtime/sweep.py::CELLS`) is **21**
  `(class, model, instrument)` cells across `imaging` / `interferometer` /
  `datacube` × `hst,jwst,ao` / `sma,alma,alma_high,jvla`.
- So: **no interferometer row, no datacube row, no `jwst`, no `ao`** — one
  instrument out of seven, and `delaunay_matern` / `knn` are mesh variants that are
  not grid cells at all.
- Hardware: `local_cpu` (82 rows), A100 (9, all `pixelization`/`mge` × `jit`/`vag`),
  RTX 2060 (2). Plus **4 malformed rows** with `hardware`/`dataset_class`/
  `instrument` all `null`.

## Scope

Add `--axis compile` to the existing `campaign` mode in
`agents/conductors/profiling/_profiling.py`. The runtime axis stays the default and
is untouched.

1. **Read the compile corpus.** Load `scripts/misc/jax_compile/results/*/*.json`
   (append-only lists of flat records). Stdlib `json` only — the same
   never-import-the-workspace rule the runtime path already follows via `ast`.
2. **Resolve each record to a grid cell** using its in-record
   `(dataset_class, model_type, instrument)`, not its file path — the results tree
   is filed by `<hardware>/<model_type>` and drops class/instrument from the path.
3. **Report coverage** over cell × transform × hardware-tier. The transform axis is
   `probe.py`'s seven: `jit`, `grad`, `vag`, `vmap`, `vmap_vag`, `laxmap_vag`,
   `pyloop_vag`. Cells not in `CELLS` are reported in their own **off-grid** bucket
   rather than silently counted or silently dropped — `knn` and `delaunay_matern`
   are real measurements from the Prodigy census and must not read as noise.
4. **Report malformed records** (missing `hardware` / `dataset_class` /
   `instrument`) as their own bucket with file + index, so they can be fixed or
   deleted deliberately.
5. **Emit a dispatch plan** of concrete `probe.py` invocations for what is missing,
   mirroring how the runtime campaign emits `sweep.py` lines:
   `python jax_compile/probe.py --model-type <m> --transforms <list>` for local,
   and the `hpc/batch_gpu/submit_*` form for `--tier a100`.

## Explicitly not in scope

- Any judgement about whether a compile time is *good* — that is phase 3.
- Any pin, baseline or dashboard — that is phase 2.
- Running `probe.py`. The agent reasons and emits a plan; it never executes the
  workspace (`ProfilingDecision` contract).

## Acceptance

- `pyauto-brain profiling campaign --axis compile` and
  `... --axis compile --tier a100` both run against a real `autolens_profiling`
  checkout and report done / missing / off-grid / malformed counts.
- The reported on-grid coverage matches the hand count above on the corpus as it
  stands. MEASURED once built: **11 of 147** cell×transform runs on the `local`
  tier and **3 of 147** on `a100`, i.e. only `imaging/mge/hst` and
  `imaging/pixelization/hst` are on-grid. (The pre-build estimate said "3–4 cells
  of 24" — the grid is 21 cells, and `knn`/`delaunay_matern` are off-grid rather
  than partial coverage.)
- `--json` emits the same structure, consistent with the existing modes.
- The runtime axis output is byte-identical to before the change (regression test).
- No file in `autolens_profiling` is written or executed by the agent.

<!-- filed 2026-08-10 as phase 1 of the compile-axis arc; coverage figures measured
     against autolens_profiling main at clone time. -->
