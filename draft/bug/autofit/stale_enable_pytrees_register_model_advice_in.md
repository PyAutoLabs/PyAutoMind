# Stale enable_pytrees register_model advice in NUTS and SMC errors and searches docs

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Witness: grep -rn enable_pytrees autofit/ autofit_workspace/scripts/searches/ returns no user-facing advice; BlackJAXNUTS with use_jax=False raises an error that names use_jax=True only.
Review-minutes: 20
Unattended: ready

Stale enable_pytrees register_model advice in NUTS and SMC errors and searches docs
Type: bug
Target: PyAutoFit
Difficulty: small
Autonomy: safe
Witness: grep -rn enable_pytrees autofit/ autofit_workspace/scripts/searches/ returns no user-facing advice; BlackJAXNUTS with use_jax=False raises an error that names use_jax=True only.

autofit/non_linear/search/mcmc/blackjax/nuts/search.py:270 and autofit/non_linear/search/mcmc/blackjax/smc/search.py:328 tell users to call enable_pytrees() / register_model(model), and the workspace script scripts/searches/mcmc.py lines 244-247 and 283-286 do the same in prose and code. Neither function is exposed on the af namespace and Fitness.__init__ (autofit/non_linear/fitness.py:261-265) already calls them internally; scripts/searches/mle.py:232-235 in the same workspace says the opposite. NUTS was verified to run without them on 2026-09-10. Fix the two error strings and the mcmc.py prose (the workspace half lands in autofit_workspace).

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->
