# Sweep the RAL active output tree: mesh + point-source results move to output/legacy_point/

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- hpc
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 5
Unattended: ready
Lane: local-dev
Filed: 2026-09-01

Human directive from the 2026-08-31-pm batch review (verbatim):

"""
I think we basically need to clear the output folder on RAL of all results for
meshes, and also the "image_plane" / "source_plane" point source fits and the
"Cluster" folder and the "point_source" folder, so I am working with a clean
output folder which updates with each task. In fact, just move them to a new
folder called "legacy_point".
"""

Context: the delaunay_fp64 retro baseline was REJECTED at that review as a
demagnified-source unphysical solution (PositionsLH not wired into the JAX
gradient runs — autolens_profiling#203, DECISIONS.md 2026-09-01). Mesh results
in the active tree are therefore spent evidence.

Do, on RAL and mirror identically (mv, never delete; structure preserved, same
pattern as the 2026-08-31 legacy/legacy_wrong quarantine):

1. Move all mesh/pixelization results, the image_plane/ and source_plane/ point
   source fits, the Cluster/ folder and the point_source/ folder from the
   active `output/` into a new `output/legacy_point/`.
2. Leave the active tree holding only what current tasks write; confirm
   `hpc/sync pull` scope still excludes legacy trees.
3. Record the move in autolens_profiling (issue #203 comment + DECISIONS.md
   line with counts per folder).

Also pending from the same review: mv the ACCEPTED mge_pos reference
(`output/legacy/searches/.../340210_9`) back into the active tree, per the MGE
reuse rule.
