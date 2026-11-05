- summary: already shipped, closed as a stale draft. PyAutoBrain 1aa2ed4 (#563) renamed `docs/organs/build` to `organs/hands` with a redirect and added Broca to the organ table. 7654757 (merged via #564), both dated 2026-11-03, brought the RTD organism pages up to date: new Nerves, DNA and Broca pages, and the hard-coded organ counts are gone.
- witness: `docs/organs/` on Brain main has nerves.md, hands.md, dna.md and broca.md, and no "five/six organs" phrasing remains in docs/. Commit message: Sphinx warnings 0→0. Both commits are on origin/main, checked 2026-11-05.
- found by: stale-draft sweep 2026-11-05. The shipping session merged without closing the draft. Closure approved by the human.

## Original prompt

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
Consequence: notify
Witness: `docs/organs/` has a page for every organ ORGANISM.md names (Nerves included, or its config-layer placement is stated on `concepts/organism.md`), every page quotes the same organ count as ORGANISM.md (a grep for the stale "five"/"six" phrasings returns nothing), the `build.md`->`hands.md` rename decision is recorded, and the docs.yml warning count stays at baseline.
Review-minutes: 0
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
