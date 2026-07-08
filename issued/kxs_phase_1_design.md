# k×s coupling — phase 1: design note + adaptive ground truth

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 1 of `oversampling_kxs_coupling.md` (split 2026-07-08; Feature Agent
score 7). **No library source edits.** Mechanism under design: adaptive
evaluation (per-pixel k_i·s) → partial bin to a uniform s-resolution fine
image → PSF convolve at s → bin s→1.

## Deliverables

1. **Design note** (`kxs_design.md` alongside this prompt, posted to the
   phase issue): settle the pre-bin placement fork from the parent prompt —
   Convolver-internal (state caches the segment map, callers unchanged) vs
   caller-side util (Convolver contract stays uniform-s) — with file/line
   grounding against the refactored helpers (PyAutoArray#361 branch), and
   the divisibility-validation and index-map design for adaptive k_i.
2. **Ground truth** (`kxs_ground_truth.py`): extend the series' brute-force
   reference — same scene, adaptive evaluation (k_i·s ∈ {4, 2} radial
   pattern with s=2), partial-bin, fine convolution, bin — producing pinned
   numbers for phases 2–3. Must reduce exactly to the existing s=2
   reference when k_i=1 everywhere.

## Acceptance

- Fork decided with a recorded rationale; ground-truth numbers printed and
  recorded in the note; k=1 reduction exact; no source edits.

Parent: `feature/autoarray/oversampling_kxs_coupling.md`.
