Retired WITHOUT a PR: the setup_notebook regeneration drift this prompt filed against
autogalaxy_workspace, autofit_workspace and HowToFit was already swept on 2026-08-07 —
the same day the prompt was filed — and nobody retired the prompt. Re-measured
2026-09-09 from clean-tree `generate.py` runs: all three repos are a **no-op**.

- issue: (none — no issue was ever opened; there was nothing left to do)
- prs: (none)
- completed: 2026-08-07 (the sweeps); verified and retired 2026-09-09

## The measurement that closed it

Clean shallow clones of `main`, PyAutoHands `33c5125`, `generate.py <project>` run from
each repo root in a cloud session on 2026-09-09:

| Repo | Prompt claimed (2026-08-07) | Measured 2026-09-09 | Notebooks on the uncommented form |
|---|---|---|---|
| autogalaxy_workspace | 127 modified / 126 flips / 6 other | **0 modified** | 134 / 134 (0 commented) |
| autofit_workspace | 31 modified / 32 flips | **0 modified** | 32 / 32 (0 commented) |
| HowToFit | 13 modified / 13 flips | **0 modified** | 15 / 15 (0 commented) |

`git status --porcelain` is empty after each run, so the navigator catalogue
(`llms-full.txt`, `workspace_index.json`) regenerates to zero diff too — the
prompt's "second regeneration is a no-op" and "catalogue checks stay green"
criteria are both met by the state already on `main`.

## What actually swept them

Three separate commits, all 2026-08-07, none of them this task:

- **autofit_workspace** `591ee20` "build: repo-wide notebook sweep — activate
  setup_notebook in generated notebooks" (Claude, 03:38 UTC) — 29 files, 30±30 lines.
- **autogalaxy_workspace** `985bff6` "pre build" (Jammy2211, 17:00 UTC) — 136 files,
  200+/152−, i.e. 254 setup_notebook flip lines plus script edits riding along in the
  same commit.
- **HowToFit** `0721771` "pre build" (Jammy2211, 17:02 UTC) — 13 files, 13±13, an exact
  match for the prompt's 13/13 measurement.

So the human's own build sweeps overtook the follow-up prompt within hours of it being
filed. The two `pre build` commits are undescribed, which is why nothing connected them
back to this task.

## Why the counts do not line up exactly, and why that is fine

`591ee20` touches 29 files against the prompt's 31; the remainder was carried by
`autofit_workspace#138` ("Add the missing setup_notebook() line to
overview_3_statistical_methods", merged 2026-08-18 as `fa55c43`), part of the separate
`howto-setup-notebook-audit` sweep that added the *missing* boilerplate to 39 scripts
across six repos. `985bff6`'s 136 files exceed the prompt's 127 because "pre build"
bundled unrelated script edits. The audit that matters is the end state, and the end
state is clean in all three repos by direct measurement, not by reconciling commit
arithmetic.

The prompt's flagged risk — autogalaxy_workspace's "6 non-flip diff lines, audit before
committing" — never needed adjudicating here: whatever they were, they are in `main` and
regeneration reproduces them exactly.

## The lesson

A follow-up prompt that files *measured* drift in sibling repos can be satisfied by a
routine `pre build` commit before anyone picks it up, and the dashboard cannot tell:
it renders faithfully as pickable backlog. This one sat 33 days. Before starting any
regeneration/sweep task, **re-run the measurement first** — it costs one `generate.py`
run per repo and is the whole task's premise. Two of the three bundle members it was
filed alongside were likewise not startable as written (see below).

## Bundle context

Picked as a member of the auto `notebooks` bundle on 2026-09-09 (three members, all
independent). The bundle resolved to one live implementation member:

- `multi_galaxy_package` — **dropped, blocked**: its only remaining leg is the SDSS
  J1011+0143 HST real-data swap-in, and MAST is unreachable from a cloud session.
  Re-probed 2026-09-09: `mast.stsci.edu:443` and `archive.stsci.edu:443` both answer
  `403` to CONNECT through the session proxy — the same failure the prompt recorded on
  2026-07-26. Needs a local/unrestricted-network session.
- `ch4_mask_overlay_never_drawn` — the live member; HowToLens#78.
- this prompt — retired here.

## Environment note (cloud session, worth keeping)

`generate.py` needs `ipynb-py-convert` on PATH and nothing else — it imports only
stdlib plus `build_util`/`generate_autofit`, so notebook regeneration works in a cloud
session with **no PyAuto library installed**. The `notebook-setup-notebook-regen-drift`
record's trap ("ipynb-py-convert cannot pip-install on modern setuptools; vendor it")
no longer applies: `python3 -m pip install ipynb-py-convert` succeeded here in seconds
under Python 3.12. The `howto-setup-notebook-audit` record's claim that PyAutoHands "is
not available in a cloud session" is also stale — it clones anonymously and runs.

## Original prompt

# Regenerate setup_notebook-drifted notebooks in autogalaxy/autofit/HowToFit workspaces

Themes:
- notebooks
- hygiene
Difficulty: small
Autonomy: safe
Consequence: judge
Review-minutes: 20
Unattended: ready
Priority: low
Filed: 2026-08-07 (backfilled from git)

## The problem

The same generator/notebook drift fixed in @autolens_workspace (#480/#481 —
committed notebooks carry the commented `# from auto* import setup_notebook;
setup_notebook()` form while PyAutoHands regeneration uncomments it, so the
notebooks never call it) exists in three sibling repos. Measured 2026-08-07 by
clean-tree `generate.py` dry-runs with PyAutoHands `2a4fb11`:

| Repo | Modified notebooks | setup_notebook flips | Other diff lines |
|---|---|---|---|
| @autogalaxy_workspace | 127 | 126 | **6 — audit before committing** |
| @autofit_workspace | 31 | 32 | 0 |
| @HowToFit | 13 | 13 | 0 |
| @HowToLens | 0 | — | — |
| @HowToGalaxy | 0 | — | — |

## Proposed fix

Mirror of autolens_workspace#481: one dedicated regeneration sweep per repo
(three PRs under this one task, mge-sigma phase-2 precedent), committing the
clean-main `generate.py <project>` notebook diff. In autogalaxy_workspace,
audit the 6 non-flip diff lines first — in autolens_workspace the analogous
extras were harmless JSON-indent normalizations of hand-edited lines, but
verify before committing.

## Verification (per repo)

- Second regeneration on the swept tree is a no-op.
- No diff content beyond the setup_notebook flip + audited/explained extras.
- Each repo's navigator/catalogue checks stay green.

## Provenance

Sibling check registered in the notebook-setup-notebook-regen-drift task
(autolens_workspace#480), run 2026-08-07 while that task's PR was in CI.
