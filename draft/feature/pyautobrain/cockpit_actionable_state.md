# Human-first cockpit: actionable state and honest freshness

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- pyautolabs.github.io
Difficulty: medium
Priority: high
Autonomy: supervised
Status: draft

Affected repositories: @PyAutoBrain and @pyautolabs.github.io.

## Proposed first increment (awaiting plan approval)

Keep the static cockpit, independent organ boards and existing v1 state feeds.
Extend the existing contract additively and demonstrate it with Brain overnight
workflow attention items. Improve the cockpit's explanation, next-action labels
and freshness handling. Preserve the complete user direction below as the design
constraint for future increments; it is not permission to implement every example.

### Human plan

1. Extend existing attention items with stable identity, canonical state, reason,
   explicit recommended actions, evidence and optional human-decision metadata.
2. Populate those fields for overnight workflow failures, blocked gates and
   unavailable observations using evidence already collected by Brain.
3. Show concise reasons and labelled next actions in the cockpit; keep legacy
   feeds readable and existing navigation/mobile behaviour intact.
4. Separate source health from observation freshness. Cached green must not
   present as currently verified healthy; retain last-known failures as context.
5. Validate contract compatibility, workflow mappings, freshness and browser
   behaviour. Document incremental adoption and action safety defaults.

### Detailed implementation plan

- `PyAutoBrain/board/_state.py`, `board/state_schema.json`: retain schema_version
  1 and required colour/status fields for current consumers. Add optional typed
  item fields: stable `id`, canonical `state` (healthy, active, stale, blocked,
  failed, action_required, unknown), `reason`, `actions`,
  `recommended_action_id`, `requires_human_decision`, `decision`. Action records
  carry an id, label, kind (link/command/prompt), target and explicit safety
  semantics. Default absent safety to unclassified, never permission to execute.
  Add only provenance/freshness fields justified by the producer; use the
  existing item URL for evidence and `updated` for computation time. Do not
  invent last_success or equate computation time with source observation time.
  Optional fields must validate when present; legacy fixtures stay valid.
  Keep source colour severity separate from canonical workflow state, rather
  than treating every red signal as failed or every yellow as a human decision.
- `PyAutoBrain/board/_board.py`: enrich `_state_items` overnight rows from the
  existing collection, using repo/workflow identity rather than array position or
  display text. Distinguish failed run, blocked gate, unreadable source and other
  conclusions honestly. Preserve evidence/run links, source conclusions and
  existing `/bug` payloads. Declare existing investigation prompts as manual
  handoffs, not callable shell commands. The same record supplies UI label and
  copy target; detection invokes nothing. Populate human-decision fields only
  with affirmative source evidence, not merely because a workflow is blocked.
- `pyautolabs.github.io/cockpit/index.html`: validate enriched fields and cached
  feeds, render reason/action/decision details only where present, and retain
  legacy prompt fallback without duplicate buttons. Keep URL scheme guards and
  escaping. Introduce a pure observation/view-model function separating current
  source status, fetch outcome and last-good context, used by header/cards/nav.
  Failed fetches and invalid timestamps cannot silently count as current green.
  Support producer-declared freshness policy if supplied; do not invent a common
  expiry interval across different organ schedules. Distinguish last fetched
  from last generated. Existing source status transitions remain separate from
  fetch failures; no new notifications, persistent monitoring or execution path.
- `pyautolabs.github.io/cockpit/sw.js`: bump shell cache for the changed page;
  feeds remain uncached. Preserve selected iframe during polling and history.
- Tests: extend `PyAutoBrain/tests/test_state_feed.py` and focused board tests
  for old feeds, invalid optional metadata, stable ids, failed/blocked/unreadable
  distinctions, explicit safety and evidence preservation. Exercise cockpit
  with old/enriched fixtures, cached green + failed fetch, cached red + failed
  fetch, bad cache, missing/invalid/future timestamps, and recovery. Browser
  checks at desktop/mobile sizes, light/dark, keyboard/copy, navigation/history
  and unchanged iframe during polling. Use existing browser tooling if present;
  do not add application dependencies for tests.
- Documentation: `PyAutoBrain/board/AGENTS.md` and website `AGENTS.md`/README
  describe additive adoption and the standing human-first architecture. Document
  that stable records can be compared later but no event bus or agent is added.

### Scope and non-goals

One bounded vertical slice across producer and consumer. No autonomous agent,
Slack integration, message bus, microservice, general permissions engine,
automatic retries/remediation, new workflow dispatch endpoint or whole-ecosystem
feed migration. Existing source owners retain authority; Brain composes their
truth. An action descriptor describes an existing operation/handoff, not a new
universal executor. Do not invent scientific choices or source timestamps.

Suggested branch: `feature/cockpit-actionable-state`.
Plan approval and workflow worktree setup are required before source edits.

### Planning evidence (2026-10-01)

- Heart entry check: STALE, test run status unknown (no report.json); install
  verification not run; no release validation for current source. Planning is
  permitted; this is not ship-time acknowledgement.
- Brain and website are clean on main. Mind was clean on main before this draft
  and its required generated dashboard refresh. No matching active task and
  `worktree_check_conflict cockpit-actionable-state PyAutoBrain pyautolabs.github.io`
  exits 0. No source worktree created yet.
- Recent Brain branches: main, feature/abell-1201-point-mass,
  feature/cortex-may-submit, claude/pyauto-cti-ci-phase-5-n4idom,
  claude/hygiene-agent-run-n9qtd5. Website: main, docs/restore-organ-sentence.
- Prior art consulted: Mind completion records organ-cockpit-state-feed,
  cockpit-page and cockpit-integrated-navigation. Preserve the independent
  feed owners, shared v1 contract, static PWA and integrated board navigation.
- Feature conductor initially resolved only Brain; actual scoped plan explicitly
  includes website consumer. Its keyword-based lensing/optimisation suggestions
  arise from examples in the full request, not this implementation. No science
  library/API changes are planned. Declared medium sizes the bounded increment,
  not all future integrations in the original request.
- Next: user plan approval, create_issue primitive, register and set up isolated
  worktrees through the applicable start skills; Brain contract/producer first,
  website consumer second. Use a worktree root inside the workspace in accordance
  with root AGENTS.md. No issue, PR or source edits yet.

## Original user request (verbatim)

I want to continue developing the PyAutoLabs cockpit/dashboard, with one important architectural goal in mind:

«The cockpit should remain primarily a high-quality human interface for me today, but its underlying state and actions should be designed so that a persistent AI agent could safely monitor it and take actions in the future.»

Do not build the autonomous agent yet. Do not over-engineer the system around speculative future integrations. The immediate priority remains making the cockpit genuinely excellent and useful to a human.

However, wherever reasonable, structure the implementation so that adding an agent later is straightforward.

Core principle

The cockpit should not merely be a visual webpage.

It should be a presentation layer over a structured, machine-readable representation of the state of PyAutoLabs.

Anything important that appears visually on the dashboard should ideally have an equivalent structured representation that another program or agent could inspect without screen-scraping the UI.

For example, a workstream/card should eventually be able to expose concepts such as:

status
health
last_checked
last_updated
last_success
owner
priority
recommended_action
available_actions
automation_safe
requires_human_decision
escalation_reason
context
links

These exact fields are not mandatory. Use the existing architecture and introduce abstractions only where they genuinely improve the design.

Status model

Where appropriate, converge toward a small, consistent status vocabulary across the cockpit, for example:

healthy
active
stale
blocked
failed
action_required
unknown

Avoid each subsystem inventing subtly different meanings for the same state.

The visual dashboard can still use richer wording, but there should ideally be an underlying canonical state.

Make problems actionable

When the cockpit identifies a problem, try to make the state answer three questions:

1. What is wrong?
2. Why does the system think it is wrong?
3. What could be done next?

For example:

Strong-lensing paper ingestion
status: stale
last_success: 12 days ago
reason: expected maximum interval is 7 days
recommended_action: run strong-lensing catch-up

This is useful to me now and is exactly the sort of structured state a future agent could act upon.

Explicit actions

Where the dashboard currently represents something I could manually fix, prefer making that operation an explicit action rather than burying the behaviour inside the UI.

Conceptually:

run_catch_up()
retry_workflow()
refresh_state()
open_issue()
rerun_tests()
restart_campaign()

The UI may expose these as buttons, links, commands, or workflows.

The important architectural principle is:

«An action should ideally exist independently of the button that invokes it.»

A future AI agent should be able to invoke the same underlying operation without pretending to click the webpage.

Separate detection from remediation

Where possible, keep these distinct:

detect problem
    ↓
describe problem
    ↓
recommend action
    ↓
execute action

Do not automatically execute something simply because it has been detected unless that behaviour is already clearly intended.

This separation will later allow us to choose whether:

- the cockpit only reports a problem,
- I manually approve the action,
- deterministic automation handles it,
- or an AI agent decides whether to act.

Future automation safety

For actions that could eventually be automated, consider whether they naturally fall into categories such as:

safe to run automatically
safe but notify afterwards
requires approval
requires scientific judgement
destructive / never automatic

Again, do not create a giant permissions framework prematurely.

But if an action already has meaningful risk or approval semantics, represent that explicitly rather than leaving it implicit.

A lightweight concept such as:

automation_safe: true / false

or an equivalent enum would be useful when appropriate.

Human decisions should remain explicit

One of the most important future behaviours will be distinguishing:

«“Claude can solve this”»

from:

«“James needs to make a scientific/design decision.”»

When a workstream is blocked by human judgement, try to represent that explicitly.

For example:

status: action_required
requires_human_decision: true
decision: "Should we prioritise image-plane or source-plane optimisation next?"
context: [...]

The cockpit should eventually make these decision points particularly easy to surface.

Event-friendly architecture

Do not implement a persistent monitoring service yet.

However, avoid architectures where the only way to know that something changed is by repeatedly rendering and visually inspecting the dashboard.

Ideally, important state transitions could eventually produce an event such as:

workflow_failed
campaign_stalled
memory_stale
tests_recovered
new_action_required
human_decision_required

These could later feed:

PyAutoLabs state
      ↓
event
      ↓
persistent Claude / other agent
      ↓
investigation or action
      ↓
updated PyAutoLabs state
      ↓
optional Slack notification

Slack should be considered an optional notification/output surface, not the central architecture.

Provenance and auditability

For important state and actions, retain enough provenance that I—or a future agent—can answer:

- Where did this status come from?
- When was it computed?
- What evidence caused it?
- What action was run?
- Did it succeed?
- What changed afterwards?

For example, links to GitHub Actions runs, issues, PRs, profiling results, logs, papers, or previous workflow runs are preferable to opaque states.

This will make autonomous behaviour much safer later.

Prefer APIs/state over screen interpretation

When adding new cockpit features, ask:

«“Could another piece of software understand this state without looking at pixels?”»

If not, consider whether there should be a structured backing model.

Do not compromise the visual design to achieve this. The human-facing cockpit should remain concise, attractive and intuitive.

The desired architecture is roughly:

              ┌───────────────────┐
              │ PyAutoLabs state  │
              └─────────┬─────────┘
                        │
               ┌────────┴────────┐
               │                 │
        Human cockpit       Future agent
               │                 │
          buttons/actions    tools/actions
               │                 │
               └────────┬────────┘
                        │
                 PyAuto ecosystem

The dashboard and the future agent should consume the same underlying truth, rather than the agent treating the dashboard UI itself as the source of truth.

Do not over-engineer

This is important.

Do not pause useful cockpit development to build:

- a general agent framework,
- a message bus,
- complex permissions infrastructure,
- generic orchestration abstractions,
- speculative Claude integrations,
- unnecessary microservices.

Instead, whenever touching an existing feature, ask whether a small architectural decision now will make future automation significantly easier.

Prefer incremental changes.

Near-term development priority

Continue optimising for:

1. A cockpit that immediately tells me the health of PyAutoLabs.
2. Clear identification of things that need my attention.
3. Useful context explaining why they need attention.
4. Obvious next actions.
5. Direct links into the underlying work.
6. Reliable state and sensible freshness/staleness indicators.
7. Minimal noise.

Then, underneath that, gradually make the state structured and the actions callable.

Long-term target

Eventually I want the possibility of:

PyAutoHeart notices something unhealthy
              ↓
structured cockpit state changes
              ↓
agent is triggered
              ↓
agent reads context / relevant skill / runbook
              ↓
agent decides whether intervention is safe
              ↓
Claude Code or another tool performs the work
              ↓
tests / checks run
              ↓
cockpit state updates
              ↓
I am notified only if useful

Examples might eventually include:

- papers have not been ingested for too long → run catch-up
- profiling campaign stalls → investigate
- CI failure appears → diagnose
- known deterministic maintenance task is due → perform it
- issue can be safely progressed → launch development task
- scientific/design choice is required → ask me rather than guessing

The goal is therefore:

«Build a cockpit that becomes the control plane for PyAutoLabs, first for a human and eventually for a human + autonomous agents.»

When implementing future dashboard changes, keep this architectural direction in mind, but always favour the simplest design that improves the cockpit today.
