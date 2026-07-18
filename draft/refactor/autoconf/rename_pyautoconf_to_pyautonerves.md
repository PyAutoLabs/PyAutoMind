# Rename the repository PyAutoConf to PyAutoNerves

Type: refactor
Target: PyAutoConf
Repos:
- PyAutoConf
- PyAutoFit
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
- PyAutoBrain
- PyAutoHeart
- PyAutoMind
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Rename the repository @PyAutoConf to **PyAutoNerves** while preserving all
functionality.

## Context

The PyAuto ecosystem is evolving into a coherent software organism.

PyAutoConf currently provides shared configuration across the ecosystem. Within
the organism metaphor this maps naturally to the nervous system. The nervous
system:

- carries signals,
- distributes configuration,
- connects organs,
- coordinates behaviour,
- communicates state.

This is a much better long-term conceptual fit than "Conf".

## Goal

Rename the repository to PyAutoNerves. Preserve all functionality.

## Repository philosophy

PyAutoNerves should own:

- shared configuration,
- defaults,
- environment settings,
- signalling,
- shared constants,
- configuration APIs,
- organism-wide coordination.

It should not become another Brain. It should not perform planning. It should
not execute workflows. It should simply provide the communication and
configuration infrastructure that allows the organism to function coherently.

Think of it as the nervous system connecting the organs.

## Documentation

Rewrite documentation to explain:

> PyAutoNerves provides the signalling and configuration layer that connects
> the PyAuto organism.

Update terminology throughout. Where appropriate replace references such as
"configuration" with "configuration and signalling", without making the wording
forced.

## Migration

Update:

- package references
- documentation
- examples
- README
- GitHub branding
- badges
- workflows
- downstream repositories — @PyAutoFit and @PyAutoArray import `autoconf`
  directly (and @PyAutoGalaxy / @PyAutoLens through them), and the organism
  repos (@PyAutoMind `repos.yaml`, @PyAutoBrain `ORGANISM.md`, @PyAutoHeart)
  name PyAutoConf in their generated organ tables.

Avoid unnecessary breaking changes. Document the migration from PyAutoConf.

## Validation

Check:

- imports
- configuration loading
- CI
- documentation links
- examples
- install instructions

## Deliverable

Create a PR titled **"Rename PyAutoConf to PyAutoNerves"**, including a concise
migration guide.

## Intake notes

- Sized **too-large** by the sizing faculty (score 20): expect start_dev to
  phase this into multiple PRs (e.g. in-repo rename/branding → cross-repo
  reference sweep incl. generated surfaces from `repos.yaml`/`ORGANISM.md` →
  GitHub-side rename + redirects + migration guide).
- PyAutoConf is **already the Nerves organ** in `PyAutoBrain/ORGANISM.md` /
  `PyAutoMind/repos.yaml` (promoted 2026-07) — this task completes that
  promotion by renaming the repository itself. The organ tables in every
  repo's AGENTS.md are generated from those sources via
  `scripts/repos_sync.py --write`; the rename must flow through them, not
  hand-edits.
- The pip package is **`autoconf`** and every library imports it
  (`from autoconf import conf`) and depends on it in `pyproject.toml`.
  "Avoid unnecessary breaking changes" makes the package/import-name question
  (keep `autoconf`, rename with a compatibility shim, or defer) the key scope
  decision to settle at start_dev before any build.
- CI across the workspaces/HowTo repos checks out the libraries by repo name
  (e.g. the smoke chain `PyAutoConf PyAutoFit PyAutoArray …`), and the Heart
  drift-checks repo lists against `repos.yaml`. GitHub auto-redirects renamed
  repo URLs, but clones, badges and workflow references still need the sweep.
- Sibling prompt in the same organism-rename family:
  `draft/refactor/pyautobuild/rename_pyautobuild_to_pyautohands.md`.
- Architectural / API risk keywords present — review scope at start_dev before
  any build.

<!-- formalised by the Intake (Conception) Agent on 2026-07-18 from user-intake;
     work-type corrected docs→refactor and target autoarray→autoconf in review -->
