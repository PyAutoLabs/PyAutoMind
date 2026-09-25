# PyAutoEyes organ decision

Type: research
Target: PyAutoEyes
Repos:
- PyAutoEyes
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: high
Status: decided

PyAutoEyes organ decision. Settle whether the per-library gallery repo
`autolens_visualization` (PyAutoMind#436) stays a lensing project repo or is
promoted to a **peer organ** owning what the whole ecosystem's figures look
like. Deliverable: a written decision with the organ identity, the state it
owns, and the boundary rules against the Brain's Eyes conductor, the Heart,
the libraries and the Mind. Implemented by the `pyautoeyes-birth` epic
(phase 0: PyAutoMind#437).

## The demonstrated need

`autolens_visualization` was born on 2026-09-25 as a permanent rendered
gallery of every PyAutoLens visualizer figure on HST-scale imaging and
interferometer data, with a gallery harness, an Eyes-agent manifest and
lint/render workflows. While it was being built the human observed (verbatim
on #437):

> It is clear that all libraries need visualization, they all share a unified
> visualization API, I need a single point of contact for managing and
> checking in on their visualization and this warrants a dashboard level API
> like other organs.

Three facts make that more than a preference:

1. **Every library draws.** PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens
   and PyAutoCTI all ship plotters on the shared `autoarray.plot` API, and the
   visual behaviour of one library is the visual behaviour of the ones built on
   it. A per-library repo would be cloned four times.
2. **The harness already exists twice.** The gallery build/run scripts are
   copy-pasted between `autolens_workspace_test/gallery/` and the new repo; a
   third copy per library is the defect this organ removes.
3. **There is no single point of contact.** No organ answers "what does the
   software show right now, on realistic data, and what changed since the last
   release?" — the Heart answers whether it is healthy, not what it looks like.

## Decision (human, 2026-09-25)

**Promote the repo to a peer organ, `PyAutoEyes`**, by renaming
`PyAutoLabs/autolens_visualization` on GitHub (history and PR #1 carry over,
not a fresh create). The lens gallery becomes the organ's first **instance**
(`organs/PyAutoEyes/lens`); galaxy, fit and cti instances follow in later
phases, each with the same layout the Eyes conductor already scans.

Storage: **plain git PNGs, re-rendered on library release only** — no LFS, no
Pages-only storage. The figures are the record; a release is the moment the
record changes.

## Why an organ — the growth rule

`PyAutoBrain/ORGANISM.md`: a new organ "must earn that by owning state or
effects no existing organ can". Eyes owns the **perception lifecycle**, which
no organ held before:

- **Rendered-figure state per library** — the PNGs themselves, on fixed
  realistic datasets, tracked in git so a figure's history is a `git log`.
- **The manifests** (`viz_manifest.yaml`, `GALLERY.md`) — the inventory of
  what each library draws.
- **The render harness** — one `eyes/` package in place of the per-repo
  copies.
- **The instance registry** (`registry.yaml`) — which libraries have a
  gallery, where, with which domains.
- **The board** — the single point of contact for the visual behaviour of the
  whole ecosystem.

Same test that earned the Gut its repo (a persistent, reusable-artifact
lifecycle) and denied hygiene one (a worklist only).

## Boundaries

- **vs the Brain's Eyes conductor** — mirror **Heart ↔ vitals** and
  **Gut ↔ hygiene**: the organ renders and holds the figures; the conductor
  surveys, reviews and judges them with the human. The Eyes organ never
  judges a figure.
- **vs the libraries** — the Eyes never edits library plot code. An accepted
  critique routes through intake → start_dev like any other change.
- **vs the Heart** — the perception mirror of the Heart: the Heart says
  whether the software is *healthy*; the Eyes show what it *shows*. The Eyes
  issue no readiness verdict.
- **vs profiling / inference** — `autolens_profiling` and `autolens_inference`
  stay per-library project repos (pinned timings are library-specific); the
  Eyes may share their datasets but never re-simulate them.
- **vs the Mind** — critiques become Mind prompts; the Eyes hold figures, not
  intent.

## Lifecycle note

Decision taken in the 2026-09-25 session that shipped `autolens_visualization`
PR #1 (record `complete/2026/09/autolens-visualization-birth.md`, closed as
pivoted). Phases 0–5 of the `pyautoeyes-birth` epic implement it; this record
is written by phase 0 (PyAutoMind#437).
