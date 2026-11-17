# Clear the Tenant Firewall Gate RED: regenerate the end-at-deliverable AGENTS.md block after PyAutoMind#575

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoBrain
- PyAutoHeart
- PyAutoHands
- PyAutoCortex
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-17
Issued: 2026-11-17
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/584
Epic: autonomous-orchestrators
Consequence: glance
Witness: `python3 PyAutoMind/scripts/repos_sync.py --check --root <root holding PyAutoMind, PyAutoBrain, PyAutoHeart, PyAutoHands and PyAutoCortex at their branch heads>` reports no mismatch (it reports "end-at-deliverable blocks (generated): 3 mismatch(es)" for Brain, Heart and Hands, and Cortex is stale too, on 2026-11-17 mains); after the PRs merge, a re-run of the Tenant Firewall Gate on PyAutoMind main is green
Review-minutes: 5
Unattended: ready
Lane: any

Source: the human, 2026-11-17 (chat, M3.6 sitting), verbatim:

> 0. Clear Heart RED. The PyAutoMind "Tenant Firewall Gate" fails on main (run 43881901227, from PyAutoMind#575): the generated end-at-deliverable hook (.claude/hooks/end-at-deliverable.sh and its .claude/settings.json matcher) is out of date in PyAutoBrain, PyAutoHeart and PyAutoHands, and PyAutoBrain/.codex/hooks.json differs from repos.yaml. First check whether PyAutoMind/.github/workflows/session_hook_propagate.yml regenerates these, and whether dispatching it is the whole fix. Otherwise regenerate the files with the Mind generator and open the PRs. No prompt exists yet: file one under draft/maintenance/ with this paragraph verbatim.

## Findings (2026-11-17)

1. **The hook half is already fixed.** Run 43881901227 ran 14:04:00–14:04:23 on the #575
   merge. The propagator (`session_hook_propagate.yml`, run 43881901164, green) ran on the
   same push and bot-pushed the regenerated `.claude/hooks/end-at-deliverable.sh`,
   `.claude/settings.json` and `.codex/hooks.json` to PyAutoBrain (14:05:11), PyAutoHeart
   (14:05:35), PyAutoHands (14:05:37) and about 45 other repos. The gate has not run on Mind
   main since (it is path-filtered on push; it has `workflow_dispatch`). Re-checked on
   2026-11-17 mains: hooks, matchers and `.codex/hooks.json` all OK.
2. **The real remaining failure is the AGENTS.md block.** The same run also reported
   `end-at-deliverable blocks (generated): 3 mismatch(es)` for Brain, Heart and Hands. #575
   changed `policy/end_at_deliverable.md` (adds "or `Monitor` or background loop on GitHub"
   and the shift-cockpit exception). The propagator deliberately does not write this block:
   its header keeps the deliverable block on "reviewed regeneration waves". So dispatching
   the propagator is not the fix.
3. **Every other repo's block is stale too** (PyAutoCortex confirmed); the gate checks out
   only Mind, Brain, Heart and Hands, so only those three show RED.

## Do

One branch and PR per repo (PyAutoBrain, PyAutoHeart, PyAutoHands, PyAutoCortex): run
`repos_sync.py --write` from a root holding Mind main and the repo, keep only the
`repos_sync:deliverable` block hunk in `AGENTS.md`. After the PRs merge, re-run the Tenant
Firewall Gate on PyAutoMind main (dispatch `firewall_gate.yml` on `main`, or re-run run
43881901227: a re-run checks out the organs' current mains), so Heart reads it green.

## Follow-ups (not in this task)

- The other ~45 repos carrying the block. Either a reviewed `--write` wave, or extend the
  propagator to carry the deliverable block as it already carries the where-to-file block
  (bot push; needs the human's approval, as the filing block did).
- The gate and the propagator start on the same push, so a canonical hook change always
  leaves one red gate run on main until someone re-runs it. Run the gate after the
  propagator (`workflow_run`), or have the propagator dispatch it.
