# interferometer-decision-matrix

- Repo: autolens_profiling (workspace-only)
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/356 (closed by the PR, then given a Shipped comment)
- PR: https://github.com/PyAutoLabs/autolens_profiling/pull/358 (MERGED, merge commit `227b5c91`, head `3884df05`, 2026-09-30; `lint` green, the only check)
- completed: 2026-09-30
- Epic: interferometer-likelihood-campaign, phase 4 (the epic deliverable) of the campaign map, now at `complete/archive/epics/interferometer_likelihood_campaign.md`
- Heart: RED development override, authorized by the live human on 2026-09-30 (~21:00 BST, "i authoroize.") for push and PR-open. The reasons at the gate were: release validation FAILED (stage integrate); workspace validation timeout (autolens_test multi_dataset/rectangular.py); manifest drift ×2. None of them is in autolens_profiling. The merge came from a separate human /prm. Nothing was released.
- Scope merged: **13 of 14 new cells**. Pending: the CPU rect 39² cell at alma_high r5.0 (RAL job 375978_3, still RUNNING at merge; the note's row reads "pending"). It is re-filed as `draft/research/autolens_profiling/interferometer_decision_matrix_last_cell.md`.

## What shipped

- **sdp81 preset:** `instruments/interferometer.py` gains `sdp81`: real SDP.81 uv coverage from `instruments/uv_coverage/sdp81_uv_wavelengths.fits`, 108,384 vis, 0.05″, 800², r3.5, nufft. There is a simulator hook in `scripts/misc/simulators/interferometer.py`, and the simulated `dataset/interferometer/sdp81/` is tracked.
- **Cells:**
  - 7 of 8 RAL CPU radius-gap cells: sma and alma_high × r2.0 / r5.0 × Delaunay-1500 / rect 39², each with numba and NumPy FFT arms.
  - The sdp81 row on CPU and A100: Delaunay, rect, and MGE-20 dense + W~.
  - 26 new `results/breakdown/interferometer/**` JSON/PNG rows.
- **Note:** `results/notes/interferometer_likelihood_decision_matrix_2026_09.md` holds the matrix, the setup cost, verification, indicative time per fit, blocked cells and caveats. It gives five draft rules:
  1. On the W~ path, the per-call cost is set by the masked-pixel extent, not by N_vis. sdp81 costs the same as alma r3.5 on the A100: 53.7 vs 49.5 ms.
  2. Meshes on the A100 always use W~ sparse. Dense OOMs from 1e6 vis and is 17–21× slower at sdp81.
  3. Meshes on CPU should trust the library numba gate (60). It routed every measured cell to the faster arm.
  4. The A100 wins every mesh cell by 8–114×, and the margin grows with the mask. CPU is viable only up to about 1 s per call. Above ~20k masked pixels, use the A100.
  5. MGE should always use `apply_sparse_operator()` (W~) on both devices.
- **RAL partition rule** (human, 2026-09-30): CPU timing legs on the `gpu` partition are limited to ≤8 CPUs/task and an array throttle of ≤%2. It is enforced by `scripts/misc/wall/check_submits.py`, with tests, and documented in `hpc/README.md`. The existing `*_crossover_fp64` submits were moved to the %2 throttle.
- **Pointers:** `results/README.md`, the Phase-4 section of `wiki/campaigns/interferometer_likelihood.md`, the `wiki/index.md` row text, and regenerated READMEs and dashboard.
- **Verification:** numba vs FFT ≤ 7.5e-9 nat; step sum 0.96–1.03; CPU vs A100 ≤ 1e-3 nat on the new cells. The existing alma_high r3.5 rect cell misses at 1.5e-3, which the note records. The gated arm's `inversion_path` is `InversionInterferometerSparseNumba`.
- **Libraries:** a private RAL clone of the mains at `/mnt/ral/jnightin/PyAuto_branch/interferometer-decision-matrix`: Nerves 1ec1c82, Fit b13169e2, Array 7a89e19a, Galaxy 4c834ced, Lens efd13c4c. The shared mirror was behind and in use, so it was left alone.

## Left open

- The last cell, alma_high rect r5.0 CPU (375978_3). It is re-filed as `draft/research/autolens_profiling/interferometer_decision_matrix_last_cell.md`. That PR also flips the `wiki/index.md` interferometer row to shipped and cleans up the RAL worktree and the private library clone.

## Original prompt

# Interferometer likelihood campaign 3/3 — phase 4: the decision matrix (epic deliverable)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Epic: interferometer-likelihood-campaign
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/356
Issued: 2026-09-30
Witness: `results/notes/interferometer_likelihood_decision_matrix_2026_09.md` has a CPU-vs-A100 row for Delaunay-1500 at sma, alma and alma_high with mask radii 2.0/3.5/5.0, and the numba breakdown JSON's `configuration.inversion_path` reads `InversionInterferometerSparseNumba` for the gated arm.

Phase 4 of the campaign map `draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md` (retained in draft/ as campaign intent until this ships). Approved plan (2026-09-30, Plan Mode) below.

## Context
Campaign `interferometer-likelihood-campaign` — prompt
`PyAutoMind/draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md`.
Phases 1–3 shipped (#328, #333, #352). Phase 4 is the user-facing answer to "which interferometer
likelihood do I use on CPU vs GPU?" — a matrix note plus the few missing rows. Research work type,
single repo **autolens_profiling** (workspace flow: start_workspace → ship_workspace). No library edits.

Survey (main @ 3ad68af) — what exists vs the grid:
- Delaunay-1500 / rect 39²: A100 fp64 at sma / alma / alma_high × r2.0 / 3.5 / 5.0 **complete**; jvla (25M) A100 r3.5.
  CPU numba + NumPy FFT (RAL) complete at alma (r2.0/3.5/4.25/5.0/6.0); **sma and alma_high only at r3.5** → 8 cells missing.
- MGE-20: r3.5 only; A100 dense OOMs ≥ alma (61 GiB / 300 GiB / 1.46 TiB asked), W~ sparse 2.7 / 19.6 / 16.7 ms;
  CPU laptop-only, alma_high W~ OOM-killed in `apply_sparse_operator`.
- sdp81 (108,384 vis, `autolens_workspace/dataset/interferometer/sdp81/`): no preset.
- No interferometer Nautilus evaluation counts anywhere; imaging counts exist (Q1 vis_pix 73,215; SLaM HST Delaunay stage `likelihood_evals` in `autolens_inference/results/slam/imaging/hst/delaunay_1250/.../stages_seed0.json`).
- `results/README.md` note pointers are hand-written (Campaign findings paragraph, lines 7–16); `build_readme.py` only regenerates auto-table blocks.

## Plan (high level)
1. Add an **sdp81 preset** to `instruments/interferometer.py`, using the real sdp81 uv coverage on the alma grid, so that N_vis is the only thing that changes between the sdp81 and alma rows.
2. Fill the **8 missing CPU cells**: sma and alma_high × r2.0 / r5.0 × Delaunay and rect, with numba and NumPy FFT arms, on RAL CPU.
3. Run the **sdp81 row**: Delaunay, rect and MGE-20 at r3.5, on CPU and A100.
4. Write the **decision-matrix note** covering every cell. Each cell is either filled or marked blocked/not measured with the reason. The note ends with a short rule set and the indicative time-per-fit column.
5. Point to the note from `results/README.md` and the wiki campaign page, update the Mind campaign map, and retire the campaign prompt once this ships.

## Detailed plan
**Branch/worktree:** `feature/interferometer-decision-matrix`, `~/Code/PyAutoLabs-wt/interferometer-decision-matrix/autolens_profiling`.
**Parallel claim (needs your approval with this plan):** autolens_profiling is claimed by `raw-pdip-forward-polish`,
which is waiting for PyAutoArray#595 to merge before its ledger-row work. Its files are `results/notes/linear_solver_accuracy_2026_09.md`,
`wiki/campaigns/linear_solver_accuracy.md`, the `euclid_latent.py` leg, and README regeneration. This task touches the new note,
`instruments/interferometer.py`, new submit scripts and new JSONs, the interferometer campaign page, and one hand-written README paragraph.
The only overlap is `results/README.md`, and whichever task ships second resolves it with a trivial merge.

1. **sdp81 preset** (`instruments/interferometer.py`, key `sdp81`):
   - Settings: pixel_scale 0.05, real_space_shape (800, 800), mask_radius 3.5, n_visibilities 108,384, transformer nufft, one-shot.
   - The simulator uses the **real `uv_wavelengths.fits`**; the harness's simulated lens stays as it is, so the adapt image and truth come from the same path as every other preset. Timing does not depend on the data values. Log-evidence agreement is compared between paths on the same dataset.
   - Wire the uv-file load wherever the presets build their uv coverage. The implementer greps the simulator entry point in `scripts/misc/likelihood_breakdown/`.
   - The note labels the row "real sdp81 uv coverage, simulated source". Fitting the real sdp81 data is out of scope: it has no adapt image or mask.
2. **CPU gap cells:** new `hpc/batch_cpu/submit_breakdown_interferometer_{delaunay,pixelization}_numba_ral_radius_gaps_fp64`, an array copied from `*_crossover_fp64` with `INSTRUMENTS=(sma sma alma_high alma_high)` and `RADII=(2.0 5.0 2.0 5.0)`.
   - Run under the #235 discipline: `gpu` partition without `--gres`, NUMBA/BLAS = 1, memo off, iid stream, pinned log-evidence, step sum checked against the full call.
   - Outputs: `results/breakdown/interferometer/{sma,alma_high}/*_numba_hpc_ral_cpu_fp64_r{2.0,5.0}.json`.
3. **sdp81 jobs:**
   - CPU submits: numba Delaunay and rect.
   - A100 submits: Delaunay and rect (`*_a100_sdp81_fp64`), plus MGE-20 dense and W~ sparse (`mge_a100_sdp81_fp64[_sparse]`). At 1e5 vis, dense MGE should fit on the A100 (alma asked for 61 GiB at 1M).
   - If a job OOMs, the cell is recorded as blocked with the requested size.
   - This gives about 6 small jobs. They are driven with `hpc/sync push-submit`, then `pull`.
4. **Note** `results/notes/interferometer_likelihood_decision_matrix_2026_09.md`:
   - **Main table:** N_vis (190 sma / 1.08e5 sdp81 / 1M alma / 5M alma_high / 25M jvla) × mask r2.0 / 3.5 / 5.0 × source (MGE-20, Delaunay-1500, rect 39²) × device/path (CPU numba direct_conv, CPU NumPy FFT, CPU JAX, CPU dense, A100 W~ sparse, A100 dense).
   - **Per cell:** ms/eval, one-off setup in seconds (W~ preload / operator build, from the existing notes), peak host RSS, and log-evidence agreement against the 0.5-nat bar. Peak VRAM is marked "not recorded": `nvidia_smi` is a snapshot, not a peak.
   - **Blocked cells** carry the reason and a citation. Examples: MGE dense OOM ≥ alma; CPU alma_high MGE W~ OOM-kill; jvla CPU not run; MGE at r2.0 / 5.0 not measured.
   - **Caveats:** the r3.5 A100 column comes from the #324 rows on older library revisions, and the phase-1 alma N-sweep rows use the uncached library.
   - **Rule set:** about 5 rules, e.g. "sma-scale runs happily on CPU numba", "the A100 W~ sparse path wins 10–100× from alma up", "numba loses to FFT above nnz/col ≈ 66 / 72", "MGE ≥ 1M vis needs W~", and "mask extent, not N_vis, sets the per-eval cost".
   - **Time-per-fit column:** labelled indicative. It multiplies ms/eval by imaging Nautilus counts (Q1 vis_pix 73,215; SLaM HST Delaunay source_pix 51,420), with each source cited. The Q1 numbers are copied inline, because their file is in an untracked tmp folder.
5. **Pointers and state:**
   - Add one sentence plus a link in the `results/README.md` Campaign findings paragraph.
   - Add a Phase-4 section to `wiki/campaigns/interferometer_likelihood.md` and flip the `wiki/index.md` row to shipped once merged.
   - Run `build_readme.py` to regenerate the README tables, then `--check` so lint passes.
   - In Mind, update the campaign map; at ship, the prompt moves to `complete/` and the epic is retired.

**Execution:** delegated to one Opus subagent with a progress file and a Monitor, per the WORKFLOW.md delegation contract. I (Opus) judge the results and write or review the rule set.

## Verification
- Campaign witness: the note has CPU and A100 Delaunay-1500 rows at sma / alma / alma_high × r2.0 / 3.5 / 5.0, and every gated arm's JSON has `configuration.inversion_path == "InversionInterferometerSparseNumba"`.
- New CPU cells: numba vs FFT log-evidence ≤ 0.5 nat (expect ~1e-8), step sum within 10 % of the full call, and CPU logL matching A100 logL to ≤ 1e-3 nats.
- sdp81: every path agrees within 0.5 nat on the same dataset.
- Every cell is filled or has a stated reason, which I audit by grepping the table for blanks.
- Repo lint green (`build_readme.py --check`, profiling lint), then `/ship_workspace`.
