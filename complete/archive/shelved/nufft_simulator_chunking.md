# The `al.SimulatorInterferometer` path that uses `al.TransformerNUFFT` (nufftax-backed) can't scale to

Type: feature
Target: PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: low
Status: SHELVED 2026-08-11 — not legacy, but nothing is waiting on it; read the 2026-08-11 block first

## 2026-08-11 — shelved: the gap is already worked around in production

Investigated to answer "is this legacy?" — **no, but it is not motivated
either.** The capability this prompt asks for is already reachable and in use;
what is left is de-duplication, not enablement.

Moved here from `draft/feature/autoarray/` so it stays out of task selection
(the Feature Agent scans `draft/feature/**`, and `lifecycle.py check`/`index`
skip `complete/archive/`). Per `complete/archive/README.md`, the revival path is
to pull it back into `draft/feature/autoarray/` — see § Revisit when below for
what would justify that.

### Who actually needs the batching

Exactly one repo and two instrument presets, per
`autolens_profiling/instruments/interferometer.py`:

| instrument | n_visibilities | `transformer_chunk_size` |
|---|---|---|
| sma | 190 | `None` — "sma is tiny; one-shot" |
| alma | 1M | `None` — "1M vis × nspread²=196 ≈ 3 GB; fits A100 one-shot" |
| **alma_high** | **5M** | **1_000_000** |
| **jvla** | **25M** | **1_000_000** |

Note this corrects the § below: the trigger threshold is between 1M and 5M
visibilities, not the ~1M this prompt derived. 1M is the right *chunk* size, not
the right *trigger*.

### Why it is stood down

`autolens_profiling` already injects `chunk_size` through a lambda factory,
because `transformer_class` is a factory contract rather than a class contract
(`PyAutoArray dataset/interferometer/dataset.py:291` sets the precedent). From
`scripts/misc/simulators/interferometer.py:101`:

```python
if transformer_choice == "nufft":
    # Lambda inject so chunk_size flows into TransformerNUFFT.__init__
    # without needing a transformer_kwargs API in Interferometer.from_fits.
    def transformer_class(uv_wavelengths, real_space_mask):
        return al.TransformerNUFFT(..., chunk_size=transformer_chunk_size)
```

That workaround is **live in 8 files** — `scripts/misc/simulators/interferometer.py`,
`scripts/misc/searches/_setup.py`, three `scripts/interferometer/likelihood_runtime/*`
and three `scripts/interferometer/likelihood_breakdown/*`. Five carry a near-identical
docstring naming the API that does not exist: *"without needing a transformer_kwargs
API on Interferometer.from_fits. Required for alma_high…"*

So the alma_high simulate path is **not blocked and never was blocked** in the way
the § at the foot claims. Verified on PyAutoArray `main` @ `5dedb5e9`: the
`chunk_size` knob, its `jax.lax.scan` branch on forward *and* adjoint, and its 5
tests are all present (PyAutoArray#330). Only the ergonomic hop is missing.

### If it is revived, the shape is already settled

The consumers converged on the API and wrote its name into their comments, so the
design question is answered by evidence rather than opinion:

- Add `transformer_kwargs: Optional[dict] = None` to `SimulatorInterferometer` and
  `Interferometer` (incl. `from_fits`), splatted into `transformer_class(...)`.
  Defaults to `{}`, so the default path stays byte-identical. Closes the identical
  `eps` gap in the same stroke.
- **Not** an explicit `chunk_size` argument: `SimulatorInterferometer` is generic
  over three transformers, `TransformerDFT.__init__` has no `**kwargs` and is the
  *default*, so a bare pass-through TypeErrors on the default path.
- No default chunk size. The ~1M figure is one GPU's budget (nspread=14 /
  complex64 / 40 GB) and belongs in the profiling caller, which already sets it.
- Scope is **two repos**: the PyAutoArray API, then deleting the 8 duplicated
  lambdas in autolens_profiling. A library-only PR does half the job.

### Revisit when

Any one of these makes it motivated again — none is true today:

1. A **non-profiling** consumer needs >1M visibilities (a workspace or user
   dataset), where the lambda workaround is not acceptable ergonomics.
2. Someone takes on the 8-site duplication in autolens_profiling as maintenance.
3. The `eps` gap bites independently — same hole, same fix.

Latent and independent of all this: the DFT-size guard at `dataset.py:118`
identity-checks `transformer_class == TransformerDFT`, so any `partial`/`lambda`
factory silently disables it. Not currently triggered (the profiling code only
lambda-wraps NUFFT, where the guard should not fire anyway). If it ever bites,
it is its own bug prompt, not this one.

---

## 2026-08-09 — the library work below is SHIPPED; only the wiring is left

Found by the `draft/` sweep. Verified against PyAutoArray main (`efaf3041`).

**Everything in § "The fix" option 1 is already on main**, delivered by
**PyAutoArray#330 ("TransformerNUFFT: add chunk_size knob to cap nufftax gather
buffer"), merged 2026-05-22** — roughly seven weeks BEFORE the Intake Agent
retroactively formalised this prompt on 2026-07-08. It landed to the letter of
the plumbing section below:

- `TransformerNUFFT.__init__` takes `chunk_size: Optional[int] = None` — this
  prompt's suggested name and its "no chunking by default" default, so the
  small-N `sma` callers pay nothing. A non-positive value raises `ValueError`.
- `_forward_native` (`autoarray/operators/transformer.py:681`) splits the
  visibility axis and iterates with **`jax.lax.scan`** on the JAX path (a Python
  loop only on the numpy path) — exactly the "do NOT use a Python `for`, it
  unrolls and blows up JIT compile time" requirement below.
- `image_from` — the adjoint via `nufft2d1`, which this prompt flagged as "out
  of scope today, but flag it" — **is chunked too**, in the same shape.

The sibling blocker this prompt names has also shipped: the `apply_sparse_operator`
alma-scale precompute OOM closed 2026-05-22 as PyAutoArray#329
([[alma-apply-sparse-operator-oom]]).

**What is actually left is one wiring leg.** `complete/2026/07/interferometer-jax-jit.md`
records it: "`chunk_size` is a `TransformerNUFFT.__init__` argument that
`SimulatorInterferometer` **NEVER sets**, so the `lax.scan` branch is unreachable
via the simulator." So the capability exists and is untested-in-anger from the
simulator side. The remaining task is to plumb `chunk_size` from
`SimulatorInterferometer` (a default chosen by the memory budget already derived
below, ~1M for nspread=14/complex64 on a 40 GB working budget), then run the
§ Verification below to confirm alma_high actually lands.

`Difficulty:` accordingly drops `too-large` → `small`; `Priority:` stays high
because the profiling sweep it unblocks is still blocked. Do **not** re-implement
the chunking.

Note also that `option 2` below (upstream `nufftax` `chunk_size`) was never the
chosen scope and remains untouched — still a legitimate follow-up, still optional.

---

The `al.SimulatorInterferometer` path that uses `al.TransformerNUFFT` (nufftax-backed) can't scale to ALMA-realistic visibility counts. At ~5M visibilities on an 800×800 real-space grid it OOMs on an A100 (80 GB) with a single ~15.7 GB allocation; at 10M it's ~31 GB. The likelihood path scales fine to the same regime because `apply_sparse_operator` precomputes a small W-Tilde matrix bounded by `N_source_pixels` (~thousands), not by `N_visibilities`. The simulator has no equivalent escape valve — every forward call does one dense nufftax spread.

The blocker is upstream in nufftax. `nufftax.transforms.nufft2.nufft2d2` calls `_interp_2d_dispatch` → `interp_2d_impl` which, at line `fw_gathered = fw_flat[:, indices_flat].reshape(-1, M, kernel_params.nspread, kernel_params.nspread)`, materialises the full gather buffer in one shot. With `M = 5_000_000` and the default `eps=1e-6` (nspread=14), that's `2 × 5e6 × 14² × 8 ≈ 15.7 GB` for a single intermediate, and JAX's other intermediates push us past A100 headroom even with `XLA_PYTHON_CLIENT_PREALLOCATE=false`.

The likelihood path proves the scaling is achievable. We need an equivalent batching escape valve for the simulator side. Two reasonable places to put it:

1. **`@PyAutoArray/autoarray/operators/transformer.py:TransformerNUFFT._forward_native`** — wrap the `nufftax.nufft2d2(self._x, self._y, image_flipped, eps, -1)` call in a chunked loop over `M`. Split `(self._x, self._y)` into batches of e.g. 200k visibilities, run `nufft2d2` per chunk, concatenate the resulting per-batch visibilities. The forward NUFFT is linear in visibility batch, so the result is bit-identical to the one-shot call.
2. **Upstream `@nufftax/transforms/nufft2.py:nufft2d2`** — add a `chunk_size` arg that does the same internal chunking. Cleaner and benefits any nufftax caller, not just autoarray.

Option 1 is the right scope for this task — keeps the change inside our codebase, lands without an upstream PR. Option 2 can be a follow-up to `nufftax` once the autoarray-side batching proves the math.

Plumbing concerns to settle while implementing:
- The constructor of `TransformerNUFFT` (currently in `@PyAutoArray/autoarray/operators/transformer.py`) needs a knob — probably `chunk_size: int | None = None` defaulting to "no chunking" so existing small-N callers (`sma` with 190 visibilities) don't pay the chunk-loop overhead.
- Equivalent batching for `TransformerNUFFT.image_from` (the adjoint via `nufft2d1`) should land in the same PR — the adjoint has the same gather pattern and same memory ceiling on big problems. Out-of-scope today, but flag it.
- Chunking interacts with JIT: a Python-level `for` loop unrolls in JAX. Use `jax.lax.scan` or `jax.lax.map` so the compiled HLO graph stays bounded regardless of `M / chunk_size`. Otherwise the forward call is fine eagerly but JIT compile time blows up.
- Picking a default `chunk_size`: needs profiling. Memory budget = `2 × chunk_size × nspread² × dtype_size`. For nspread=14 + complex64 + a 40 GB A100 working budget, `chunk_size ≈ 1_000_000` is the natural ceiling.

Verification: re-run `autolens_profiling/simulators/interferometer.py --instrument alma_high` on an A100 (currently OOMs in the simulate jobs under `@z_projects/profiling/hpc/batch_gpu/submit_simulate_interferometer_alma_high`). With the batching in place, it should land cleanly and produce the same data the un-chunked call would have on a hypothetical 200 GB GPU. Then the downstream `@autolens_profiling/likelihood_runtime/interferometer/delaunay.py` and `@autolens_profiling/likelihood_runtime/datacube/delaunay.py` A100 sweeps that depend on alma_high stop being blocked.

Note: the runtime path also has its own ALMA-scale OOM, but it's a different one — see the sibling prompt `@PyAutoPrompt/autoarray/alma_apply_sparse_operator_oom.md` for the `apply_sparse_operator` precompute issue. Both need to land before the full A100 sweep (alma + alma_high × interferometer/delaunay + datacube/delaunay × fp64 + mp) can run end-to-end.

**This task feeds back into the open profiling work**: the A100 sweep on `autolens_profiling/likelihood_runtime/{interferometer,datacube}/delaunay.py × {sma, alma, alma_high} × {fp64, mp}` was started today, shipped the 4 SMA-only cells, and explicitly punted alma_high on this blocker. Once this prompt's chunking lands (and the sibling `alma_apply_sparse_operator_oom` prompt clears the alma-scale precompute OOM), come back and re-run the 4 alma_high SLURM submits at `@z_projects/profiling/hpc/batch_gpu/submit_{interferometer,datacube}_delaunay_a100_alma_high_{fp64,mp}` to fill in the missing rows of `comparison.json` and `@autolens_profiling/likelihood_runtime/OPTIMIZATION_NOTES.md`.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
