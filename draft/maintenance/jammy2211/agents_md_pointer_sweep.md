# Finish the CLAUDE.md → @AGENTS.md sweep for the Jammy2211-owned repos

Type: maintenance
Target: Jammy2211 repos
Repos:
- Jammy2211/autofit_workspace_developer
- Jammy2211/euclid_assistant
- Jammy2211/admin_jammy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: complete

<!-- RESOLVED 2026-07-13. euclid_assistant CLAUDE.md -> content-free @AGENTS.md
     pointer + canonical AGENTS.md header (Jammy2211/euclid_assistant#7, merged
     squash). The other two repos needed no change: autofit_workspace_developer
     already carries a compliant @AGENTS.md pointer; admin_jammy has no AGENTS.md
     (record-only per this prompt's rule — slated to leave PyAutoLabs). Reached
     them from a local full checkout rather than a Jammy2211-rooted session.
     repos_sync.py --check now reports "CLAUDE.md -> AGENTS.md pointers: OK". -->


Follow-up from the ecosystem AGENTS.md/CLAUDE.md standardization epic
(`z_features/agents_md_standardization.md`, completed 2026-07-12). That sweep
covered every reachable `repos.yaml` repo, but the three **`Jammy2211/*`** repos
could not be reached from that session: `add_repo` refused with *"cross-tier adds
are not supported in v1"* because the session's sources were all `pyautolabs`, and
a different GitHub owner can't be added mid-session.

**What to do:** run the same spec-1 check on each of the three repos —
- If it HAS an `AGENTS.md` but a missing / non-compliant `CLAUDE.md`, add the
  canonical content-free `@AGENTS.md` pointer (one branch + pointer-only PR per
  repo; auto-mergeable once CI is green).
- If it has NO `AGENTS.md`, do **not** auto-create one; just record it (same rule
  the epic used). `admin_jammy` in particular is slated to leave `PyAutoLabs/` and
  may be doc-light — check before assuming.

**How to reach them:** start a session **rooted on one of the `Jammy2211` repos**
as the initial source (so the session's owner tier is `Jammy2211`), then
`add_repo` the other two from the same owner. Alternatively run it from a context
that already has `Jammy2211` access.

**Note:** these three are already in `repos.yaml`, so once reachable,
`python3 scripts/repos_sync.py --check` (run with them checked out) will report
their pointer status directly — no new tooling needed, just execution.

<!-- filed 2026-07-12 as the reachability tail of the standardization epic; the
     PyAutoLabs sweep found 17/17 eligible repos already compliant, so this is
     expected to be tiny (likely 0-3 trivial pointer PRs). -->
