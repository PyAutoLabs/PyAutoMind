# HowToLens tutorial 4 (point sources): make image-plane vs source-plane clear

Type: docs
Target: HowToLens
Repos:
- HowToLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: notify
Witness: tutorial_4_point_sources.py runs clean end to end, and every plot title starts with "Image Plane:" or "Source Plane:".
Review-minutes: 0
Unattended: ready
Lane: wsl-data

Blocked on: the PointSolver source-plane figure task (`aplt.plot_point_solver(..., show_source_plane=True)`) being merged and released.

File: HowToLens `scripts/chapter_1_introduction/tutorial_4_point_sources.py`.

1. Make the direction explicit: rewrite "The Lens Equation" and "Point Solver" so it is clear both methods only ray-trace image plane → source plane. The current wording ("for a point source we want to find every image-plane position") reads as a source → image mapping.
2. Prefix every plot title with "Image Plane:" or "Source Plane:"; add one source-plane plot (caustic + point source star).
3. Add an illustrative "rays miss a point" figure after "Point Sources" (the human is producing the final image; draft at `/mnt/c/Users/Jammy/Workspace/Science/scratch/howtolens_point_source_figure/point_source_ray_tracing.png`): the source is smaller than an image pixel, without PSF blurring each image would sit in one pixel, and grid ray tracing finds nothing.
4. Use `aplt.plot_point_solver` with the new source-plane option (GIF optional) after "Point Solver".
5. Add "how do we know where the source is?": the source centre is a free parameter, fitted until the predicted image positions match the observed ones; link forward to the `point_source` modelling examples.
6. Head off two student questions: the solver ignores flux (changing `intensity` does nothing; `al.ps.PointFlux` handles fluxes); redshifts don't change images in arcseconds, only the arcsec → kpc conversion (maybe as an Ask AI prompt).
7. Regenerate notebook/markdown, render the figures, ship through /review.

Origin: Slack questions from a student reading tutorial 4, 2026-11-13.

<!-- formalised by the Intake (Conception) Agent on 2026-11-13 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/8169607b-10f4-4b45-83a0-175c19a43c37/scratchpad/p2.md -->
