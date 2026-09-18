# MassField sibling sweep: HowToLens and autolens_assistant move straight to the flat `fields=`

Type: docs
Target: workspaces
Repos:
- HowToLens
- autolens_assistant
Themes:
- cluster
Difficulty: medium
Autonomy: safe
Priority: low
Consequence: notify
Witness: an AST re-walk (never a grep — memory `ASTwitness`) over `HowToLens/scripts/` reports zero `al.Galaxy(..., shear=)` and zero `af.Model(al.Galaxy, ..., shear=)` — every chapter's external shear is a bare `al.MassField` in `fields=`, prior paths reading `fields.shear.gamma_1` (28 sites in 22 scripts at the 2026-09-18 survey), mirrored by the 28 sites in 22 notebooks after regeneration with project key `howtolens`; the chapter-2 prior-passing prose is rewritten, not just its code; HowToLens CI green on every script; autolens_assistant wiki/skill pages show the flat `fields=` slot and every edited wiki body is re-provenanced.
Review-minutes: 3
Unattended: ready
Epic: mass-field
Phase: 5
Blocked-by: autolens_workspace#562 and autolens_workspace_test#322 merged (both DRAFT pending the PyAutoGalaxy/PyAutoLens PyPI release)
Filed: 2026-09-17
Amended: 2026-09-18

Fifth phase of `draft/feature/autogalaxy/mass_field_epic.md`. Re-scoped 2026-09-17 on
the human's ruling that the user-facing API is `fields=` everywhere (no shear or other
field on a `Galaxy` in any workspace script), and **amended 2026-09-18 to teach the
flat form directly** — see "Why this was amended".

## The idiom to teach — flat, not a collection

```python
field = af.Model(al.MassField, redshift=0.5, shear=af.Model(al.mp.ExternalShear))

model = af.Collection(
    galaxies=af.Collection(lens=lens, source=source),
    fields=field,
)
```

Prior paths read **`fields.shear.gamma_1`** — *not* `fields.field.shear.gamma_1`. The
collection form (`fields=af.Collection(field=field)`) remains valid library API and is
what several fields at several redshifts still need, but it is **not** what the
tutorials teach. Every code edit, every prose sentence and every printed prior path in
this phase uses the flat form.

## Why this was amended

The prompt was written in the **collection era** (2026-09-17) and its Witness did not
mention the flat form. Epic phase 6 then shipped the flat adoption sweep across
`autolens_workspace` and `autolens_workspace_test` (autolens_workspace#561; PRs #562 +
#322). **Run as originally written, this phase would have landed both repos in the
collection form and needed a third pass.** It now goes straight to flat.

## HowToLens — a galaxy-attached → flat migration

Measured 2026-09-18:

- **28 galaxy-attached sites in 22 scripts**, mirrored by **28 sites in 22 notebooks**.
- **Zero `MassField`, zero `fields=`.** The repo is at the **PRE-phase-3
  galaxy-attached** form, so this is a **galaxy-attached → flat** migration, **not**
  collection → flat. (An earlier survey counted 23 files / 55 `al.mp.ExternalShear`
  mentions; the 28-in-22 figure is the AST walk over model-building sites and is the
  one to work from.)

### Named hazards

- **`chapter_2/tutorial_10_prior_passing.py:190`** passes
  `shear = result_1.model.galaxies.lens.shear`, and its prose at **:185** teaches that
  *"passing the shear is the same as passing the bulge parameters"*. **That lesson
  breaks under `fields=`** — the shear is no longer a galaxy component, so the analogy
  is false once migrated. This needs a **prose rewrite**, not a code edit: the new
  lesson is that a field is passed as its own model object, from `result.model.fields`,
  and that free-vs-fixed still rides on `.model` vs `.instance` exactly as it does for
  a galaxy.
- **`chapter_2/tutorial_9_search_chaining.py:287-288`** is a **deliberate, taught**
  manual prior reset. It must **survive** as `field.shear.gamma_1 = ...` — do not delete
  it, and keep the surrounding prose that explains why a tutorial resets a prior by hand.
- **`chapter_4/tutorial_2_multi_galaxy.py:164-165`** carries prose acknowledging the
  divergence from the workspace idiom. After migration that acknowledgement is
  **redundant** and should go.
- **`tutorial_6_weak_lensing.py` (61 `shear` mentions) and `simulator/weak_lensing.py`
  are weak-lensing PHYSICS prose — EXCLUDED.** They are not migration targets, and a
  count of "shear" in this repo is dominated by them. Do not let a grep-driven sweep
  touch them.

### Repo mechanics

- **CI runs EVERY script** — `no_run.yaml` has **zero entries** — and HowToLens
  deliberately does **not** use `PYAUTO_SMALL_DATASETS`. So a migration error is caught,
  but slowly, and there is no subset to lean on.
- **Notebooks regenerate with project key `howtolens`** (memory `CWD+key`). The
  **chapter-1 markdown mirror** also carries the galaxy-attached form and needs
  `generate_markdown.py` over its curated yaml — `generate.py` rebuilds `notebooks/`
  only (memory `md≠nb`).
- Committed datasets are bit-identical and are **not** regenerated.

## autolens_assistant — 11 files

Six skills/wiki pages carry galaxy-attached **code**; five are prose/catalogue mentions.
**Wiki body edits need re-provenance** (memory `reprov`).

**Claim conflict:** the repo is currently claimed by `codex-hook-parity`. A
parallel-claim waiver plus a fresh worktree is needed, recorded on `active.md` the way
the euclid/sersic rows do it.

## Not in scope

`autolens_workspace_test` was folded into phase 3 on 2026-09-17 (its one legacy
regression script, `galaxy_attached_legacy.py`, is phase 3's deliverable and stays in
the **collection** form as the regression) and is not in scope here.

If the AST walk is empty for a repo, record that in the PR and skip it — but note that
a zero `fields=` count here means *never migrated*, not *clean*.
