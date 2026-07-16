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
