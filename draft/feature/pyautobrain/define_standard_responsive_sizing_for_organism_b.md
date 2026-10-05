# Define standard responsive sizing for organism boards

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoEars
- PyAutoPulse
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready

# Define standard responsive sizing for organism boards

Type: feature
Difficulty: medium
Priority: normal
Autonomy: supervised

Primary target: @PyAutoBrain, the owner of the shared board theme. Audit consuming boards and identify any repo-specific adoption work during planning; do not assume every repo needs edits.

## Objective
Define a consistent responsive sizing standard for the organism's boards, using the wider Ears board as the preferred desktop reference. Establish the shared implementation and an evidence-based rollout plan while preserving usable phone/tablet layouts.

## User request (verbatim)

I like the board a lot, but its wide compared to other boards, can we do an assessment of whether this width is bad (e.g. for mobile) or if we can put in a plan to make all boards this width? It seems strange that other boards are narrow and I cant think why that would be other than for mobile. Ears width is defo good, so its a mobile thing?

Ok, I want you to intake this as a task to define standard sizing and I'll run it in another chat.

## Assessment already completed
- Shared theme `PyAutoBrain/board/_theme.py`: body maximum 44rem (normally 704px), increasing to 60rem (960px) at a 64rem viewport breakpoint. The comments describe phone-first reading width and an earlier widening for laptop data boards.
- Heart consumes that shared theme. Ears overrides it with a 1240px maximum and 24px desktop / 16px mobile padding (`PyAutoEars/ears/presentation.py`). Pulse uses an independent 1200px main container (`PyAutoPulse/pulse/board.py`). Reconfirm these values on current main before planning.
- Maximum desktop width does not impose that width on phones: the outer page still shrinks to fit the viewport.
- Ears browser checks passed at 390px and 1280px in light/dark themes without whole-page horizontal overflow. Its phone tables have their own horizontal scroll (740px conversation and 650px coverage minimum widths); important columns can remain off-screen. That is a separate mobile interaction trade-off, not a reason to keep desktop boards narrow.
- Ears redesign shipped in PyAutoEars PR #10; Mind record `complete/2026/10/community-board-readability.md`. The user explicitly likes the wider result.

## Starting proposal for the next chat
1. Standard outer maximum: 1240px (or equivalent relative unit), with consistent fluid sizing and responsive gutters. Keep compact screens fluid rather than imposing a minimum page width.
2. Separate content measures: tables, metrics and data rows can use the full board width; prose, prompts and expanded explanations should have a comfortable narrower reading measure, initially around 65ch.
3. Define phone/tablet behavior independently: wrap/reflow summary rows and controls; keep titles, key status and primary actions easy to reach; use clearly usable local horizontal scrolling only for genuinely dense tables. Preserve keyboard and touch usability and avoid whole-page overflow.
4. Audit actual published layouts and CSS ownership before rollout: shared-theme consumers versus independent renderers/local overrides. Produce a board-by-board adoption matrix with justified exceptions, affected repos/files, and phased work where needed.
5. Put sizing values/rules in the shared presentation layer with documentation. Reuse the existing theme/components rather than adding unrelated design changes or a new styling dependency. Any independent renderer adoption should follow the approved rollout plan.

## Acceptance and validation
- A documented sizing standard explains desktop maximum, gutters, reading measure, breakpoints, dense-table behavior, and the difference between maximum width and mobile overflow.
- The adoption matrix covers the organism board family from its authoritative registry, naming exceptions and follow-up phases instead of silently omitting boards.
- Compare before/after at representative widths: 390px phone, 768/820px tablet, 1024px laptop and 1440px desktop; include light/dark and expanded rows, long titles/URLs and populated tables.
- Verify no whole-page horizontal overflow, accessible keyboard disclosures/copy controls, legible prose, and reachable mobile actions. Record table-local scrolling as an explicit design decision.
- Keep each board's identity, data contracts, freshness/unknown semantics, orchestration actions and publication behavior intact.
- The future session runs start-dev and obtains plan approval before implementation. This intake only files the task; it does not authorize a cross-repo rollout, deployment or merge now.

<!-- formalised by the Intake (Conception) Agent on 2026-10-05 from file:tmp/standard-board-sizing.md -->
