## requarantine-delaunay-and-keep-abort-stack
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/287
- completed: 2026-08-28
- workspace-pr: autolens_workspace_test#289 (merged 20377c91 -> main)
- library-pr: PyAutoHands#271 (merged 17308862 -> main)
- what shipped:
  - `autolens_workspace_test/config/build/no_run.yaml` — `multi_dataset/jax_likelihood/delaunay.py` re-quarantined as `NEEDS_FIX 2026-08-28` with the evidence; history note updated.
  - `PyAutoHands/autohands/build_util.py` — `_timeout_output` now keeps the faulthandler stack that `kill_group` SIGABRTs the child specifically to produce.
- diagnosis (and what it is NOT): the script hung 1805 s at the release cap in integrate run 33177898708 *after* completing vmap+JIT in 9.3 s — the second, already-compiled `fitness._vmap` call (`delaunay.py:208`, 1.8 s locally) deadlocked. Not a release-profile difference: the script's own `ENV: jax full_datasets` makes smoke and release identical for it (only `PYAUTO_TEST_MODE`/`PYAUTO_FAST_PLOTS` differ and neither is read on this path), and smoke ran the same program in 18.9 s the same day. Not Delaunay-specific: it is the XLA CPU `FftThunk`/ducc0 Eigen-pool futex deadlock root-caused in `complete/2026/08/xla-cpu-eigen-pool-deadlock.md`, which `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false` (already in force on the failing run) reduces but does not eliminate. Not reproducible on an 8-core WSL box (4/4 pass). **Nothing in PyAutoArray or PyAutoLens to fix.** The script had been restored from `no_run.yaml` on 2026-08-27 by PyAutoFit#1528 on 24/24 clean re-times; this is the first hang since.
- the Hands half, and why it mattered here: `kill_group` SIGABRTs a timed-out child precisely so the child leaves a faulthandler stack — and `_timeout_output` then kept only the last `TIMEOUT_OUTPUT_TAIL_CHARS = 2000` characters of stderr. The dump's trailing `Extension modules: ... (total: 86)` list alone is ~1900 of them, so **the one diagnostic the runner exists to capture was written and then discarded.** That is why this hang had to be attributed by family match to the eigen-pool epic instead of by its own stack. `_timeout_output` now detects a dump (`Fatal Python error:` / `Current thread 0x`), drops the `Extension modules:` paragraph, keeps the dump whole, and applies the tail cap only to the text before it. No behaviour change when no dump is present.
- validation: skip-list discovery checked through `autohands.build_util.should_skip` on both the raw YAML list (as `run.py` passes it) and `no_run_list_with_extension_from(..., '.py')` — `delaunay.py` SKIP, `delaunay_mge.py` and `imaging/jax_likelihood/delaunay.py` still RUN — against a **baseline control** run on `no_run.yaml` at HEAD showing all three RUN before the edit. `slow_skip_check.py`'s NEEDS_FIX banner picks the new entry up. PyAutoHands: 433 tests pass plus the new `TestTimeoutOutputKeepsTheAbortStack` (noisy stderr + dump + 1887-char module list -> frames survive, module list gone, leading noise still truncated; dump-only input returned whole; plain long stderr truncates as before).
- deliberately not smoke-run: a `autolens_workspace_test` smoke was already running in this environment for #286, and parallel smoke runs are a known false-failure source; a skip-list line exercises nothing a smoke would run. The next integrate wave is the real check.
- follow-ups NOT in scope: a per-call heartbeat in `autofit/non_linear/jax_compile.py` (the path is silent once compiled, which is why 1805 s of nothing looked like a crash rather than a hang), and the three other #1528-restored entries that share this exposure.
- heart context: corrective PR for the Heart RED reason `release validation FAILED (stage integrate)` — job `integrate / run_scripts (3.12, autolens_test, multi_dataset)`.

## Original prompt

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
