# session_hook_propagate.yml bot-pushes the end-at-deliverable AGENTS.md block

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: notify
Witness: after one dispatch, `repos_sync.py --check` over a full workspace reports 0 end-at-deliverable block mismatches, Heart manifest_drift shows that surface green, and the Tenant Firewall Gate on PyAutoMind main is green
Review-minutes: 0
Unattended: ready
Lane: any

Source: the human, /health session 2026-11-18, choosing between a ~46-PR reviewed
regeneration wave and letting the propagator carry the block: "Bot-push via
propagator" — i.e. approval for bot pushes of the `repos_sync:deliverable`
AGENTS.md block, as already given for the where-to-file block (PyAutoMind#442).

Background: PyAutoMind#575 changed `policy/end_at_deliverable.md`. The
propagator (`.github/workflows/session_hook_propagate.yml`) bot-pushed the hook,
`settings.json` matcher and `.codex/hooks.json` to ~49 repos, but by design does
not write the deliverable AGENTS.md block ("deliverable blocks stay out of this
job and keep their reviewed regeneration waves"). deliverable-block-wave-575
(PyAutoMind#584) regenerated it by PR in Brain, Heart, Hands and Cortex only; its
follow-up names this option. On 2026-11-18 Heart's manifest_drift still reports
"end-at-deliverable blocks (generated) — 46 mismatch(es)" (every other manifest
repo, PyAutoFit, PyAutoLens, the workspaces, assistants, visualization repos,
pyautolabs.github.io …).

Do: extend the propagator so the job that already writes the where-to-file
block (`repos_sync.write_filing_blocks`) also writes the `repos_sync:deliverable`
block (the same narrow write-only-this-block pattern: insert/fill the markers,
touch nothing else), triggered on pushes that change `policy/end_at_deliverable.md`
or the generator. Update the workflow's header comment (it currently says the
deliverable block stays on reviewed waves) and any doctrine that states it.
Then dispatch it once to clear the current 46 stale blocks.

Also consider the race noted in complete/2026/11/deliverable-block-wave-575.md:
the Tenant Firewall Gate and the propagator start on the same push, so every
canonical hook/block change leaves one red gate run on main. Run the gate after
the propagator (`workflow_run`) or have the propagator dispatch it.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/2076909a-d18c-4718-a05e-9afa6642996d/scratchpad/intake/propagate.md -->
