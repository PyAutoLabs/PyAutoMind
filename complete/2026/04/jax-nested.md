## jax-nested
- issue: https://github.com/Jammy2211/autofit_workspace_developer/issues/5
- completed: 2026-04-14
- workspace-pr: https://github.com/Jammy2211/autofit_workspace_developer/pull/6

## Original prompt

The file @autofit_workspace_developer/searches_minimal has examples which run an autofit toy model using
searches with a minimal interface.

This paper presents a JAX GPU nested sampling search:

https://arxiv.org/abs/2601.23252

Which has a public giuthub:

https://github.com/yallup/nss/

Can you implement it using a new simple search_minimal? If you need a gradient it should be simple to
extend the likleihood function to include a gradient. Ideally you would show fits which just use jax.jit
and which use the jax.grad functionality.