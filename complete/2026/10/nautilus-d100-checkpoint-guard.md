## nautilus-d100-checkpoint-guard
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1697
- completed: 2026-10-16
- epic: search-extensibility
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1698
- summary: Nautilus at D ≥ 91 failed before sampling in the `correlated_nd` pilot (60 d100 rows). Two root causes verified against nautilus-sampler 1.0.5 / h5py 3.13.0: (a) nautilus's ellipsoid fit needs n_live > n_dim (`bounds/basic.py:298`) and nothing checked it; (b) `Ellipsoid.write` stores D×D matrices as HDF5 attributes and `Sampler.write` opens with the earliest libver whose 64 KiB header-message cap fails from D = 91 ("object header message is too large"). PyAutoFit#1698 (merge e04700b8d) adds: a fail-fast `check_model` override (also at `run(ctx)` entry) raising `SearchException` with `NAUTILUS_N_LIVE_MESSAGE` before any likelihood call, requiring n_live > prior_count and n_points_min ≥ prior_count + 1; a run-scoped `_large_attribute_hdf5()` proxy giving nautilus `libver=('v108','latest')` on both execution paths (full checkpoint + resume at any D; remove when nautilus fixes upstream — a strict xfail control XPASSes then); `checkpoint: bool = True` opt-out (not an identifier field); a `Path(None)` fix when no checkpoint file. Tests: D=100 ellipsoid write/read round trip, the xfail control, a D=100 integration run that reaches the first checkpoint write and resumes (with a fast stand-in bound, since real nautilus rejection sampling at D=100 with ~100 live points does not finish in 80 s), guard tests with zero likelihood calls; 25 passed + 1 xfailed; CI green on 5 legs. Docs: `docs/design/checkpointing.md` "Nautilus at 91 or more parameters" with an upstream-issue link pending.
- follow-up: human posts the upstream nautilus-sampler issue drafted in the PR body and adds the link to `docs/design/checkpointing.md`; autofit_inference witness (d100 Nautilus n_live_200 at a pin carrying #1698) and a later `correlated_nd` amendment re-admitting d100 Nautilus — expect it to be slow at D=100 regardless; the harness should treat `SearchException` as `deferred`.
- traps: OOM and cap kills both exit 137 under `timeout` (see the 2a record); nautilus checks only n_dim ≤ 1 at construction, every other floor surfaces at the first bound.

## Original prompt

# `@PyAutoFit` Nautilus fails before sampling at D = 100: live-point guard…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Memory: reading-queue.md; wiki/methods/concepts/sampler-benchmarks.md; wiki/lensing/sources/dark-matter-substructure.md
Status: formalised
Consequence: judge
Witness: `corr_gaussian_d100` Nautilus `n_live_200` runs to completion at the pin on both backends (autofit_inference harness, one seed); the live-point guard rejects `n_live_100` at D = 100 before any likelihood call with a named error; search conformance suite green. Follow-up (separate, autofit_inference): a protocol amendment re-admitting d100 Nautilus into a later `correlated_nd` wave.
Review-minutes: 20
Unattended: ready

Evidence: the `correlated_nd` pilot (autofit_inference RAL 410866, judged in autofit_inference#18, B5c-2a) lost all 60 `corr_gaussian_d100` Nautilus rows before sampling, both backends, every seed:
- `n_live_100`: nautilus requires more live points than dimensions and raises. PyAutoFit let the run start and fail; this should be a declared capability/guard (fail fast with a clear message naming the floor, ideally at the A1 declaration/preflight layer) so a benchmark marks the cell `deferred` by construction, not `failed`.
- `n_live_200` / `n_live_400`: nautilus's HDF5 checkpoint cannot store a D = 100 bound — `object header message is too large` — in the checkpoint path PyAutoFit calls (the A3 Checkpointer/resume split wires `filepath`). The sampler itself is fine; the checkpoint write kills the run.

Consequence: amendment A2 of `correlated_nd@2` deferred every d100 Nautilus cell and d100 warm NUTS (its provider). The scored wave has no D = 100 nested-sampling leg until this is fixed.

Wanted:
1. Live-point floor: a fail-fast guard in the Nautilus search (or the capability declaration) with a precise error; a conformance test.
2. Checkpoint: a PyAutoFit-side fix or workaround — chunked/alternate storage of large bounds, a `checkpoint=False`/alternate-format setting for large D, or a documented resume-less mode — whichever keeps resume semantics honest; regression test at D = 100 (small n_live) that writes and reloads a checkpoint.
3. If the limit is nautilus's own, file an upstream issue (draft for the human; the human posts) and record it in the search docs.

Witness: `corr_gaussian_d100` Nautilus `n_live_200` runs to completion at the pin on both backends (autofit_inference harness, one seed); the live-point guard rejects `n_live_100` at D = 100 before any likelihood call with a named error; search conformance suite green. Follow-up (separate, autofit_inference): a protocol amendment re-admitting d100 Nautilus into a later `correlated_nd` wave.

Human ruling 2026-10-16: intake and then start the follow-up.

<!-- formalised by the Intake (Conception) Agent on 2026-10-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/525f7109-4545-4825-9b1b-2bdb3d87fac1/scratchpad/intake_a.md -->
