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

## Diagnosis (2026-11-05, read-only)

`agents/conductors/hygiene/hygiene.sh` `enumerate_condemn_candidates` (~l.554) skips only `cur` — the branch HEAD of
the CANONICAL checkout. A task branch lives in a separate worktree, so it is not `cur`; with zero commits it is an
ancestor of origin/main → `merged=yes` → "recommend straight delete". Fix: per repo, build a skip set from
`git -C "$dir" worktree list --porcelain` (`branch refs/heads/<b>` lines) plus the claimed branches for that repo
from `worktree_list_claimed` (source bin/worktree.sh), and `continue` on them. Test: canonical repo + `git worktree
add -b feature/x` (no commits) must not list feature/x; plus an active.md-claimed branch with no worktree.
