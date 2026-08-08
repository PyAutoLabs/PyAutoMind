- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/209 (CLOSED completed)
- pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/210 — squash-MERGED 2026-08-08 as `83b65f1c`, 4 files, +250/-8
- classification: library (PyAutoBrain) — bug, infrastructure
- branch: `claude/automind-task-planning-ef00l2` (cloud session; NOT the `feature/<task>` convention)
- worktree: none — cloud session with only the PyAutoMind + PyAutoBrain checkouts, no `~/Code/PyAutoLabs-wt`. Nothing to release.

## What was wrong

`worktree_list_claimed` (`bin/worktree.sh`) split every `  - <repo>` claim bullet in
`active.md` on `": "`, the schema the `start_library`/`start_workspace` references
document. Writers also emit `  - <repo> (<branch>)`, which the split swallowed whole:
`repo` became `autolens_workspace (feature/foo)`, never equalled the requested repo
name, and `worktree_check_conflict` — the `start_dev` step-6 guard choosing between
`active.md` (can start) and `planned.md` (blocked) — returned "no conflict" for those
claims.

**The split is roughly even: 162 colon-form vs 139 paren-form across `active.md`
history.** So about half of all claims were invisible to the guard, not a rare shape.

Two further defects in the same awk, neither in the original prompt:

- `worktree:` was captured on sight, so a `repos:` block placed **above** it emitted
  `-` for the worktree path — an order-dependent field.
- Bare `  - <repo>` claims (no branch at all, e.g. `  - PyAutoReduce`) and colon-form
  lines with trailing notes (`  - HowToFit: feature/x (base 65e8fbd == origin/main)`)
  both occur in the real ledger and needed handling.

## Fix

Rewrote the awk block: match `": "` first, else a ` (`-delimited branch, else treat
the whole line as a bare repo name; strip trailing whitespace from `repo`. Claim rows
now accumulate per task and flush via `flush()` on `/^## /` and at `END`, replacing
emit-on-sight so field order no longer matters. `worktree_check_conflict` itself was
never changed — it was reading bad input.

Both forms stay accepted rather than migrating the ledger.

## Traps and findings

- **BLAST RADIUS WIDER THAN THE PROMPT.** The prompt scoped this to "the routing
  decision only". `skills/repo_cleanup/reference.md` also defines its `CLAIMED`
  protection set as the `(repo, branch)` pairs from this function, so malformed repos
  and empty branches left in-flight branches short one of their three guards against
  delete proposals. `IN_WORKTREE` and `OPEN_PR` still covered them, so no branch was
  lost — but a `repo_cleanup` sweep was running with one protection set effectively
  empty.
- **THE PROMPT'S PREMISE WAS WRONG, AND SO WAS THE FIRST CHECK OF IT.** The prompt
  says the paren form is "what every skill and every existing entry writes"; it is
  ~53/47 and both are live. A first history sweep reported *zero* paren-form lines,
  appearing to refute the prompt outright — that was a **SHALLOW CLONE** showing two
  days rather than the record. `git fetch --deepen=500` gave the real counts. Either
  reading taken at face value would have sent the docs change the opposite wrong way.
  Cloud-session clones are shallow: check `git rev-parse --is-shallow-repository`
  before drawing any conclusion from repo history.
- **SIZING NOT TAKEN.** The Bug Agent scored this `large (8)`; the prompt header says
  `small`. The prompt header was right — the change is a 41-line awk rewrite plus
  tests. Score is prose-driven off a long prompt, same as the
  `mge-sigma-min-workspace-sweep` precedent.
- **BACKGROUND GITHUB POLLING IS A DEAD END IN CLOUD SESSIONS.** A `curl`-based CI
  watcher looped silently on `KeyError` because unauthenticated `api.github.com`
  returns `"GitHub access is not enabled for this session"`. It would never have
  fired. GitHub reads here must go through the MCP tools.
- The `worktree:` value for this task's own entry is the literal string `none`, which
  parses as-is; the guard prints it in the conflict message without complaint.

## Validation

- `tests/test_worktree_conflict_guard.py` (new, 13 tests) — drives the real bash
  functions against temp `PYAUTO_MAIN` fixtures, on the `test_worktree_claim_guard.py`
  idiom. **Written first and confirmed FAILING on all four defects** against the
  unfixed parser; the colon-form and guard-contract cases passed throughout, isolating
  the regression.
- Full suite 250 passed locally and on both CI legs (3.12, 3.13), first run, no
  retries. The count reconciles with local (237 baseline + 13 new), confirming the new
  fixture tests actually ran rather than being collected-but-skipped.
- **Corpus check against the real ledger:** all **258** claim lines in `active.md`
  history parse to a bare repo name, **0** malformed, and all **32** distinct names
  resolve against `PyAutoMind/repos.yaml`.
- **Live dogfood:** this task's own `active.md` entry was deliberately written in the
  paren form. With the fix, `worktree_check_conflict some-other-task PyAutoBrain`
  exits 1 and names the claiming task — the first time the step-6 guard has fired on
  the real ledger — while `worktree_check_conflict worktree-claim-parser-forms
  PyAutoBrain` still exits 0.

## Docs corrected

`skills/start_library/start_library.md` and `skills/start_workspace/reference.md` now
state that both forms parse and the branch is optional. This also corrected a factual
error in the former: it claimed `worktree:` is what `worktree_check_conflict` reads,
when the `  - <repo>` bullets are the claim and `worktree:` is only reported alongside.

## Follow-up available (NOT done here)

Several `active.md` entries carry hand-written `repos-none-claimed:` notes explaining
that they deliberately avoid `  - Repo` bullets "because `worktree_check_conflict`
treats any such bullet as a live claim". Those contortions were written to steer
around a guard that never fired. They are harmless now but no longer necessary —
worth a sweep, deliberately left alone here rather than editing a shared ledger inside
an unrelated PR.

## Original prompt

# `worktree_check_conflict` has never detected a conflict

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: high

`PyAutoBrain/bin/worktree.sh` → `worktree_check_conflict` always exits 0. The
`start_dev` step-6 conflict guard, which decides whether a new task registers in
`active.md` (can start) or `planned.md` (blocked), has therefore never fired for
any task.

## Root cause

`worktree_list_claimed` (worktree.sh:309-335) parses `PyAutoMind/active.md` with:

```awk
/^  - [A-Za-z]/ {
  gsub(/^  - /, "")
  split($0, parts, ": ")
  repo   = parts[1]
  branch = parts[2]
  printf "%s\t%s\t%s\t%s\n", task, repo, branch, wt
}
```

It expects `  - PyAutoFit: feature/foo`. But `active.md` is written today as:

```markdown
- repos:
  - autolens_workspace (feature/multistart-prodigy-start-here)
```

No `": "` separator. So `parts[1]` swallows the whole line and `repo` becomes
`autolens_workspace (feature/multistart-prodigy-start-here)`, with `branch`
empty. Confirmed live:

```
$ source PyAutoBrain/bin/worktree.sh && worktree_list_claimed
multistart-prodigy-start-here	autolens_workspace (feature/multistart-prodigy-start-here)		~/Code/PyAutoLabs-wt/multistart-prodigy-start-here
```

`worktree_check_conflict` (worktree.sh:340-355) then compares
`"$existing_repo" == "$want"`, i.e. `"autolens_workspace (feature/...)"` against
`"autolens_workspace"`. Never equal → `rc` stays 0 → "no conflict", always.

Reproducer (`autolens_workspace` is claimed by two active tasks as of
2026-07-29):

```bash
source PyAutoBrain/bin/worktree.sh
worktree_check_conflict some-new-task autolens_workspace; echo "exit=$?"
# exit=0   <-- should be 1
```

## Fix

Parse both shapes in the `worktree_list_claimed` awk block — the current
`  - <repo> (<branch>)` form and the legacy `  - <repo>: <branch>` form the
awk was written for — so `repo` is always the bare repo name. The branch is
informational (used only in the conflict message), so tolerate it being absent.

Do **not** "fix" this by rewriting `active.md` into the colon form: the
paren form is what every skill and every existing entry writes, and
[[feedback_active_md_dash_repos]] records that these `  - Repo` lines are the
claims. The parser is what is wrong.

Note the schema drift runs both ways —
`PyAutoBrain/skills/start_workspace/reference.md` ("active.md registration")
still documents the colon form the awk expects:

```markdown
- repos:
  - PyAutoFit: feature/<task-name>
```

So the parser matches the *documented* schema and the writers drifted away from
it. Accepting both forms fixes the guard without a migration; whether to also
re-align the docs on one form is a separate call.

## Validation

- `worktree_check_conflict <new-task> autolens_workspace` exits 1 and names both
  `multistart-prodigy-start-here` and `assistant-start-here-scripts`.
- `worktree_check_conflict multistart-prodigy-start-here autolens_workspace`
  still exits 0 (a task never conflicts with itself).
- `worktree_list_claimed` emits the branch in its own column again.
- Repos claimed by no task still exit 0.

## Notes

- Found 2026-07-29 while running `start_dev` for
  `draft/docs/workspaces/likelihood_function_jax_section_to_pointer.md`; the
  guard reported no conflict on two repos that two active tasks both claim.
- Blast radius is the routing decision only — it makes `start_dev` register
  every task as startable, so genuinely-colliding tasks silently proceed in
  parallel instead of queueing in `planned.md`. Every parallel-claim decision
  made to date was made by a human reading `worktree_list_claimed` by eye, not
  by the guard.
