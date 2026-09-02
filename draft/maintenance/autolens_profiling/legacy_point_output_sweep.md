# Sweep the RAL active output/ tree: move mesh, point-source and Cluster results to output/legacy_point/

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- hpc-gpu
- profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: glance
Review-minutes: 5
Unattended: never
Lane: local-dev
Filed: 2026-09-01
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/205 (opened 2026-09-01 as a Cortex gate ref; reuse in start_dev — never open a second)

## Where this came from

The 2026-08-31-pm batch review's `delaunay-fp64-retro-baseline` rejection
(2026-09-01) carried a programme-wide finding *and* an output-tree directive.
The human inspected
`output/legacy_wrong/searches/nautilus/imaging/delaunay/hst/hpc_a100_fp64/` and
identified the solution as a demagnified-source unphysical solution — the
classic Inversion bias `PositionsLH` exists to remove. The binding consequence
for the redo is that every mesh / pixelization run must carry a `PositionsLH`
positions penalty; mesh rows produced without it are not citable as references.

The directive this prompt enacts is the second half of that ruling, recorded
verbatim in `autolens_profiling/results/notes/inference/DECISIONS.md` (entry
"2026-09-01 — Batch 2026-08-31-pm review rulings", lines 1553-1559):

> **Output-tree consequence (human directive, verbatim intent):** clear the RAL
> active `output/` of all mesh results, the `image_plane`/`source_plane` point
> source fits, the `Cluster` folder and the `point_source` folder — moved (not
> deleted) to a new `output/legacy_point/` folder, so the active tree is clean and
> updates with each task. Laptop action, queued as a local-dev prompt in the Mind
> (`draft/maintenance/autolens_profiling/legacy_point_output_sweep.md`).

## What to do

**Move, do not delete.** Everything named below is relocated into a new
`output/legacy_point/` folder that mirrors the source tree's shape, so any of it
can be cited or pulled back:

1. all mesh results in the RAL active `output/` tree;
2. the `image_plane` and `source_plane` point-source fits;
3. the `Cluster` folder;
4. the `point_source` folder.

Do the same on the laptop mirror (`/mnt/c/Users/Jammy/Science/inference_programme/`)
so the two trees stay in step — a sweep on one side only reintroduces the drift
this is meant to remove.

**This is a laptop action.** It needs the SSH endpoint to RAL and the local
mirror, so it cannot run in a cloud session (`Lane: local-dev`). Nothing is
submitted, cancelled or modified on the cluster — this is a file move.

## Why it matters

The active `output/` tree is what each new task reads and updates. Leaving the
quarantined and superseded families in it means every subsequent read has to
know which subtrees are spent, which is exactly the state the 2026-08-31 rewind
was meant to end. After the sweep the active tree holds only work the redo can
actually cite.

## Acceptance

- `output/legacy_point/` exists on RAL and on the laptop mirror and holds all
  four families named above, with their directory structure preserved.
- The active `output/` tree no longer contains them.
- Nothing was deleted — a spot check can find any moved run under its new path.
- A one-line note appended beside the ledger recording that the sweep ran and on
  what date.
