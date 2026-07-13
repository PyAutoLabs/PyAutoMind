## test-mode-separate
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1193
- completed: 2026-04-12
- library-pr: https://github.com/PyAutoLabs/PyAutoConf/pull/86, https://github.com/PyAutoLabs/PyAutoFit/pull/1195, https://github.com/PyAutoLabs/PyAutoArray/pull/265, https://github.com/PyAutoLabs/PyAutoGalaxy/pull/343, https://github.com/PyAutoLabs/PyAutoLens/pull/432
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/29, https://github.com/PyAutoLabs/autogalaxy_workspace/pull/25, https://github.com/PyAutoLabs/autolens_workspace/pull/51

## Original prompt

PYAUTOFIT_TEST_MODE has become a bit of a catch all term for things I dont want to run when testing,
it incldues disable some visualization and posiition resmapling in autolens as opposed to just
making the sampler run faster.

Furthermore, there is also PYAUTOARRAY_OUTPUT_MODE which outputs images to hard disk, which si use.

Can you look at all PYAUTOFIT_TEST_MODE clauses and work out which are not doing a sampler speed up.
Can you then suggest names for us to use for them all.

I also want us to move to environment variables just being PYAUTO, so PYAUTO_TEST_MODE, PYAUTO_OUTPUT_MODE,
we will also rename PYAUTO_WORKSPACE_SMALL_DATASETS to PYAUTO_SMALL_DATASETS.