# complete/ — the finished-work archive

One file per shipped task, bucketed by completion date:

```
complete/<YYYY>/<MM>/<slug>.md      # months zero-padded → lexical == numerical order
complete/unknown/<slug>.md          # entries with no derivable completion date
```

This is the third and final state of a prompt's lifecycle
(`draft/ → active/ → complete/`), written by `scripts/lifecycle.py record` when
`ship_library` / `ship_workspace` records a task done. The dated records **are**
the completion ledger — the task's `active.md` entry is simply removed.

## What a record holds

Each `<slug>.md` is the **rich completion record** (the substance that used to
live as one `## <slug>` section in the retired monolithic `complete.md`): the summary,
PRs, key traps/findings, worktree notes — plus, appended under
`## Original prompt`, the prompt the task started from. The rich record is the
point: an agent looking up "have we hit this before / what did we learn about
X" reads one record, not a 6000-line file.

## How to look something up (token-light — RAG is dead)

1. Read `complete/index.md` (the curated navigation — grouped `[[slug]]` links
   with one-line hooks, grouped by date, `unknown` last). It is **generated**
   from the records by `scripts/lifecycle.py index` — regenerate with
   `lifecycle.py index --apply`; a hand-curated **Highlights** band between the
   `CURATED` markers survives regeneration.
2. Follow one or two links to the records you need.
3. Only then grep a specific `complete/<YYYY>/<MM>/` bucket.

## Provenance

- Records are **written by the ship skills** via
  `lifecycle.py record <slug> --date <YYYY-MM-DD> --from-file <body> --apply`,
  not by hand. They are the **sole** completion ledger.
- `index.md` is generated (`lifecycle.py index`); `lifecycle.py index --check`
  fails on staleness (CI).
- `scripts/lifecycle.py check` guards the invariant (no `active.md` slug has a
  record — finished work must leave `active.md`; no file in two states).
- The historical bulk was produced once by `lifecycle.py split-complete` from
  the monolithic `complete.md` ledger, which was **retired** on 2026-07-16
  (issue #81) after a parity backfill — its full history is in git.
