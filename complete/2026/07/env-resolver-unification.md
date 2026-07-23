## Outcome — SHIPPED, 8 PRs merged 2026-07-23

Issue: https://github.com/PyAutoLabs/PyAutoHands/issues/185 (closed).
Merged (order mattered for the first pair): PyAutoHands#186 (validator: release
profile optional), PyAutoHeart#103 (smoke-tests.yml validates every
smoke-profile workspace), then HowToFit#32, HowToGalaxy#42, HowToLens#52,
autolens_workspace#325, autofit_workspace#115, autogalaxy_workspace#151
(run_smoke fork → shared `autohands/env_config.py` resolver).
autofit_workspace_test shipped nothing (see corrections). Shipped under a
human-authorized Heart-RED exception (RED = "release validation FAILED (stage
integrate)", pre-existing and unrelated).

## Verification

- Resolved-env diff harness: OLD fork logic vs shared `apply_profile`, empty
  base, over smoke lists ∪ smoke notebooks ∪ every `.py` under `scripts/` —
  **674 entries across 6 repos, 0 diffs**. Only behavioural change is the
  ambient `PYAUTO_*` scrub; verified nothing in the per-PR gate injects any
  (no `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK` injection in the reusable workflow
  or callers — the old aged-draft concern applies to the mega-run path, which
  already used env_config and was green 2026-07-21).
- 15/15 validator tests (2 new: missing-smoke errors; smoke-only passes).
- All 6 migrated repos validate clean (user trio under
  `--strict-derivation --strict-markers`); Family-A strict controls
  (autolens/autofit_workspace_test) still clean.
- HowTo trio's migrated run_smoke.py is byte-identical to the Family-A
  template; user trio preserved notebook machinery + the autogalaxy
  `_BUILD_DIR` one-liner difference.

## Corrections found during execution (both premise bugs, both verified)

1. **Issue step 5 was stale**: autofit_workspace_test's release profile was
   already redesigned 2026-07-15 (`PYAUTO_DISABLE_JAX: "0"` default,
   `overrides: []`, in-file rationale why name-derivation is unneeded there —
   af.Analysis defaults use_jax=False, scripts opt in). Dropped; zero changes
   in that repo.
2. **"Six exempt repos" was wrong**: the three user workspaces carry
   `profile_release.yaml` and were already strict-validated; only the HowTo
   trio was exempt — and `validate_env_profiles.py` hard-required BOTH
   profiles, so closing the workflow exemption alone would have failed the
   HowTos on `profile_release.yaml: missing`. Fix: release profile now
   optional in `validate_workspace` (smoke stays required); a `_test` repo
   losing its release profile still fails loudly in the release runner.

## Gotchas for future sweeps

- The "one resolver" invariant claimed by env_profile_redesign.md §5 held only
  for Family A until this task; treat doc claims of unification as unverified
  until grepped (same lesson as the rename campaigns).
- `gh pr create` fails with "not a git repository" from the worktree ROOT —
  run it from inside each repo dir (worktree root is not itself a git repo).
- Family-A run_smoke WRAPPER drift remains (autolens_workspace_test has the
  #196 Popen/SIGKILL timeout wrapper; the other three have the older
  subprocess.run variant) — deliberately out of scope; hygiene follow-up.

## Follow-ups

- **Phase 1b** (next, unblocked by this): in-file `# ENV:` declarations —
  draft/feature/workspaces/env_inline_declarations.md.
- Then Phase 2 (mirror restructure + cull), eyes-gallery repoint, and the
  independent test_results relayout (all drafted 2026-07-23).
- Superseded draft archived: refactor/workspaces/
  unify_pyauto_env_injection_into_profiles.md (its SKIP_WORKSPACE_VERSION_CHECK
  finding shipped with #161 step 3; remainder folded into this task).

## Original prompt

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
