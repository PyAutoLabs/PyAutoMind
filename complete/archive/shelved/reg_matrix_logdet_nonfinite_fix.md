# [WITHDRAWN 2026-07-17] superseded by draft/feature/autoarray/gradient_safe_logdet_settings_option.md — the verdict ruled out changing the DEFAULT log-det (C4: current lam-dependence is correct to machine precision). Kept for provenance only. Do NOT start.

# Fix the non-finite log_det_regularization_matrix_term (pix NaN phase 2)

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

Phase 2 of autolens_workspace_developer#104 (phase 1 shipped via
autolens_workspace_developer#105 — read `searches_minimal/pix_nonfinite_findings.md`
first; the probe is `searches_minimal/probe_nonfinite_pix.py`).

Phase 1 localised the pixelized likelihood's non-finite walls to **exactly one
site**: `AbstractInversion.log_det_regularization_matrix_term`
(`autoarray/inversion/inversion/abstract.py:734-764`) — the
`log(diag(cholesky(H)))` of the reduced regularization matrix — as the first
non-finite stage in BOTH the forward and backward walks, culprit parameter = the
regularization coefficient. The three other suspected sites are exonerated (the
curvature-reg cholesky at `abstract.py:719` is finite at 1.69e4; the NNLS Jacobi
preconditioner has no zero diagonal; the kernel-CDF weight-map normalise is
finite). Both death classes — in-basin (r_E 1.28, beside the Nautilus mode 1.31)
and out-of-basin (r_E 5.93) — die at the same site, so ONE fix covers both and no
"penalty for invalid space" verdict is needed.

**Mechanism (confirmed structurally).** `constant_regularization_matrix_from`
(`autoarray/inversion/regularization/constant.py:43-58`) builds
`H = lam^2 * L + 1e-8 * I`, where `L` is a graph Laplacian — positive
SEMI-definite, with the constant vector as an exact null mode. The `1e-8` diagonal
lift is **absolute, not scaled to lam**, so `eig_min` is pinned at 1e-8 while
`eig_max ~ lam^2 * degree`, giving `cond(H) ~ lam^2 * 1e8`. Verified against the
real library function: `eig_min == 1e-8` across four decades of lam; at lam=1e5 it
goes numerically negative (-9.9e-6) and numpy raises `LinAlgError` where JAX
returns NaN silently (`abstract.py:762` already documents that asymmetry).

**START HERE — the open question phase 1 deliberately did not guess.** The
synthetic clean 4-connected grid only fails at lam >= 3e4, but the real fit died
at lam ~ 6.9e3 (read off the logged regularization_matrix min = -4.7988e7 = -lam^2).
A numpy-vs-JAX backend divergence is RULED OUT (tested — they agree exactly), so
the real REDUCED matrix must be worse-conditioned than a regular grid. **Dump the
real `regularization_matrix_reduced` spectrum at the death point before choosing a
fix.** Candidate explanations, all untested:
- the inversion is 920x920 = 900 mesh pixels + 20 UNREGULARIZED MGE linear
  amplitudes, which is why the term uses `regularization_matrix_reduced`
  (`abstract.py:331`) + `zeroed_ids_to_keep` — the reduction may not leave a clean
  Laplacian;
- the kernel-CDF adaptive mesh may yield isolated/disconnected mesh pixels
  (degree 0 -> diagonal 1e-8 alone; k components -> k null modes);
- `constant.py:55-58` scatters with `unique_indices=True` — if `neighbors` ever
  holds duplicate (i,j) pairs that flag is a false promise to XLA and the
  scatter-add is undefined.

Then decide the fix (cheapest first): scale the lift with the coefficient
(`1e-8 * (1 + lam^2)` or a relative floor `eps * trace(H)/S`), bounding cond(H) in
lam; or use `slogdet` / an eigenvalue sum instead of `log(diag(cholesky))` so an
indefinite matrix fails loudly rather than NaN-ing; or treat the null space
explicitly — `log det(lam^2 L + eps I)` for singular `L` is eps-dependent by
construction, so the 1e-8 is doing load-bearing SCIENCE work while presenting as a
numerical hack (worth a Warren & Dye / Nightingale & Dye cross-check on how the
evidence normalisation should treat it).

**This is a science-visible change**: any of these alters `log_det(H)` and
therefore every reported Bayesian evidence. An evidence-parity check against
current results is mandatory before it ships — do not treat this as a pure
numerical patch.

Reproduction traps: will NOT run locally (one point's `value_and_grad` needs
10.90 GiB; a 15GB/6GB-VRAM laptop OOMs on both CPU and GPU) — use the RAL A100
(`probe_nonfinite.sbatch`, `--partition=gpu --mem=64gb`, ~5 min). The recorded
#101 death points reproduce nothing (they are LAST-FINITE params); use the seed-0
rejected draws (12 and 35 of 90).

Related and NOT in scope here: the PyAutoFit gradient-guard bug
`draft/bug/autofit/fitness_where_guard_nan_gradient.md` (the resample guard does
not protect gradient consumers) — separate repo, separate fix, arguably higher
leverage.
