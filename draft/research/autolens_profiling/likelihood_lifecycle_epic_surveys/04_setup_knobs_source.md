# Survey 04 — Compute-setup knobs in PyAutoLens: what an "auto / optimal setup" factory must replace (2026-10-21, Explore worker, read-only)

Nothing in the stack picks the compute setup from the hardware today. JAX on/off, sparse operator on/off and its type, core count, and fp32/fp64 are each set by hand, and science projects reach for argparse `--use_cpu` switches. A few narrow automatic choices do exist; they are listed in §1 and §3.

**Stale fact.** The note that "`apply_over_sampling` drops the sparse operator" is out of date. PyAutoArray `db94e80a` (2026-09-27, in tags 2026.10.11.1 and later) made it carry the operator over: `array/PyAutoArray/autoarray/dataset/imaging/dataset.py:594-596,620`. Several workspace and science scripts still describe the old behaviour (§4, §5).

---

## 1. Library knobs

| Knob | Where set / read (file:line) | Default | Automatic choice today? |
|---|---|---|---|
| `use_jax` (base) | `fit/PyAutoFit/autofit/non_linear/analysis/analysis.py:88-118`. This is the only reader of `PYAUTO_DISABLE_JAX` on the Analysis path (`:94`). It falls back to numpy with a banner if jax is not installed (`:97-116`). Resolved value is exposed as `is_jax` (`:154-169`). | **False** (base `af.Analysis`) | Fallback only: env var or jax missing → False. No GPU check. |
| `use_jax` (lens) | `lens/PyAutoLens/autolens/analysis/analysis/lens.py:42,64-73` (re-checks jax installed). Also `analysis/analysis/dataset.py:50,92-104`, `imaging/model/analysis.py:53`, `interferometer/model/analysis.py:54`, `point/model/analysis.py:66` | **True** | Same fallback |
| `use_jax` (galaxy) | `galaxy/PyAutoGalaxy/autogalaxy/analysis/analysis/analysis.py:36`, `analysis/analysis/dataset.py:37`, `imaging/model/analysis.py:48`, `interferometer/model/analysis.py:274`, `ellipse/model/analysis.py:46` | True | — |
| `use_jax` (weak) | `lens/PyAutoLens/autolens/weak/model/analysis.py:37,54` | **False** ("conservative") | — |
| `use_jax` → `xp` | `af.Analysis._xp` (`analysis.py:171-174`) and `AnalysisLens._xp` (`lens.py:75-81`). Fits work it out backwards with `self.use_jax = xp is not np`: `autogalaxy/abstract_fit.py:36`, `autolens/interferometer/fit_interferometer.py:114`, `point/fit/abstract.py:92`, `galaxy/to_inversion.py:92` | — | — |
| `use_jax` on solvers | `PointSolver` (`autolens/point/solver/point_solver.py:76-92`). `ShapeSolver(use_jax=False)` rejects True (`shape_solver.py:46,584-634`) | False | — |
| Search JAX knobs | `use_jax_vmap` / `use_jax_jit` are **deprecated** (`autofit/non_linear/settings.py:19,47-63`, `fitness.py:203-320`, `search/runtime.py:128-140`). Nautilus batches iff `analysis.is_jax` (`search/nest/nautilus/search.py:442-452`) | None | **Yes**: batching follows `is_jax` |
| Imaging sparse operator (JAX) | `Imaging.apply_sparse_operator(batch_size=128)` at `array/PyAutoArray/autoarray/dataset/imaging/dataset.py:625-696` → `ImagingSparseOperator`. Deliberately ignores `PYAUTO_DISABLE_JAX` (`:654-664`) | not applied | No |
| Imaging sparse operator (numba CPU) | `Imaging.apply_sparse_operator_cpu()` at `dataset.py:698-769` → `SparseLinAlgImagingNumba`. Needs numba (`:722-731`). Both builders refuse `psf.convolve_over_sample_size > 1` (`:667-670`, `:717-720`) | not applied | No |
| Operator dropped by mask/noise change | `_warn_sparse_operator_discarded` at `dataset.py:71-91`, fired by `apply_mask` (`:472`) and `apply_noise_scaling` (`:557`) | — | Warns only |
| `apply_over_sampling` | `dataset.py:579-623`. **Now keeps** `sparse_operator` (`:620`) | — | — |
| Imaging inversion routing | `inversion_imaging_from` in `autoarray/inversion/inversion/factory.py:95-169` | — | **Yes, dataset-based:** sparse is off if every linear object is a func-list, e.g. MGE-only (`:138-144`). The operator **type** decides numba vs JAX sparse (`:148-162`). There is **no check that the operator matches `xp`**. |
| Interferometer sparse operator | `Interferometer.apply_sparse_operator(method="nufft", use_jax=False, eps, nufft_chunk_size, batch_size, chunk_k, pool_noise_map...)` at `dataset/interferometer/dataset.py:529-660`. `PYAUTO_DISABLE_JAX` forces `use_jax=False` (`:598-608,659`). Also `apply_sparse_operator_from_chunks` (`:791`, `:911`) | not applied | No |
| Interferometer inversion routing | `inversion_interferometer_from` at `factory.py:182-268`. Numba `direct_conv` vs FFT decided by `_use_interferometer_numba` (`:271-416`) | cost model | **Yes, a cost model:** predicts both routes' time from source pixels, mapping non-zeros and extent (`:379-409`). It is single-thread calibrated. |
| `Settings.interferometer_route` | `autoarray/settings.py:449`; config `general.yaml inversion.interferometer_route: null` | None | Force `"fft"` / `"numba"` |
| `Settings.interferometer_numba_nnz_per_source_max` | `settings.py:405`; config null. 0 is a kill switch | None → cost model | — |
| `Settings.interferometer_direct_conv_symmetric_max_work_fraction` | `settings.py:~470`; config 0.7 | 0.7 | Picks the symmetric kernel when serial |
| Transformer class | `Interferometer(transformer_class=TransformerNUFFT)` (`dataset/interferometer/dataset.py:56`, `from_fits` `:223`, `:404`). Simulator default is **`TransformerDFT`** (`dataset/interferometer/simulator.py:70`). Classes are in `operators/transformer.py:166` (DFT) and `:316` (NUFFT: `eps=1e-12`, `chunk_size=None`, needs nufftax) | NUFFT (dataset), DFT (simulator) | **Guard only:** raises if DFT and more than 10,000 visibilities (`dataset.py:197-211`, `raise_error_dft_visibilities_limit`). No automatic choice. |
| `use_mixed_precision` | `Settings(use_mixed_precision=False)` (`settings.py:13,40-105,269`). Only JAX paths honour it: `convolver.py:644-687`, `mapper_util.py:504` | False | No. The docstring says "most beneficial for GPU" but nothing checks for one. |
| `use_positive_only_solver` | `settings.py:308-313` → config `inversion.use_positive_only_solver: true` | True (config) | — |
| JAX positive-only solver | `positive_only_solver` (`settings.py:524-540`): `pdip` or `certified`. NumPy always uses fnnls. Also `nnls_solver_tol`, `nnls_max_iter`, `certified_*`, `nnls_preconditioning_no_mapper` | `pdip` | Partial: `certified` applies only to mapper-only JAX inversions |
| `nnls_warm_start_memo` | `settings.py:349-365`; config true; env `AUTOARRAY_NNLS_WARM_START=0` | True | NumPy only |
| `use_edge_zeroed_pixels` (the old `force_edge_pixels_to_zeros`) | `settings.py:315-331`; config true. Only has an effect with the positive-only solver | True | — |
| `use_border_relocator` | `settings.py:333-338`; PyAutoArray config **false**, autolens_workspace config **true** (`config/general.yaml:19`) | differs by layer | — |
| `log_det_method`, `regularization_term_method` | `settings.py` ~391/398; config `cholesky` / `matmul` | — | — |
| Preloads | `autoarray/preloads/{abstract,imaging,interferometer}.py`. Built by `AnalysisImaging(shared_preloads=False)` → `shared_state_from` (`autolens/imaging/model/analysis.py:54,147-185`) | off | No |
| Legacy names | `SettingsInversion`, `use_w_tilde`, `force_edge_pixels_to_zeros`, `SettingsInterferometer`: **none appear in source any more** (grep is empty). They are replaced by `aa.Settings` plus a dataset `sparse_operator`. | — | — |
| `number_of_cores` | `SettingsSearch(number_of_cores=1)` (`autofit/non_linear/settings.py:16,61`) and `NonLinearSearch(number_of_cores=1)` (`search/abstract_search.py:95,165`) | 1 | **JAX fork rule:** forced to 1 when `is_jax` (`parallel/pool.py:35-39,60-90`, applied in `PoolFactory` `:151-158`). EP factor searches refuse more than 1 (`pool.py:93-130`). No `cpu_count()` anywhere in the libraries. |
| Thread pinning check | `warn_if_threads_unpinned` (`search/runtime.py:89-125`): warns when cores > 1 and any of OPENBLAS/MKL/OMP/VECLIB/NUMEXPR is not 1. Config `parallel.warn_environment_variables` | warn | Warns only |
| numba config | `general.yaml numba: {use_numba, cache, nopython, parallel: false}`, read at import in `autoarray/numba_util.py:10-17`, and in `interferometer_numba/sparse.py:305-315`, `mappers/mapper_util.py:134-146`, `mesh/interpolator/sibson.py:584` | parallel false | — |
| test_mode | `autonerves/test_mode.py`: `PYAUTO_TEST_MODE` 0–3, plus skip_* and `disable_jax()` (`:256-271`) | 0 | — |
| `xp` dispatch | There is **no** `numpy_wrapper` / `xp` module in PyAutoArray. `xp` is an argument threaded through every call (design doc: `array/PyAutoArray/docs/agents/jax_and_decorators.md`). `autonerves/jax_wrapper.py` only sets environment and registers pytrees, and is the first import of every library: `autofit/__init__.py:1`, `autoarray/__init__.py:1`, `autogalaxy/__init__.py:1`, `autolens/__init__.py:1` | — | — |

**Other automatic choices that already exist:**
- **Sibson cavity unroll:** decided from `jax.default_backend() != "cpu"` (`sibson.py:136-157`). This is the only real backend-detecting choice in the likelihood path.
- **MultiStartGradient memory probes:** skipped when `jax.default_backend()=="cpu"` (`search/mle/multi_start_gradient/search.py:923`).

## 2. Environment variables and config keys

| Var / key | Where read or set | Effect |
|---|---|---|
| `PYAUTO_DISABLE_JAX=1` | `autofit/.../analysis/analysis.py:94`; `graphical/declarative/factor/hierarchical.py:86`; `autonerves/test_mode.py:256-271`; `autoarray/dataset/interferometer/dataset.py:13-25,480,659,911`; `inversion_interferometer_util.py:19-28` | Forces numpy and turns off the JAX NUFFT builder. **Not** honoured by `Imaging.apply_sparse_operator` (deliberate) |
| `XLA_FLAGS` | `autonerves/jax_wrapper.py:23-83`. Appends `--xla_disable_hlo_passes=constant_folding`, `--xla_gpu_autotune_level=0`, `--xla_gpu_enable_triton_gemm=false`. Same idea in `setup_colab.py:27,297` | Compile-time / GPU GEMM tuning. Set at import. |
| `JAX_ENABLE_X64` | `jax_wrapper.py:88-106`: forced to True unless already true | fp64 everywhere. Mixed precision is per-op through `Settings` |
| `JAX_COMPILATION_CACHE_DIR`, `JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS` | `jax_wrapper.py:109-134` (default `~/.cache/pyauto_jax`) | Persistent compile cache |
| `JAX_PLATFORMS` | Library: only `autofit/mcp/__main__.py:19` (setdefault cpu). Workspace: `guides/hpc/batch_cpu/submit:29-30` (+`JAX_PLATFORM_NAME`); euclid_dr1 `hpc/batch_cpu/*`; cowls_ansofi `scripts/slam.py:141-143` | Keeps JAX off the GPU. **jax_wrapper does not touch it.** |
| `OPENBLAS/MKL/OMP/VECLIB/NUMEXPR_NUM_THREADS` | Read by `search/runtime.py:89-105`. Set in `guides/hpc/batch_cpu/submit:35-41` (= SLURM cpus) and euclid two-stage submit (full count for vis_lp, **1** for vis_pix) | Avoids oversubscribing threads |
| `NUMBA_NUM_THREADS` | Not read or set anywhere. Only mentioned in a docstring at `interferometer_numba/inversion_interferometer_numba_util.py:291` | — |
| `AUTOARRAY_NNLS_WARM_START=0` | `inversion/inversion/nnls_memo.py:112` | Kill switch for the NNLS memo |
| `AUTOARRAY_NUMBA_OPERATED_MEMO=0` | `imaging_numba/sparse.py:126` | Disables the operated-matrix memo |
| `AUTOGALAXY_DEFLECTIONS_MEMO`, `_MAX_MB` | `autogalaxy/profiles/mass/abstract/deflections_memo.py:158,170` | Deflection memo |
| `PYAUTO_SIBSON_QUERY_CHUNK`, `PYAUTO_SIBSON_UNROLL_CANDIDATES` | `sibson.py:110-112,140-157` | Override GPU chunk size / unroll |
| `PYAUTO_TEST_MODE`, `_SAMPLES`, `PYAUTO_SKIP_FIT_OUTPUT`/`_VISUALIZATION`/`_CHECKS`/`_LATENTS` | `autonerves/test_mode.py:5-80` | Smoke / CI behaviour |
| `PYAUTO_SMALL_DATASETS` | `autoarray/util/dataset_util.py:85,140,642,683`, `mask_2d.py:371`, `uniform_2d.py:228,570`, `over_sample_util.py:509`, `autogalaxy/analysis/model_util.py:171`, `autolens/point/...` | Caps data size |
| `PYAUTO_FAST_PLOTS`, `PYAUTO_OUTPUT_MODE` | `autoarray/plot/utils.py:15,390`, `plot/output.py:196,225`, `autogalaxy/util/plot_utils.py:469,520` | Plotting |
| `PYAUTOFIT_JAX_COMPILE_HEARTBEAT_SECS` / `_DUMP_SECS`, `CI`, `BUILD_SCRIPT_TIMEOUT` | `autofit/non_linear/jax_compile.py:31-84` | Compile diagnostics |
| `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK` | `autonerves/workspace.py:13,242` | Version handshake bypass |
| `USE_JAX` | Not present anywhere | — |
| Smoke / release profiles | `autolens_workspace/config/build/profile_smoke.yaml:11-21` (`PYAUTO_DISABLE_JAX=1`, `JAX_ENABLE_X64=True`, `NUMBA_CACHE_DIR`); `profile_release.yaml:28-36` (`PYAUTO_DISABLE_JAX=0`) | — |
| Config `inversion:*` | `autoarray/config/general.yaml` (all keys in §1); workspace overrides in `config/general.yaml:14-20` | — |
| Config `numba:*` | `autoarray/config/general.yaml numba:`; workspace `config/general.yaml:28-32` | — |
| Config `parallel.warn_environment_variables`, `test.*`, `hpc.hpc_mode` | `runtime.py:108`, `fitness.py:58,75,166,1146`, `paths/abstract.py:203`, `autoarray/plot/__init__.py:10` | — |
| Config `jax:` | **No such section in any library or workspace config** | — |

## 3. PyAutoNerves (`organs/PyAutoNerves`)

What it already owns:
- **Its role:** "the configuration/serialization layer connecting workspace conventions to libraries (layered config, version handshake, test_mode), delivered as the `autonerves` package" (AGENTS.md organism table). AGENTS.md also says it provides "the shared `jax_wrapper` / `test_mode` utilities".
- **Downstream rules point here:** PyAutoFit and PyAutoArray AGENTS.md both say "autofit [autoarray] depends on **autonerves** only… Shared utilities (e.g. `test_mode`, `jax_wrapper`) belong in autonerves."
- **Layered config:** `conf.py`. Resolution order is "workspace → last-imported library → … → PyAutoFit (`Config.push(keep_first=True)`, keys lowercased)" (README, Nerves board section).
- **Version handshake:** `workspace.py` (`check_version`, `version.minimum_library_version`, `workspace_version_check`, `_BYPASS_ENV_VAR = "PYAUTO_SKIP_WORKSPACE_VERSION_CHECK"` at `:13`). Python version check is in `__init__.py:15-40`.
- **test_mode:** `test_mode.py` (levels 0–3, skip_* flags, `disable_jax()` at `:256-271`).
- **JAX environment setup:** `jax_wrapper.py` (§2) runs at import, before jax is imported by any library. This is the only point where `JAX_PLATFORMS` could reliably be set.
- **Board:** `scripts/board.py:144` scans `PYAUTO_*` env vars for the Nerves board.

Hardware / environment detection:
- **GPU:** only `setup_colab.check_jax_using_gpu()` (`setup_colab.py:135-174`). It loops over `jax.devices()`, prints GPU/TPU/CPU, and logs "JAX did not detect a GPU or TPU device… recommended to reinstall JAX with GPU support". It is Colab-only and not called from library code.
- **JAX importable:** `importlib.util.find_spec("jax")` warning at `jax_wrapper.py:8-21`.
- **Numba importable:** checked ad hoc in each library (`factory.py:411-414`, `imaging/dataset.py:722-731`).
- **Core count:** nothing reads `os.cpu_count` / `sched_getaffinity` / `SLURM_CPUS_PER_TASK` in any library. The SLURM read exists only in a workspace script (`guides/hpc/example_cpu_and_gpu.py:256`).
- **Is it the natural home?** Yes, by the import-direction rule. A detector must sit below autofit and autoarray, and env vars such as `JAX_PLATFORMS` and `XLA_FLAGS` must be set before jax imports, which `jax_wrapper` already does. Choices that depend on the dataset (imaging vs interferometer, pixelization vs MGE, number of visibilities) cannot live there. They belong in PyAutoArray (dataset/factory) or PyAutoLens (Analysis).
- **Related organ:** PyAutoDNA's row says "Nerves enforces runtime compatibility". DNA owns environment inventory receipts, but only as offline collection.

## 4. Workspace examples (`lens/autolens_workspace/scripts`)

**`imaging/start_here.py`**
- `:296-305`: "`AnalysisImaging` defaults to `use_jax=True` when JAX is installed (set explicitly below for clarity). The search driver wraps the likelihood in `jax.vmap(jax.jit(...))` internally… Watch for `JAX: Applying vmap and jit to likelihood function -- may take a few seconds.` in the log… Force NumPy with `use_jax=False` (or `PYAUTO_DISABLE_JAX=1`) when debugging."
- `:344`: `use_jax=True,  # JAX will use GPUs for acceleration if available, else JAX will use multithreaded CPUs.`
- **Stale:** the "JAX: Applying vmap and jit…" string no longer exists in library source. It is also cited at `guides/using_jax.py:34`. The current message is `jax_compile.py:310`: "JAX jit compiling {description}, could take seconds or minutes...".

**`imaging/features/pixelization/cpu_fast_modeling.py`** — the steps a user does by hand:
1. Check numba is installed, with an `input()` prompt (`:31-58`).
2. `dataset.apply_over_sampling(...)` (`:133`), **then** `dataset.apply_sparse_operator_cpu()` (`:161`).
3. `af.Nautilus(..., number_of_cores=2)` (`:249-254`).
4. `AnalysisImaging(..., use_jax=False)` (`:258-262`).
5. SLaM: `SettingsSearch(number_of_cores=2)` (`:569-574`) and `use_jax=False` on every analysis (`:551,604,668,690,707`).
6. After the pixelization re-sample: `apply_over_sampling` → `apply_sparse_operator_cpu()` again (`:658-663`). The comment at `:642-645` ("belongs to the `Imaging` it was built from, so it is rebuilt after the re-sample") is **stale**: harmless now, but a wasted rebuild.

The text also makes claims that are not quite current:
- `:10-16` says CPU many-core can "outperform JAX GPU" for pixelizations, and that JAX is better for parametric sources.
- `:150` says "The current implementation does **not support JAX**", but `Imaging.apply_sparse_operator()` is now the JAX implementation (`dataset.py:654-660`).

**`multi_galaxy/features/pixelization/cpu_fast_modeling.py`:** same pattern, without the re-sample step: `apply_over_sampling` (`:136-144`) → `apply_sparse_operator_cpu()` (`:158`), `number_of_cores=2` (`:302`), `use_jax=False` (`:311`). `group/features/pixelization/cpu_fast_modeling.py` also exists.

**SLaM:**
- `guides/modeling/slam_start_here.py` uses `use_jax=True` on every analysis (`:159,350`). `SettingsSearch` has no `number_of_cores` (`:615-620`).
- There is no `slam_pipeline/` package in the workspace.
- `guides/hpc/example_cpu_and_gpu.py:256` sets `number_of_cores = int(os.environ.get("SLURM_CPUS_PER_TASK", 1))` **but** `:324` uses `use_jax=True`. The fork rule (`pool.py:82-86`) therefore cuts it to 1 core with only an INFO line. This is a contradiction in the example.
- The assistant skill `al_configure_search.md:84-123` documents the split rule: parametric → JAX, no cores; pixelised CPU → `apply_sparse_operator_cpu()` + `use_jax=False` + cores; GPU → JAX throughout, no sparse operator; build two `SettingsSearch` objects for SLaM.

**Interferometer:**
- Every modelling example uses `transformer_class=al.TransformerNUFFT`: `modeling.py:136`, `start_here.py:204,484`, `features/pixelization/modeling.py:208`.
- Pixelization uses the sparse operator **with JAX**: `dataset.apply_sparse_operator(use_jax=True, show_progress=True)` (`features/pixelization/modeling.py:238`), analysis `use_jax=True` (`:414`). Datacube does the same (`features/datacube/modeling.py`, `delaunay.py`).
- So the rule differs by dataset: an imaging GPU fit gets **no** sparse operator, an interferometer GPU fit **does**.
- Visibility-count text exists at `start_here.py:153-171`: "Which is faster is set by the product `N_vis x N_pix`… Below `N_vis x N_pix ~ 1e7` the DFT wins; above it the NUFFT does. At a typical 64x64 mask that crossover is near 5,000 visibilities… Past `~1e8`… the DFT's allocation reaches ~109 GB at a million visibilities… more than 10,000 visibilities and `TransformerDFT` raises an error."
- `features/pixelization/modeling.py:428-447` says sparse-mode "VRAM… [and] run times… independent of the number of visibilities".
- **Stale:** `start_here.py:35-36` says "`TransformerDFT` (the default in this script)", but the script uses NUFFT.

## 5. Science-project `--use_cpu` switches

`euclid_dr1` and `cowls_ansofi` are not under `lens/`. They are at `/mnt/c/Users/Jammy/Science/active/{euclid_dr1,cowls_ansofi}`. `euclid_dr1` is a clone of `lens/euclid_strong_lens_modeling_pipeline` (`organs/PyAutoCortex/projects.yaml:118-130`).

**`cowls_ansofi/scripts/slam.py`**: environment is set before autolens is imported.
```python
USE_CPU = "--use_cpu" in sys.argv[1:]
os.environ["JAX_ENABLE_X64"] = "True"
if USE_CPU:
    os.environ["PYAUTO_DISABLE_JAX"] = "1"
    os.environ.setdefault("JAX_PLATFORMS", "cpu")
...
    dataset = dataset.apply_over_sampling(over_sample_size_lp=over_sample_size)
    if use_cpu:
        dataset = dataset.apply_sparse_operator_cpu()          # :278-279
settings_search = af.SettingsSearch(..., number_of_cores=number_of_cores)   # :716-722
settings = al.Settings(use_mixed_precision=False, nnls_warm_start_memo=False) # :726
analysis = al.AnalysisImaging(dataset=dataset, use_jax=not use_cpu, ...)    # :413,468,532,589,658
if use_cpu: dataset = dataset.apply_sparse_operator_cpu()      # :752 after re-sample
```
- The env block is at `:139-143`.
- Docs at `:101-115` and `:740` still say `apply_over_sampling` "drops the operator" (stale).
- `:111-112` warns that `apply_sparse_operator()` "silently makes a leg that is neither". That is the missing backend/operator consistency check from §1.

**`euclid_dr1`**:
- argparse at `util.py:1705-1716`: `--number_of_cores` (default 1) and `--use_cpu` ("CPU mode: disables JAX and applies the sparse operator for vis_pix").
- In `scripts/initial_lens_model.py`: `use_jax=not use_cpu` (`:361`, `:671`); `if use_cpu: dataset = dataset.apply_sparse_operator_cpu()` after `apply_over_sampling` (`:629-634`). Docs at `:475-484` give the old drop reasoning ("~5x slower per evaluation" if applied first), now stale.
- It runs as two processes (`hpc/batch_cpu/submit_initial_lens_model_two_stage:134-169`):
  - Stage 1: `env JAX_PLATFORMS=cpu OMP/MKL/OPENBLAS_NUM_THREADS=$THREADS ... --stage=vis_lp`. This is JAX on CPU, no `--use_cpu`.
  - Stage 2: `env *_NUM_THREADS=1 ... --stage=vis_pix --use_cpu --number_of_cores=$THREADS`.
- An open Mind draft is about merging the two stages: `organs/PyAutoMind/draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md`.

## 6. Existing "auto / optimal / recommended" setup

- `grep -rn "optimal|recommended setup|auto_setup|choose.*backend|hardware" lens/PyAutoLens/autolens` finds only two unrelated hits in `potential_correction/iterative.py:388,427` ("near-optimal un-gauged start").
- No setup factory exists in any of the five libraries.
- No Mind prompt matched "auto setup" / "compute setup".
- Assistant skills (`lens/autolens_assistant/skills`) that mention sparse / numba / use_jax, titles only: `init-slam`, `al_greeting_cosmos_web_ring`, `al_potential_correction`, `al_audit_skill_apis`, `al_build_interferometer_model`, `al_run_search`, `al_refresh_api_docs`, `_bootstrap_skill`, `al_setup_environment`, `al_debug_fit_failure`, `al_inspect_results_mcp`, `al_configure_search` (holds the decision table, `:84-123`), `feedback`.

## 7. What the CLI prints at run start

`log_fit_start` (`fit/PyAutoFit/autofit/non_linear/search/runtime.py:242-262`) is called from `abstract_search.py:295`. This is the only announcement of the setup:
```python
if analysis.is_jax:
    device = jax.devices()[0]; backend = device.platform.upper()
    logger.info(f"Starting non-linear search with JAX ({backend}: {device_name}).")
else:
    logger.info(f"Starting non-linear search with {search.number_of_cores} cores.")
```

Other messages:
- **Core downgrade:** `pool.py:82-86` logs "`{where}: number_of_cores={requested} requested, running with 1 core. {JAX_FORK_REASON}.`". `search.summary` gets "Number of cores = N (requested M)" (`pool.py:166-172`).
- **JIT:** `jax_compile.py:310` "JAX jit compiling {description}, could take seconds or minutes...", then "still compiling" heartbeats and "compiled … in" (`:141,150,331,349`).
- **Import time:** `jax_wrapper.py` logs the JAX-not-installed WARNING and INFO lines about XLA_FLAGS, X64 and the compile cache.
- **Datasets:** `Imaging.apply_sparse_operator` logs "IMAGING - Setting Up Sparse Operator For low Memory Pixelizations." (`imaging/dataset.py:672-674`); interferometer logs "INTERFEROMETER - Finished W-Tilde (JAX) in %.3f seconds" (`inversion_interferometer_util.py:1172`).
- **Not printed:** nothing in PyAutoLens/PyAutoGalaxy Analysis `__init__` (`autolens/imaging/model/analysis.py:44-83`, `autogalaxy/analysis/analysis/dataset.py:30-74`) reports the choice. No log says whether a sparse operator is attached or which type, which inversion class the factory picked, numba vs FFT routing, mixed precision, or transformer class.

---

### Gaps a factory would need to close
1. `use_jax` defaults differ by layer: base `af.Analysis` False; lens / galaxy / interferometer / point True; weak False.
2. Nothing checks that the sparse operator matches the backend (`factory.py:146-162`).
3. The imaging and interferometer sparse-operator rules are opposite on GPU.
4. Core count, GPU presence and `JAX_PLATFORMS` are left to batch scripts.
5. Mixed precision is never chosen automatically.
6. Several docs (workspace `cpu_fast_modeling.py:642-663`, `start_here.py:299`, interferometer `start_here.py:35-36`, cowls/euclid docstrings) describe behaviour that has changed.
