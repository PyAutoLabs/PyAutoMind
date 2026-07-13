# Bring the public front-door organ tables under repos_sync

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Problem

`PyAutoMind/scripts/repos_sync.py` is the body-map generator: from `repos.yaml`
(organ identity) plus `PyAutoBrain/ORGANISM.md` it regenerates the organ tables
inside the workspace-root `AGENTS.md` and each per-organ `AGENTS.md`, and
`--check` catches drift. But the **public-facing** organ listings are
hand-maintained copies that are *not* under this sync, and they drift silently —
on 2026-07-13 the **Gut** organ had fallen out of all three:

1. `.github` org profile README — the organ table (`PyAutoLabs/.github`, `profile/README.md`).
2. PyAutoScientist repo README — the organ table (`PyAutoLabs/PyAutoScientist`, `README.md`).
3. `pyautolabs.github.io` — the `index.html` organism blurb that enumerates organs in prose ("an organism of … repositories — Mind, Brain, …").

These were fixed by hand this session, but nothing prevents the next new organ
from being dropped again.

## Goal

Adding a new organ to `repos.yaml` must **propagate to** (generate) or be
**drift-checked against** (`--check`) these three public docs, so no organ can
silently vanish from the front door.

## Scope / considerations

- These three docs live in **separate repos** from PyAutoMind, so the generator
  cannot assume they sit in the working tree. Options to weigh in the plan:
  - a **cross-repo** generate/check that operates on sibling checkouts when
    present and is a no-op (with a warning) when absent, and/or
  - a **drift report** the `/morning` and/or `/health` pass surfaces (gh-API
    read of the three files on `main`, compared against the canonical organ set)
    rather than an in-tree rewrite.
- Prefer the **marker-block** idiom already used by `repos_sync.py` for the
  `AGENTS.md` tables (generated region between sentinel comments) for the two
  README tables; the `index.html` prose blurb needs a marker span or a
  loosened check (assert every organ name appears) rather than a full rewrite.
- The two README tables and the prose blurb have **different formats** from the
  `AGENTS.md` tables (link style, column set, the Nerves/Gut ordering) — the
  generator must render each target's own format, not force one house style.
- Keep `repos.yaml` the single source of truth; ORGANISM.md remains the
  boundary/role prose source. Do not introduce a second organ registry.

## Acceptance

- A new organ added to `repos.yaml` either regenerates or fails `--check`
  against all three public docs.
- `repos_sync.py --check` (and/or the morning/health drift surface) would have
  flagged the missing **Gut** row/name in each of the three docs.
