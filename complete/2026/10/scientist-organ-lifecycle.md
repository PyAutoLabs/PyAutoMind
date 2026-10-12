## scientist-organ-lifecycle
- issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/73 (closed)
- completed: 2026-10-12
- workspace-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/74 (MERGED)
- summary: Independent profiles distinguish available, setup-incomplete, connected and paused observation. Setup promotion and resume validate identity/feed before atomic writes; pending/paused entries make no feed requests or revive cache as current.
- validation: 126 Python, 7 Node, four Chromium layouts plus no-JS passed; three offline configuration checks passed. Exact-head Board tests PR run and its sole test job passed. Workflow push trigger is main-only. Author diff review; no independent review claimed.
- readiness: Heart STALE — release validation incomplete: no rehearsal for current source. No release claimed.
- limits: pause only affects Scientist observation, not owner jobs/services; visitors need the updated published page. No independent destination deployed.
- next: Remaining programme work includes a real independently hosted acceptance run, record-preserving upgrades/recovery and collaborator acceptance. Implementation of observation lifecycle is complete.

## Original prompt

# Explicit optional-organ setup and pause states

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoScientist
Difficulty: medium
Autonomy: supervised
Consequence: judge
Status: active
Issued: 2026-10-12
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/73

## Original request

ok conitnue

## Context and scope

Continue the optional-organ activation milestone after Broca setup and publication
PRs #17/#19. @PyAutoScientist currently stores only connected organs and fetches
every selected feed. Add explicit setup and observation-pause state, while owners
retain readiness and jobs. This is one Scientist PR, not remote provisioning.

## High-level plan

- Show available organs and setup-incomplete entries without contacting their feeds.
- Keep connected, paused and evidence-needs-attention states distinct.
- Add preview/apply operations to begin setup, pause observation and validate resume.
- Prove transitions, preservation and zero fetches for setup/paused organs in Python
  and browser checks; document the fresh-chat workflow.

Tier: judge — merge mode: human /prm.

## Detailed implementation plan

1. `scripts/instance_profile.py`: extend schema v1 compatibly with optional
   `organ_setup` entries (canonical organ key -> explicit repo/pages_url) and an
   optional boolean `paused` on existing connections. Existing profiles remain
   valid and unchanged by loading. Reject an organ appearing in both maps. No
   local setup paths, task history or private records enter public snapshots.
2. `scripts/organ_lifecycle.py` (new): preview/apply begin-setup and pause/resume
   actions; reuse existing profile/project validation and atomic input-checked
   writes. Store only chosen connection/setup state; Mind remains the task ledger.
   Resume validates the selected HTTPS feed and identity before unpausing.
3. `scripts/connect_organ.py`: promote a matching pending setup entry only after
   successful feed validation. Preserve no-op/retry behavior, reject conflicting
   identities, and require explicit resume for a paused connection. Never discard
   configured connection data when the feed becomes unavailable.
4. `scripts/organism_board.py` and `scripts/overview.js`: render an opt-in available
   catalogue plus setup-incomplete and paused cards for independent profiles.
   Skip setup/paused feed requests on server and browser, including startup,
   interval and visibility refresh; do not revive cached evidence as current.
   Keep connected evidence status separate from configuration state. Use existing
   shared components and native disclosures; preserve keyboard focus and no-JS
   readability. Available/setup entries are not counted as connected or included
   as active board destinations. Existing unprofiled dashboard behavior is retained.
5. Extend profile, connection, collector and Node/browser tests: old-profile
   compatibility; invalid transitions; failed validation preserves profile bytes;
   setup->connected->paused->resumed; changed-input refusal; no network while
   pending or paused; grey/stale/missing feeds never imply an uninstalled organ;
   browser/server agreement and cache behavior. Inspect representative desktop
   and mobile rendering with a differently named instance.
6. `STARTER.md` and a bounded example: distinguish pause of Scientist observation
   from stopping jobs/services. Explain availability, setup, validated connection,
   pause and owner evidence. Use copyable AI prompts, not browser-side config writes.

## Acceptance boundaries

Pause means Scientist observation only. It does not cancel compute, suspend GitHub
Actions or stop services. Connection means validated location/contract, not healthy
evidence. No hosting destination or collaborator access is needed for this PR.
Live independent deployment, record-preserving upgrades and collaborator validation
remain separate milestones.

## Branch and readiness survey

Scientist canonical main is clean at 2f69a3a; no active claim. An old unregistered
pyautodna-stack-management worktree is clean with no commits ahead of main and
will be left alone. Proposed branch `feature/scientist-organ-lifecycle`, bundle
`.worktrees/scientist-organ-lifecycle`; start_workspace -> ship_workspace.

Three clean canonical library checkouts were fast-forwarded to resolve Heart's
behind-origin reasons. Refreshed Heart at 2026-10-12T14:30:53Z: STALE, no RED or
YELLOW reasons; only `release validation incomplete: no rehearsal for current source`.
This permits development, not release. Plan awaits explicit approval.

Approved by user: "I approve", 2026-10-12.

## Implementation handoff — 2026-10-12

PR https://github.com/PyAutoLabs/PyAutoScientist/pull/74 at 13a16de on
feature/scientist-organ-lifecycle, bundle .worktrees/scientist-organ-lifecycle.
Optional organ_setup entries and paused connection flags preserve old profiles.
New lifecycle CLI previews/applies setup/pause/resume; setup promotion and resume
validate identity/feed and retain atomic write/input-change guards. Pending/paused
feeds are excluded from server/browser collection and cached evidence; owner jobs
are unaffected. Available catalogue and setup cards use native disclosures.
Paused Heart reports UNKNOWN. Existing unprofiled behavior is retained.

126 Python + 7 Node tests PASS; four Chromium layouts plus no-JS PASS (network,
cache, focus, disclosures, overflow); mobile/desktop screenshots inspected. Three
offline config checks and author diff review PASS. Evidence: bundle pytest.log,
node.log, browser-evidence/, lifecycle.html and readiness.json. Heart STALE only
for missing current-source rehearsal. No independent review claimed.

Next: human /prm. Actual independent deployment and owner execution controls remain
separate; observation pause requires republishing/reloading the Scientist page.
