## repin-rectangular-mge-after-490
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/286
- completed: 2026-08-28
- workspace-pr: autolens_workspace_test#288 (merged d40e7df8 -> main)
- what shipped: re-pinned two `imaging/jax_likelihood` rectangular-MGE vmap likelihood constants —
  `scripts/imaging/jax_likelihood/rectangular_mge.py` `-85.41696632` -> `-105.52806249`, and
  `scripts/imaging/jax_likelihood/rectangular_mge_rtu.py` `-11.65793201` -> `-131.56973816`.
  **No library change** — re-pin only.
- attribution (bisected, not assumed): both moves are attributable solely to PyAutoArray #490 (`72fb01d1`), a *verified correctness fix* to the rectangular mapper's row weights and integer-bracket cells whose own PR states that downstream constants must be regenerated. The regen commit `f0ef8f2` skipped exactly these two scripts because they hung on the vmap stall that `7d803e7` fixed the next day — so the pins were never stale by neglect, they were deferred and then forgotten.
- the scary-looking number that isn't: the RTU pin moves ~10x in relative terms, which reads like a regression. It is a near-zero baseline — the absolute move is -120 against -20 for the plain script, while #490 moved sibling pins by +-8000. Judge pin moves in absolute log-evidence, not as ratios off a value near zero.
- correctness evidence beyond the bisect: post-fix fits are sane — no NaNs, mapper rows sum to 1, reduced chi^2 ~ 3.6, and the Bilinear and RTU meshes now agree to within 26 in log-evidence where they were 74 apart before. The fix moved the two meshes *together*, which is what a correctness fix should do.
- validation: both scripts run to completion locally (exit 0, 60 s / 50 s) under the smoke profile with their `ENV: jax full_datasets` declaration — the eager-vs-jit round-trip asserts that sit after the pin execute for the first time and pass. Siblings `multi_dataset/jax_likelihood/rectangular_mge{,_rtu}.py` still pass untouched.
- heart context: corrective PR for the Heart RED reason `workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, autolens_test scripts/imaging/rectangular_mge_rtu.py)`.
- parallel worktrees: `autolens_workspace_test` was claimed simultaneously by `requarantine-delaunay-and-keep-abort-stack` (#287) on its own worktree and branch; file sets disjoint (`scripts/imaging/jax_likelihood/rectangular_mge*.py` here vs `config/build/no_run.yaml` there). Both merged cleanly.

## Original prompt

# rectangular_mge JAX vmap likelihood pins are 0.24 / 10.3 relative diff off…

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace_test
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-08-28

Found 2026-08-28 by PyAutoHeart. This blocks BOTH the workspace smoke wave and
the release integrate wave, and is the top contributor to today's local
readiness verdict RED 45.

- Workspace Smoke run: https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33179766004
  (job `smoke / run_scripts (3.12, autolens_test, imaging)`, profile_smoke.yaml)
- Release Integrate run: https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33177898708
  (profile_release.yaml)

Both runs reproduce it, so it is not profile-specific.

## The failure

Two scripts in `autolens_workspace_test` fail at the same line — line 306,
`np.testing.assert_allclose(..., rtol=1e-4)`, message
"rectangular_mge: JAX vmap likelihood mismatch":

`scripts/imaging/jax_likelihood/rectangular_mge.py` (failed after 27.8s):

    AssertionError:
    Not equal to tolerance rtol=0.0001, atol=0
    rectangular_mge: JAX vmap likelihood mismatch
    Mismatched elements: 6 / 6 (100%)
     [0]: -105.52806248678235 (ACTUAL), -85.41696632 (DESIRED)
    Max absolute difference among violations: 20.11109617
    Max relative difference among violations: 0.23544615
     ACTUAL: array([-105.528062, -105.528062, -105.528062, -105.528062, -105.528062, -105.528062])
     DESIRED: array(-85.416966)

`scripts/imaging/jax_likelihood/rectangular_mge_rtu.py` (failed after 28.6s):

    Mismatched elements: 6 / 6 (100%)
     [0]: -131.56973816080836 (ACTUAL), -11.65793201 (DESIRED)
    Max absolute difference among violations: 119.91180615
    Max relative difference among violations: 10.28585568
     ACTUAL: array([-131.569738, -131.569738, ...])
     DESIRED: array(-11.657932)

Note the two scripts have moved by very different amounts: the plain
rectangular_mge pin is off by 24%, the RTU variant by a factor of ~10.3. That
asymmetry matters — a single re-pin story has to explain both, and a 10x move
on the RTU mesh is not obviously "a small numerical refinement".

All 6 vmap lanes agree with each other to the printed digits in both cases, so
the vmap/batching machinery itself is self-consistent; what has moved is the
scalar likelihood value, not the vectorisation.

## The fix-locus question this task must answer FIRST

Do not re-pin on sight, and do not start patching the library on sight. The
whole point of this task is to establish which of the two it is:

1. **Stale pin** — a deliberate library change moved the rectangular / MGE
   likelihood and the workspace pins were never updated. If so the fix is to
   re-pin, and the prompt/PR must carry the *justification*: which commit moved
   it, why that change is correct, and why the new value is the right one.
2. **Genuine regression** — a library change moved the likelihood by accident.
   If so the fix is in the library and the pins stay.

Required procedure:

- Reproduce both scripts locally against the installed stack.
- Attribute the move: `git bisect` (or targeted `git log -S` / checkout-and-run)
  across recent `main` commits in PyAutoArray / PyAutoGalaxy / PyAutoLens until
  the commit that moved the value is named.
- Then, and only then, decide re-pin vs library fix, and record the decision.

## Bisect candidates (starting points, not conclusions)

Recent `main` commits that plausibly touch a rectangular + MGE + linear-solve
likelihood:

- PyAutoArray `72fb01d1` "fix: correct mirrored row weights + round-off-dependent
  cells in rectangular mapper" (#490) — directly touches the rectangular mapper's
  bilinear row weights; a prime suspect for both scripts, and the RTU asymmetry.
- PyAutoArray `051cfd3e` "fix: form the reconstruction covariance on the
  parameters the solve solved for" and `a7703a2e` "fix: correct the NaN/zero
  invariant, and record the measured value change" (#493) — the second commit
  message explicitly says a measured value changed.
- PyAutoArray `0ff036ac` "perf: reuse precomputed Convolver state, cache
  operated-matrix dict, hoist linear-func pair loop" (#497).
- PyAutoGalaxy `10f5047e` "perf: batch MGE linear-func PSF convolution on the
  numpy path" (#588) — the MGE half.
- PyAutoGalaxy `3913c688` / PyAutoLens `253341a96` "rectangular mesh split
  follow-up — RTU/Bilinear prior configs" (#579 / #707) — especially relevant to
  the RTU variant's much larger move.

A `perf:` commit that moves a likelihood by 24% is itself a finding, not a
re-pin.

## Out of scope

Do not "fix" this by loosening `rtol`, by wrapping the assert in a guard, or by
skipping the scripts. The pin exists to catch exactly this.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/682229dd-73ea-488e-8436-f7a3e9ef00e7/scratchpad/bug1.txt -->
