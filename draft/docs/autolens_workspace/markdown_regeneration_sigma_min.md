# Regenerate autolens_workspace markdown/ so the MGE pages show sigma_min

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- mge
- notebooks
- docs-hub
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-08 (backfilled from git)

Seven curated `markdown/` pages still show MGE snippets **without**
`sigma_min`, because `markdown/` was deliberately not regenerated when the
sigma_min sweep shipped. Users reading those pages get the pre-sweep idiom.

## Provenance

This is "DEBT 2 of 2" from `mge-sigma-min-workspace-sweep`
(`complete/2026/08/mge-sigma-min-workspace-sweep.md`, autolens_workspace#466,
phase 1 PR #467 merged `92019316`). It was **deferred by an explicit human
decision on 2026-08-04**, not overlooked. Split out here so it survives its
parent task's completion record instead of being buried in it.

DEBT 1 (the autogalaxy_assistant baseline re-pin) was cleared on 2026-08-04 via
autogalaxy_assistant#11.

## What is stale

7 of the 30 curated `markdown_examples.yaml` entries are among the scripts the
sweep changed:

```
start_here.py
imaging/start_here.py
imaging/modeling.py
multi_dataset/start_here.py
multi_dataset/modeling.py
group/start_here.py
group/modeling.py
```

`scripts/` and `notebooks/` **were** regenerated (93-for-93, no unrelated
churn). Only `markdown/` lags.

## Why it was deferred — and why this is not a quick job

`generate_markdown.py` **refuses to run under `PYAUTO_TEST_MODE`**: it executes
each script for real in order to render the figures. A fresh worktree has no
`output/` resume cache, so a regeneration pass means **real fits**, not a smoke
run. That is the whole reason it was deferred, and it is still true — budget
accordingly, and prefer a checkout that already has a warm `output/`.

## Trap carried from the parent task

The three scripts declaring `ENV: full_datasets` (`group/start_here.py`,
`imaging/start_here.py`, `multi_dataset/start_here.py` — note all three are in
the stale set above) **fail with an unrelated `IndexError`** if run with
`PYAUTO_SMALL_DATASETS=1`: the dataset is capped to 16px against a 209px mask.
This reproduces on pristine `main`, so it is a runner-environment artefact, not
a code bug. **Honour the in-file `ENV` declaration** when running these.

## Acceptance

- The 7 pages show the current `sigma_min=dataset.pixel_scales[0] / 10.0` idiom.
- No unrelated churn in the other 23 curated pages — regeneration is
  notoriously noisy, so diff before committing.
- Image-plane vs source-plane distinction is preserved in the rendered
  snippets: source-plane MGEs keep the `-4` default and must **not** acquire a
  pixel-scale floor.
