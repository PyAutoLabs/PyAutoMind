# Active Tasks

## transformed-message-factor-gradient-unpack
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1501 (issued 2026-08-19)
- issued: 2026-08-19
- prompt: active/16_transformed_message_factor_gradient_unpack.md
- status: HOLD — do not start dev. Fix-or-delete hangs off the PyAutoFit#1498 logpdf-contract
  decision (parked #1500 design bundle); dead code (zero production callers), crashes on first
  call if ever exercised.
- external: community PR https://github.com/PyAutoLabs/PyAutoFit/pull/1502 (@trexfr-ops) targets
  this exact unpack — review via /community before any local work; the #1498 adjudication decides
  whether the method should exist at all.
- registered: 2026-08-19 by the wake_up session — the issuing session (claude/autofit-priors-messages-audit-ylvenv)
  filed the prompt + issue but not this entry, tripping Lifecycle Drift on main.
- repos-none-claimed: this entry claims NO repos — one line deliberately, not 2-space bullets.

## jax-stall-block-until-ready
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1528 (issued 2026-08-27)
- issued: 2026-08-27
- prompt: active/jax_compile_stall_3_root_cause.md
- epic: jax-compile-stall (phase 3 of 3 — phases 1 and 2 shipped/closed-as-partial)
- status: library-dev
- worktree: none — web-github session; direct clones under /home/user, no local worktree
- classification: both (library-first — PyAutoFit merges before the workspace PRs)
- repos:
  - PyAutoFit: feature/jax-stall-block-until-ready
  - autogalaxy_workspace_test: feature/jax-stall-block-until-ready
  - autolens_workspace_test: feature/jax-stall-block-until-ready
- branch-names-must-match: PyAutoHeart's reusable smoke-tests.yml clones the dependency chain
  at the MATCHING branch name, so a library-side A/B only reaches workspace CI while all three
  branches share this exact name. Do not rename one of them.
- reframed-at-start_dev: the prompt's five hypotheses are all compile-side, but phase 2's
  faulthandler stacks (two repos, two scripts, identical) park the process in
  jax.block_until_ready — compilation completes in ~16s. Planned from the corrected
  execution-hang framing, per the phase-2 record's closing instruction.
- deterministic-reproducer: autolens_workspace_test imaging/jax_likelihood/mge_group is
  16/16 lifetime executions with zero completions (5/5 at 300s both legs, run 32664682689;
  3/3 at 1800s both legs, run 32758924176). Every A/B has a binary readout — the prompt's
  "loop it until it hangs" problem is already solved.
- scope-floor: steps 0 (PyAutoFit instrumentation), 4 (restore coverage) and 5 (epic
  bookkeeping) ship regardless of whether the hypothesis ladder lands a root cause.
  Re-decide before the jax/jaxlib version bisect rather than rolling into it.
- heart: expect the ship gate's Heart leg un-consulted — pyauto-heart was unreachable from
  the web-github environment on phases 1 and 2, and this is the same environment.
