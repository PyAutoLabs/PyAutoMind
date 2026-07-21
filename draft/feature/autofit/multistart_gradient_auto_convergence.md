# Auto-convergence (early stopping) for the multi-start gradient searches

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Feature: auto-convergence (early stopping) for the multi-start gradient searches in @PyAutoFit (af.MultiStartProdigy/MultiStartAdam/MultiStartADABelief/MultiStartLion). Today AbstractMultiStartGradient runs a FIXED n_steps budget with NO convergence criterion — users must guess n_steps and there is no auto-stop. Add a first-class 'auto' mode (default True) so users don't hand-tune step count. Mirror the existing AutoCorrelationsSettings precedent (Emcee/Zeus terminate early on a convergence check): a MultiStartGradientConvergence-style settings object with check_for_convergence=True, a plateau check on the GLOBAL best figure-of-merit over a window (rtol/atol + min_steps), keeping n_steps as a HARD CEILING/max budget (never runs forever). The loop already tracks best_fom + fom_history and checkpoints at iterations_per_full_update boundaries, so the check slots in there. SCOPE: PARAMETRIC SOURCES ONLY for now (MGE/Sersic, the smooth well-behaved regime where global-best plateau genuinely means converged). Pixelized is explicitly OUT OF SCOPE — its best-fom climbs in long plateaus punctuated by breakthrough jumps (resurrection churn), so plateau detection false-stops there; the real goal for pixelized is making the LIKELIHOOD smooth (localise/fix the non-finite regions), not band-aiding the optimizer. So when resurrect=True the auto behavior stays conservative/off and leans on the ceiling. Results contract (part 2, must ship together): add converged:bool + stop_reason ('converged'|'max_steps') + the convergence settings to samples_info; surface the fom_history convergence trace in the standard result artifacts so users can verify the plateau; and extend aggregator/samples_summary test coverage for variable-length runs (guard the known zero-weight/NaN diagnostic-row aggregator IndexError edge). Likely large -> phase into (1) convergence loop + settings, (2) results-contract + aggregator hardening. Unit tests numpy-only; JAX validation in autofit_workspace_test. Successor to the multi-start gradient v2 work (contrib rules + resurrection, Fit#1398/#1400).

<!-- formalised by the Intake (Conception) Agent on 2026-07-21 from user-intake -->
