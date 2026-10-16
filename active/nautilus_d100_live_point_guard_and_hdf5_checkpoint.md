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
