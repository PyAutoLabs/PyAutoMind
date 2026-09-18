# The latent smoke's empty-block assertion names one cause unconditionally — echo the real warning instead

Type: test
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Themes:
- ci-smoke
- jax-compile
Difficulty: small
Autonomy: safe
Priority: normal
Status: draft
Consequence: notify
Witness: with the latent block deliberately emptied by a cause OTHER than the model-assertion one (e.g. a raising profile reached through a latent), the assertion message quotes the `compute_latent_samples` warning / traceback taken from `search.log`, and no longer states PyAutoLens#734 / PyAutoFit#1600 as the cause.
Review-minutes: 0
Unattended: ready
Filed: 2026-09-18

`autolens_workspace_test/scripts/misc/latent/latent_integration_smoke_jax.py`
(the `__On-Disk Assertions__` block, ~line 304) asserts exactly one
`files/latent/latent_summary.json` and tells the reader what an empty list means:

> An EMPTY list is the PyAutoLens#734 / PyAutoFit#1600 failure: the model assertion
> raised inside the latent engine's per-sample `jax.jit` for every sample, so the whole
> latent block was dropped.

It attributes **any** empty latent block to that one cause, **unconditionally**.

In the real incident the cause was entirely different: a **JAX 0.11.2
`functools.partial` regression in PyAutoGalaxy's zero-contour solver**, reached via the
`effective_einstein_radius` latent, fixed by `90e757d3`. The assertion confidently
pointed the investigation at the wrong two issues.

PyAutoFit already writes what actually happened: the `compute_latent_samples`
warning and traceback land in `search.log`. **Echoing that into the assertion message
would have turned a multi-hour investigation into a two-minute diagnosis.**

The change is small and deliberately narrow: on failure, read the run's `search.log`,
pull the `compute_latent_samples` warning / traceback if present, and include it in the
message; keep the #734 / #1600 note only as *one possible* cause, or drop it. If no
such warning is found, say so — "no `compute_latent_samples` warning in `search.log`"
is itself a useful line, because it rules the known class out.

Filed 2026-09-18 from the flat-`fields=` adoption sweep (issue autolens_workspace#561),
whose own investigation hit exactly this misdirection.
