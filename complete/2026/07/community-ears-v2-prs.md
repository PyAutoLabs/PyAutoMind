- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/125 (CLOSED via PR)
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/126 (merged 2a75453)
- summary: community conductor v2 — the Ears hear pull requests. `community scan` gained two legs per qualifier group: open PRs authored by non-self humans (bot-filtered, merged into the awaiting-response ranking via the same last-actor detection) and open PRs with review requested from a self login (any author); surface adds open_external_prs + awaiting_review + counts, with per-pass distinct degraded labels. `community triage` accepts PR refs (incl. /pull/ URLs) and adds the change-shape block (draft, changed files, +/-, requested reviewers, mergeable state, head→base); PR routes name a *human review with session-drafted comments* — never the ship-gate review faculty (boundary recorded in the conductor AGENTS.md, alongside the review-thread-comments limit). Rate-limit hardening found live: COMMUNITY_SEARCH_PAUSE (default 2s) between the up-to-six search calls, because GitHub's secondary limit trips on bursts even when search quota shows 30/30. 77 tests passed (8 community; 2 new).
- traps: GitHub secondary rate limits are burst-based and OPAQUE — `gh api rate_limit` showed full search quota while searches 403'd; the honest-degrade path (per-pass `degraded:` labels) is what made the throttle visible and debuggable. The first degraded labels were ambiguous ("pr search failed" for both the external-PR and review-requested passes) — fixed to distinct tags.
- concurrency: PyAutoBrain claim conflicts at start were BOTH non-blocking — ic50-assistant-seed (clone/-only PR #120, zero overlap, user-approved pattern) and retire-complete-ledger (stale claim: its Brain PR #123 had merged and the worktree was already deleted). User "go" recorded the override in active.md.
- heart: shipped + merged through the same six unrelated organism-scope RED reasons acked throughout 2026-07-16 (manifest drift grew 2→4 mismatches from the day's merges); human authorized PR-open and merge together ("i authorize, merge").

## Original prompt

# Community conductor v2 — external PRs + review requests

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: human-required
Priority: normal
Status: formalised

Original request (2026-07-16): "do v2" — the staged follow-up recorded in
`agents/conductors/community/AGENTS.md` at the v1 birth (issue PyAutoBrain#119,
PR #122): external PRs and review requests were explicitly out of scope for v1.

Extend the Ears so the community scan hears **pull requests**, not just issues:

- `community scan` additionally surfaces (a) open PRs authored by non-self
  humans (same bot filter + awaiting-response detection as issues) and
  (b) open PRs where review is requested from a self login. Counts + ranked
  lists ride the same CommunityScan surface; `/wake_up`'s digest line covers
  them without new machinery.
- `community triage <ref>` accepts PR refs (including `/pull/` URLs) and adds
  a PR block: draft state, changed files / additions / deletions, requested
  reviewers, mergeable state — the review judgment itself stays with the
  human/session (this is NOT the ship-gate review faculty).
- Same principles as v1: read-only, stdlib-only, never posts; replies and
  reviews are drafted in the session and human-gated; state stays on GitHub.
- Extend the hermetic test suite (stub gh) for the PR searches, the
  review-requested leg and the PR triage block; update the conductor
  AGENTS.md (modes, capability audit, retire the "out of scope for v1"
  note), the /community skill body, and the dispatcher description; then
  regenerate the command surface.
