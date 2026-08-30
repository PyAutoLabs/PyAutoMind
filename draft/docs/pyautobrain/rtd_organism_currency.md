# RTD organism docs currency: Nerves page, organ-count drift, hands.md rename

Type: docs
Target: pyautobrain
Repos:
- PyAutoBrain
Themes:
- docs-hub
- mind-workflow
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-19 (backfilled from git)

Found by the 2026-08-19 readability census (#237). The RTD narrative
(@PyAutoBrain/docs/, published at pyautoscientist.readthedocs.io) has drifted
from the canonical organism:

- `docs/organs/` has six pages (mind, brain, heart, build, memory, gut) and
  **no `nerves.md`** — ORGANISM.md calls Nerves "the seventh organ".
- Organ counts disagree: `docs/satellites.md` says "The five organism repos",
  `docs/index.md` says "six git repositories — Mind, Brain, Heart, Hands,
  Memory, Gut", `docs/concepts/organism.md` says "The six organs", while
  ORGANISM.md and the body map have seven. Decide the canonical framing (is
  Nerves presented as a full organ page or as the config layer inside the
  adoption story?) and make every page agree.
- `docs/organs/build.md` documents the organ named **Hands** — consider
  renaming to `hands.md` (+ toctree). This changes a published RTD URL, so it
  is a human call (Sphinx has no redirects by default).

Judgment-tier prose (tutorial register) — keep in Opus per the model split.
Gate: docs.yml warning-count baseline must stay green.
