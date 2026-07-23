# Env resolver unification: collapse the six Family-B run_smoke.py forks onto env_config (Phase 1a)

Type: refactor
Target: workspaces
Repos:
- autolens_workspace
- autofit_workspace
- autogalaxy_workspace
- HowToFit
- HowToGalaxy
- HowToLens
- autofit_workspace_test
- PyAutoHands
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Phase 1a of the maintainability plan from the 2026-07-23 advisory review of the
three "Test Environment Variables / Testing / Test Workspace" issues. Root
cause identified: script env requirements are stored away from scripts, keyed
by path patterns, and the resolution machinery is silently forked.

**The finding.** The "one resolver" invariant of the env-profile redesign
(PyAutoHands/docs/env_profile_redesign.md §5) only holds for the four `_test`
repos (Family A), whose vendored `.github/scripts/run_smoke.py` imports the
shared `PyAutoHands/autohands/env_config.py`. Six repos (Family B) carry
hand-forked resolution — `autolens_workspace`, `autofit_workspace`,
`autogalaxy_workspace` (231/232-line variants, local `build_env` ~:68) and
`HowToFit`/`HowToGalaxy`/`HowToLens` (112-line variants, local `build_env`
~:52). The forks omit BOTH behaviours that only exist in `env_config.py`:

1. no `PYAUTO_*` scrub (`MANAGED_ENV_PREFIXES`, env_config.py:28, loop :89) —
   ambient vars the profile is silent on leak into script runs (the
   five-night-seed failure shape, still live in these six repos);
2. no `derive_jax_markers` support (`is_jax_marked`, env_config.py:155) — the
   derivation would be silently ignored if enabled in their profiles.

**The task.**
1. Migrate all six Family-B `run_smoke.py` copies to import `env_config`
   (`build_env_for_script`, `load_env_config`), deleting the local forks of
   `load_env_config`/`build_env`/`pattern_matches`. Keep per-repo wrapper
   differences (notebook support in the user workspaces) — only the env
   resolution collapses. PYTHONPATH wiring for the import already exists in
   the reusable gate (PyAutoHeart/.github/workflows/smoke-tests.yml:108-111).
2. Adopt `derive_jax_markers: true` in
   `autofit_workspace_test/config/build/profile_release.yaml` and delete its
   four remaining hand-enumerated PYAUTO_DISABLE_JAX overrides (the last
   Family-A holdout; note autofit defaults JAX-on, so confirm the derivation
   direction is correct there before flipping).
3. Turn the strict validator on for all migrated repos: `--strict-derivation`
   and `--strict-markers` in the reusable smoke workflow. Today
   `validate_env_profiles.py` only runs when a workspace has a
   `profile_release.yaml` (smoke-tests.yml:85-100), which exempts exactly the
   Family-B repos — close that exemption (validate the smoke profile even
   where no release profile exists).
4. Verify by the established gate: resolved-env diff over every script
   (`resolve_clean`, empty base) must be EMPTY per repo before/after
   migration, except where a leak is being deliberately closed — enumerate
   any non-empty rows in the PR body as the intentional behaviour change.

**Supersedes** the aged draft
`draft/refactor/workspaces/unify_pyauto_env_injection_into_profiles.md`
(build-chain campaign, Hands#155, now closed): its smoke-profile
SKIP_WORKSPACE_VERSION_CHECK finding has since shipped (profile-owned as of
the #161 step-3 scrub) and it predates the autoconf/PyAutoBuild renames.
Fold anything still-live from it into this task and archive it.

**Why now.** This unblocks Phase 1b (in-file `# ENV:` declarations), which is
a single-point change in `apply_profile` (env_config.py:96) — but only reaches
repos that actually resolve through it. Evidence trail: July failure census
classified ~7/23 distinct failure signatures as env-pairing drift, and the
whole RED-blocker set was cleared with zero library edits.
