# Unify PYAUTO_ env injection: profiles, not workflow env: blocks (Phase 3 step 3, re-scoped)

Type: refactor
Target: workspaces
Repos:
- autofit_workspace_test
- autogalaxy_workspace_test
- autolens_workspace_test
- PyAutoHeart
- PyAutoBuild
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Build-chain campaign (PyAutoBuild#155) Phase 3 step 3, re-scoped 2026-07-17
after measurement killed the naive "scrubbed baseline" (see #161 comment).

**The discovery:** PYAUTO_ behavioural vars have TWO sources of truth — the
profile files (config/build/env_vars*.yaml, resolved by autobuild/env_config)
AND workflow-level `env:` injections:
- PyAutoHeart workspace-validation.yml:85 → PYAUTO_SKIP_WORKSPACE_VERSION_CHECK
- PyAutoBuild python_matrix.yml:85-87 → PYAUTO_TEST_MODE/SMALL_DATASETS/FAST_PLOTS
- PyAutoBuild release.yml:270-273,623 → those + SKIP_WORKSPACE_VERSION_CHECK

The **smoke profiles do NOT set SKIP_WORKSPACE_VERSION_CHECK** (measured:
set=0 in all three smoke env_vars.yaml); smoke relies entirely on the CI
env: injection (workspace-validation.yml comment: without it "every script
fails fast with WorkspaceVersionMismatchError"). This dual mechanism is the
same "one concept per name" duplication Phase 3 targets, and it is why a
blanket env_config PYAUTO_ scrub (the doc's §5 baseline) breaks smoke.

**Scope (the correct step 3):**
1. Add `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK: "1"` to the three smoke
   env_vars.yaml (so the profile is self-sufficient — belt-and-braces like
   the release profiles already are).
2. Remove the PYAUTO_ `env:` injections from workspace-validation.yml /
   python_matrix.yml (release.yml last, most carefully — it dispatches live
   releases; verify each removed var is set by the profile the run loads).
3. THEN land the deny-list scrub in autobuild/env_config.build_env_for_script
   (strip the managed PYAUTO_ family from the base before applying the
   profile), with the resolve-diff proof run against the REAL CI env (carrying
   the remaining ambient vars), not a synthetic clean env.

**Blocked:** autolens_workspace_test is claimed (dpie-lenstool-default as of
2026-07-17). Step needs all three smoke profiles edited consistently — all or
nothing. Resume when that claim frees.

**Guard against the near-miss:** the design-doc §5 "allowlist base" is wrong
(deny-by-default enumerates every infra var; a miss breaks the release path).
Use a deny-list of managed PYAUTO_ keys. And prove the resolve-diff against
the real CI environment — the synthetic-clean-env proof passed while the real
one would have gone red (the "reproduce in the real env" lesson).

<!-- filed 2026-07-17: Phase 3 step 3 re-scoped after measurement; see PyAutoBuild#161 -->
