Kept Python/JAX caches off $HOME on HPC (RAL admin request 2026-09-25): tracked activate.sh HPC branches in autolens_inference and the three assistants now export every cache under ${PYAUTO_HPC_CACHE:-$(dirname "$PYAUTO_HPC_BASE")/.cache}; autolens_inference submit scripts no longer point numba/matplotlib at /tmp.

Merged 2026-09-25 (human `/prm`, all checks green; shipped under the recorded Heart RED development override):
- PyAutoLabs/autolens_inference#14 — `activate.sh` cache block; `/tmp` cache exports removed from 12 `hpc/` files; `hpc/README.md` + `AGENTS.md`
- PyAutoLabs/autolens_assistant#135 — `activate.sh` cache block (HPC branch only)
- PyAutoLabs/autogalaxy_assistant#30 — `activate.sh` cache block + cache docs (`ag_setup_environment.md`, `sandbox.md`, `hpc.md`, re-provenanced)
- PyAutoLabs/autofit_assistant#51 — `activate.sh` cache block (HPC branch only)

With `PYAUTO_HPC_BASE` set, every cache (XDG/pip/matplotlib/numba/CUDA/Triton/JAX/astropy) now lands under `${PYAUTO_HPC_CACHE:-$(dirname "$PYAUTO_HPC_BASE")/.cache}` (`/mnt/ral/jnightin/.cache` on RAL). The RAL venv hot-fix (`/mnt/ral/jnightin/PyAuto/PyAuto/bin/activate`, backup `.bak_20260925`) stays as the backstop for untracked project copies.

Remaining: phase 2 (autolens_profiling, euclid_strong_lens_modeling_pipeline) is in PyAutoMind `planned.md` as `hpc-cache-off-home-phase2`, blocked on those repos' active claims.

Heart RED development override recorded (issue #13, PR bodies, autonomy_log red-override row).

## Original prompt

# Keep Python/JAX caches off `$HOME` on HPC — tracked `activate.sh` + submit-script tidy

Type: maintenance
Target: autolens_inference
Repos:
- autolens_inference
- autolens_assistant
- autogalaxy_assistant
- autofit_assistant
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Issued: 2026-09-25
Issue: https://github.com/PyAutoLabs/autolens_inference/issues/13
Consequence: glance
Witness: sourcing each repo's `activate.sh` with `PYAUTO_HPC_BASE` set exports `XDG_CACHE_HOME`, `PIP_CACHE_DIR`, `MPLCONFIGDIR`, `NUMBA_CACHE_DIR`, `CUDA_CACHE_PATH`, `TRITON_CACHE_DIR` and `JAX_COMPILATION_CACHE_DIR` under `${PYAUTO_HPC_CACHE:-$PYAUTO_HPC_BASE/../.cache}` (a preset value still wins); `git grep -E "(NUMBA_CACHE_DIR|MPLCONFIGDIR)=/tmp" -- hpc/` returns nothing in autolens_inference.

## Original request (verbatim, 2026-09-25)

RAL server admin: "Can you fix your jobs on the cloud cluster so they do not cache python stuff in /home/jnightin/.cache? I found a few broken nodes where the (small) root disk was full due to python junk getting cached there. None of the nodes have a separate disk for /home and hence it's easy to fill the disk when users inadvertently use things that default there."

User: "ok do all 3 of these: … 4. Make the cache fix permanent … 5. Tidy the /tmp cache paths in submit scripts." Decision: permanent fix lives in the **tracked activate.sh** (workspace-only, no library change); split by conflicts — this task covers the unclaimed repos; autolens_profiling (103 submit scripts) and euclid_strong_lens_modeling_pipeline follow as a blocked phase 2 (`draft/maintenance/workspaces/hpc_cache_off_home_phase2.md`).

## Background

- `organs/PyAutoNerves/autonerves/jax_wrapper.py:110-116` defaults `JAX_COMPILATION_CACHE_DIR` to `$XDG_CACHE_HOME/pyauto_jax` or `~/.cache/pyauto_jax`; pip, matplotlib, numba, CUDA and Triton also default under `$HOME`. On RAL `/home` is each node's small root disk.
- Hot-fix already live (2026-09-25): a cache-redirect block appended to `/mnt/ral/jnightin/PyAuto/PyAuto/bin/activate` (backup `activate.bak_20260925`), pointing at `/mnt/ral/jnightin/.cache`. Lost if the venv is rebuilt — hence this task.
- Submit scripts set `NUMBA_CACHE_DIR=/tmp/numba_cache` / `MPLCONFIGDIR=/tmp/matplotlib`; `/tmp` is on the same small root disk.
