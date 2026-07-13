# complete/ — the finished-work archive

One file per shipped task, bucketed by completion date:

```
complete/<YYYY>/<MM>/<slug>.md      # months zero-padded → lexical == numerical order
complete/unknown/<slug>.md          # entries with no derivable completion date
```

This is the third and final state of a prompt's lifecycle
(`draft/ → active/ → complete/`), advanced by `scripts/lifecycle.py move` when
`ship_library` / `ship_workspace` records a task done — in lockstep with the
`active.md → complete.md` ledger move.

## What a record holds

Each `<slug>.md` is the **rich completion record** (the substance that used to
live as one `## <slug>` section in the monolithic `complete.md`): the summary,
PRs, key traps/findings, worktree notes — plus, appended under
`## Original prompt`, the prompt the task started from. The rich record is the
point: an agent looking up "have we hit this before / what did we learn about
X" reads one record, not a 6000-line file.

## How to look something up (token-light — RAG is dead)

1. Read `complete/index.md` (the curated navigation — grouped `[[slug]]` links
   with one-line hooks). *(Built by the follow-up Phase-2 task
   `complete_archive_wiki.md`; until then, grep the dated buckets.)*
2. Follow one or two `[[slug]]` links to the records you need.
3. Only then grep a specific `complete/<YYYY>/<MM>/` bucket.

## Provenance

- Records are **written by the ship skills** via `lifecycle.py`, not by hand.
- `scripts/lifecycle.py check` guards the invariant (no slug in both `active.md`
  and `complete.md`; every record has a ledger entry; no file in two states).
- The historical bulk was produced once by `lifecycle.py split-complete` from
  `complete.md`; `complete.md` is retired once that split is verified.
