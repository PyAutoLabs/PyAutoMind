# hygiene tidy recommends deleting branches of live, claimed tasks

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Filed: 2026-11-04 (pre-rehearsal /hygiene sweep)

`pyauto-brain hygiene tidy` on 2026-11-04 listed, as "merged branch → skips the pen: recommend straight delete":
- `feature/magnification-maps-wiring` in PyAutoArray, PyAutoGalaxy and PyAutoLens: an ACTIVE claimed task (library-dev) whose worktrees hold uncommitted edits;
- `feature/tutorial-link-sweep` in PyAutoGalaxy and PyAutoLens: then-live Codex task branches (subsequently merged; see `complete/2026/11/tutorial-link-sweep.md`). This remains evidence of the bug at observation time.

They count as "merged" only because they have no commits beyond main yet. Fix: exclude every branch named in `PyAutoMind/active.md` `repos:` bullets, plus any branch checked out in a worktree, before classifying. Use the claim reader the worktree guard already uses (`worktree_list_claimed`). Add a regression test with a claimed zero-commit branch.
