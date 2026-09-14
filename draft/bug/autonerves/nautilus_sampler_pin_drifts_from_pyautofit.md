# Colab pins `nautilus-sampler==1.0.4` while PyAutoFit declares `1.0.5`

Type: bug
Target: PyAutoNerves
Repos:
- PyAutoNerves
Difficulty: trivial
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: notify
Witness: `autonerves/setup_colab.py`'s `nautilus-sampler` specifier matches the one PyAutoFit's `pyproject.toml` declares, checked by a test that reads both rather than hard-coding either version, so the two cannot drift apart again silently.
Review-minutes: 10
Unattended: ready

`autonerves/setup_colab.py` pins `nautilus-sampler==1.0.4` in `_SHARED_EXTRAS`:

    "nautilus-sampler==1.0.4",

while PyAutoFit's `pyproject.toml` (line 85) declares:

    "nautilus-sampler==1.0.5",

Every other sampler specifier in that list matches autofit exactly — the comment
above `_SHARED_EXTRAS` says outright that "their specifiers track that file" — so
this one looks like drift rather than intent.

Why it matters: the Colab bootstrap installs with `pip install *packages --no-deps`,
so pip performs no resolution and the pinned 1.0.4 is simply what lands. Every
Colab user of all six `_PROJECTS` entries therefore runs `af.Nautilus` on 1.0.4
against an autofit that expects 1.0.5. Nothing errors at import, which is exactly
why it went unnoticed.

Found during PyAutoNerves#165 / #166 (the regression test asserting all three
samplers are installed). That test deliberately matches on requirement NAME with
the specifier split off, so it passes either way and does not catch this.

Fix direction: decide which version is correct and align the two. Prefer a check
that derives the expected specifier from PyAutoFit's `pyproject.toml` rather than
restating a literal in a second place — restating it is what allowed the drift.
Consider whether the other `_SHARED_EXTRAS` pins deserve the same treatment.

Type: bug
Target: PyAutoNerves
Difficulty: trivial
Priority: normal

<!-- found during PyAutoNerves#166 close-out, 2026-09-14 -->
