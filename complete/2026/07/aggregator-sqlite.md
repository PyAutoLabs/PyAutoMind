## aggregator-sqlite
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1377
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1380 (MERGED)
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/49 (MERGED)
- summary: Aggregator Phase D — sqlite database exercised + assessed. Fixed: db Aggregator slicing inverted (agg[:5] on 26 → 21; old test passed by 2-fit coincidence) + DatabasePaths.save/load_samples_summary implemented (direct-write fits never stored the summary — silent abstract no-op). Workspace: 4 database scripts fixed (manual output/ paths missing the test-mode segment — the standing workspace-validation failures), 8/8 now pass; mock harness stamps per-copy unique_tag (db keys fits by identifier; copies collapsed 25→1); new profile_database.py sqlite-vs-directory grid.
- verdict: sqlite offers NO loading-speed advantage — build ~0.4s/result, ORM values("samples") 2-10× slower than the post-#1376 directory Aggregator; queries fast once built; single-file (HPC inodes) is the real use case. Making it fast = ORM reconstruction work, recorded as out of low-hanging scope. Direct-write path NOT broken at smoke level (contrary to suspicion) — its real gap was the missing samples_summary, now fixed.
- traps: open_database silently prepends conf output_path (+test_mode segment) to relative sqlite paths — decoy empty file appears at the literal path; use absolute paths. Direct-write stores minimised samples by design (save_all_samples=False → ~1 row). generate_mock_results leaves conf.instance.output_path pushed.
- shipped+merged through 5-reason pre-existing Heart RED on user ack (ship+merge) — this pair fixes part of the workspace-validation reason.

## Original prompt

# Exercise, fix and assess the sqlite results database build path

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Exercise, fix and assess the sqlite results database build path (aggregator Phase D)

Phase D follow-up of the aggregator profiling task (PyAutoFit#1375; phases A+B merged as
PyAutoFit#1376 + autofit_workspace_test#48). Original goal 3 of that prompt, verbatim:

"dont work on sqlite database builds on 1 or 2, but then do a follow up where you use this
functionality, inevitably encounter and fix bugs for its use, and assess the code which
writes directly to the sqlite database, which has not been used in a long time and I'm sure
is buggy. If its hard to fix dont bother, but its good to work out where its at."

Concretely, in @PyAutoFit (autofit/database/) driven from @autofit_workspace_test:

1) Use the merged mock-results harness (scripts/profiling/aggregator/mock_results.py) to
   exercise the sqlite build-from-directory path (autofit/database/aggregator/scrape.py,
   af.Aggregator(database file) + add_directory) at scale; fix the bugs encountered where
   they are cheap; extend the profiling grid with a database-build + database-query stage
   so sqlite loading can be compared against the directory Aggregator.
2) Assess the direct-write path (session-based writing during a fit, database.py paths) —
   long unused and suspected buggy. Fix if cheap; otherwise produce a written where-it's-at
   assessment (what works, what is broken, what it would take) rather than sinking time.
3) The existing scripts/database/{directory,scrape,session}/ scripts in
   autofit_workspace_test are the current coverage — run them, note which still pass.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/aa483bab-3f5b-4ffe-b121-c968ff80ffae/scratchpad/intake_sqlite_phase_d.md -->
