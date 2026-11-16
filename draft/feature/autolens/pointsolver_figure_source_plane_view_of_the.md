# PointSolver figure: source-plane view of the triangles

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `aplt.plot_point_solver(..., show_source_plane=True, output_path=tmp)` on the HowToLens tutorial 4 lens (SIE einstein_radius=1.6, q=0.9, angle=45, point at (0.07, 0.07)) writes a figure whose source-plane panels draw kept traced triangles for all 4 images, each containing the source coordinate; existing point_solver.png output is unchanged when the option is off.
Review-minutes: 3
Unattended: ready
Lane: wsl-data

Add a source-plane view to `aplt.plot_point_solver` (PyAutoLens `autolens/point/plot/point_solver_plots.py`), e.g. `show_source_plane=True`.

For each displayed step, add a source-plane panel next to the image-plane one:
- `step.plane_triangles` (the corners of the tested triangles ray-traced to the source plane), with kept triangles in the same colours as the image-plane panel;
- the point source as a star, plus the caustics.

Requirements:
- Show all multiple images, as the existing figure does, not just one: the kept traced triangles of every image overlap the point.
- Zoom per step so the shrinking traced triangles stay visible.
- The kept-then-rejected triangle near a singular lens centre traces to a huge triangle; draw it hatched/clipped in the existing "kept, then rejected" style so it does not swamp the panel.
- Also works for the GIF (`animate=True`).

Reference prototype (follows one image only): `/mnt/c/Users/Jammy/Workspace/Science/scratch/howtolens_point_source_figure/point_solver_triangles.py`.

Motivation: a student reading HowToLens tutorial 4 asked why point sources use "forward mapping" (source → image). They don't: the solver still only ray-traces image → source, keeping image-plane triangles whose traced triangle contains the point. The source-plane panel makes that visible. The HowToLens tutorial 4 clarity task depends on this shipping and being released first.

Origin: Slack questions from a student reading tutorial 4, 2026-11-13.

<!-- formalised by the Intake (Conception) Agent on 2026-11-13 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/8169607b-10f4-4b45-83a0-175c19a43c37/scratchpad/p1.md -->
