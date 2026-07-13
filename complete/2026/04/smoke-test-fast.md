## smoke-test-fast
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/34
- completed: 2026-04-06
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/253, https://github.com/PyAutoLabs/PyAutoGalaxy/pull/325
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/35, https://github.com/PyAutoLabs/autogalaxy_workspace/pull/11

## Original prompt

The workspace scripts are used as integration tests and smoke tests, with
good examples being @autolens_workspace/scripts/imaging/modeling.py
and @autolens_workspace/scripts/interferometer/modeling.py.
PYAUTOFIT_TEST_MODE=2
These run with PYAUTOFIT_TEST_MODE=2, which skips sampling but still performd
a likelihood evaluation to test the model.

However, we would benefit from these smoke tests running a lot faster as they
are a core part of ensuring the software from top to bottom is working. WE ultimately
want all scritps, if possible, to run really fast.

Can you run the abvoe two modeling.py scripts using PYAUTOFIT_TEST_MODE=2 and give a break
down of where the run time is? We can then work towards making them run a lot faster
and thus having quick smoke tests and integration tests.