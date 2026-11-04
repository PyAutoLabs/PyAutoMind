- epic: autonomous-orchestrators (pilot 4c follow-up; issue PyAutoBrain#579)
- summary: PyAutoBrain#580. Digest picks are named `[title](Mind blob link) (`slug`; size · repos)` via `_orchestrator.pick_record` (shared by dispatch and shadow) and `_digest.label`. `why:` = brief admission rule + `_brief.rank_note` (queue.md #k, or "not in queue.md · ~N review-min · priority P", plus epic phase). A shadow digest's counters print as one line (`_digest.SHADOW_COUNTERS`). A shadow pilot row leaves `merges` as `?` (the human's own merges in the window = the epic's baseline). Mind docs (pilot.md header, batches/AGENTS.md) updated in this close-out commit.
- trigger: shadow shift 1 check-in (human, 2026-11-04): the digest had "no content" (6 bare slugs, `why: scoped tier notify`), and "how am i meant to know how long the review takes if the shadow cant do anything". Shift 1's row was corrected to 5 human review-min / 11 merges / 6 overrules.
- finding surfaced by the new why: every notify prompt grades ~0 review-min, so cheapest-first ranks all notify work above glance, and ties fall to the path, so shift 1's picks were alphabetical. queue.md (empty of prompts) is the human's lever.
- witness: PASS. Shift-2 brief rendered on the real backlog (2 titled, linked named tasks; one-line counters); shift 1 re-rendered with rank notes; Brain 1564 passed; tenant firewall OK; the old shift-1 record still validates.
- heart: GREEN (release); glance tier, in-turn merge.

## Original prompt

# Shift digest: readable picks, and a shadow row that measures the human's baseline

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-11-04
Issued: 2026-11-04
Epic: autonomous-orchestrators
Consequence: glance
Witness: a shadow digest built from a fixture shows each pick as its prompt title, size, target repos and a linked prompt path, with a `why:` that names the planner's ranking (queue.md position, or "not in queue.md" with review-minutes and priority, plus epic and phase); a shadow digest's all-zero counters collapse to one line; a shadow pilot row lands `merges` as `?` for the human; `batch watch` shows the titles; the full Brain suite passes
Review-minutes: 10
Unattended: never
Lane: local-dev

Parent: draft/feature/pyautobrain/autonomous_orchestrators_epic.md. A follow-up from pilot 4c (PyAutoBrain#574) shadow shift 1 (2026-11-04). Human check-in: "theres no even any content there?" and "how am i meant to know how long the review takes if the shadow cant do anything".

1. **Picks are unreadable.** The digest listed 6 bare slugs (`batch_slice — proposed (shadow) — notify — why: scoped tier notify`). Record the prompt's title, difficulty, repos, epic and phase in each pick (both `_propose` and dispatch, through one helper; `survey` adds `title`). The digest and `batch watch` render a title-first line with the details and a link to the prompt on GitHub.
2. **`why:` says nothing.** `scoped tier notify` is the admission rule, not the ranking. The planner orders by queue.md rank, then review-minutes, then priority, then path; shift 1's 6 picks were alphabetical among ties. Append the ranking to `pick_reason`'s line.
3. **Shadow counters are noise.** In a shadow digest, the all-zero counters collapse to one line.
4. **The shadow row measured the wrong thing.** The epic's baseline is "the human works as today, minutes are logged": the human's own review minutes and merges in the window. In a shadow pilot row, `merges` lands as `?` (a human/check-in cell, counted after the shift), and the docs say review-minutes means the human's own review time. Shift 1's row was corrected by hand on 2026-11-04 (5 minutes, 11 merges).

<!-- filed by hand 2026-11-04 at the human's request ("do the fixes"); headers mirror intake's -->
