## blackjax-nuts-example
- issue: https://github.com/Jammy2211/autofit_workspace_developer/issues/13
- completed: 2026-05-06
- workspace-pr: https://github.com/Jammy2211/autofit_workspace_developer/pull/14
- repos: autofit_workspace_developer
- notes: Added `searches_minimal/nuts_jax.py` — BlackJAX NUTS on the same 1D Gaussian as the rest of the JAX scripts. Window adaptation tunes step size + diagonal inverse mass matrix; sampling runs in a JIT'd `jax.lax.scan`. Recovers truth in 1.83s, ESS 1216/2000, 0 divergences — fastest JAX path in the folder (beats nss_grad's 5.2s). Also wrote a non-git follow-up `z_projects/concr/scripts/cancer_sim/graphical_nuts.py` that runs joint NUTS over the 93-dim cancer-sim factor graph (4.4s wall, ESS 880/1000, 0 divergences); kept local since z_projects isn't tracked. Pre-task: shipped the unregistered `feature/searches-minimal-converged` work first (PR #12 — shared `_metrics.MLTracker` across all searches_minimal scripts) so this task could use `MLTracker.from_log_l_history` for evals/time-to-ML.
