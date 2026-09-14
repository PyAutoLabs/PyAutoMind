# HowToGalaxy and HowToLens have no `__Paths__` orientation block

Type: docs
Target: workspaces
Repos:
- HowToGalaxy
- HowToLens
Themes:
- howto
- tutorials
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Witness: Tutorial 1 of HowToGalaxy and of HowToLens each opens with a `__Paths__` section that names the repo as the working directory, lists what lives in its `config/`, `dataset/` and `output/` folders, and links the repo's own clone URL — matching the shape HowToFit's tutorial 1 already has.
Review-minutes: 20
Unattended: ready
Filed: 2026-09-14

HowToFit's `scripts/chapter_1_introduction/tutorial_1_models.py` opens with a
`__Paths__` section that orients the reader: this is your working directory,
config loads from here, data loads from here, results are written here, and
here is where to clone it if you do not have it.

**HowToGalaxy and HowToLens have no equivalent section at all.**

This is not cosmetic. It is *why* those two repos accumulated scattered stale
paths after the HowTo split while HowToFit had exactly one: with no single
place that states where the reader's files live, the same information gets
restated ad hoc across many tutorials, and each restatement drifts
independently. The `howto-stale-self-location` task (issue HowToGalaxy#75)
fixed 29 such scattered references across the two repos; a `__Paths__` block is
the structural fix that stops them recurring.

## Scope

Add a `__Paths__` section to tutorial 1 of @HowToGalaxy and @HowToLens, modelled
on HowToFit's, naming each repo's own clone URL. Then check whether any of the
per-tutorial path restatements the `howto-stale-self-location` task corrected can
now simply defer to it rather than repeating it.

## Ordering

Depends on `howto-stale-self-location` (issue HowToGalaxy#75) landing first —
this builds on the corrected paths rather than racing them.

## Provenance

Split out of `active/howto_stale_workspace_self_location.md` at plan time,
2026-09-14: the correction shipped there, this is new authorship and was held
back deliberately rather than smuggled into a fix PR.
