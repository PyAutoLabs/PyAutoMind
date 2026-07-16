## community-voice-agent
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/119 (CLOSED via PR)
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/122 (merged 16338af)
- summary: birth of the community conductor — the Ears, the organism's receptive language function (Wernicke to the Workspace Agent's Broca/Voice #118): `pyauto-brain community` scan (open issues by non-self humans across every repos.yaml home, bot-filtered, awaiting-response = last word not ours, ranked by waiting days) + triage <ref> (context-sufficiency signals, clarifying-question seeds, comment tail); /community skill drafts every outward reply for human approval and routes actionable work via /start_dev_for_user; /wake_up gained the community scan step + 💬 digest category. Read-only + stdlib-only; conversation state stays on GitHub labels + active.md user-facing entries. 6 hermetic contract tests (stub gh via COMMUNITY_GH; proves no mutating endpoint hit, no file writes); 75 total passed; live-verified both modes.
- naming: intake-approved alias was "the Voice" but workspace-agent #118 merged first carrying it — resolved to "the Ears" mid-task (Broca produces = workspace speaks through examples; Wernicke comprehends = community hears and converses; the human remains the mouth). Analogy carried in the conductor AGENTS.md first line per the founding prompt's requirement.
- first live scan: 7 open external issues, 5 awaiting response — all @rhayes777, 54 days (input-validation series PyAutoArray#333/#332, PyAutoGalaxy#440, PyAutoLens#532/#531); plus @mwiet PyAutoLens#564 + @HRSAstro PyAutoMind#18 (ours-to-watch). Ready-made first /community session.
- heart: shipped through unrelated organism-scope RED on explicit user ack (6 reasons verbatim in PR body; heart-ack was in active.md). Workspace impact: none (Brain CLI/skill infra); smoke tests n/a.
- concurrency: task queued in planned.md blocked-by workspace-agent, unblocked the same morning when #118 merged + claim cleaned; the Mind sweeper's auto-commit carried the draft→active prompt move mid-registration (pathspec-limited commits kept sessions untangled); ic50 #120 (clone/-only) open in parallel, no overlap.
- v2 staged (recorded in conductor AGENTS.md): external PRs / review requests out of scope for v1.

## Original prompt

# Community communication agent — listen and respond to user GitHub issues

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: formalised

I need to think about how I communicate with users and people who put up github issues with requests for new features,
bugs, etc.

Currently, I would just put the GitHub link into a agent chat and go from there but we can formalism this.

First, the wake up skill should give a summary of whether other users (e.g. not me) have raised issues across
any repos so I can then rspond to them.

Do we need a dedicated brain agent for listening to and communicating with users and the community? I dont see why not,
I'm not exactly gonna go to GitHub adn do this myself. I think the agent would be incharge of routing the task,
finding the right brain agent to implement it, and giving the poster updates on whats going on. The point is this
agent knows its communicating with someone else and thus in a conversation, and should really read their github
issue and assess if what theyve provided is enough context or if it should ask for more. so it should pretty much
draft the whole response, assess the issue itself and only real on me to guide it. 

This agent could be called ears? listed? but it also talks to the user, so communicate? Think about the brain
conductor organ analogy.

## Intake review decisions (2026-07-16)

- **Name:** `/community` — alias "the Voice Agent". The organ analogy is the brain's
  language faculty (Broca + Wernicke): comprehension and production are one system,
  so neither "ears" nor "mouth" alone — a voice that presumes an ear. "community"
  itself is functional, not organic — so the agent description file's FIRST LINE
  must carry the analogy, e.g. "the Voice — the organism's language faculty
  (Broca + Wernicke): it hears the community and speaks back", matching how
  intake opens as "the Conception Agent".
- **Scope: one prompt, two legs.** (1) Sensory leg: the `/wake_up` skill (renamed
  from `/morning`, PR merged 2026-07-16) gains a summary of open issues/comments
  raised by non-Jammy humans across all repos.
  (2) Conductor leg: a new PyAutoBrain `/community` conductor that reads a user-filed
  issue, judges whether context is sufficient (else drafts a clarifying question),
  routes actionable work via the existing `start_dev_for_user` / dev-workflow
  primitives, and drafts every outward reply + progress update for human approval.
- **Autonomy is load-bearing:** human-required. All outward messages to real users
  are drafts gated on Jammy; the agent assesses and drafts, the human sends/approves.
- **Anchors on existing machinery:** `start_dev_for_user` (dispatch primitive for
  user-filed issues), `/wake_up` (where the summary leg lands), the
  user-facing-issue update cadence memory (~5 milestones for bugs, 4 for features).
- **Difficulty: medium** (sizer said small; new conductor + morning leg +
  conversation-state handling across ~25 repos).

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/108dd0d1-943c-42df-87c0-7a71fd409e72/scratchpad/intake_raw.md -->
