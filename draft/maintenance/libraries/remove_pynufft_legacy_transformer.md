# Remove pynufft + legacy TransformerNUFFTPyNUFFT

Type: maintenance
Target: libraries
Repos:
- @PyAutoArray
- @PyAutoGalaxy
- @PyAutoLens
Difficulty: low-medium
Autonomy: supervised
Priority: normal
Status: shipped
Filed: 2026-08-22 (backfilled from git)

Re-homed 2026-08-22 from `draft/refactor/autoarray/`. The Brain Refactor Agent
refused it there (`SUSPECT-API-CHANGE`, effective autonomy `human-required`):
deleting a public class is not behaviour-preserving, so it cannot be a
`refactor/`. `maintenance/` ("dependency updates, hygiene, cleanup") is the
taxonomy fit for removing a dependency.

## Original request (verbatim, 2026-08-19)

> do we even use pynufft? maybe we should file a follow up to remove it I think
> its purely for one function, so make that filing remove it but also include
> this check of import time.

## Corrections to the original filing (measured 2026-08-22)

The 2026-08-19 filing had two factual errors, both found during implementation:

1. **pynufft was never a base dependency.** It sat in the `optional` extra
   (`PyAutoArray/pyproject.toml:67`) and the `dev` extra (line 77). A plain
   `pip install autoarray` never had it, so `TransformerNUFFTPyNUFFT` already
   raised `pynufft_exception()` for most users.
2. **The import-time saving is ~10 ms, not ~230 ms.** Measured as the median of
   7 runs on Python 3.13 with the dev extras: `import autoarray` goes
   369.8 ms → 359.9 ms. `pynufft`'s 0.19 s *cumulative* import is ~95 %
   `scipy.sparse` (0.11 s), which `autoarray/operators/derivative_util.py:30`
   pulls in eagerly for `csr_matrix` regardless of pynufft. Only ~10 modules and
   ~10 ms are exclusive to pynufft.

The removal is still worth doing — an unmaintained dependency, one dead class,
and a `dev` extra that is broken against SciPy >= 1.17 — but **not** on
import-time grounds. The real 0.10 s win is filed separately as
`draft/maintenance/libraries/defer_scipy_sparse_import.md`.

## The Intel-macOS decision (settled 2026-08-22)

The original filing flagged one blocking question: does removing the pynufft
fallback cost Intel-Mac users their interferometer transformer? Verified
against PyPI:

- `jaxlib`'s **last Intel-macOS (x86_64) wheel is 0.4.38**, uploaded
  2024-12-17. Every release since (through 0.11.1) is `macosx_11_0_arm64` only.
- `jaxlib` has **never published an sdist**, for any version — so there is no
  pip fallback that builds from source.
- PyAutoNerves' floor is `jax>=0.7.0`
  (`PyAutoNerves/pyproject.toml:38`, markered
  `sys_platform != "darwin" or platform_machine == "arm64"`).
- `nufftax` is pure-JAX; even its `xp=np` path calls `nufftax.nufft2d2`. So no
  JAX means no `TransformerNUFFT` either.

So Intel macOS keeps **`TransformerDFT` only** for interferometry — exact, pure
numpy, but O(N_vis x N_pix). Human decision (2026-08-22): accept this; record
it as a release-note line, not a blocker. The broader "is Intel macOS a
supported platform" question is filed as
`draft/research/libraries/intel_macos_support_policy.md`.

## Work done (branches pushed 2026-08-22)

All three on `claude/remove-pynufft-6uwt2z`:

- **@PyAutoArray** — deleted `TransformerNUFFTPyNUFFT`, the `NUFFTPlaceholder`
  / `NUFFT_cpu` module-scope try-import and `pynufft_exception()`; dropped the
  re-exports from `__init__.py` and `type.py` and its arm of the `Transformer`
  union; removed the three `test__nufft_pynufft__*` tests and the `"pynufft"`
  arm of the nufftax-absent skip filter in `conftest.py`; dropped `pynufft`
  from `optional` and the `pynufft==2022.2.2` pin from `dev`. Rewrote
  `nufftax_exception()` and the `use_adjoint_scaling` docstrings, which cited
  the deleted class. **1164 passed, 1 skipped.**
- **@PyAutoGalaxy** — dropped the `__init__.py:29` re-export and the `optional`
  entry; updated installation docs, the feature overview and the live citation
  surface (`files/citations.{md,tex,bib}`, `docs/index.md`) to cite `nufftax`.
  **1103 passed, 1 skipped.**
- **@PyAutoLens** — same, minus the citation *addition* (nufftax was already
  cited); the PyNUFFT entry was simply dropped. **532 passed, 1 skipped.**

`paper/` in both downstream repos was deliberately left untouched — published
JOSS records of what the software used at time of publication, not live docs.

## Remaining (both open items now closed — see above)

1. **Workspace tier** (not started, needs the workspace repos):
   - `autolens_workspace_test/scripts/interferometer/nufft.py:211` — the one
     executable use; drop or replace the PyNUFFT leg of the parity comparison.
   - Four prose mentions in autolens_workspace (`start_here.py`, `using_jax.py`,
     `simulator.py`, `linear_light_profiles/modeling.py`) describing it as a
     "non-JAX fallback".
   - Check `PyAutoHands/autohands/config/no_run.yaml` per the ship_library
     reference.
2. **PR bodies need the `## API Changes` breaking entry** (release-notes
   contract): `TransformerNUFFTPyNUFFT` removed; migration is `TransformerNUFFT`
   (nufftax), or `TransformerDFT` where JAX is unavailable.
3. All three library PRs **must merge together** — the downstream re-exports
   break at import the moment PyAutoArray's removal lands alone.
4. Closes the separate bug draft
   `draft/bug/autoarray/pynufft_scipy_pinv2_dev_extra.md`: the
   `pynufft==2022.2.2` dev pin calls `scipy.linalg.pinv2`, absent from SciPy
   1.17.1 (confirmed 2026-08-22 — `hasattr(scipy.linalg, "pinv2")` is `False`).
   Retiring the backend was one of that prompt's three sanctioned remedies.

## Shipped 2026-08-22

Library tier merged: @PyAutoArray#475, @PyAutoGalaxy#583, @PyAutoLens#709 —
all green on CI, including each repo's `unittest-nojax` job, which is the
standing evidence that the no-JAX path survives without the pynufft fallback.
Merged galaxy -> lens -> array so main was never red (dropping a re-export is
safe against an autoarray that still has the class; the reverse is not).

Workspace tier raised: @autolens_workspace#497 (prose across `scripts/`,
`notebooks/`, `markdown/`) and @autolens_workspace_test#261 (the `nufft.py`
parity script rewritten around `TransformerDFT` as its sole reference; verified
by running it — all four tests pass, 3.0e-14 relative residual at 256x256).

`PyAutoHands/autohands/config/no_run.yaml` checked: no nufft entries, nothing
hidden there.

Two things found along the way that are NOT closed by this task:

1. ~~`use_adjoint_scaling` is now a no-op on both remaining transformers.~~
   **RESOLVED 2026-08-22 — @PyAutoArray#478.** Parameter and the
   `adjoint_scaling` attribute both removed from `TransformerDFT` and
   `TransformerNUFFT`, and from the sole caller
   `Interferometer.apply_sparse_operator`.

   The history, since it matters for anyone holding old results: `TransformerDFT`
   **never** applied the factor; `TransformerNUFFTPyNUFFT` did
   (`image *= self.adjoint_scaling`, a Kaiser-Bessel compensation — the only real
   user, deleted in #475); `TransformerNUFFT` applied it until **bd18a769
   (2026-05-22)**, which removed the multiplication because "the nufftax adjoint
   is already the mathematical adjoint and needs no extra scaling".

   Verified numerically before removing: `True` vs `False` was bit-identical
   (`0.000e+00`) on both classes, and nufftax matches the exact DFT at 1.562e-13
   relative — the same figure before and after. Applying the factor would have
   been a 4096x error on a 32x32 grid, not a correction.

   **Caveat worth raising with users:** anyone who used `TransformerNUFFT` with
   `use_adjoint_scaling=True` *before* 2026-05-22 has results that differ by
   `4 * N_y * N_x` from anything regenerated today. That discrepancy dates from
   bd18a769, not from #478.
2. ~~The `apply_sparse_operator` / `TransformerNUFFT` incompatibility is
   unverified.~~ **RESOLVED 2026-08-22 — there is no incompatibility.**
   @PyAutoArray#479, @autolens_workspace#498, @autolens_workspace_test#263.

   The `NotImplementedError` guard was removed for nufftax by @PyAutoArray#329
   (bd18a769, 2026-05-22); only the workspace comment stayed stale, for three
   months. Verified directly: `apply_sparse_operator` runs with
   `TransformerNUFFT` at every scale tried and its dirty image matches the
   `TransformerDFT` one to **~3e-13 relative**. Both paths are supported.

   What was genuinely undocumented is *which to choose*, and it is not the
   visibility count. The DFT setup costs `O(N_vis * N_pix)` against the NUFFT's
   `O((N_vis + N_pix) log N)` plus a fixed ~2s overhead, so the **product**
   decides. Seven CPU measurements agree on a crossover near `1e7`:
   ratio 0.21x / 0.27x / 0.70x at 1.3e6 / 2.6e6 / 5.2e6, then 1.16x / 1.50x /
   1.41x / 1.92x at 1.0e7 / 2.1e7 / 2.3e7 / 8.3e7. At a 64x64 mask that is
   ~5,000 visibilities; on a 32x32 mask the DFT still wins at 4,000.

   Memory is the decisive axis: the DFT allocates with the same product
   (60 -> 239 -> 293 -> 446 MB as the grid grows at fixed N_vis=4000) while the
   NUFFT allocates nothing measurable. At 10.7 bytes/element that is ~109 GB at
   1M visibilities, independently corroborating the ~123 GB bd18a769 recorded
   by a different route — so past ~1e8 the NUFFT is the only feasible path.

   Guidance added as an INFO on the existing setup log, fired only for a
   NUFFT-backed transformer below the crossover. Deliberately **not** a
   construction-time warning: `Interferometer` defaults to `TransformerNUFFT`,
   so that would fire on every small dataset in every tutorial and test. The
   dangerous direction is already a hard `DatasetException` above 10,000
   visibilities with an opt-out.
