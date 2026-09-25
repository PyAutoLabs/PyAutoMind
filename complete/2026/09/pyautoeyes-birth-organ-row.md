Phase 0 of the `pyautoeyes-birth` epic: PyAutoEyes registered as an organ —
organ row in `repos.yaml`, boundary prose in `ORGANISM.md` and the docs,
`SIBLING_ORGANS` lists in Brain/Heart/Hands, session-start hook chains, and every
generated `repos_sync` map block and organ table. Issue PyAutoMind#437 (closed).

## PRs (merge order, 2026-09-25)

1. PyAutoLabs/PyAutoMind#438 — `a1d5092e`
2. PyAutoLabs/PyAutoCortex#44 — `3a780e9c`
3. PyAutoLabs/PyAutoNerves#171 — `921a590f`
4. PyAutoLabs/PyAutoGut#8 — `8cc3ff0e`
5. PyAutoLabs/PyAutoBrain#415 — `7684c838`
6. PyAutoLabs/PyAutoHeart#237 — `059059d9`
7. PyAutoLabs/PyAutoHands#288 — `8f38ef4f`
8. PyAutoLabs/pyautolabs.github.io#11 — `3948062d`
9. PyAutoLabs/PyAutoScientist#34 — `c3314a6f`

Every branch proven merged at close-out (`gh pr view` state=MERGED, and the
worktree HEAD is an ancestor of `origin/main` with 0 commits ahead, per repo).

## Gates

- Heart RED for reasons unrelated to these repos; shipped under the human's
  contemporaneous RED override: "can you do 2 and 3 i authorize RED overrule".
- CI green on every other leg. Two legs were red by construction, and broken as follows:
  - PyAutoMind#438 tenant-firewall leg: it reads the *installed* hook copies,
    which on a hook PR are the previous generation. Mind merged first with that
    leg red, which propagated the new generation.
  - PyAutoBrain#415: red while it depended on the unmerged Mind row; re-run
    green after the Mind merge.
- No library release gate: organ PRs only, so nothing is pending release.

## Deviations

- The `.github` org-profile organ row was applied by the human (the public-surface
  guard denies it to the agent).
- Organ order: phase 0 appended Eyes after Gut everywhere. The human ruled on
  2026-09-25 that the canonical order is Brain, Mind, Cortex, Memory, Eyes, Heart,
  Hands, Nerves, Gut. The reorder is filed as a follow-up,
  `active/eyes_organ_order.md` (PyAutoMind#439).

## Original prompt

# PyAutoEyes phase 0 — organ row, boundary prose, local move

Type: feature
Target: PyAutoEyes
Repos:
- PyAutoMind
- PyAutoBrain
- PyAutoHeart
- PyAutoHands
- pyautolabs.github.io
- PyAutoScientist
Themes:
- mind-workflow
- visualization
Difficulty: medium
Autonomy: supervised
Priority: high
Lane: local-dev
Status: draft
Consequence: judge
Witness: `python3 PyAutoMind/scripts/repos_sync.py --check` exits with only the pre-existing hub-blurb leg red and an Eyes organ row present; every organ AGENTS.md map block lists PyAutoEyes; `pyauto-brain eyes survey organs/PyAutoEyes/lens` rc=0
Review-minutes: 15
Epic: pyautoeyes-birth
Phase: 0
Filed: 2026-09-25
Issued: 2026-09-25

Phase 0 of 6 in the `pyautoeyes-birth` epic. **Human-gated** (the GitHub rename
and the org-profile row are human acts). Gates phase 1 (the restructure needs
the organ row and the renamed checkout).

## Request (verbatim)

> As development on this unfolds, I realise that we can promote this from a
> workspace level task (e.g. autolens_visualization) to an organ level
> repository (e.g. PyAutoEyes). It is clear that all libraries need
> visualization, they all share a unified visualization API, I need a single
> point of contact for managing and checking in on their visualization and this
> warrants a dashboard level API like other organs.

> ok lets go forward with PyAutoEyes, there is also the dashboard aspect where
> this provides a single point of contact with the behaviour of the whole
> software ecosystem

## Context

`autolens_visualization` (PyAutoMind#436) was born on 2026-09-25 as a
per-library project repo: a permanent rendered gallery of every PyAutoLens
visualizer figure, a gallery harness, an Eyes-agent HTML gallery/manifest, and
lint/render workflows. The GitHub repo exists and PR #1 is merged; the three
organ registration branches (Mind/Brain/Heart) were verified green but never
pushed — they are discarded by this pivot (#436 closed as pivoted, completion
record `complete/2026/09/autolens-visualization-birth.md`).

**Decision (human, 2026-09-25):** promote it to an **organ, PyAutoEyes** — one
library-neutral home for what the whole ecosystem's figures look like, with
per-library instance subtrees, one harness, an instance registry and a Pages
board that is the single point of contact for visual behaviour.

**Growth-rule justification** (`PyAutoBrain/ORGANISM.md`: an organ "must earn
that by owning state or effects no existing organ can"): Eyes owns the
perception lifecycle — rendered-figure state per library, the manifests, the
render harness (today copy-pasted between `autolens_workspace_test/gallery` and
the new repo), the instance registry and the board. The Brain's Eyes conductor
stays where it is and drives the organ, exactly as Health→Heart and
Build→Hands. Eyes renders and holds figures; it never judges (the conductor
judges with the human) and never edits library plot code (critiques route via
intake).

**Human choices already made:**
- **Rename** the GitHub repo (`autolens_visualization` → `PyAutoEyes`) so
  history and PR #1 carry over — not a fresh create.
- **Plain git PNGs, re-render on library release only** — no LFS, no
  Pages-only storage.

**Human-only actions** (the public-surface guard denies them to the agent):
- `gh repo rename PyAutoLabs/autolens_visualization PyAutoEyes`
- the `.github` org-profile README organ row
- the Heart RED override authorization for shipping (Heart is RED for reasons
  that touch none of these repos; verbatim reason strings go on the issue).

## Shape of the organ (target state, reached by phases 1–4)

```
organs/PyAutoEyes/
  AGENTS.md  CLAUDE.md  README.md  REFERENCE.md      # organ prose + repos_sync markers
  bin/pyauto-eyes                                    # bash dispatcher (Heart pattern)
  eyes/                                              # python package: harness
    registry.py   build.py   run.py   board.py       # generalised gallery_build/run + dashboard
  registry.yaml                                      # instances: lens, galaxy, fit, cti
  lens/      <- today's autolens_visualization content, unchanged layout:
    scripts/<domain>/visualization.py, scripts/misc/{simulators,test}, dataset/, config/,
    instruments/, GALLERY.md
  galaxy/  fit/  cti/                                # later phases, same layout
  dashboard.md  dashboard.html                       # organ board (per instance: figures, stale, gaps)
  .github/workflows/{lint.yml, render.yml, pages_dashboard.yml, dashboard_refresh.yml}
  tests/                                             # hermetic harness + registry + board tests
```

Each instance root keeps the exact layout the Eyes conductor already scans
(`scripts/<domain>/visualization*.py`, `scripts/<domain>/images/...`,
`output/gallery/{gallery.html,viz_manifest.yaml}`), so
`pyauto-brain eyes survey organs/PyAutoEyes/lens` works with **no conductor code
change** in phase 1. The conductor gains registry awareness in phase 2.

## Task (phase 0)

Human first: `gh repo rename`; the org-profile row. Agent, in one task
worktree (`feature/pyautoeyes-birth-organ-row`), PRs in the Cortex order
**Mind → Brain → Heart → Hands → hub/Scientist**:

1. **PyAutoMind**: `repos.yaml` organ row after Gut (`path: organs/PyAutoEyes`,
   `category: organ`, `organ: Eyes`, `role`, `public_role`); `ORGANS` frozenset
   in `scripts/repos_sync.py:138`; `policy/session_start_hook.sh:134-140` dir
   chains; `ROUTING.md`; `epics.md` (`pyautoeyes-birth` already added at the
   pivot — update notes); the three carried drafts (`multi_galaxy_gallery`,
   `group_cluster_gallery`, `eyes_survey_recursive_producers`) already
   retargeted at the pivot; decision record
   `complete/2026/09/pyautoeyes-organ-decision.md` (what state Eyes owns;
   modelled on `complete/2026/07/pyautogut-organ-decision.md`); then
   `repos_sync.py --write` (map blocks, organ tables, hooks). No
   `autolens_visualization` rows (the unpushed ones are dropped).
2. **PyAutoBrain**: `SIBLING_ORGANS` (`agents/_pyauto_root.py:61`),
   `bin/_pyauto_root.sh:86-88`, `ORGANISM.md` table row + boundary prose +
   growth-rule mention, `docs/concepts/organism.md`, new `docs/organs/eyes.md`
   + toctree `docs/index.md:52-63`, `README.md:82` organ count,
   `organs/AGENTS.md` routing row, `tests/test_policy_seams.py:104`
   `WITNESS_EXEMPT` (until phase 1 tests land), `bin/clean_slate.sh`
   dataset-wipe exclusion; Eyes conductor prose
   (`agents/conductors/eyes/AGENTS.md`, `skills/eyes/eyes.md`) default
   instance → `organs/PyAutoEyes/lens`.
3. **PyAutoHeart**: `_SIBLING_ORGANS` (`heart/_workspace.py:72`),
   `heart/_workspace.sh:91-93`, `config/repos.yaml` drift exclusion → organism
   list entry.
4. **PyAutoHands**: `_SIBLING_ORGANS` (`autohands/_workspace.py:42`).
5. **pyautolabs.github.io** `index.html` blurb; **PyAutoScientist** README
   table (generated); **.github** profile (human).

Local: move `lens/autolens_visualization` → `organs/PyAutoEyes` (checkout
with origin set to the renamed repo); content moves into `lens/` in phase 1.
Discard the three stale organ branches + the `autolens-visualization-birth`
worktree after the phase-0 branches exist.

## Witness

`python3 organs/PyAutoMind/scripts/repos_sync.py --check` green on every leg
except the pre-existing hub-blurb leg; every generated `repos_sync:map` block
names PyAutoEyes; Brain/Heart/Hands pytest green;
`pyauto-brain eyes survey organs/PyAutoEyes/lens` rc=0.

## Ship policy

Heart is RED for unrelated reasons; the phase's PRs ship only under a
contemporaneous human RED override recorded in the four sinks. Merge stays
human (`/prm`). Brain merges before any Eyes conductor change relies on the
registry.
