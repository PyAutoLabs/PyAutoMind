# nautilus_plotter.py corner_cornerpy raises ValueError "range is not valid or the sample…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Found 2026-08-28 by PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33177898708, job
`integrate / run_scripts (3.12, autofit, plot)`, env profile
`profile_release.yaml`. Failed after 3.1s.

`autofit_workspace/scripts/plot/nautilus_plotter.py` fails; the sibling
`emcee_plotter.py` passed (8.3s) in the same job, and `dynesty_plotter.py`,
`get_dist.py`, `zeus_plotter.py` are skipped, so nautilus is the only live
failure in that directory.

## Traceback tail

Preceded by three warnings that are themselves the tell — the sample handed to
corner is degenerate before corner ever rejects it:

    scipy/stats/_kde.py:588: RuntimeWarning: Degrees of freedom <= 0 for slice
      self._data_covariance = atleast_2d(cov(self.dataset, rowvar=1,
    numpy/lib/_function_base_impl.py:2901: RuntimeWarning: divide by zero encountered in divide
      c *= np.true_divide(1, fact)
    corner/core.py:922: UserWarning: Attempting to set identical low and high ylims
      makes transformation singular; automatically expanding.

then:

    Traceback (most recent call last):
      File ".../workspace/scripts/plot/nautilus_plotter.py", line 106, in <module>
        aplt.corner_cornerpy(
      File ".../autofit/non_linear/plot/plot_util.py", line 112, in wrapper
        return func(*args, **kwargs)
      File ".../autofit/non_linear/plot/samples_plotters.py", line 80, in corner_cornerpy
        corner.corner(data=data, **settings)
      File ".../corner/corner.py", line 248, in corner
        return corner_impl(
      File ".../corner/core.py", line 370, in corner_impl
        hist2d(
      File ".../corner/core.py", line 687, in hist2d
        raise ValueError(
    ValueError: It looks like the provided 'range' is not valid or the sample is empty.

## It did NOT fail under smoke

This did not reproduce in the same day's Workspace Smoke run
(https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33179766004). So it may
well be **release-profile specific**: the release profile runs the sampler for
real rather than in the truncated smoke configuration, so the Nautilus samples
object the plotter is handed differs between the two profiles. Establish which
profile produces which sample shape before assuming a plotting bug.

## What to investigate

- Reproduce under `profile_release.yaml` (not smoke) with the workspace CWD.
- Determine what `data` actually is at `samples_plotters.py:80` — empty,
  single-row, or zero-variance in one or more parameters. The `Degrees of
  freedom <= 0` KDE warning points at a sample with <= 1 effective row for at
  least one slice.
- Then decide the locus: is the Nautilus samples -> corner data conversion in
  PyAutoFit dropping or collapsing samples, or is the workspace script asking
  for a corner plot of a search result that legitimately has too few samples
  under this profile?

## Out of scope

Do not fix this by try/excepting the plot call, by skipping the script, or by
adding a silent "if the sample is empty, return" guard. If the sample really is
degenerate, the fix is upstream of the plot.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/682229dd-73ea-488e-8436-f7a3e9ef00e7/scratchpad/bug2.txt -->
