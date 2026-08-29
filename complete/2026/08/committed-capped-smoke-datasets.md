- issue: none — retired as obsolete without an issue or PR
- completed: 2026-08-29
- repos: autolens_workspace (no change)
- summary: Prompt (filed 2026-07-22) described four capped 15x15 smoke datasets (`dataset/imaging/{double_einstein_ring,mass_stellar_dark,extra_and_scaling_galaxies}`, `dataset/group/scaling_relation` + group variants) committed as if real. Verified 2026-08-29 against `autolens_workspace` main (`8ed2af05`, `fb5d8e2d` release tag): `git ls-files` tracks nothing under any of those folders, `dataset/.gitignore` is a bare `*` / `!.gitignore`, the folders are empty on disk, and `git log --all --name-status` over those paths returns nothing on any branch or stash — the only relevant history is `b5db285e` "chore: untrack gitignored dataset/ files" (2026-04-18), which predates the prompt. The related loader mislabel was fixed separately by PyAutoArray#431 (`complete/2026/08/small-datasets-loader-pixel-scales.md`). Nothing to regenerate or remove; retired from the ci-smoke — bundle 2 membership as already resolved.

## Original prompt

# Capped smoke datasets were committed as if they were real

Type: maintenance
Target: autolens_workspace
Repos:
- autolens_workspace
Themes:
- ci-smoke
- hygiene
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-07-22 (backfilled from git)

Capped smoke datasets were committed as if they were real data.

Four dataset folders in autolens_workspace have 15x15 data.fits and noise_map.fits committed at 0.6 arcsec/px, when their simulators declare 130x130 (or 250x250) at 0.1 arcsec/px: dataset/imaging/double_einstein_ring, dataset/imaging/mass_stellar_dark, dataset/imaging/extra_and_scaling_galaxies, dataset/group/scaling_relation (and the group/ variants of the same names).

15x15 was the OLD PYAUTO_SMALL_DATASETS cap size, before commit 656be94b changed it to 16x16. So these are smoke-mode artifacts that were force-added past dataset/.gitignore (which ignores everything bar 20 real-data dirs) and committed as if they were genuine datasets.

Two consequences:
- They sit permanently modified in git status, because any capped run now overwrites them at 16x16. This is the mystery dirty dataset/ tree that shows up in every workspace session and risks being swept into an unrelated commit.
- They are a trap for anyone reasoning about pixel scale: the committed file's true scale (0.6) disagrees with its own simulator's declared scale (0.1).

Proof of the 0.6 scale: the committed 15x15 extra_and_scaling_galaxies image has clumps at (+3.60,+2.40) and (-1.80,-3.60) arcsec under 0.6, matching its simulator's declared galaxy centres (3.5,2.5) and (-2.0,-3.5). Under 0.1 they would be at (0.60,0.40) and (-0.30,-0.60), nowhere near.

Decide per folder whether the dataset should be regenerated at full resolution and re-committed, or removed from git and left to the auto-simulation path like every other generated dataset. Check whether anything depends on the committed copy first.

Related: draft/bug/autoarray/small_datasets_loader_pixel_scales.md, which fixes the loader that mislabels these.

<!-- formalised by the Intake (Conception) Agent on 2026-07-22 from user-intake -->
