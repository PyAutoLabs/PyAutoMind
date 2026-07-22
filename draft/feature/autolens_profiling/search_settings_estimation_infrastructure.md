# Search settings-estimation + profiling infrastructure (n_starts / batch_size / n_batch)

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Right now `n_starts`, `batch_size`, `n_batch` and vmap width are hand-set per
cell, but the correct values depend jointly on **the data, the model and the
device VRAM**, and vary vastly between cells. `vram/config.py` already does this
for Nautilus `n_batch` (A100-probed per dataset/model/instrument, consumed via
`vmap_batch_for`) — there is **no equivalent for the MultiStart gradient
family**. Build the missing half: probe or estimate per-(cell, device) settings
for the MultiStart searches and let the builders in `searches/_samplers.py`
consult it instead of hardcoding.

Seed evidence measured on the 4-lens + 4-source group cell (54 free params,
8 MGE bases, autolens_profiling#82), RTX 2060 6 GB:

- `n_starts` and `batch_size` are **distinct levers**: `n_starts` is a
  *scientific* knob (multi-start coverage), `batch_size` is purely a *memory*
  one and is numerically identical to the vmap. Both have real uses; neither
  substitutes for the other.
- XLA compile time scales ~**linearly with `n_starts`** unbatched:
  16 starts = 13 min 35 s, 32 starts = 26 min 53 s (projects ~53 min at 64).
  Linear scaling suggests XLA unrolls per-start rather than compiling one
  kernel and mapping it — worth understanding on its own.
- `batch_size` chunking via `jax.lax.map` bounds memory but costs a lot of
  compile: 64 starts + `batch_size=8` exceeded 44 min still compiling, vs
  13 min 35 s for 16 unbatched. So chunking is the wrong trade **unless no
  workable `n_starts` fits at all**.
- Unbatched 64 starts requests a single **4.71 GiB** allocation and OOMs a 6 GB
  card; 32 starts peaks ~5.1 GB against a 4.9 GB budget.
- The JAX persistent compile cache (autonerves sets `JAX_COMPILATION_CACHE_DIR`,
  `min_compile_time_secs=1`) **does** absorb this compile — a 4.27 MB
  `jit_call` entry is written ~2 min after compile completes — so repeat runs of
  the same graph shape are cheap, and the shared `value_and_grad` entry should
  be reused across optimizers. Caveat: killing a run inside that ~2 min window
  loses the entry.

Goal: an estimator that, given dataset + model + device, proposes
`n_starts` / `batch_size` (and flags when a cell simply cannot fit), plus the
profiling harness to populate it — the MultiStart analogue of `vram/`.

Related: [[project_multi_start_gradient_v2_shipped]],
[[project_searches_first_class_a100_findings]].
