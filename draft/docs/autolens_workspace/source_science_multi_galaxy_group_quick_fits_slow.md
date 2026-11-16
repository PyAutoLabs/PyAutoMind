# multi_galaxy and group source_science "quick fits" take many hours

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: low
Status: formalised
Epic: cluster-strong-lensing
Filed: 2026-11-02
Consequence: judge
Review-minutes: 20
Unattended: no
Lane: any

## Original request (human, 2026-11-02)

> yes go ahead and file both

## Problem

Arc phase 7b added a `__Magnification Errors__` section to all 11 `source_science.py` scripts: a quick Nautilus fit
followed by posterior draws. On the single-lens scripts the quick fit takes about 10 minutes on a laptop CPU. The
`scripts/multi_galaxy/source_science.py` quick fit (two lenses with linear Sersic light and Isothermal mass, free
centres, MassField shear, SersicCore source; ~30 free parameters, Nautilus n_live=200, PositionsLH 0.3) was still in
Nautilus's exploration phase (N_eff 4, f_live 1.0) after ~400k likelihood calls and ~9 h of laptop time, and was
stopped. The group scripts and the multi_galaxy/group MGE and pixelization variants use similar models and were not
run in full. The human judged further end-to-end validation runs unnecessary; the scripts currently say the fit
"can take several hours".

## Expected

The multi_galaxy and group quick fits finish in a time a reader will wait for (tens of minutes), for example by
putting Gaussian priors on the lens centres around the known values, fixing the lens light to the true model, or
reducing the source model, explained in the script's prose. Update the "can take several hours" wording to the
measured time.

Witness: one full (non-smoke) run of each changed script converges, with its fit time quoted in the prose.
Note: never run smoke and full runs of scripts sharing a dataset folder concurrently, and move any cached output
aside before rerunning (both bit phase 7b).
