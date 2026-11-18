# A shift worker's update of its own claim is not a Mind-writer conflict

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-11-18
Issued: 2026-11-18
Epic: autonomous-orchestrators
Consequence: judge
Witness: `python -m pytest tests/test_orchestrator_mind_writer.py -q` passes with new tests that fail on today's main: (a) a claim committed earlier this shift, then the same task's drop-section + append of that `## slug` in one run, commits and replaces the section; (b) the same pair on a section another slot or a human wrote is set aside as a conflict; (c) a lone drop-section still applies last and is withheld when a sibling is set aside; (d) a re-dispatch's repeated claim is still skipped
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-18, in the cockpit for shift 2026-11-18-pm2, after a NEEDS YOU event: "Why does it need me" → told it was a writer bug → "Yes and then implement the fix for 2" → plan approved: "Approved".

## Why

At 20:27Z the shift worker for `stellar_m_l_gradient_profiles_sersicgradient_piv` opened PyAutoGalaxy#726 and updated its own `active.md` claim the standard way: `drop-section active.md <slug>` then `append` the new section (status `library-shipped, awaiting-merge`, `library-pr:`, `workspace-pr:`, the extra autolens_workspace_test repo). The Mind writer (`agents/conductors/batch/_mind_writer.py`) treats every `drop-section` as a closing op (`_closing`), applied after the task's other ops, so the append ran first against the still-present section; `_new_sections` counts a duplicate section as the shift's own only for a re-dispatched task (`own_tasks`), so it raised "already in active.md, not this shift's own claim — conflict", set the append aside and withheld the drop with it. The watcher posted NEEDS YOU; the claim was repaired by hand (Mind d5fb06628). Every worker that updates its claim at PR-open hits this.

## Fix (approved plan)

- In `commit_ledger`, pair a task's `drop-section(path, slug)` with an `append` on the same path whose text holds `## slug`: the pair is an update, not a close — the drop leaves the closing set and applies immediately before its append, as one unit.
- Ownership guard for the pair: main's section must be one this shift committed earlier (`ctx["prior"]`) or its `- session:` must name `shift worker <this slot> (…)`; otherwise ConflictError as today.
- A lone drop-section stays closing; re-dispatch repeats stay skipped.
- Note in `agents/conductors/batch/AGENTS.md` (the Mind writer paragraph).
- Do not pull the merged fix into the watcher's checkout until shift 2026-11-18-pm2's late window closes (22:15Z).
