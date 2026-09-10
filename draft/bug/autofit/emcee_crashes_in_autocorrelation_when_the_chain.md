# Emcee crashes in autocorrelation when the chain is too short

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Witness: af.Emcee(nwalkers=10, nsteps=50).fit(...) on the 1D Gaussian example completes with a warning instead of raising IndexError.
Review-minutes: 20
Unattended: ready

Emcee crashes in autocorrelation when the chain is too short
Type: bug
Target: PyAutoFit
Difficulty: small
Autonomy: safe
Witness: af.Emcee(nwalkers=10, nsteps=50).fit(...) on the 1D Gaussian example completes with a warning instead of raising IndexError.

af.Emcee with too few steps crashes instead of degrading gracefully: nwalkers=10, nsteps=50 raises IndexError: index 0 is out of bounds for axis 0 with size 0 from emcee/autocorr.py:38 via autofit/non_linear/search/mcmc/emcee/search.py:353, because the autocorrelation analysis has no usable samples. Skip or warn on the autocorrelation check when the chain is shorter than it needs, rather than failing the fit. Found 2026-09-10 (a tutorial had to use nsteps=500 to avoid it).

<!-- formalised by the Intake (Conception) Agent on 2026-09-10 from user-intake -->
