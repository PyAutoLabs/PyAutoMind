# A shift-owned "keep Heart green" lane: read the reasons, file or dispatch the fixable ones, never release

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-11-13
Issued: 2026-11-13
Epic: autonomous-orchestrators
Consequence: judge
Witness: (a) `pyauto-brain batch green --json` over a saved RED/YELLOW feed fixture classes every reason as `dev-fixable`, `release-scope` or `human-only` and prints one proposed bug draft per `dev-fixable` reason; run twice, it files nothing new the second time (dedupe key = reason class + repo + script/workflow); (b) a test proves the lane's code path cannot call `gh workflow run` on release/nightly workflows, `build`, `pre_build`, `--accept-red` or any `force` (grep + an import/exec allow-list test); (c) in one live M3 shift, the digest has a "Heart" section listing each reason, its class and the task filed or dispatched for it
Review-minutes: 25
Unattended: never
Lane: any

Original request (human, 2026-11-13): "having the autonomous agent constantly trying to ensure its green (without having it be overly eager doing releases)." This is the roadmap's M2 side item "a shift-owned keep the nightly green lane" and REL-3's proposed change. REL-3 was re-checked 2026-11-13 (holds).

**What each shift does (a step at brief/plan time, before backlog picks).** For M3 it runs in `batch brief`/`batch plan`, a session, not the watcher: the watcher's network surface (`PyAutoBrain/AUTONOMY.md:835-870`) does not include reading the Heart feed, and moving the lane into the tick needs a dated amendment.
1. Read Heart's **release** verdict from the published feed (`PyAutoBrain/bin/heart_feed.py`, no `--repos`), 6 h age rule applies; STALE → the lane does nothing and says so in the digest.
2. Class each red/yellow reason:
   - `dev-fixable`: red `main` CI on a library or workspace; a Stage 3 failing script (with its error line); a quarantined script whose bug task has no PR; a weekly organ workflow whose fix merged but has not rerun.
   - `release-scope`: needs a rehearsal or a release to clear (rehearsal stale or "source moved", install verification of the released bootstrap — check F audits the PyPI-released bootstrap, `complete/2026/09/colab-gate-candidate-audit.md`).
   - `human-only`: anything AUTONOMY.md reserves (forcing YELLOW, accepting a named RED, quarantine doctrine, version choice).
3. For `dev-fixable`: file one bug draft via intake (Lane, Consequence set; dedupe against `draft/` and `active/`), add it to `queue.md`'s top **only if the human's queue allows the lane to** (a brief flag `green-lane: file|file+pick`), and with `file+pick` dispatch it as a normal glance/notify pick. For the other two: one digest line each, no action.
4. Report "nights shipped over active nights" (REL-3's metric) and days RED by class (`verdict_history_and_cause_classes.md`).

**Never:** release, dispatch `nightly-release.yml`/`release.yml`/Release Integrate/rehearsals, run `/build`, `/pre_build`, set or thaw a freeze, add a quarantine entry, or pass `--force`/`--accept-red`. Those stay the human's (programme "Always the human's").

**Judge question (REL-10 residual).** M2.1 removed release-scope reasons from the dev gate, so most fixes ship. But a fix for red `main` CI in repo X touches X, and X's red CI blocks its own ship (`heart/readiness.py:79-84`), so it still needs the live-human corrective exception (`PyAutoBrain/AUTONOMY.md:928-1007`). Options: (1) keep it human: the lane files and the human runs `/prm`; (2) a dated ruling letting a PR ship at glance when its diff touches the failing job's paths, its own checks are green, and the red reason is the only in-scope one. Recommend (1) for M3, rule on (2) at the M3 gate with evidence.

**Constraint (REL-13, preserve):** the nightly driver's exit codes, activity gate, kill switch and no-force inputs are not touched; the lane only reads the driver's outcome.

Links: `draft/feature/pyautobrain/nightly_outcome_record_and_same_night_bug_tasks.md` (slice 2 files per-script bugs at night; this lane picks them up by day; build that first or share its dedupe key), `draft/feature/pyautobrain/nightly_ships_on_quarantine_only_yellow.md` (with it, a quarantined script stops blocking the night; this lane owns getting its bug fixed before the 7-day expiry).
Programme: M3 (run in M3.1/M3.2 shifts); M6 exit test "the nightly kept green by a shift".

<!-- drafted 2026-11-13 by the REL intake session (scratch/intake_2026-11-13) -->
