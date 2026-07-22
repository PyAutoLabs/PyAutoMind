Build-chain integrity campaign — closed 2026-07-22, epic PyAutoHands#155 CLOSED.

Six phases, ~45 merged PRs across PyAutoHands, PyAutoHeart, PyAutoBrain,
PyAutoMind and 8 workspaces. The umbrella existed to sequence five separately
filed briefs as one campaign; that job is done and the single remaining item
(env-profile steps 4-8) has its own issue, so the coordinating entry is
retired rather than carried.

WHAT SHIPPED (by phase). Phase 0: run() side-effect-free in test_run +
version_skew (Heart#79); full lifecycle-path coverage in the sizing faculty
(Brain#128). Phase 1: the pre_build failure audit (docs/pre_build_failure_audit.md,
#157) plus its three landable steps — dead lines (#158), release.yml owned
staging (#159), and the deletion of the dataset/config "sweep human dirt into
the release" vestige (#160). Phase 2: Heart's readiness-evidence audit (#83/#84)
and its fixes — caller-decided fetch_cloud with local/cloud AND-agreement
(Heart#85), report.json + test_run sidecar now stating their own surface
(Hands#164 + Heart#86), and the first verify_install evidence ingest, which
dropped "install verification not run" from readiness. Phase 3: env-profile
redesign (design doc #162) steps 1-3 — validate_env_profiles (#163), the single
resolver folding three byte-identical run_smoke forks (afwt#52/agwt#74/alwt#174),
and the scrubbed baseline env (#165 + three smoke profiles). Phase 4: the
version model, fork (b) — mains authoritative — as four tasks, all now done
(floors x7; version_skew reworked to floor-vs-newest-tag, Heart#96; the
assistant's --check-version de-gated from __version__; the orphaned README pins
removed). Phase 5: the agent-failure-modes capstone (Brain#131) and all six
mitigations, including the pipefail agent-shell default, the Mind commit guard,
worktree_remove's stale-claim refusal (Brain#134), branch_contribution
(Brain#139) and the review faculty's unverified-claim finding (Brain#140).

THIS SESSION (the closeout). The 2026-07-17 pickup queue was stale by three
items — version_skew, the Phase 4 consumers, and the HowTo simulator stage had
all closed via other sessions. Verified each against the code rather than the
index, then shipped the two genuinely open ones:

- Phase 4 task 4, README pins (autofit_workspace#107, autofit_workspace_test#64,
  autolens_workspace_test#198, PyAutoHands#174). The three surviving `<pkg> vX`
  lines had had no owner since the runner bump was removed (#120/#121) and
  pre_build's local sed never staged its edit (deleted #158); they were up to
  ~2 months stale and, after 2026.7.9.1, one named a YANKED release. Decision:
  drop the pins, do not re-own them — re-adding a runner sed+commit means a new
  commit-to-main step of the kind #120/#121 deliberately removed, to maintain a
  string no gate reads. The floor (version.minimum_library_version) is the
  checked signal; version_skew verifies it. pre_build's VERSION variable, dead
  since #158, was removed with them.
- mind_commit_guard v1.3 (PyAutoBrain#148). The guard fired live three times,
  every one a FALSE POSITIVE ON ITS OWN AUTHOR (v1.0 quoted gh body, v1.1
  cd-away commit, v1.2 cd inside a for-loop body), against ZERO confirmed
  catches — the `-- <files>` habit did that work. Narrowed, not retired: it may
  now deny only when confident, failing open on compounds, subshells/brace
  groups, and any non-clause-leading cd. 22/22 tests green, plus a live
  PreToolUse payload check on all three historical FPs.

RESIDUE (parked, not dropped): env-profile steps 4-8, prompt
draft/feature/workspaces/env_profile_migration_steps_4_to_8.md, owned by
PyAutoHands#161 (left OPEN). Step 4 — replacing the hand-enumerated JAX folder
lists with the jax_*/*_jax/*_jit derivation rule, and triaging the 15
vacuous-JAX scripts the validator found — is release-surface risk exercised
only by the mega-run; steps 5-8 (strict validator gates, profile renames, the
al.AnalysisDataset one-reader fold, the human-gated use_jax sentinel) follow it.
Steps 1-3 already delivered the core value, so this is unurgent standalone work.

WHAT THE CAMPAIGN LEARNED. The load-bearing finding is about refusals, and the
campaign's own guards proved it in both directions. Brain#134's stale-claim
refusal true-positived on the author (it blocked a worktree_remove because
active.md still claimed a merged task — exactly failure mode F4), because its
precondition is DECIDABLE: is this branch merged into origin/main's first-parent
chain. mind_commit_guard false-positived on the author three times, because its
precondition requires modelling an unbounded input space (arbitrary shell). A
refusal whose trigger is decidable earns its keep; one that must guess spends
its budget on false positives and trains bypass-by-default. Recorded in
docs/agent_failure_modes.md mitigation 2.

Two methodological traps worth carrying forward. (1) The step-3 near-miss: a
synthetic clean-env resolve-diff passed 65/65 while the REAL CI env would have
gone red, because the smoke profiles relied on a PYAUTO_ var injected by the
workflow, not the profile — prove env changes against the real CI env, never a
model of it. (2) Stale indexes: three of five queue items were already done, and
following the index rather than the code would have redone them. Verify state
at the source before working from any tracker, including this one.

## Original prompt

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

## CAMPAIGN CLOSED 2026-07-22 — epic PyAutoHands#155 closed

The umbrella's job (sequence five filed briefs as one campaign) is done. All
six phases shipped; the five-item pickup queue left on 2026-07-17 is now four
done and **one parked residue**, which has its own issue and does not need a
coordinating entry. This prompt is recorded to `complete/2026/07/` and dropped
from `active.md`.

**DONE (merged):** Phase 0a-b · Phase 1 (audit + 3 pre_build steps) · Phase 2
(evidence audit + test_run fix + verify_install run + surface recording) ·
Phase 3 steps 1-3 (validator #163, single resolver, scrubbed base #165) ·
Phase 4 task 1 (floors 2026.7.9.1 ×7) · Phase 5 all 6 items + 2 guard fixes +
API-gate F5. ~40 PRs; 6 live refusal/routing mechanisms.

**Queue resolution (the 2026-07-17 index was stale by 3 items):**
1. Phase 4 task 2, version_skew floor rework — **DONE** (Heart#96, branch
   claude/wake-up-u53v8z). `heart/checks/version_skew.py` compares each
   workspace floor against the newest `YYYY.M.D.B` tag:
   UNSATISFIABLE/OK/BAD/UNKNOWN. Verified 2026-07-22: 7/7 floors OK against
   2026.7.22.1.
2. Phase 4 tasks 3-4 — **DONE**. Task 3: `audit_skill_apis.py check_version`
   gates on the API-surface hash only; the `__version__` equality that
   structurally false-positived on source checkouts is informational.
   Legacy `workspace_version`/`version.txt` removal landed with the
   version-model-honesty epic (last holdout HowToFit#23). Task 4 closed
   2026-07-22: the three orphaned README pins were **removed** in favour of
   "install the latest release" + the floor (autofit_workspace#107,
   autofit_workspace_test#64, autolens_workspace_test#198), and pre_build's
   now-dead `VERSION` var went with them (PyAutoHands#174). Runner
   re-ownership was considered and rejected — see the audit doc §1.1.
3. Phase 2 §5.5, HowTo simulator stage — **DONE** (HowToLens#39,
   HowToGalaxy#30; HowToFit needed no change — it already self-simulates and
   `af.util.dataset.should_simulate` does not exist). Namespace differs per
   repo: `al.` / `ag.`. The `howtolens/`+`howtogalaxy/` unset overrides were
   DEAD (matched 0 files); the real blockers were missing/wrong-producer
   guards.
5. mind_commit_guard v1.3 — **DONE** (PyAutoBrain#148). Evidence decided it:
   3 false positives on the guard's own author, 0 confirmed catches. Narrowed
   (not retired) to deny only when confident — fails open on compounds,
   subshells, and non-clause-leading `cd`.

**PARKED RESIDUE — the only remaining work, tracked on PyAutoHands#161:**
4. `draft/feature/workspaces/env_profile_migration_steps_4_to_8.md` — Phase 3
   steps 4-8. Step 4 (derivation rule + triage of the 15 vacuous-JAX scripts)
   is RELEASE-SURFACE RISK and only the mega-run exercises it; steps 5-8
   follow. Steps 1-3 already delivered the core value, so this is not urgent.
   The prompt stays in `draft/` and picks up via `/feature` or
   `/start_dev <path>` — no umbrella needed.

Epic tracker: PyAutoHands#155 (CLOSED). Env-profile sub-issue:
PyAutoHands#161 (OPEN, owns the residue). Agent failure-modes: PyAutoBrain#130.
Full component-brief detail is below.

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
