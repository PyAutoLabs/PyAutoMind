## likelihood-lifecycle-p5h
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/141
- completed: 2026-11-25
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/142
- epic: likelihood-lifecycle (phase 5H)
- supersedes (retired with this record): draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md

Euclid pipeline adopts `--setup <auto|cpu|gpu|setup_id>` (default auto) and `--number_of_cores auto`; `--use_cpu` is a deprecated alias for `--setup cpu`. dr1.yaml vis_lp/vis_pix use `--setup=cpu --number_of_cores=auto`. Human ruling kept local `--stage all` (CPU) as one process (vis_lp JAX then forked numba vis_pix); HPC routes stay two-process. Merged after library release 2026.11.25.1.

Before the next RAL use: run HPCPullPyAuto so the shared install carries 2026.11.25.1 (needs the human's OK per policy/hpc_ral.md).

## Original prompt

# Likelihood lifecycle phase 5H: euclid_strong_lens_modeling_pipeline: `--setup` replaces `--use_cpu`, `--number_of_cores auto`, and the single-process draft closed as superseded

Type: feature
Target: euclid_strong_lens_modeling_pipeline
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- hpc-gpu
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/141
Consequence: judge
Witness: `util.parse_fit_args` accepts `--setup <auto|cpu|gpu|setup_id>` (default `auto`, the same values as `PYAUTO_SETUP`) and `--number_of_cores` accepting `auto` (default `auto`). `--use_cpu` is a deprecated alias that maps to `--setup cpu` with a one-line stderr warning (the `--skip_pix` precedent). `scripts/initial_lens_model.py` and the other fit scripts pass `setup=setup` to their analyses instead of `use_jax=not use_cpu`, the hard-coded `use_jax=True` and the manual `apply_sparse_operator_cpu()`; the SED stage is untouched. `hpc/campaign/dr1.yaml`, `hpc/batch_cpu/{stage,template,submit_initial_lens_model,submit_reload_coolest,submit_reload_wcs}`, `hpc/template.py`, `hpc/README.md`, `start_here.py`, `scripts/README.md` and `AGENTS.md` use the new CLI. Pooled stages keep `JAX_PLATFORMS=cpu` and `BLAS_THREADS=1`, with a comment citing the RAL OpenMP-fork failure; tooling and catalogue jobs keep their pins. The tests are updated, and the repo's test suite plus CI pass.
Review-minutes: 20
Unattended: no
Lane: any
Gate: 5A–5E and the setup banner MERGED. Merge with or after the library release, like 5F/5G. RAL runs library main via the shared install, so run `HPCPullPyAuto` before any RAL run of the new CLI. Plan approved by the human on 2026-11-25.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-25

## Context

- **Report :256 / ledger :73:** 5H = science projects `--use_cpu` → `--setup`, env blocks removed, and the euclid single-process-route draft closed by it.
- **Survey 2026-11-25:**
  - `util.py:1705-1830` holds `parse_fit_args` (`--use_cpu` :1753; `--number_of_cores` :1746; the `--skip_pix` deprecated-alias precedent at :1782-1820).
  - `scripts/initial_lens_model.py` :366, :676 (`use_jax=not use_cpu`), :638-639 (`apply_sparse_operator_cpu`) and :764-781 (cores only for vis_pix).
  - `full_model.py`, `mge_lens_only.py`, `sersic_lens_model.py` and `lens_model_waveband.py` hard-code `use_jax=True`. `sersic_lens_model_waveband.py` (SED) must not get the setup change.
  - `hpc/campaign/dr1.yaml` :74, :89, :111; `hpc/batch_cpu/stage` :98, :198-206; `submit_initial_lens_model` :58, :67-69, :112; `template` :41-49, :69; `submit_reload_coolest` :136-141; `submit_reload_wcs` :110-115.
  - `hpc/template.py` :15-263; `start_here.py` :135-137, :475-481; `hpc/README.md` :101, :149-224; `AGENTS.md:197`.
  - `hpc/diagnostics/jax_fork_control.py` :670, :700.
  - Tests: `tests/test_util.py` :119-148, `test_hpc_campaign.py` :117-118, `test_hpc_sync.py` :330/:407, `test_stage_guard.py` :84/:156, `test_vis_lp_model.py` :313. CI uses PyAutoHeart's reusable workflow against library main.
  - No live campaign uses the pipeline: euclid_dr1 is complete and frozen; euclid_detailed is dormant.
- **Design calls (human-approved 2026-11-25):**
  1. `--use_cpu` maps to `--setup cpu` (a CPU intent: vis_lp JAX-CPU, pixelized vis_pix numba sparse).
  2. Keep the two-process stage structure; pooled stages keep `JAX_PLATFORMS=cpu` and `BLAS_THREADS=1`, with a comment.
  3. Close `draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md` as superseded by `setup="auto"`, not validated. Its production-scale RAL witness becomes an optional follow-up needing the human's go-ahead (there is an open RAL OpenMP-fork finding, ledger :332, job 414150).
  4. Defer the Science area: `active/euclid_detailed` (dormant) gets a Mind note to adopt `--setup` when revived.
  5. Merge with or after the release; `HPCPullPyAuto` before RAL use.
- Keep the CLI wording identical to `draft/feature/autolens_assistant/hpc_setup_flag_and_wiki_auto_setup.md`.

## Out of scope

- Science-area projects.
- The assistant hpc templates (separate draft).
- Running the single-process RAL witness.
- The R6 default flip.
