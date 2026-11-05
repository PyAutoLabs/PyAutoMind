# clean_slate.sh --packaging silently finds nothing on the grouped repo layout

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

`pyauto-brain hygiene packaging` reported 10 ignored `*.egg-info/` and `build/` directories (Nerves, Fit, Array, Galaxy, Lens), and recommends `@PyAutoBrain/bin/clean_slate.sh --packaging`. On the dev box, `DRY_RUN=1 clean_slate.sh --packaging` printed only "Dry run only — nothing changed": it enumerates repos with `for dir in */` at `$PYAUTO_ROOT` (line ~155), but `~/Code/PyAutoLabs` groups repos (`fit/PyAutoFit`, `array/PyAutoArray`, `organs/PyAutoNerves`, ...), so no repo matches. The hygiene scan itself handles the grouped layout, so the scan and the remedy disagree.

The 10 directories were removed by hand on 2026-11-04, using the same rule: ignored and no tracked files. Fix: enumerate repos the way the hygiene scanner does (or through the shared repo resolver), and add a test with a grouped-layout fixture. The dataset/output/scratch scopes of `clean_slate.sh` probably share the same blind spot; check them too.

## Diagnosis (2026-11-05, read-only)

Confirmed: `bin/clean_slate.sh:155` is `for dir in */; do repo="${dir%/}"; [ -d "$repo/.git" ] || continue` at `$ROOT`,
so every grouped checkout (`fit/PyAutoFit`, `organs/PyAutoNerves`, ...) is skipped for ALL scopes, not just
`--packaging`. Fix: source `bin/_repo_paths.sh` and iterate `pyauto_repo_list "$ROOT"` → `pyauto_repo_path`, keeping
`$repo` as the path used by the loop body (it is only used as a path + label). Test: grouped fixture
(`<root>/grp/RepoA/.git` + ignored `RepoA.egg-info/`) under `DRY_RUN=1 --packaging` must print the dir.


---

# Second bug in this task (same Brain claim)

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
