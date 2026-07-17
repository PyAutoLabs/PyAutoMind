# Claude Development Prompt: Port lensing_potential_correction into the PyAuto stack

Type: feature
Target: PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> This is an implmeentation of the potential corrections, which supports
> PyAutoLens, can you take this and incorporate it proeprly into the PyAuto
> ecosystem source code:
> https://github.com/caoxiaoyue/lensing_potential_correction . It uses a lot
> of linear algebra, so maybe belongs in the autoarray inversion module, but
> its also very lensing specific so could go further down. For now, dont
> worry about JAX, we have a JAX code whichw e can bring in in a future PR,
> or maybe I'll just ask you to do it later. Also make sure docs and other
> materials cite this properly
> https://github.com/caoxiaoyue/potential_correction_paper.

## Goal

Incorporate Xiaoyue Cao's `potential_correction` package (the gravitational-
imaging technique: pixelised corrections dpsi to the lensing potential,
reconstructed jointly with the pixelised source by maximising Bayesian
evidence, Matern-family regularisation) into the PyAuto libraries proper,
replacing its wrapper-over-2024.1.27.4 status with first-class, tested,
maintained source code on the current API.

## Constraints and notes

- NumPy/numba implementation only in this PR — the JAX port is a known
  follow-up (external JAX code exists and will be brought in later).
- The external code targets autolens 2024.1.27.4; the port must modernise to
  the current API (Tracer construction, over-sampling instead of
  SettingsImaging sub_size, aa.decorators, current mask/grid attributes).
- autoarray already ships Gaussian/Exponential/Matern kernel regularizations
  (inversion/regularization/*_kernel.py) — reuse, do not duplicate Cao's
  covariance_reg equivalents.
- Do not adopt the external repo's heavy optional deps (GPy, multiprocess,
  powerbox, numba-scipy) as library requirements.
- Layering: generic masked-grid sparse differential operators and any new
  generic regularizations belong in autoarray's inversion layer; the dpsi
  mesh/pairing, joint source+dpsi fit, Analysis classes and visualization are
  lensing-specific and belong in PyAutoLens (cf. the `autolens/weak`
  subpackage precedent); pixelised Input-deflections/potential mass profiles
  belong in PyAutoGalaxy.
- Citation: docs, docstrings and README materials must cite Cao et al. (2025)
  via https://github.com/caoxiaoyue/potential_correction_paper and credit
  https://github.com/caoxiaoyue/lensing_potential_correction as the origin.

## Acceptance criteria

- Potential-correction fit (dpsi-only and joint source+dpsi) runnable from
  the installed stack on current main, with unit tests (numpy-only, no JAX).
- No duplicated regularization/operator code between autoarray and the port.
- Citations present in the new modules' docstrings and the relevant docs.
