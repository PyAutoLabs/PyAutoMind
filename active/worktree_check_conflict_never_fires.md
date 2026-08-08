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
