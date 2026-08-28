# multi_dataset/jax_likelihood/delaunay.py exceeds the 1800s release-profile cap — hangs after the vmap JIT…

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoFit
- PyAutoLens
- autolens_workspace_test
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Issued: 2026-08-28

Found 2026-08-28 by PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33177898708, job
`integrate / run_scripts (3.12, autolens_test, multi_dataset)`, env profile
`profile_release.yaml`.

`autolens_workspace_test/scripts/multi_dataset/jax_likelihood/delaunay.py`:

    status: timeout
    elapsed: 1805.07 s
    cap:     1800 s     ("Timed out after 1805s (cap 1800s)")

It passed under the Workspace Smoke run
(https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33179766004), so this is
release-profile specific.

## The strongest clue: it is not the JIT

The captured stdout tail shows the script got through JAX compilation quickly
and then went quiet for the remaining ~29 minutes. Script start 14:02:27; the
last lines written were at 14:03:10:

    2026-08-28 14:03:10,858 - autofit.non_linear.jax_compile - INFO - JAX jit
      compilation of vectorized (vmap) likelihood function: result materialized
      in 0.0 seconds.
    2026-08-28 14:03:10,858 - autofit.non_linear.jax_compile - INFO - JAX jit
      compilation of vectorized (vmap) likelihood function complete in 9.3 seconds.
    [-8853.06659309 -8853.06659309 -8853.06659309]
    JAX Time To VMAP + JIT Function 9.286787271499634

So the vmap + JIT stage cost 9.3 s and produced a finite, self-consistent
likelihood. The hang is in whatever the script does *after* that line — the
next stage (gradient / jacobian compile, or a further eval) never printed
anything for ~1795 s. Profile that stage, not the vmap JIT.

## It is also specific to this one script

Every sibling in the same directory passed comfortably in the same job — the
directory's total was 2155.9 s of which this script alone was 1805 s:

    delaunay.py              TIMEOUT  1805.1 s
    delaunay_mge.py          passed     28.6 s
    rectangular.py           passed     18.2 s
    rectangular_mge.py       passed     24.6 s
    rectangular_mge_rtu.py   passed     25.7 s
    mge_group.py             passed     62.8 s
    shared_preloads.py       passed     48.7 s
    dataset_model.py         passed     18.6 s

`delaunay_mge.py` finishing in 28.6 s while plain `delaunay.py` hangs is the
sharpest lead available: the two differ in the source light model, so compare
them directly.

## What to do

- Reproduce locally under `profile_release.yaml` with the workspace CWD, and
  bisect the script by stage to find which post-vmap stage never returns.
- Candidate causes to rule in or out: a gradient/jacobian compile that blows up
  on the Delaunay mesh (there is prior history of Delaunay-family gradient
  pathologies — sqrt/dual-area NaN, non-jittable split regularization); a
  preload path that is rebuilt per dataset instead of shared; a multi-dataset
  fan-out that multiplies compile count by the number of datasets.
- Fix in the library if the cost is a library pathology; otherwise adjust the
  script's release-profile configuration. The likely loci are PyAutoArray (the
  Delaunay mesh / regularization and its gradient), PyAutoLens (the multi-dataset
  analysis fan-out) and PyAutoFit (the jax_compile stage that logs the timings
  above) — establish which by profiling before editing any of them.

## Out of scope

Explicitly NOT acceptable as a fix: adding a silent guard, mutating env vars
inside the script to dodge the cost, disabling JAX for this script, or simply
raising the cap without first explaining where the 1795 s goes.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/682229dd-73ea-488e-8436-f7a3e9ef00e7/scratchpad/bug3.txt -->
