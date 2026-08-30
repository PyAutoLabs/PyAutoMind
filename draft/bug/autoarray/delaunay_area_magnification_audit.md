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
Phase: 6
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-08-28

Phase 6c of 10 in the Euclid DR1 preparation epic. **Can run alongside phase 6b and does
not gate on it** — 6b is the empirical half (does μ come out right on data?), 6c is the
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
