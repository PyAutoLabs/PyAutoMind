## rect-adapt (rectangular adaptive-mesh edges — MERGED)
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/372 (CLOSED)
- completed: 2026-07-10 (--auto chain; human-directed merge via the kernel-cdf session; coordinated order #375→#374). Retired to complete.md + worktree/branch cleaned 2026-07-13 (/morning).
- pr: https://github.com/PyAutoLabs/PyAutoArray/pull/375 — MERGED (squash) 2026-07-10.
- summary: rectangular adaptive-mesh `edges_transformed` fix. Consumers `plot/inversion.py` (pcolormesh) + `mesh_geometry/rectangular_rotated.py` both inherit it. Verification upthread on #372. Follow-up mcmc-corner-smoke (a nightly blocker) was queued in planned.md on autofit_workspace/PyAutoFit claims.

## Original prompt

# The - RectangularMagnification light adaptive pixelization visualization show signs of

Type: bug
Target: PyAutoArray
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

The - RectangularMagnification light adaptive pixelization visualization show signs of issue.

In the file @autolens_workspace_develope/@plotting_alignment, I have made lots of visuals of the
rectangular mesh's source reconstruction. I see small offsets compared to plots of sources using other methods,
which I trust more.

Thereofre I think this plotting code @PyAutoArray/autoarray/plot/inversion.py:

        y_edges, x_edges = mapper.mesh_geometry.edges_transformed.T
        Y, X = np.meshgrid(y_edges, x_edges, indexing="ij")
        im = ax.pcolormesh(
            X,
            Y,
            pixel_values.reshape(shape_native),
            shading="flat",
            norm=norm,
            cmap=colormap,
        )
        _apply_colorbar(im, ax, is_subplot=is_subplot)


May be causing a small shift or misalignment?

Can you give me an assesment of of the code and if you think such an issue is feasible?

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
