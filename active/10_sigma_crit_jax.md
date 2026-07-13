# Weak lensing FitWeak upgrades: per-galaxy sigma_crit scaling + JAX support

Type: feature
Target: weak
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Two follow-ups from the completed weak series (epic z_features/weak_shear.md), combined because both rework FitWeak internals:

(1) Per-galaxy sigma_crit (lensing-efficiency) scaling on the redshift storage shipped in 7a: when
WeakDataset.redshifts is present, FitWeak scales the model shear per galaxy by beta_i/beta_ref where
beta = D_ls/D_s (angular diameter distances from the tracer's cosmology; z_ref = the tracer's source-plane
redshift; galaxies at z <= z_lens get zero signal). For is_reduced datasets both gamma AND kappa scale:
g_i = (s_i*gamma)/(1 - s_i*kappa). Datasets without redshifts are unchanged (single effective source plane).

(2) JAX/pytree support for FitWeak, mirroring AnalysisPoint: register_instance_pytree(FitWeak,
no_flatten=(constants)), thread xp through the fit statistics (LensCalc hessian methods already take xp),
AnalysisWeak(use_jax=True) path registers pytrees in fit_from. Default stays use_jax=False. Library unit
tests NumPy-only per repo rules; JAX validation via an autolens_workspace_test parity script
(fitness._vmap per the standing rule), which also un-parks the old fast_visualization D.2.b.iii item.
