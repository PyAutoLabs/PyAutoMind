## Outcome — SHIPPED + MERGED 2026-07-24 (Hands#193 + Heart#106, lockstep pair)

Issue: https://github.com/PyAutoLabs/PyAutoHands/issues/192 (closed).
test_results/ → run_logs/ with runs/<run-type>/<YYYY>/<MM>/<timestamp>/,
regenerated index.md (newest-first, per-project pass/fail), AGENTS.md,
latest symlink kept, --run-type arg (smoke default — run_all has NO release
path today; release runs pass the flag). 20 historical runs migrated on disk
(the folder is gitignored — state, not history), 14 stale April flat files
deleted. All 8 reader sites moved in lockstep (checks consts, tick.sh guard,
health_release, health_sync). PyAutoBrain vitals manifest updated directly.

## The live bug fixed
health_sync's "Last autohands run" dashboard line had read the legacy flat
test_results/*.json (last written 2026-04-26) — silently showing April data
for months. Now reads run_logs/latest/report.json (verified real values).

## Gotchas
- The two silent-breakage traps from the reader-map research (tick.sh -d
  guard; health_sync compgen guard) were the whole reason for lockstep; a
  brief fail-safe degraded-tick window existed between disk migration and
  merge (anticipated, attributable).
- readiness_evidence_audit.md's old path mention deliberately KEPT — dated
  measured record; rewriting would falsify history.
- Worktree path resolution: Heart readers resolve ~/Code/PyAutoLabs from
  parents[3]-name check — worktrees fall back to the main checkout.

## Follow-ups
None blocking. Future: release-prep mega-runs should pass --run-type release.

## Original prompt

# PyAutoHands run-log relayout: Mind-style hierarchy + index, rename test_results (Phase 3)

Type: maintenance
Target: pyautohands
Repos:
- PyAutoHands
- PyAutoHeart
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised

Phase 3 of the 2026-07-23 maintainability plan. Independent of Phases 1-2 —
can run any time. Origin (user): "test_results makes me think its unit tests
and inside its not clear when stuff ran. The folder structure should mirror
PyAutoMind/complete (e.g. 2026/04/), with the type of run being a folder and
then time stamps making it numerically run down being in there. PyAutoMind
also has an index.md and AGENTS.md to make looking up information quicker."

**Target layout:** rename `PyAutoHands/test_results/` → `run_logs/` (or
similar — NOT "test_results"), with `runs/<run-type>/<YYYY>/<MM>/<timestamp>/`
(zero-padded months, lexical=numerical), a maintained `index.md` (one line
per run: date, type, pass/fail counts, link) and an `AGENTS.md` describing
the layout. Keep the `latest` symlink mechanism. Migrate existing
`runs/<ISO-ts>/` dirs into the new hierarchy; DELETE the stale flat top-level
`*__script.{json,md}` files (legacy pre-runs/ leftovers, last written
2026-04-26).

**This is a single-writer + ~8-reader lockstep change (2026-07-23 survey).**
There is no shared path constant — every site hardcodes the string; writer
and readers must change in ONE coordinated pair of PRs (Hands + Heart):
1. `PyAutoHands/autohands/run_all.py:33` (RESULTS_BASE), `:152` (run-dir
   template — add type/year/month nesting), `:56-63` (latest symlink),
   docstrings :12,:126-127. Add index.md/AGENTS.md emission here (or in
   result_collector.RunReport.write, :147-157).
2. `PyAutoHands/tests/test_run_all_history.py:4,57,79` — layout assertions.
3. `PyAutoHeart/heart/checks/test_run.py:35` (TEST_RESULTS_LATEST — feeds
   the readiness verdict's count enrichment).
4. `PyAutoHeart/heart/checks/script_timing.py:43` (same constant).
5. `PyAutoHeart/heart/tick.sh:24` — the `-d .../latest` guard; if missed,
   script-timing baselines SILENTLY stop accruing every tick.
6. `PyAutoHeart/scripts/health_release.sh:31` (PYAUTO_STATUS_FULL_DEFAULT).
7. `PyAutoHeart/scripts/health_sync.sh:371-393` — reads the FLAT legacy
   files for the "Last autohands run" dashboard line; it is ALREADY showing
   April data. Repoint it at `latest/report.json` (fixes a live staleness
   bug) — if missed it vanishes silently (compgen guard).
8. Docs/skills sweep (stale-making, not breaking):
   PyAutoHeart/skills/pyauto-status-full/reference.md:29,32,122,
   health_agent/capabilities.{yaml,md}, docs/readiness_evidence_audit.md,
   PyAutoBrain agents/faculties/vitals/HEART_CAPABILITIES.md:31. Cleanup:
   PyAutoHands/.claude/settings.local.json:9-10 (dead PyAutoBuild paths).

**Safety notes.** Readiness fails safe: an unreadable `latest/report.json`
degrades test_run.py to ready=None (yellow "ready unknown"), never false
green — but do the rename while Heart is otherwise GREEN so a yellow blip is
attributable. The `latest` symlink is absolute-resolved (run_all.py:62);
migrating historical run dirs dangles it — re-link as part of the migration.
CI/workflows are confirmed path-independent (workspace-validation.yml uses
its own working dir + Actions API); PyAutoMind references are archival
records only — do not rewrite history there.
