# Bundles

Sets of **independent** tasks that make sense to run in one orchestrated
session: an architect session (Fable) plans them, subagent sessions (Opus)
implement them, and every member still gets its own issue and its own PR — so
`/prm` closes each one out exactly as it would a standalone task. The skill
that runs one is `start_bundle` (PyAutoBrain).

**A bundle is not an epic.** An epic is *ordered* and phase-gated: one phase at
a time, worked through its ledger, and its members are pulled out of the pick
lists so nobody starts phase 3 first. A bundle is a *flat set* — its members
have no order and no dependency on each other, so they stay in their usual
dashboard sections and a bundle is only an additional VIEW of the backlog. If
the members must happen in order, it is an epic (`epics.md`), not a bundle.

This file holds **pinned** bundles only — the ones a human decided are worth
doing together. The dashboard also proposes **auto** bundles, computed fresh
from the backlog every time it is rendered (same target repo, unblocked,
non-epic, under a size cap, minimum two members); those are proposals and are
never written here. Pinning is how a proposal becomes a record — and how a
bundle that spans repos, or that no rule would ever spot, gets onto the page.

Schema per entry: `## <slug>` then `- title:` / `- members:` / `- rationale:`
(why these belong in one session) / `- status:` (optional, coarse and durable).
`- members:` opens a list of prompt paths, one per indented `  - <path>`
bullet, and closes at the next `- key:` line.

A member prompt may also declare its own membership in its header:
`Bundle: <slug>` (this file's slug). A prompt carrying that header leaves the
auto pool, and if its slug names no entry here the dashboard renders the group
with a ⚠️ rather than silently dropping it.

<!-- No entries yet: the dashboard's auto bundles cover the same-repo case, so
     pin one only when the grouping is something a rule would not find. -->
