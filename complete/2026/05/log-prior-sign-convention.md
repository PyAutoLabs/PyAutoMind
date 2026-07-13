## log-prior-sign-convention
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1266
- completed: 2026-05-15
- library-prs:
  - PyAutoFit: https://github.com/PyAutoLabs/PyAutoFit/pull/1269
  - autofit_workspace_test: https://github.com/PyAutoLabs/autofit_workspace_test/pull/27
- notes: |
    Sign-convention fix for Prior.log_prior_from_value across the Gaussian-family
    priors and LogUniformPrior. Switched to density form (log p(x), negative for
    low-density, zero at mode). NormalMessage flipped to -(value-mean)**2/(2σ**2);
    LogGaussianPrior similarly with the -log(value) Jacobian preserved;
    LogUniformPrior replaced 1.0/value (Jacobian gradient, not a log) with
    -log(value) on NumPy + xp.where(in_bounds, -xp.log(value), -xp.inf) on JAX.
    UniformPrior and TruncatedNormalMessage already correct. No Fitness changes —
    sign lives entirely at the Prior boundary, as architecture demanded.

    Empirically confirmed bug by two controlled experiments (Emcee + LBFGS,
    flat likelihood + GaussianPrior(5,1)) — pre-fix they diverged to 10^146 and
    8e143 respectively; post-fix both behave correctly. Both scripts promoted
    to autofit_workspace_test/scripts/prior_correctness/ as permanent regression
    gates that fail loudly if any future refactor reverts the sign.

    Validation: pytest test_autofit 1242 passed, 1 skipped; 4 test pins updated
    (test_prior.py + test_model_mapper.py — they had rubber-stamped the buggy
    values); priors_xp_dispatch.py 28 assertions pass (24 existing parity + 4
    new density-form gates); 4 autofit_workspace searches pass; EP runs to
    completion (confirmed unaffected — uses Message.logpdf directly); 44/44
    5-workspace smoke green.

    Bug existed since commit db4016db42 (4 May 2022) for LogUniformPrior and
    pre-dates that for the Gaussian family — ~4 years. Hidden because (a) most
    production fits use nested samplers which bypass log_prior_from_value, (b)
    most MCMC fits used UniformPrior which is sign-agnostic, (c) the existing
    test pins rubber-stamped the wrong values.

    Migration warning: cached Emcee/Zeus/MLE-Drawer/LBFGS/BFGS samples.csv with
    non-uniform priors are biased and should be re-run. Dynesty/Nautilus chains
    unaffected (priors via prior_transform); only their stored log_prior column
    is wrong-signed and auto-recovers on next aggregator load.
