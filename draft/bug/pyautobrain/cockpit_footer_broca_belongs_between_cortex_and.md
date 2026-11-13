# Cockpit footer: Broca belongs between Cortex and Memory

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoBroca
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: in PyAutoBrain config/policy.yaml `board: boards:`, `broca` is listed immediately after `cortex` and immediately before `memory`; every published cockpit board footer shows Cortex → Broca → Memory.
Review-minutes: 0
Unattended: ready

On most cockpit dashboards the organ footer strip shows Broca at the far right next to Gut. It should sit between Cortex and Memory.

Root cause candidate: PyAutoBrain `config/policy.yaml` `board: boards:` block — the canonical footer order read by `board/_theme.py` `board_links()` ("file order IS the order") — lists `broca: PyAutoBroca` after `nerves`, just before `gut`. Fix: move it to between `cortex` and `memory`.

Then do a general scan of every cockpit dashboard/renderer (Scientist/organism, Brain, Mind dashboard via `_intake._board_links`, Cortex, Memory, Eyes, Ears, Heart, Hands, Pulse, Insight, DNA, Nerves, Broca, Gut) to confirm each reads the single policy.yaml order and none keeps a drifted private copy (hard-coded footer tuples, hero/organ lists, Broca's own board.py, Scientist activity_feed/navigation). Fix any that do, and regenerate/redeploy the affected boards so the footers update.

<!-- formalised by the Intake (Conception) Agent on 2026-11-13 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/fc63d406-07d4-46f9-90c1-0e77b3d98de4/scratchpad/broca.md -->
