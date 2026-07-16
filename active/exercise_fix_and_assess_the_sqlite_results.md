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
