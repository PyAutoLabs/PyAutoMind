## power-law-omega-convergence
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/125
- completed: 2026-08-14
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/126
- merge-commit: ee8a34c51d1fc3fc8f1913964fff9c73eeff0b5a
- summary: Bounded the fixed 20-term JAX PowerLaw omega recurrence across the packaged slope and ellipticity priors, measured its JAX transformation and CPU cost, and carried the backend difference through a complete 7x7 `FitImaging` fixture. The stable finding remains persistent profiling evidence.
- validation: GitHub Actions lint run 31812775745 succeeded at the exact merged PR head across ruff lint/format, README idempotence, 41 tests, links, and all section smoke tests. The one-shot evidence run 31811929415 also succeeded with JAX 0.10.2 on CPU and the full PyAuto source stack.
- evidence: The 20-term angular series exceeds `1e-4` relative error over 0.05736 absolute default-prior mass. Covering the live 0.999 ellipticity clamp at that tolerance needs 10,240 terms. A static binned `lax.switch` policy retains reverse-mode differentiation and `vmap`, but is 125.3x slower than 20 terms at the clamp; the bounded complete-likelihood grid moved by at most 0.005575 log-likelihood units.
- decision: No PyAutoGalaxy source issue was opened. The tested candidate did not meet the prompt's requirement to improve accuracy without imposing worst-case cost on ordinary shapes, and the bounded likelihood probe did not establish materiality sufficient to justify that cost.
- release: not performed; this merged profiling research changes no packaged library behavior.

## Original prompt

# Bound PowerLaw omega-series accuracy and cost

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Source: `component.power-law.series-vs-hyp2f1-divergence`
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/125

The JAX PowerLaw deflection path uses a fixed 20-term Tessore–Metcalf omega series while NumPy uses SciPy hyp2f1. The stable detector measures a reachable, science-affecting relative deflection error of 0.297 at factor 0.99.

Map accuracy and cost over public slope, ellipticity factor, angular coordinates, term policy, and actual prior reachability. Exercise eager, jit, reverse-mode grad, and vmap. Include cold-compile and warm-runtime cost plus at least one complete likelihood sensitivity probe.

A constant term-count bump is not an adequate answer: the initial sweep shows ordinary factors converge quickly but factor 0.99 can need more than 1280 terms, depending on slope. Evaluate statically binned lax.cond/lax.switch scans, and reject dynamic-loop candidates that lose reverse-mode differentiation.

Retain the stable finding ID. Do not modify PyAutoGalaxy in this task. Open a bounded source issue only if the evidence identifies a defensible policy that improves accuracy without imposing worst-case cost on ordinary galaxy shapes.
