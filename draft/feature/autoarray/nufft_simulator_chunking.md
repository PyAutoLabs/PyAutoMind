# The `al.SimulatorInterferometer` path that uses `al.TransformerNUFFT` (nufftax-backed) can't scale to

Type: feature
Target: PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: high
Status: PLANNED — re-scoped 2026-08-09, planned 2026-08-11; read both dated blocks below before the original text

## 2026-08-11 — implementation plan (Feature Agent)

Planned via `pyauto-brain feature` (selection mode ranked this 1st of 27 feature
prompts, score 13 / impact 18; specific mode emitted the `FeatureDecision`
below), with the `memory` faculty consulted for prior art. Every claim here was
re-verified against PyAutoArray `main` @ `5dedb5e9`.

### Confirmed still true

The 2026-08-09 re-scope holds. `chunk_size` is on `TransformerNUFFT.__init__`
(`autoarray/operators/transformer.py:577`), the `jax.lax.scan` branch is live on
**both** forward and adjoint (4 call sites, lines 699/723/805/836), and 5 tests
cover it in `test_autoarray/operators/test_transformer.py`. **Do not
re-implement the chunking.**

The gap is exactly one hop wide. `SimulatorInterferometer.via_image_from`
constructs `self.transformer_class(uv_wavelengths=..., real_space_mask=...)`
(`autoarray/dataset/interferometer/simulator.py:173`) and hands
`transformer_class=self.transformer_class` to the returned `Interferometer`,
which reconstructs it the same 2-arg way (`dataset/interferometer/dataset.py:102`).
No caller can reach `chunk_size` through either.

### Three findings the 2026-08-09 block did not have

1. **`TransformerDFT.__init__` takes only `(uv_wavelengths, real_space_mask)` —
   no `**kwargs`** (`transformer.py:122`), and it is `SimulatorInterferometer`'s
   *default* `transformer_class`. A naive pass-through TypeErrors on the default
   path. `TransformerNUFFT` *does* have `**kwargs`, so the two are asymmetric.
2. **`transformer_class` is already a factory contract, not a class contract** —
   `dataset.py:291` passes `lambda uv_wavelengths, real_space_mask: self.transformer`.
   So `functools.partial(TransformerNUFFT, chunk_size=...)` works *today*,
   undiscoverably — but it silently defeats the DFT-size guard at `dataset.py:118`,
   which identity-checks `transformer_class == TransformerDFT`. That guard hole is
   pre-existing and independent of this task; fix it here since we are in the file.
3. **`eps` is unreachable through the identical hole.** Same gap class, same four
   sites. Whatever mechanism lands should close both or it will be re-litigated.

### CORRECTION to this prompt's stated justification

The § at the foot claims this unblocks the alma_high A100 profiling sweep. That
is **stale**. `complete/2026/07/profiling-dataset-auto-simulate.md` records the
alma_high dataset as deliberately **committed** (229 MB, "CANNOT be
uncommitted"), so the sweep consumes it without simulating. And the sibling
prompt `nufft_mapping_matrix_column_chunking.md` establishes that the
likelihood-side alma_high cell is blocked on the **column** axis
(`1600 × 1600 × 1500 × 16 B = 61.44 GB`), which this chunking explicitly does not
touch — that prompt states outright that the existing visibility chunking "does
nothing for this allocation".

The two axes are orthogonal, so there is **no scope collision** — but the
sweep-unblocking argument belongs to the sibling prompt, not this one. The honest
justification for this task is narrower and still sound: alma_high-scale
simulation is currently **impossible at any setting**, which blocks dataset
regeneration and any new large-N instrument. `Priority: high` is arguably
overstated on the corrected justification; the work is genuinely `small` either
way.

### Design decision — `transformer_kwargs`, opt-in, no default

Three shapes were considered. **Chosen: a `transformer_kwargs: Optional[dict]`
splatted into `transformer_class(...)` at the construction sites.**

- Rejected *explicit `chunk_size` arg*: narrowest diff and matches this prompt's
  letter, but hardcodes one implementation's knob into a class that is generic
  over three transformers (DFT / NUFFT / NUFFTPyNUFFT), and `eps` would demand
  the same treatment next. It also puts the DFT TypeError on the *default* path.
- Rejected *document `partial()`, no API change*: smallest change, but leaves the
  capability undiscoverable, which is precisely the state that produced this
  prompt.
- `transformer_kwargs` defaults to `{}`, so **the default path is byte-untouched**,
  it closes `eps` in the same stroke, and it keeps NUFFT vocabulary out of a
  transformer-agnostic container.

**No default chunk size.** The prompt's ~1M figure is derived for
nspread=14 / complex64 / a 40 GB budget — one GPU's memory budget does not belong
in a library default. Two further reasons: existing NUFFT simulator callers must
keep their exact code path (`profiling-dataset-auto-simulate.md` used *per-dataset
byte identity* as its gate and records that NUFFT float non-determinism already
makes alma/alma_high non-reproducible — do not perturb that), and the sma-class
caller at 190 visibilities should pay nothing. The 1M value belongs in the
autolens_profiling caller.

### Scope

Library (PyAutoArray), one PR:

1. `SimulatorInterferometer.__init__` gains `transformer_kwargs: Optional[dict] = None`,
   stored as `{}` when unset; splatted at `simulator.py:173` and forwarded to the
   returned `Interferometer` (`simulator.py:206`).
2. `Interferometer.__init__` gains the same parameter, splatted at `dataset.py:102`;
   `from_fits` (`dataset.py:141`) threads it through.
3. Raise a clear `exc.DatasetException` when `transformer_kwargs` is non-empty and
   the chosen `transformer_class` rejects the keys, rather than surfacing a bare
   `TypeError` from the transformer constructor.
4. Fix the `transformer_class == TransformerDFT` identity check at `dataset.py:118`
   so a `partial`/`lambda` factory no longer silently disables the 10k-visibility
   DFT guard (finding 2).
5. `apply_over_sampling`'s lambda at `dataset.py:291` returns a prebuilt instance
   and must keep ignoring `transformer_kwargs` — assert that, do not "fix" it.

Follow-on (**separate prompt, do not bundle**): set `chunk_size` at the
autolens_profiling simulate caller. That is the workspace half and only becomes
testable on real hardware.

### Acceptance

CPU-verifiable, in `test_autoarray/dataset/interferometer/` — copy the shape of
`test_simulator_use_jax.py`, which is the existing precedent for constructor-wiring
tests on this class:

- `SimulatorInterferometer(transformer_class=TransformerNUFFT, transformer_kwargs={"chunk_size": 8})`
  produces a transformer with `chunk_size == 8`, and its visibilities match the
  `transformer_kwargs=None` run to within NUFFT tolerance at small N.
- The same for the `Interferometer` returned by `via_image_from` — the knob must
  survive the round trip, which is the specific hop that is broken today.
- Default construction (`transformer_kwargs` unset, `TransformerDFT`) is
  unchanged — no new kwarg reaches the transformer.
- `transformer_kwargs={"chunk_size": 1}` against `TransformerDFT` raises the clear
  exception from scope item 3, not a bare `TypeError`.
- The `dataset.py:118` DFT guard still fires when `transformer_class` is a
  `partial`/`lambda` wrapping `TransformerDFT` with >10k visibilities (regression
  test for finding 2).

**Not gated on hardware.** The A100 `alma_high` simulate run stays the closing
confirmation, but it is a human-run step on RAL and must not block the PR — no
CI leg can reach an A100, and per the correction above no downstream sweep is
waiting on it.

### FeatureDecision

```
Repos affected:       PyAutoArray (+ autolens_profiling, follow-on prompt)
Difficulty:           small (declared; derived too-large — the prompt is long
                      because it accumulated findings, not because the work grew)
Recommended workflow: library  (corrected from the agent's `combined` — the
                      workspace half is split to its own prompt per
                      "one prompt = one task = one PR")
Phase decision:       direct
Execution plan:       start_dev → start_library → ship_library
Risks:                Default-path byte identity (mitigated: transformer_kwargs
                      defaults to {}); the pre-existing DFT-guard identity check
                      is widened in the same PR and needs its own regression test.
Next action:          start_dev draft/feature/autoarray/nufft_simulator_chunking.md
```

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
