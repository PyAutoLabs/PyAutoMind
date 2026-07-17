# mind_commit_guard v1.3: fail open on shell it can't confidently attribute (for-loops, subshells)

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

`mind_commit_guard` (v1.2, PyAutoBrain#138) has false-positived on its author
THREE times: v1.0 on a quoted `gh comment` body, v1.1/pre-v1.2 on a `cd`-away
PyAutoBuild commit, and now (2026-07-17) on a **for-loop with `cd` inside the
body** — the `cd` is not the first token of a clause (it follows `do`), so
`_cd_target` doesn't track it and the guard resolves the commit to the ambient
PyAutoMind cwd. All three were legitimately NON-Mind commits.

The pattern: the guard tries to attribute a commit to a repo by parsing
arbitrary shell, and guesses wrong on anything beyond `cd X && git commit` /
`git -C X commit`. A guard should **only DENY when confident** the commit
targets the shared PyAutoMind checkout. Fix: when the command contains a
construct the clause parser cannot confidently attribute — a `for`/`while`
loop, a subshell `(...)`, a function body, or a `cd` that is not a
clause-leading token — **fail OPEN** (allow), because the deny path's whole
justification is certainty. The narrow, high-confidence DENY cases (a bare
`git commit` whose effective cwd is unambiguously a PyAutoMind checkout, or an
explicit `git -C <mind> commit` without `--`) stay. A noisy refusal trains
bypass-by-default (docs/agent_failure_modes.md §4) — this guard is now the
campaign's own example of that cost.

Also weigh: has the commit guard caught a REAL bad Mind commit since deploy, or
only FP'd while the `-- <files>` habit did the real work? If it is all cost and
no catch, the honest move may be to narrow it to near-nothing (bare `git
commit` in a Mind cwd only) or retire it in favour of the habit + the
stale-claim guard (which HAS true-positived). Decide with the evidence.

<!-- filed 2026-07-17 after the 3rd guard false-positive-on-author (for-loop) -->
