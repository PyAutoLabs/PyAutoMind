# searches/mcmc.py corner plot crashes under smoke settings

Type: bug
Target: autofit_workspace
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised

Original request (user, 2026-07-09): "yes put mcmc in mind" — file the
smoke-test failure from the 2026.7.9.1 release run.

`autofit_workspace/scripts/searches/mcmc.py` fails in release.yml's
`run_smoke_tests` job (and will fail Heart's `workspace-validation.yml
mode=release` the same way):

```
ValueError: It looks like the parameter(s) in column(s) 0, 1, 2 have no
dynamic range. Please provide a `range` argument.
```

The corner plot receives degenerate Emcee samples under the smoke env profile
(PYAUTO_TEST_MODE / SMALL_DATASETS / FAST_PLOTS — too few steps for any
spread), so `corner` cannot infer axis ranges. Evidence: release run
https://github.com/PyAutoLabs/PyAutoBuild/actions/runs/29041595906 (job
run_smoke_tests autofit_workspace, 2026-07-09).

**Why it now matters more than an advisory red**: the nightly release path is
ARMED (2026-07-09). Stage 3 of every active night runs the workspace script
matrix at release fidelity — this crash makes `release_ready=false` → Heart
not GREEN → the nightly stops and pages. This script is a nightly blocker in
practice until fixed.

Constraints:
- Fix the producer, not with a silent guard (no swallowing the ValueError):
  either give the smoke profile enough steps for spread, or pass an explicit
  `range` to the corner call where degenerate samples are a legitimate smoke
  outcome, or adjust via config/build/env_vars.yaml overrides (NOT os.environ
  mutation) — see feedback memories on smoke env vars.
- Verify with the same env profile CI uses (env_vars.yaml smoke profile), and
  confirm searches/mcmc.py passes locally before shipping.
