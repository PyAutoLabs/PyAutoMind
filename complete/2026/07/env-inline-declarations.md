## Outcome — SHIPPED, 7 PRs merged 2026-07-23

Issue: https://github.com/PyAutoLabs/PyAutoHands/issues/187 (closed).
Merged: PyAutoHands#188 (mechanism: `# ENV:` parser + apply_profile hook +
validator, merged FIRST), autofit_workspace_test#72 (pilot),
autogalaxy_workspace_test#89, autolens_workspace_test#207,
autolens_workspace#326, autogalaxy_workspace#152 (migrations), then
PyAutoHeart#104 (CI flag flip — deliberately last). autocti_workspace_test +
autofit_workspace: nothing to ship (verified clean). Shipped under
human-acknowledged Heart YELLOW (workspace-validation backlog + 33 stale
parks, both pre-existing).

**231 scripts now declare env intent in-file**; the failure class "script
moved → override silently orphaned → wrong env" is structurally closed:
declarations travel with files, apply LAST in resolution (no profile pattern
can defeat them), and `--strict-declarations` in the PR gate errors on new
declarable pattern-overrides.

## Design decisions that mattered

- **UNSET semantics** (not set-"0"): mirrors the old unset-overrides exactly →
  smoke resolution byte-identical to HEAD (provable no-op); reader semantics
  verified absent ≡ "0"/off for all four vars (test_mode.py:14,
  analysis.py:68, mask_2d.py:363 et al., plot/utils.py:15 et al.).
- **Smoke-profile overrides only migrated.** Release-only `set:{VAR:"0"}`
  overrides are profile POLICY (release fidelity), not script intent — a
  profile-agnostic declaration would have changed smoke behaviour. Left.
- **The jax-on-unmarked carve-out**: an override unsetting DISABLE_JAX that
  matches non-jax-marked scripts (al_test `database/scrape/`) CANNOT migrate —
  release would flip "1"→absent = numpy→JAX, a real behaviour change. The
  validator's strict check skips exactly this shape.
- **Diff gate with one equivalence class**: literal equality except
  (declarable var, old "0" → new absent). Zero violations across 7 repos ×
  both profiles.
- **CI flag flip sequenced last** — flipping before the migrations merged
  would have failed their own PR CI.

## Residual overrides (legitimate, by design)

autofit_workspace_test `features/assertion` (set TEST_MODE "1");
al_test `database/scrape/` (jax-on-unmarked); autofit_workspace's two
plotter overrides (release pins TEST_MODE=1 + non-declarable
PYAUTO_SKIP_FIT_OUTPUT); mixed remainders keep only non-declarable vars
(PYAUTO_SKIP_FIT_OUTPUT, PYAUTO_SKIP_VISUALIZATION); all release-profile
`set:` overrides. Non-declarable skip vars are a possible future token
extension if they ever churn.

## Gotchas

- Declarations are PROFILE-AGNOSTIC — before migrating any per-profile
  override, check the OTHER profile's resolution for the matched scripts.
- 189 PyAutoHands tests (26 new). Harnesses:
  scratchpad verify_declarations.py pattern (old = HEAD profile with
  declarations monkeypatched off; new = worktree; empty base).
- autogalaxy_workspace push hit one 90s timeout; single retry clean.

## Follow-ups

- Phase 2 (next): mirror restructure + cull of autolens_workspace_test —
  draft/refactor/autolens_workspace_test/mirror_restructure_and_cull.md.
  Restructure is now near-free (declarations travel with files).
- Then: eyes_gallery_repoint, test_results_relayout (drafted).
- Optional future: extend token vocabulary to the non-declarable skip vars
  if their override lists ever churn.

## Original prompt

# In-file `# ENV:` declarations: script env requirements travel with the script (Phase 1b)

Type: feature
Target: workspaces
Repos:
- PyAutoHands
- autolens_workspace_test
- autogalaxy_workspace_test
- autofit_workspace_test
- autocti_workspace_test
- autolens_workspace
- autofit_workspace
- autogalaxy_workspace
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Blocked-by: draft/refactor/workspaces/env_resolver_family_b_unification.md (Phase 1a)

Phase 1b of the 2026-07-23 maintainability plan. DO NOT start until Phase 1a
(resolver unification) has merged — the mechanism only reaches repos that
resolve through the shared `env_config.py`.

**The problem.** Per-script env requirements live in pattern-keyed override
blocks in each workspace's `config/build/profile_smoke.yaml` (~21 blocks in
autolens_workspace_test, 15 autogalaxy, 9 autofit — ~45 total). A moved or
renamed script silently orphans its override: nothing fails at the config
layer, the script just runs with the wrong env. The July failure census
attributes ~7 of 23 distinct failure signatures to exactly this class.
Reading across the 45 blocks, they collapse to a small capability vocabulary:
needs-JAX, needs-full-resolution, needs-real-plots, needs-real-output,
needs-real-search.

**The task.**
1. Define a one-line header declaration parsed from the script file, e.g.
   `# ENV: jax full_datasets real_plots` (placed near the top; exact syntax
   at implementer's discretion but greppable and dumb to parse). Token →
   env-var mapping:
   - `jax`           → PYAUTO_DISABLE_JAX=0   (union with the existing
                        `is_jax_marked` name derivation; keep both)
   - `full_datasets` → unset/0 PYAUTO_SMALL_DATASETS
   - `real_plots`    → unset/0 PYAUTO_FAST_PLOTS
   - `real_search`   → unset/0 PYAUTO_TEST_MODE
   - `real_output`   → all four of the above (the database/scrape shape)
2. Implement as ONE new function in `PyAutoHands/autohands/env_config.py`,
   called from `apply_profile` (env_config.py:96) in the same precedence slot
   as the existing derivation hook (:125): scrub → defaults → overrides →
   declarations/markers last, so no profile override can silently defeat a
   script's declared intent. Reuse the header-parsing idiom already proven in
   `autohands/navigator.py` (`_docstring_blocks` :87) rather than inventing a
   new parser.
3. Extend `validate_env_profiles.py`: (a) declarations must round-trip — a
   declared script resolving the wrong value is an error; (b) NEW
   pattern-overrides in profiles that duplicate a declarable capability are
   an error under strict mode (grandfather nothing — see step 4); (c) keep
   the dead-pattern and legacy-name guards as-is.
4. Migrate: convert the ~45 existing override blocks to in-file declarations
   across the listed repos, then delete the override blocks. Each override's
   WHY-comment (many are small essays) moves into the script next to its
   declaration — the knowledge colocates too, not just the flag.
   Verification is the established gate: resolved-env diff over every script
   (resolve_clean, empty base) must be EMPTY before/after per repo.
5. Keep `no_run.yaml` out of scope — skip-behaviour is a separate path
   (`build_util.should_skip`), not env resolution. Do not merge the two.

**Triage rule to encode in the docs (from the July census):** an env fix must
be justified by the script's declared intent, never by making a failure
disappear — at least three July failures first mis-diagnosed as env gaps were
real library bugs (Convolver cap PyAutoArray#398, empty-HDU PyAutoFit#1415,
SersicCore PyAutoGalaxy#515). Declarations make "add an override until it
passes" unavailable; the docs should say why.
