# Auto-request GitHub Copilot code review on every PR, org-wide

Type: maintenance
Target: PyAutoLabs org (all repositories) — GitHub config, not a code repo
Repos:
- (org-level) PyAutoLabs — applies to all repositories, present and future
Status: planned

## Why

Copilot code review has become part of the working loop: on M2/M3/M4 of the
release-validation redesign, a Copilot review was requested on each PR and its
findings folded back in as retroactive fixes (a real bug — a stray literal quote
inside a `python3 -c '...'` block that broke bash quoting — was caught this way).
Right now that review has to be **requested by hand on each PR** (via
`mcp__github__request_copilot_review`, or a chat instruction to the agent).
That is easy to forget and does not cover PRs opened by humans or other agents.

The durable fix is to make Copilot review **auto-initiate on every PR** at the
GitHub level, so it fires regardless of who or what opens the PR, with no
per-session setup and no reliance on an agent remembering to ask.

## What to do

Create an **organisation-level branch ruleset** on `PyAutoLabs` that
automatically requests a Copilot code review. Verified steps (GitHub Docs,
"Configuring automatic code review by GitHub Copilot"):

1. `PyAutoLabs` org → **Settings**.
2. Sidebar → *Code, planning, and automation* → **Repository** → **Rulesets**.
3. **New ruleset** → **New branch ruleset**.
4. **Ruleset name** e.g. `auto-copilot-review`; **Enforcement status: Active**.
5. **Target repositories** → **Add target** → *Include by pattern* → `*`
   (all repos, present and future).
6. **Target branches** → **Add target** → *Include default branch*.
7. **Branch rules** → tick **Automatically request Copilot code review**.
   Optionally also tick **Review new pushes** (re-review each push, not just
   once) and/or **Review draft pull requests**.
8. **Create**.

Scriptable alternative (if rolling out across several orgs): the org rulesets
REST API `POST /orgs/{org}/rulesets` — confirm the exact rule-type payload for
the Copilot-review rule before scripting; the UI path above is the verified one.

## Acceptance

- A newly-opened PR into any PyAutoLabs repo's default branch shows **Copilot**
  under *Reviewers* automatically, with no manual request.
- Works for PRs opened by a human, by Claude Code, and by any other agent.

## Notes / constraints

- **Plan requirement:** automatic Copilot review needs a **Copilot Pro, Pro+, or
  Max** plan on the org. Confirm the org's plan before relying on this.
- **Why not do it agent-side:** a chat instruction only covers PRs the agent
  opens in that session; a global `~/.claude/CLAUDE.md` does not survive the
  cloud/mobile ephemeral container (reclaimed on inactivity). Only the org
  ruleset is durable + all-repos + author-agnostic.
- A repo-level ruleset (same rule under a single repo's Settings → Rules →
  Rulesets) is the fallback if the org plan can't cover `*`.
- Cannot be applied by the cloud/mobile agent: the GitHub MCP surface exposes
  PR/issue/actions tools but no ruleset-write endpoint, and there is no `gh`
  CLI in that environment. This is a ~2-minute human toggle in the GitHub UI.

## Provenance

Written during the M4 release-validation-orchestrator session (PyAutoBrain #8),
where Copilot review was requested manually on the PR — this task exists so that
manual step becomes unnecessary going forward.
