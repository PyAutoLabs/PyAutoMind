# group/slam.py: the dPIE sigma prior's upper limit can be 0 under test mode (flaky smoke)

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Consequence: judge
Witness: (1) `scripts/group/slam.py` cannot build `af.UniformPrior(lower_limit=0.0, upper_limit=sigma_upper)` with `sigma_upper <= 0`: the bound has a positive floor, or the luminosity it comes from is guarded, and a comment says why; (2) the guarded bound is positive for a total luminosity of 0, a negative value and NaN, and the script runs end to end under the smoke profile (`PYAUTO_TEST_MODE=1` plus the profile defaults) — the earlier "20 runs in a row" was dropped by the human, 2026-11-19, since the guard makes a 0 bound impossible by construction; (3) the full-mode behaviour (a real fit's luminosity-derived bound) is unchanged
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in chat: "do all sensible things before we do another orchestrator run."

## Why

Workspace Smoke run 44573385455 (dispatched 2026-11-19 17:05Z for the M3.7d witness) went red on one script: `autolens_workspace/scripts/group/slam.py`, 4.55 s in, `autonerves.exc.PriorException: The upper limit of a prior must be greater than its lower limit`, at `slam.py:329`, `mass.sigma = af.UniformPrior(lower_limit=0.0, upper_limit=sigma_upper)`. `sigma_upper = 287 * einstein_radius_upper**0.5` comes from the extra galaxies' total MGE luminosity in the light-only result. Under `PYAUTO_TEST_MODE=1` that result is a 20-call search, and its intensities can sum to 0. A re-run of the failed job passed (attempt 2, green), and the script passed locally on the same library SHAs, so this is a flake, not a library break. Since M3.7e a red sweep blocks unattended merges on every repo in autolens_workspace's install chain until a green sweep or `/clear-sweep`, so a flake here can stall a shift.

## Shape

Floor the bound (for example `einstein_radius_upper = max(..., <small positive value>)`) or skip the luminosity scaling when the total is not positive, with a one-line comment. Check the same pattern in the other group/cluster scripts that derive priors from MGE luminosity.
