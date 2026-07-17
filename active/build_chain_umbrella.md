# Build-chain umbrella: one coordinated fix across five filed briefs

Type: bug
Target: PyAutoBuild
Repos:
- PyAutoBrain
- PyAutoBuild
- PyAutoHeart
- PyAutoMind
- workspaces
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

## CAMPAIGN STATE + REMAINING PICKUP QUEUE (updated 2026-07-17)

This entry is the single index for the build-chain campaign. It stays in
`active.md` so `/morning` and `/health` surface it; each remaining item below
is a filed `draft/` prompt that `/feature` (or `/start_dev <path>`) picks up.
(Hygiene/Health don't own this — their scans are narrow; the pickup path is
`/feature` over these prompts + this tracker.)

**DONE (merged):** Phase 0a-b · Phase 1 (audit + 3 pre_build steps) · Phase 2
(evidence audit + test_run fix + verify_install run + surface recording) ·
Phase 3 steps 1-3 (validator #163, single resolver, scrubbed base #165) ·
Phase 4 task 1 (floors 2026.7.9.1 ×7) · Phase 5 all 6 items + 2 guard fixes +
API-gate F5. ~40 PRs; 6 live refusal/routing mechanisms.

**REMAINING — pick up via `/feature` / `/start_dev`, recommended order:**
1. `draft/feature/pyautoheart/version_skew_floor_rework.md` — Phase 4 task 2;
   UNBLOCKED by floors; enforces "floor names an installable version". Do next.
2. `draft/feature/pyautobuild/version_model_consumers_and_readme_pins.md` —
   Phase 4 tasks 3-4 (assistant --check-version; orphaned README pins; then
   remove legacy workspace_version/version.txt). After task 2.
3. `draft/bug/workspaces/howto_validation_needs_simulator_stage.md` — Phase 2
   §5.5; ~30 HowTo tutorials adopt `should_simulate` (judgment prose; own
   session). Fork (b) decided; do NOT restore committed datasets.
4. `draft/feature/workspaces/env_profile_migration_steps_4_to_8.md` — Phase 3
   steps 4-8; step 4 (15-script JAX triage) is RELEASE-SURFACE RISK, do
   carefully; steps 5-8 follow. Least urgent (steps 1-3 already delivered the
   core value).
5. `draft/bug/pyautobrain/mind_commit_guard_v13_fail_open_on_complex_shell.md`
   — guard v1.3: fail open on complex shell, OR decide the commit-guard's fate
   (3 FPs on author, 0 confirmed catches). Small.

Epic tracker: PyAutoBuild#155. Env-profile sub-issue: PyAutoBuild#161. Agent
failure-modes: PyAutoBrain#130. Full component-brief detail is below.

---

PyAutoBuild is the centre of gravity. This umbrella combines five already-filed
PyAutoMind draft briefs (plus their filed satellites) that all touch the
build/release/validation chain, so the work is sequenced as a single campaign
instead of five disconnected drafts. The umbrella's job is to sequence and
unify; each component brief remains the authoritative statement of its own
problem — read it in full before starting its phase.

## Component briefs

1. **`draft/research/pyautobuild/pre_build_git_add_failure_audit.md`**
   (research, medium, Model: Fable) — pre_build.sh has exactly three
   failure-tolerant sites (:55, :79, :88) and all three are implicated: :79 was
   bug 1 (fatal under set -e, fixed PyAutoBuild#154); :88 is bug 2 (unmatched
   glob → git rejects the whole pathspec list, exit 128 swallowed by `|| true`,
   nothing staged — filed, unfixed); :55 seds a README.rst no workspace has, so
   its `|| true` is permanently load-bearing and a real sed failure is
   indistinguishable from the expected one. Three sites, three hits — the idiom
   is the suspect. Leads with the design question: release.yml regenerates and
   commits the same artifacts on the runner, so what is pre_build's local
   commit for? Redundant (delete it — the #47 shape) or load-bearing in an
   unexercised case? Find out; do not assume the tidier answer. Known
   unverified claim inside: whether the README bump edits but goes uncommitted.

2. **`draft/bug/pyautobuild/release_version_sync_back_to_main.md`** (bug,
   medium) — a release leaves `__version__` stamps and workspace pins frozen on
   main (by design since PyAutoBuild#120's floor model) while Colab URLs move,
   producing recurring "drift" alarms and two hand-done 15-repo bumps. The
   2026-07-15 findings reframe it as an undecided fork: (a) re-add commit-backs
   to main (rejected once — they caused stale CI storms and an org-wide cron
   pause) vs (b) keep mains authoritative and fix the three consumers that
   still read a floor as an exact pin (assistant `--check-version`, Heart
   `version_skew`, workspaces without floors). Evidence leans (b). The genuine
   bug either way: after 2026.7.9.1 the floors named the *yanked*
   2026.7.6.649 — a floor must always name an installable version.

3. **`draft/research/pyautoheart/readiness_evidence_chain_audit.md`**
   (research, large, Model: Fable) — four measured integrity failures in the
   evidence behind Heart's release verdict, found in one half-day: (1) the
   install-verification leg discarded every PASS for months (fixed, PR#77);
   (2) Heart's own test suite clobbers live `~/.pyauto-heart` state (filed, see
   satellites); (3) the `test_run` leg's history is incomparable across runs —
   the smoke surface silently doubled and 30 failures trace to missing
   simulated datasets, possibly downstream of PyAutoBuild#150 dropping
   `git add -f dataset/` (**unestablished — settle it**); (4) the Brain feature
   agent's path parser misroutes post-lifecycle-split prompts (now filed, see
   satellites). Core deliverables: a per-leg evidence map (artifact, writer,
   has the writer ever run, is the leg satisfiable at all) and a judgment on
   what the GREEN gate is worth today — whether the nightly's standing grant
   should stand, narrow, or pause. **Its own instruction: read the pre_build
   audit first; findings 3 and 5 intersect it.**

4. **`draft/research/workspaces/env_profile_and_validation_gate_redesign.md`**
   (research, large, Model: Fable) — redesign the env-profile + validation-gate
   system after one missing YAML line held nightly-release red for five nights.
   Eight observed failure modes (silent override, vacuous tests,
   hand-maintained lists, release config untestable at PR time, inconsistent
   siblings, silent pattern over-match, duplicated resolvers, layered duplicate
   env reads); already-tried-and-rejected list (smoke_tests.txt promotion,
   static guard, loud warning — killed by adversarial review; writing it down —
   refuted by a note that did not fire one day later). Target: a verified map,
   a design that makes the failure modes structurally hard, an incremental
   migration path, and an answer to the open question: is mode=release
   validating the NumPy path for most of the ag/al surface intended? Guard: do
   NOT copy autofit_workspace_test's DISABLE_JAX reasoning to ag/al, where
   use_jax defaults True and the var is genuinely load-bearing.

5. **`draft/research/pyautobrain/agent_failure_modes_structural_mitigations.md`**
   (research, large, Model: Fable) — the companion asking how to stop the
   *agent* producing these bugs: fourteen itemised errors from one session in
   five shapes (verification that confirms the assumption ×5, stored belief
   over repo ×2, recall instead of enumeration ×2, unvalidated tools ×3,
   shared-state/convention ×4). Load-bearing findings: a note naming the exact
   trap did not fire one day later (documentation is refuted as a primary
   mechanism); repos.yaml held every hand-listing miss and was never reached
   for. Hypothesis to attack: mechanisms that REFUSED an action caught ~100%,
   mechanisms that INFORMED caught 0%. Deliverables: validated taxonomy, ranked
   structural mitigations demonstrated against the catalogue, honest attack on
   the memory system, an estimate of the unnoticed-error set.

## Filed satellites (in scope, referenced by the briefs)

- `draft/bug/pyautoheart/test_suite_clobbers_live_heart_state.md` (small,
  HIGH) — brief 3's finding 2, filed separately. Also a **precondition**:
  brief 3 forbids running Heart's suite against a live state dir until fixed.
- `draft/bug/pyautobuild/root_level_git_add_stages_nothing_on_unmatched_glob.md`
  (small) — brief 1's bug 2. **Hold the fix**: brief 1's design answer may
  delete the line instead of hardening it; fixing it first pre-empts the audit.
- `draft/bug/pyautobrain/feature_agent_path_parser_predates_lifecycle_split.md`
  (small, safe) — brief 3's finding 4, filed 2026-07-16 while decomposing this
  umbrella. Sibling: `draft/bug/pyautobrain/intake_writes_legacy_layout.md`
  (the writer side of the same pre-#71 assumption).
- `draft/feature/workspaces/minimum_library_version_adoption.md` (small, HIGH)
  and `draft/feature/pyautoheart/version_skew_floor_rework.md` (small) — the
  two floor-model consumers brief 2's fork (b) would execute; the version_skew
  rework depends on the adoption landing first.

## Task decomposition (worked out 2026-07-16)

**Phase 0 — small unblockers (independent, land first, in any order):**
- Fix `test_suite_clobbers_live_heart_state` (design-first per its brief:
  prefer `run()` returning the summary and only the CLI persisting; sweep
  `heart/checks/` for siblings; decide deliberately on the autouse fixture).
  Unblocks Phase 2's method safely.
- Fix `intake_writes_legacy_layout` + `feature_agent_path_parser_...` (both
  small/safe Brain fixes; the second is the reader side of the first).

**Phase 1 — pre_build audit (brief 1).** First research phase: brief 3 says
read it first, and its design answer decides both the fate of the glob bug
(fix vs delete the line) and the #150→missing-datasets question brief 3's
finding 3 hangs on. Output: the failure-class enumeration, the
redundant-vs-load-bearing verdict, a target design (possibly a smaller file).

**Phase 2 — Heart evidence-chain audit (brief 3).** After Phase 1 (consumes
its #150 verdict) and Phase 0 (safe suite runs). Output: per-leg evidence map,
the what-is-GREEN-worth judgment, and the human decision on the nightly's
standing grant.

**Phase 3 — env-profile/validation-gate redesign (brief 4).** Parallelisable
with Phases 1–2 (different surface), but reconcile before finalising: its
answer to the ag/al mode=release NumPy question feeds brief 3's "what does the
verdict validate", and both feed the same release chain. Output: design doc +
incremental migration plan.

**Phase 4 — version-model fork (brief 2).** Decide fork (a)/(b) with Phases
1–3 evidence in hand; current evidence leans (b): land
`minimum_library_version_adoption`, then `version_skew_floor_rework`, rework
the assistant `--check-version` to be source-checkout-aware (or drop equality
for the API-surface hash), enforce "a floor names an installable version"
whichever fork wins, then rewrite or shelve the sync-back prompt with the
reasoning recorded. Never re-add stamp commit-backs without confronting the
#120 history (CI storms, cron pause).

**Phase 5 — agent failure-mode mitigations (brief 5).** Last, deliberately:
every earlier phase's "Trust nothing here" section, plus any new errors made
during Phases 0–4, are additional catalogue data; the refusals-vs-reminders
hypothesis should be tested against the enlarged set. Its mitigations then
protect all future campaigns.

**Cross-cutting constraints (from the briefs; apply to every phase):**
- Research briefs are Model: Fable, supervised, design-first — plan approval
  before implementation; judgment, not merged fixes, is the deliverable.
- Never dispatch `release.yml` as a test — `rehearsal` defaults to `false` = a
  real PyPI release. `workspace-validation.yml mode=smoke` is safe.
- Never reintroduce `git add -f` for `dataset/` (#126/#150).
- Do not copy DISABLE_JAX reasoning across af/ag/al surfaces (use_jax defaults
  differ).
- Prefer deleting the trap to hardening or documenting it.
- Each brief carries a "Trust nothing here" section: treat every inherited
  number as re-measurable and re-measure it.

<!-- filed 2026-07-16 by /intake (umbrella over five existing drafts); task decomposition added same day after reading all component briefs + satellites in full -->
