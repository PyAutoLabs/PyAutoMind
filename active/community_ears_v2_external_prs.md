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
