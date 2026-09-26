## interferometer-mge-breakdown
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/308
- completed: 2026-09-26
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/312
- summary: Interferometer likelihood campaign 1/3. Adds an interferometer MGE breakdown cell to the shared harness (library path + chunked-transform arm + W~ arm), with JAX CPU runs for sma/alma/alma_high (+ DFT) and RAL A100 fp64 runs for sma/alma/alma_high/jvla (+ mp for alma_high/jvla), all on nufftax 0.6.1. The note `results/notes/interferometer_mge_breakdown_2026_09.md` ranks the levers: (1) W~ route for MGE-only fits, 356-1746x on A100; (2) chunked transform, since the library path OOMs the A100 at alma and up (65.9 GB / 322 GB / 1.61 TB); (3) complex128 scatter costs a fixed ~0.85 s on GPU, and float64-then-cast is ~6000x faster; (4) the GPU is slower at sma (0.1x) and 44x/55x faster at alma/alma_high; (5) mixed precision gives no gain.
- follow-ups: filed in Mind commit 28ff960e. Lever 1 is now in flight as `interferometer-mge-w-tilde-route` (PyAutoArray#575; PRs PyAutoArray#576, PyAutoGalaxy#629, PyAutoLens#750). The rest stay as drafts: interferometer_chunked_transform_mapping_matrix, interferometer_transform_mapping_matrix_real_scatter, ral_venv_dependency_floor_drift, workspace_interferometer_mge_sparse_operator_memory_docs.
- heart: human acknowledged YELLOW at ship (2026-09-26, unrelated reasons).
- trap: nufftax 0.4.0 in the shared RAL venv sent x64 GPU NUFFTs to fp32 Pallas (0.25 nats off). Those runs were thrown away and redone on nufftax 0.6.1 after the human upgraded the venv; final round r3 was jobs 351078-351083.
- trap: a stale local autolens_workspace_test dataset/interferometer/simple turned up later. Regenerate it before local interferometer timing.
- ral-worktree: /mnt/ral/jnightin/autolens_profiling_wt/interferometer-mge-breakdown still exists on RAL (remote, not cleaned by this close-out).

## Original prompt

# Interferometer likelihood campaign 1/3: MGE breakdown on JAX CPU and A100 GPU, optimisation task list

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- mge
- likelihood-profiling
- jax-gpu
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: `results/breakdown/interferometer/mge_hpc_a100_fp64.json` exists with non-null `steps` and `results/notes/interferometer_mge_breakdown_2026_09.md` ranks the levers with per-instrument dense-vs-W~ numbers.
Review-minutes: 6
Unattended: ready
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-25
Issued: 2026-09-25

Mirror of the CCD imaging MGE breakdown (`scripts/imaging/likelihood_breakdown/mge.py`,
`results/breakdown/imaging/mge_*`) for the interferometer MGE likelihood, on JAX CPU
(laptop, 1 thread pinned) and the RAL A100 (`hpc/batch_gpu/submit_breakdown_*`).

## What

- Write `scripts/interferometer/likelihood_breakdown/mge.py` on the shared harness
  (`_profile_cli.py`, `scripts/misc/likelihood_breakdown/timing.py`, `jit_profile`,
  `call_accounting`). No interferometer MGE breakdown cell exists; only the runtime cell
  `likelihood_runtime/mge.py` (full-JIT + vmap).
- Model: mass fixed at truth (Isothermal + shear), source = 20 linear Gaussians via
  `al.model_util.mge_model_from` (same MGE-20 as imaging); no lens light (record why in
  the note). Steps, in library order: ray-tracing, per-Gaussian image evaluation
  (`LightProfileLinearObjFuncList.mapping_matrix`), batched `transform_mapping_matrix`
  (NUFFT of n_gauss columns, `transformer.py:505-550`), data vector D, curvature F
  (`A.T @ A` on real/imag, O(N_vis * n^2)), PDIP NNLS solve, log-det terms,
  `fast_chi_squared`. Record the same JSON schema as imaging (`steps`, `jit_phases`,
  `setup_split`, `vmap_batch`) into `results/breakdown/interferometer/mge_*`.
- Instruments: sma (190 vis, DFT and NUFFT arms), alma (1M), alma_high (5M, chunked
  NUFFT); jvla (25M) on the A100 only if the gather buffer fits with `chunk_size`.
  The VRAM note (`scripts/misc/vram/config.py`) marks MGE at alma+ "inherently blocked"
  by the 62.7 GB gather buffer from #56, measured before `TransformerNUFFT(chunk_size=)`
  existed; re-test with the chunked transformer and update or confirm the block.
- fp64 on every leg; add an mp arm on the A100 only (imaging precedent: mp helped only
  at jvla).
- Regenerate the README dashboards (`build_readme.py --check` is a CI gate).

## Then: optimisation task list

From the breakdown, write `results/notes/interferometer_mge_breakdown_2026_09.md` with
a ranked lever list, each with the step it attacks, the structural bound, and the
predicted gain. Candidates to evaluate explicitly (do not implement here; file each
worthwhile one as its own prompt):

1. **Route MGE-only fits through the sparse operator.** `factory.py:202-208` sets
   `use_sparse_operator=False` when every linear object is a func-list, so an MGE-only
   fit always pays the O(N_vis * n^2) dense NUFFT path even after
   `apply_sparse_operator()`. The W~ func-list blocks already exist
   (`operated_matrix_slim_from`, `curvature_matrix_func_list_from`,
   `inversion_interferometer_util.py:1466,1628`). Measure what a W~ MGE-only evaluation
   would cost (O(n * M log M), N_vis-independent) against the dense path at each
   instrument; this is the lever that would make MGE usable at alma+ on any device.
2. NUFFT-per-Gaussian vs one batched call; `eps` (1e-12 default) sensitivity on
   log-evidence.
3. GPU vs CPU for the NUFFT itself (May runtime: A100 MGE 711 ms vs CPU 231 ms at sma).
4. Shared eccentric-radius evaluation on the JAX path (NumPy already shares it,
   `linear/abstract.py:397-470`).
5. Certified active-set solver excluded for MGE (`abstract.py:580-583`); whether PDIP is
   the right solver at n=20.

Also fix the doc/code mismatch in
`autolens_workspace/scripts/interferometer/features/multi_gaussian_expansion/modeling.py:322-324`
(claims MGE memory depends on the mask alone with `apply_sparse_operator()`; the code
takes the dense path) — file it as a workspace docs prompt, do not edit it here.

## Done when

- Committed `results/breakdown/interferometer/mge_breakdown_{sma,alma[,alma_high]}_v<release>.{json,png}`
  (CPU) and `mge_hpc_a100_fp64[_mp].json` (A100), README dashboards regenerated,
  lint green.
- The note carries the ranked lever list, the CPU-vs-GPU MGE verdict per instrument, and
  filed follow-up prompts for every lever worth pursuing.
- The alma+ VRAM block for MGE is re-tested and the VRAM config comment updated.

Consequence: glance
Witness: `results/breakdown/interferometer/mge_hpc_a100_fp64.json` exists with non-null `steps` and `results/notes/interferometer_mge_breakdown_2026_09.md` ranks the levers with per-instrument dense-vs-W~ numbers.
Review-minutes: 6

<!-- formalised by the Intake (Conception) Agent on 2026-09-25 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ab334050-3e04-48cf-8914-a1e38ba0a9e5/scratchpad/prompts/interferometer_mge_breakdown_jax_cpu_gpu.md -->
