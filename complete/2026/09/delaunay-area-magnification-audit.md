## delaunay-area-magnification-audit
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/522
- completed: 2026-09-04
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/523
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/523
- epic: euclid-dr1-prep (Mind phase 8, was 6c)

Source-code audit of every Delaunay pixel-area and magnification path in PyAutoArray,
with the empirical half left to Cortex phase 7 (`magnification_robustness`). The audit
answered the epic owner's question — "does the code look right?" — with a proven **no**:
two real, independent defects, neither fixed here by design, each filed as its own bug
prompt. The full per-path table and every measured number are on PyAutoArray#522.

## What shipped

PyAutoArray PR #523 (`feature/delaunay-area-magnification-audit`, head `8c2e0d18`, merge
commit `548ff1e`), issue #522 closed. Tests + one docstring, **no behaviour change**:

- `test_autoarray/inversion/pixelization/mesh_geometry/test_delaunay.py` (+3):
  `areas_for_magnification` on an n×n unit lattice (interior cells exactly 1.0, hull cells
  zeroed, Σ = (n−2)²); bounded boundary cells are **kept** (only unbounded Voronoi regions
  are zeroed); repeat calls agree and the `-1` sentinel is never written back.
- `test_autoarray/inversion/pixelization/interpolator/test_delaunay.py` (+4):
  `barycentric_dual_area_from` — single triangle gives `A/3` per vertex; Σ equals the
  convex-hull area exactly; exact integration of a linear field; NumPy-vs-JAX in-graph parity.
- `areas_for_magnification` docstring rewritten to the proven semantics: Voronoi cell areas
  from `voronoi_areas_numpy`, only unbounded cells zeroed, bounded boundary cells kept, and
  these are **not** the barycentric dual areas the Delaunay interpolator uses.
- The two tests that pin the current Voronoi semantics carry comments saying the follow-up
  fix must flip them deliberately.

## Findings (the audit proper)

1. **Delaunay `areas_for_magnification` returns the wrong area for the mapper it serves.**
   The mapper is barycentric-linear, so the exact quadrature weight for
   `Σ reconstruction × area` is the barycentric dual area (`barycentric_dual_area_from`,
   already computed one module away and used only to position regularisation split points).
   Identity-lens μ recovers 1.0 to ≤ 2e-5 with dual areas for every source shape tested,
   including a random reconstruction; with Voronoi areas it is biased −13 % … −53 % on
   adaptive-style meshes and −95 % … −99 % when the source fills the hull, because bounded
   boundary Voronoi cells reach 10⁵× their dual area (one cell measured at 234× the entire
   hull). `zeroed_pixels` cannot rescue it: the pathology lives one ring *inside* the convex
   hull. Filed: `draft/bug/autoarray/delaunay_magnification_uses_voronoi_not_dual_areas.md`.
2. **The pipeline's `magnification` latent is a hard 0/0 for any pixelization-only source.**
   `Galaxy.image_2d_from` returns zeros when the galaxy has no `LightProfile`, so
   `total_source_flux = 0.0` → `magnification = inf` (dropped as non-finite under current
   code; recorded as a `0.0` sentinel in 9/9 archived `vis_pix` results). The Sersic control
   reproduces `truth.json` bit-for-bit, so the latent's definition is sound and only the
   pixelized route is broken. Never touches `areas_for_magnification` — the two defects are
   independent. Filed: `draft/bug/autolens/magnification_latent_zero_for_pixelized_source.md`.
3. **Plotting is consistent with the mapper, not with the denominator.** The `tripcolor`
   surface integrates to `F_dual` to 1.00000000 and exceeds `F_vor` by 18.47× — the picture
   and the mapper's own flux agree with each other; `areas_for_magnification` is the odd one
   out. Docstring says Gouraud but matplotlib defaults to flat shading (cosmetic here).
4. **`sqrt` is not on the magnification path.** The only `sqrt` in the Delaunay package
   feeds split-point offsets for the regularisation matrix and cannot change the flux integral.
5. **Rectangular-mesh lead, not established:** the meshes `source_science.py` actually ships
   with show a tight +6 % / +28 % scale offset with a guard-ring signature. Handed to the
   cluster epic's `draft/test/workspaces/mesh_magnification_correctness.md`, not claimed here.

## Statements to the science phases

- **Cortex phase 7 (`magnification_robustness`):** Delaunay magnification numbers from the
  `source_science.py` recipe are NOT trustworthy until the autoarray follow-up ships; expected
  bias is negative (μ under-estimated). Sersic rungs 1-4 are sound. The Delaunay rung cannot be
  scored against `latent.magnification` at all (finding 2) — it needs the area-based quantity
  computed explicitly.
- **Cortex phase 4 / Mind phase 9:** the `vis_pix` catalogue `magnification` column is a `0.0`
  sentinel today; phase 4's numerics witness must exclude it (or the autolens follow-up must
  ship first), and phase 9's magnification layer depends on it.

## Traps / notes

- `areas_for_magnification` had **zero** tests in any repository and zero library callers; the
  one test touching `voronoi_areas` pinned a 29.8 arcsec² boundary cell as expected behaviour.
  Any fix needs a regression test built from the identity-lens construction (issue #522 §2),
  not a re-pin of the snapshot.
- The out-of-hull nearest-vertex fallback in `pixel_weights_delaunay_from` is piecewise
  constant and a separate flux hazard (4.7×–16.7× over-count when the data grid extends past
  the hull) — worth remembering when the fix lands.
- Reproduction scripts (`part1_flux_integral.py` … `part3b_fit_latent.py`) lived in the
  audit session's scratchpad and were not committed; the numbers are on the issue.
- Close-out ran on the mcp lane from a cloud session: worktree
  `~/Code/PyAutoLabs-wt/delaunay-area-magnification-audit` and the local
  `feature/delaunay-area-magnification-audit` branch are left for the laptop.

## Original prompt

# Audit the Delaunay pixel-area and magnification source code for correctness bugs

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- PyAutoLens
Themes:
- pixelization
- euclid
Difficulty: small-medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Epic: euclid-dr1-prep
Phase: 8
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28
Issued: 2026-09-04
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/522

Phase 8 of the Euclid DR1 preparation epic (was 6c; renumbered 2026-09-01 in the Cortex split,
where the old 6b became `PyAutoCortex` `phases/euclid/magnification_robustness`). **Can run
alongside the magnification-robustness phase and does not gate on it** — that phase is the
empirical half (does μ come out right on data?), this one is the
source-code half (does the code look right?). Either can find the defect first.

User request (verbatim, the follow-up clause of 6b):

"""
We have also never really validated or tested the magnifcitations using
the Delaunay source model, and this could even have bugs (E.g due to pixel areas not being quite right). So, for this
Euclid epic do all of the magnification comparisons you can on the 10 lenses in this spirit, but also have a follow up issue
which checks if the soruce code itself looks like it might have a bug or issue with the Delaunay area and thus magnification calculations.
"""

## Where to look

- `PyAutoArray` mesh geometry: the Delaunay `areas_for_magnification` implementation
  (`voronoi_areas`, with boundary cells zeroed via a `-1` sentinel) and its
  rectangular-adaptive sibling. The cluster epic's audit
  (`draft/test/workspaces/mesh_magnification_correctness.md`) already established that
  `areas_for_magnification` exists for **only two** mesh geometries, has **zero library
  callers** (it serves only workspace scripts), and has **no direct test** — only its
  delegates are tested. That is exactly the shape a latent bug hides in.
- The boundary-cell semantics. Zeroing boundary cells changes the summed source-plane
  area and therefore μ directly. Is the zeroing correct, or does it bias μ high?
- `PyAutoArray/autoarray/plot/inversion.py::_plot_delaunay` and the Delaunay mapper —
  check whether the areas used for *plotting* and the areas used for *magnification*
  come from the same computation. Divergence there is a classic source of "the picture
  looks right but the number is wrong".
- The interaction with `sqrt` on dual areas — there is a known NaN hazard in the Delaunay
  dual-area gradient path; check whether the same expression is on the magnification
  path.

## Method

This is an audit, not a rewrite. Read the code, then **prove** each suspicion or drop it:

- Construct known-answer configurations (a uniform triangulation of known total area,
  a mesh with an analytically computable source-plane area) and check the code returns
  the analytic value. A resemblance verdict is not verification.
- Where a suspected bug is found, reproduce it in a minimal test **before** proposing a
  fix, and check whether it is reachable from the paths Euclid actually uses.
- Do not exempt a case because it "looks intentional" — if boundary zeroing is
  deliberate, find the commit or comment that says so.

## Deliverables

1. A written audit: each area/magnification code path, what it computes, and whether it
   is correct.
2. Known-answer tests for Delaunay `areas_for_magnification` (the missing direct test),
   landed regardless of whether a bug is found — the absence of a test is itself the
   defect the cluster-epic audit flagged.
3. If a real defect is found: **file a separate bug prompt** for the fix rather than
   growing this one, and tell phase 6b immediately so its Delaunay leg is interpreted
   correctly.

## Acceptance / gate

- Every Delaunay area/magnification path either verified against an analytic answer or
  flagged with a reproduced failing case.
- Direct tests exist where there were none.
- A clear statement to 6b: are its Delaunay magnification numbers trustworthy?
