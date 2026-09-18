# `files/*_experiment.py` import a module that no longer exists — decide whether to keep them

Type: maintenance
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Consequence: glance
Witness: every script under `PyAutoArray/files/` either imports successfully against the installed stack, or is gone; `git grep -c rectangular_spline` returns 0.
Review-minutes: 3
Unattended: ready

## The finding

`PyAutoArray/files/ghost_peak_experiment.py:51` and `files/pca_rotation_experiment.py:40` both do:

    from autoarray.inversion.mesh.interpolator.rectangular_spline import (...)

That module does not exist. The live contents of
`autoarray/inversion/mesh/interpolator/` are `abstract.py`, `delaunay.py`, `knn.py`,
`rectangular.py`, `rectangular_uniform.py`, `sibson.py`. So both scripts fail at import.

Independently confirmed by the workspace's own PyAuto API gate, which refused an import
attempt with: *"STALE `autoarray.inversion.mesh.interpolator.rectangular_spline` — not in
installed stack (missing `.rectangular_spline`); closest live names: rectangular"*.

## Provenance

Both were committed with the `rectangular-adapt-cdf` spike (`f9aceea3`, `f9c6d218`) and the
module has since been renamed or removed. Their docstrings still told readers to
`source ~/Code/PyAutoLabs-wt/rectangular-adapt-cdf/activate.sh` — a task bundle long gone —
which is corroborating evidence that nothing has run them since. Those docstring lines were
corrected in PyAutoBrain#393 (phase 2 of the workspace regroup); the dead import was left
alone as out of scope for a prose fix, and is filed here instead.

Nothing references either file except each other and `files/ghost_peak_findings.md`.

## The decision, which is a human's

Not obviously a bug to fix — the question is whether these spike scripts are still wanted:

- **Keep and repair** — repoint the import at whichever live module replaced
  `rectangular_spline` (`rectangular.py` / `rectangular_uniform.py`), and check the symbols
  they import still exist under their new names. Only worth it if the experiments are still
  interesting.
- **Retire** — delete both scripts, and decide separately whether `ghost_peak_findings.md` is
  a result worth keeping without the script that produced it (it may well be: the finding
  outlives the spike).

Do not "fix" them by guessing an import that makes them parse. If they are kept they should
actually run.
