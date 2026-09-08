## delaunay-nn-launch-latency

- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/532
- completed: 2026-09-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/533
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/307
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/227
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/533
- scope: **Phase A only** — Phase B and Phase C of the prompt are deliberately not filed (see below)
- phase-b: **not re-filed, superseded by a better lever.** The A100 breakdown shipped with this task attributes the remaining per-call cost: the cavity early exit targets only the ~6.4 ms Sibson share and is worth ≈ 1.3 ms per call at `vmap` 16 (≈ 2.5 % of a production evaluation), while the ConstantSplit regularization assembly is ~10.0 ms per call (~19 %) and is untouched by anything Phase A or Phase B can do. The human agreed at close-out to point the next prompt at the assembly instead: `draft/feature/autoarray/delaunay_nn_constant_split_assembly.md`. Phase B stays unfiled until that lands.
- phase-c: **unfiled.** The loop-free k-ring cavity (which changes fp summation order) is now the smallest of the three levers on the batched number and must be re-costed against the post-#533 figures in `results/notes/delaunay_nn_launch_latency.md` before it is planned.

### What shipped

Three cuts to `autoarray/inversion/mesh/interpolator/sibson.py`, none of which change a number:

1. **Gated candidate unroll** — the 3-trip candidate-edge `fori_loop` inside the Sibson cavity walk is unrolled at trace time when `_sibson_unroll_candidates()` is true (`PYAUTO_SIBSON_UNROLL_CANDIDATES` wins if set, otherwise `jax.default_backend() != "cpu"`). The same `add_candidate` calls for edges 0, 1, 2 in that order, so the same cavity insertion order, the same stencil column order and the same floating-point summation order. ~28 % fewer kernel launches per chunk (1,244 → 892).
2. **Single concatenated pass** — `jax_delaunay_nn` locates and interpolates the data grid and the 6,000 `ConstantSplit` cross points in one Sibson pass, computing the circumcircles once. This is the PyAutoArray#531 pattern applied one boundary further in, and it is the whole scope of the superseded `sibson_single_concatenated_walk` draft.
3. **`SIBSON_QUERY_CHUNK` is a memory guard again** — default **4096**, with `PYAUTO_SIBSON_QUERY_CHUNK` as an import-time override so it can be swept without editing source.

Plus the evidence machinery: a **split-Sibson breakdown stage** in `autolens_profiling` (which is what made the attribution below possible) and an extended `scripts/misc/jax_assertions/delaunay_nn.py` gate in `autolens_workspace_test` asserting single-pass parity, chunk invariance and the chunk env override.

### The numbers (A100, `euclid-ral-gpu-2`, ten job units in one 28-minute window)

| | control | shipped | |
|---|---:|---:|---|
| params→H prefix, unbatched | 143.90 ms | **28.21 ms** | **5.10×** |
| params→H prefix, per call @`vmap` 16 | 24.32 ms | **16.44 ms** | **1.48×** |
| whole likelihood, single JIT | 201.32 ms | **76.32 ms** | **2.64×** |
| whole likelihood, per call @`vmap` 16 | 58.02 ms | **52.62 ms** | **1.10×** |

Full note (provenance table, chunk sweep, attribution caveats): `autolens_profiling/results/notes/delaunay_nn_launch_latency.md`.

### Witness verdict — half met, and the note says which half and why

- **Unbatched half (params→H ≤ 60 ms): met.** 28.21 ms shipped; met at every chunk ≥ 512.
- **Batched half (≤ 11 ms per call at `vmap` 16): not met.** 16.44 ms. The new split-Sibson stage names the reason: the **ConstantSplit regularization assembly reads 9.9–10.2 ms per call at every chunk and on the control leg** — 143× barycentric Delaunay's equivalent H row (0.07 ms) and ~19 % of the 52.6 ms batched whole likelihood. After Phase A roughly 60 % of the per-call params→H prefix is the 33-wide split-stencil assembly, not the Sibson loops. 10 ms of the witness was never Sibson's to give, which is why the batched half was unreachable by this task's scope and why the follow-up points at the assembly.

### The default-chunk ruling (4096)

The pre-registered rule (plan A.3) was "the largest of 512/1024/2048/4096 whose peak VRAM at `vmap` 16 stays under ~50 % of the 80 GB and which is fastest per call; if 4096 wins on both, ship 2048 unless the margin is > 15 %". 4096 was fastest on both readings, but **the VRAM clause turned out vacuous and was therefore not used to break the tie**: the ~41.5 GiB plateau (50.7 % of 81,920 MiB) is identical at every chunk *and* on the control leg, the card read 0 MiB before every job, and a 16× change of chunk moves it by 8 MiB — so the plateau is this cell's `vmap`-16 dense inversion block, not the cavity intermediates. With that leg dead the decision rests on speed alone: 4096 is 14.0 % faster per call at `vmap` 16 than 2048 (16.451 vs 19.127) and 9.4 % faster unbatched — a margin the rule's "ship 2048 unless > 15 %" clause would have sent to 2048 had the VRAM clause been live. It is not, so **4096 ships**, with `PYAUTO_SIBSON_QUERY_CHUNK` kept as the documented escape hatch for a smaller GPU or a much larger cell. The constant's comment now carries the sweep table, the rule and the guard arithmetic.

### Gates, pins and tests

- **CPU is gated off the unroll.** The paired CPU A/B ratio was **0.993** — rolled is marginally faster there — so `_sibson_unroll_candidates()` defaults to false on the CPU backend and the unroll is a GPU-only trace-time choice.
- `EXPECTED_LOG_EVIDENCE_HST = 29144.581944` held **exactly on every one of the ten legs** and at every chunk; `pinned_drift: []` on all four runtime rows. The chunk is bit-neutral by construction and the sweep proves it end-to-end: five different `lax.map` block sizes, one log evidence.
- **1,456 PyAutoArray unit tests** pass, including new `test_sibson.py` coverage for the unroll gate, the concatenated pass and chunk invariance.
- The `autolens_workspace_test` jax_assertions gate was extended rather than duplicated.

### Traps worth remembering

- **The 35.4 → ~0 ms collapse of the "Split-point Sibson" breakdown row is an attribution shift, not a saving.** Before the change a prefix stopping at step 6 never asked for the split points, so XLA dead-code-eliminated the second Sibson pass out of it and its whole cost surfaced in that row's subtraction. Only `regularization_matrix_prefix_s` — the params→H prefix — says whether work actually went away.
- The shipped leg's interpolator-prefix `vmap` number (8.944 ms) is the *first* prefix measured in that run and carries warm-up; the split-Sibson prefix in the same run, a strict superset, reads 6.434 ms. Read the Sibson share at `vmap` 16 as ≈ 6.4 ms per call.
- All ten job units ran on the same node with identical `xla_flags` (`--xla_disable_hlo_passes=constant_folding --xla_gpu_autotune_level=0`), so these rows are comparable with the 2026-09-07 `delaunay_walk_early_exit.md` rows and **not** with the 2026-07-10 `preopt_breakdown_baseline.md` rows. The shared `/mnt/ral/jnightin/PyAuto` install was deliberately not touched (live subhalo-validation and Euclid DR1 CPU runs); every leg prepended a private PyAutoArray checkout to `PYTHONPATH`.

### Superseded

`draft/feature/autoarray/sibson_single_concatenated_walk.md` — its entire scope (one concatenated Sibson locate instead of two) shipped as cut A.2 of PyAutoArray#533. Retired at this close-out to `complete/2026/09/sibson-single-concatenated-walk.md`; its `Superseded-by:` chain now ends here.

## Original prompt

# DelaunayNN (Sibson) on the A100: kill the kernel-launch latency in the cavity walk

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
- autolens_workspace_test
Themes:
- jax-gpu
- delaunay
- profiling
- performance
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: the A100 DelaunayNN breakdown's params→H prefix (`regularization_matrix_prefix_s`, `results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_walk_early_exit.json` is the 2026-09-07 baseline: 144.789 ms unbatched / 24.424 ms per call at vmap 16) drops to at most 60 ms unbatched and 11 ms per call at vmap 16 after Phase A, with `EXPECTED_LOG_EVIDENCE_HST = 29144.581944` unchanged and the `delaunay_nn.py` / `delaunay_nn_caps.py` jax_assertions passing
Review-minutes: 40
Unattended: ready
Filed: 2026-09-07
Issued: 2026-09-07
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/532
Supersedes: draft/feature/autoarray/sibson_single_concatenated_walk.md

Original request (verbatim):

> ok then prm, then HPCPullPyAuto, then go on to do the work on delaunayNN. We recently did a likelihood_breakdown of delaunay_nn, so check that out and then work out if on the A100 we can make it really fast overall

## The measurement (A100, HST / Hilbert-1500 / MGE-60 / ConstantSplit, post PyAutoArray#531)

DelaunayNN costs 197.0 ms per likelihood unbatched against 62.0 ms for barycentric Delaunay,
and the whole excess sits in the two Sibson passes: the params→H prefix is 144.8 ms (NN) vs
7.2 ms (Delaunay); per call at vmap 16 it is 24.4 ms vs 5.1 ms. The four-way split charges
92 ms to "Triangulation + interpolation" (the data-side pass over 17,980 queries) and 45 ms to
the H row (the split-side pass over the 6,000 ConstantSplit points, which re-runs the whole
Sibson pipeline including a second circumcircle computation). The downstream rows are
identical to Delaunay's (blurred mapping matrix 8.36 vs 8.34 ms at vmap 16), so the 32-wide
mapper costs nothing after the setup.

The compiled HLO of `sibson_mappings_weights_from_tables`
(`PyAutoArray/autoarray/inversion/mesh/interpolator/sibson.py`) has three nested loops: the
`lax.map` over `SIBSON_QUERY_CHUNK = 256` queries (95 sequential chunks: 71 data + 24 split),
the 32-trip cavity `fori_loop` (`MAX_CAVITY_TRIANGLES`, the loop always runs to the cap), and a
3-trip candidate `fori_loop` inside it. That is 32 × (4 + 3 × 11) + 60 = 1,244 kernel launches
per chunk, 95 % of them in the cavity walk, ≈ 118,000 launches per likelihood. Against the
measured 144.8 ms that is ~1.1 µs per launch: the A100 launch floor. Corroboration: 16× the
lanes (vmap 16) cost 2.7× the time. The cost is dispatch latency serialised by the chunk loop,
the same disease `DELAUNAY_LOCATE_CHUNK` had, one level down. Observed cavity sizes on this
cell are mean 3.5, max 9 (audit maxima across 101 traced meshes: 25 main / 19 split).

## Phase A: one PR, all launch-count reductions that keep bit-identical output

1. Unroll the 3-trip candidate `fori_loop` in `process_triangle` (`sibson.py` ~179–201) into a
   Python `for edge in range(3)`. Insertion order is preserved, so stencil column order and
   fp summation order are unchanged; verified bit-identical on CPU. Launches per chunk
   1,244 → 892.
2. Raise `SIBSON_QUERY_CHUNK` (`sibson.py:36`, bound at `mesh/mesh/delaunay_nn.py:47`). The
   chunk is only a memory guard; sweep 512 / 1024 / 2048 / 4096 on the A100 at vmap 16 and
   record peak VRAM (a vmap-64 OOM on this cell is already on record in
   `delaunay_nn_hpc_a100_fp64_vmap64.json`). Ship the largest value with comfortable headroom
   as the new default; keep the constant overridable.
3. Locate and interpolate the data grid and the split points in one concatenated
   `mappings_weights_for` call in `jax_delaunay_nn` (`sibson.py` ~670 and ~699), slicing at
   `n_query`, and hoist `delaunay_circumcircles_from` so the circumcircles are computed once.
   Split points keep their own nearest-vertex fallback. Small on its own (~1 chunk), worth it
   once the chunk is large.
4. Add a `_setup_prefix_fn` stage to
   `autolens_profiling/scripts/imaging/likelihood_breakdown/delaunay_nn.py` that stops after
   `_mappings_sizes_weights_split`, so the H row separates split-side Sibson from the
   33-wide ConstantSplit assembly (the ~27 ms non-chunk residual is currently unattributed).

Expected: params→H ≈ 50 ms unbatched (2.9×) and ≈ 9 ms per call at vmap 16 (2.7×).

## Phase B: early-exit the cavity walk (after Phase A is measured)

Convert the cavity `fori_loop` (`sibson.py` ~203–208) to a `lax.while_loop` with
`cond = (position < cap) & any(position < count)`, cap kept as the safety bound, overflow
detection (`sibson.py` ~198, ~418–423) unchanged. Under vmap the exit is at the global max
(~25), so the win is ~20 % of the cavity part: worth ~7 ms after Phase A. Gradient contract:
today the `fori_loop` lowers to `scan` and is reverse-mode differentiable; `while_loop` is
not, so the float inputs to `_contains_query` (`query`, `circumcentres`, `circumradii_squared`)
must be `stop_gradient`-wrapped as they enter the loop (integer/bool outputs only, zero a.e.
derivative), while the `circumcentres[safe_cavity]` gather at ~259 that feeds the Sibson
weights stays traced. Re-run the DelaunayNN gradient checks after.

## Phase C (separate prompt, not this task): loop-free cavity via a fixed k-ring gather

Replace the cavity walk with a one-shot containment test over the seed simplex's k-ring
(3-ring 21 / 4-ring 45 candidates), compact, overflow → NaN as now. Removes the loop
entirely (launches per chunk → ~80) for an estimated floor of ~30 ms unbatched / ~6 ms per
call at vmap 16, but changes candidate ordering and therefore fp summation order in the
mapping matrix, so the pin needs a relative tolerance and the cap audit must be re-run.
File after Phase B's numbers.

## Contracts (do not relax)

- Pin `EXPECTED_LOG_EVIDENCE_HST = 29144.581944` in `delaunay_nn.py` passes unchanged through
  Phases A and B; a shift means a mapping or summation order changed and is a bug.
- Judge on the params→H prefix (`regularization_matrix_prefix_s`), not on the Tri+interp or H
  rows: both are prefix differences and step 3 moves work between them exactly as #531 did
  for Delaunay (`results/notes/delaunay_walk_early_exit.md`).
- `SIBSON_MAX_NEIGHBORS` / `MAX_CAVITY_TRIANGLES` stay at 32 (cap audit
  `results/notes/delaunay_nn_cap_audit.md`); any cap change re-runs
  `autolens_workspace_test/scripts/misc/jax_assertions/delaunay_nn_caps.py`.
- `jax_sibson` (`sibson.py` ~505) is exercised by
  `autolens_workspace_test/scripts/misc/jax_assertions/delaunay_nn.py` (`sibson_tables`), so
  it stays; apply the unroll to the shared `sibson_mappings_weights_from_tables` so both
  entry points benefit.
- Unit tests stay NumPy-only; JAX-path parity, jit/vmap and gradient checks live in the
  workspace_test jax_assertions scripts.

## Verification on the A100

Same-node, same-session A/B as PyAutoArray#531 (control = private checkout at the merge
base, feature = branch; shared `/mnt/ral/jnightin/PyAuto` untouched while science jobs run):
`scripts/imaging/likelihood_breakdown/delaunay_nn.py --config-name hpc_a100_fp64 --split-setup
--vmap-batch 16`, plus the chunk sweep for step 2 with peak-VRAM readings, and the runtime
cell. Report every row unbatched and per call at vmap 16, the params→H prefix, the new
ConstantSplit stage, and the single-JIT total, against the 2026-09-07 post-#531 baseline.

Folds in `draft/feature/autoarray/sibson_single_concatenated_walk.md` (filed 2026-09-07 as the
follow-up of `complete/2026/09/delaunay-walk-early-exit.md`); the analysis above shows the
concatenation alone is worth ~1 chunk, so it ships as step A.3 rather than on its own.
