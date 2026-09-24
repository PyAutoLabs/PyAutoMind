# MGE NNLS fix (PyAutoArray#571): SLaM 60-column GPU timing and parity, single…

Type: research
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Difficulty: too-large
Autonomy: supervised
Priority: medium
Memory: wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md; wiki/lensing/sources/lens-modeling-methods.md
Status: formalised
Consequence: glance
Witness: A results/notes entry plus JSON rows record, for the SLaM source_lp[1] 60-column MGE model (2 lens bases x 20 Gaussians, sigma_min = pixel_scale/10, 20 source Gaussians, 17 free parameters), the single-call and vmap16/vmap50 per-evaluation likelihood cost on the RTX 2060 and an A100 in fp64 with the released library BEFORE and AFTER PyAutoArray#571 (nnls_preconditioning_no_mapper jacobi vs raw), the NNLS share of each batch, and GPU-vs-CPU parity (max |dlogL|) on the 48 near-truth vectors of scripts/imaging/hazards/mge_nnls_capture.py.
Review-minutes: 3
Unattended: needs-slicing

# MGE NNLS fix (PyAutoArray#571): SLaM 60-column GPU timing and parity, single and vmap

Type: research
Target: autolens_profiling
Priority: medium
Repos:
- autolens_profiling
Witness: A results/notes entry plus JSON rows record, for the SLaM source_lp[1] 60-column MGE model (2 lens bases x 20 Gaussians, sigma_min = pixel_scale/10, 20 source Gaussians, 17 free parameters), the single-call and vmap16/vmap50 per-evaluation likelihood cost on the RTX 2060 and an A100 in fp64 with the released library BEFORE and AFTER PyAutoArray#571 (nnls_preconditioning_no_mapper jacobi vs raw), the NNLS share of each batch, and GPU-vs-CPU parity (max |dlogL|) on the 48 near-truth vectors of scripts/imaging/hazards/mge_nnls_capture.py.

Blocked until a release ships PyAutoArray#572 (the profiling harness runs the installed library; A100 runs need the RAL mirror synced via HPCPullPyAuto).

Context: the 2026-09-24 audit measured only CPU timing for the fix (neutral: 27.3 -> 25.8 ms single, 31.3 -> 30.3 ms/eval vmap16). On GPU the pre-fix behaviour made every Nautilus vmap batch run all 50 PDIP iterations whenever one lane failed (NNLS ~28% of a 2060 batch, ~44% of a single A100 evaluation), so the fix should cut batch cost; that is unmeasured. GPU parity of the raw-forward PDIP is also unmeasured (the audit saw CPU/GPU/vmap divergence on the failing vectors pre-fix).

Ask:
1. Reuse the SLaM model recipe of scripts/imaging/hazards/mge_nnls_capture.py (prior creation order matters for vector reproduction) in a likelihood_runtime-style cell or a hazards script; time single, vmap16 and vmap50 per-evaluation cost on the RTX 2060 and RAL A100, fp64, with the setting forced to jacobi and to raw, interleaved minima.
2. Record NNLS share per config via the existing solve ablation pattern (unconstrained solve swap) or stats["iterations"].
3. GPU parity: run the 48 capture vectors on GPU, report max |logL_gpu - logL_cpu| and max |logL_jax - logL_numpy|, and iterations per lane.
4. Ingest into the README dashboards (build_readme.py --check) and a results/notes/mge_nnls_fix_gpu_2026_XX.md verdict; route any regression to /intake as a bug.

<!-- formalised by the Intake (Conception) Agent on 2026-09-24 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/4c46534e-38b6-47fd-9021-8040da7c7d92/scratchpad/mge_audit/prompt_followup.md -->
