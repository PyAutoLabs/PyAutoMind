# Rewrite docs/api/plot.rst to document the functional plot API

Type: docs
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoGalaxy
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up from PyAutoLens#592 (release-docs polish, Phase A). The audit found that
`docs/api/plot.rst` in PyAutoGalaxy and PyAutoLens (and almost certainly PyAutoFit)
documented an **object-oriented plotting subsystem that has been removed** — `MatPlot1D/2D`,
`Visuals1D/2D`, `Units/Figure/Axis/Cmap/Colorbar/.../Title/Legend`, and every
`*Scatter` / `*Overlay` / overscan wrapper (~34 entries per file). These are truly absent from
the installed stack; plotting is now a **functional API** (`aplt.plot_array(...)`,
`aplt.subplot_*(...)`, `output_path=`/`output_filename=`/`output_format=` kwargs).

Under #592 those dead OO entries were **pruned** (the "Plot Customization" and "Matplotlib
Wrappers" sections removed) so the docs are correct but now thinner. This prompt is the
**positive rewrite**: document the current functional plot API properly.

Scope:
- Add a "Plot Customization" / "Output & Figure Control" section to each `plot.rst` describing
  the functional API: passing `output_path`, `output_filename`, `output_format` (and any
  title/label/colormap kwargs) directly to the `aplt.*` calls — grounded against the installed
  API (`dir(autolens.plot)` / `dir(autoarray.plot)`; note `Output` survives in `autoarray.plot`).
- Keep the surviving "Plotters [aplt]" and "Non-linear Search Plot Functions" sections.
- Do PyAutoFit's `plot.rst` in the same pass (once its `ep-graphical-docs` worktree, PR #1334,
  has merged — it currently claims the PyAutoFit checkout).
- Anchor the prose on the workspace plot guides (`autolens_workspace/scripts/guides/plot/`).

Ground every documented symbol against the live API before listing it (use `PYAUTO_SKIP_API_GATE=1`
to introspect). See PyAutoMemory note: plot API docs stale.
