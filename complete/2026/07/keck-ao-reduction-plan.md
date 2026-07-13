## keck-ao-reduction-plan
- completed: 2026-07-09
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/9 (closed)
- summary: Keck-AO research task — SHARP literature pass + tooling survey + draft design; delivered as docs/design/keck_ao.md via keck-ao-reduction's PR #12

- completed: 2026-07-09
- pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/59 (merged, squash 4af8a756)
- notes: |
    Design-only deliverable (prompt was "design, not yet implement"): merged
    agents/conductors/clone/DESIGN.md + AGENTS.md pointer — no clone.sh/_clone.py/
    CLI wiring. Clone Agent (pyauto-brain clone) / Mitosis Agent: CloneDecision
    (dry-run first), mandatory clone-mode question (exact-clone | differentiated-
    sibling | lightweight-seed), organ boundary (Brain plans / Build executes /
    Heart validates / Memory cites-not-copies), reference-owned template seam
    (autolens_assistant modes/maintainer.md Assistant-as-template), analyze/apply/
    audit modes, phased v0→v2. Prerequisite met: reference-assistant audit landed.
    Shipping cleared the PyAutoBrain claim → unblocks profiling_agent (its design
    phase was already settled: conductor verdict, first increment scoped).
    Follow-ups (phased, filed as predecessors near shipping, never bulk-issued):
    v0 analyze-only, v1 seed births, v2 differentiated siblings.

## Original prompt

# Plan the Keck adaptive-optics (NIRC2 AO) data-reduction workflow

Type: research
Target: PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Original request: "For PyAutoReduce can you plan out how we reduce keck-AO
data, read SHARP papers for scientific context."

Plan the Keck adaptive-optics (NIRC2 AO) imaging data-reduction workflow for
PyAutoReduce — how raw Keck AO data becomes modeling-ready datasets for
PyAutoLens/PyAutoGalaxy, alongside the existing HST (ACS/WFC3) and JWST
(NIRCam) phases. Read the SHARP (Strong-lensing High Angular Resolution
Programme) papers for scientific context on AO strong-lens imaging — PSF
handling (AO PSFs are time-variable and poorly known, unlike HST/JWST),
sky subtraction, distortion correction, and coaddition. Deliverable is a
design/plan document, not code.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from user-intake -->
