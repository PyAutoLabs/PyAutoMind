# Weak lensing shear profile and convergence map visualization

Type: feature
Target: weak
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Weak lensing shear profile and convergence map visualization. Add the two canonical cluster weak-lensing diagnostics missing from autolens/weak/plot: (1) an azimuthally averaged tangential and cross shear radial profile helper (binned gamma_t / gamma_x vs radius with error bars, cross-shear as the standard B-mode null test) computed about a chosen centre from a WeakDataset or FitWeak; (2) a Kaiser-Squires style convergence map reconstruction plotted from the shear field. Re-export into aplt alongside the existing nine quiver helpers and demo both in autolens_workspace/scripts/weak (extend simulator.py / fit.py outputs). Tangential shear profiles are THE standard observable in cluster weak lensing (Oguri 2012 SGAS; Medezinski 2016 A2744).

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
