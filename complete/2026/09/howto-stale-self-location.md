Stale self-location paths left behind when the HowTo lecture series was split
out of the `*_workspace` repos. Tutorials still told the reader that their own
working directory, config, dataset and output folders lived inside
`autogalaxy_workspace` / `autolens_workspace`.

**Merged 2026-09-14:** HowToGalaxy#76 (3 commits), HowToLens#82 (4 commits).
Issue HowToGalaxy#75.

## What shipped

55 prose lines across the two repos. The governing distinction, applied to every
hit: *is this sentence telling the reader where THEIR files are (fix), or
pointing them at the sibling workspace's examples (keep)?* ~45 cross-references
in HowToGalaxy and 60 in HowToLens are correct post-split and were left
untouched.

- HowToGalaxy: 24 lines / 13 scripts, plus the tuning-fork image and the
  `.url_check_allowlist.txt` entry grandfathering it.
- HowToLens: 31 lines / 18 scripts.
- Both: the clone URL neither repo had (see "Absorbed follow-ups").

## What the filed scope missed

The survey undercounted; verifying each path against the code rather than
string-swapping is what found the rest.

- **Four paths wrong beyond the repo name** (HowToLens): `output/t7_with_positions`,
  a folder name left from when that tutorial was numbered 7 *and* missing its
  chapter prefix; four `tutorial_searches.py` prints with no path at all past
  `workspace/output`; a simulator naming `simple__no_lens_light` when it writes
  `simple__no_lens_light__mass_sis`; and a search path naming the wrong run. A
  prefix-strip would have preserved all four.
- **A second spelling of the same defect**: 13 + 17 print strings saying
  `checkout the workspace/output/...`, naming a directory that exists in neither
  repo. Found only because the first agent flagged it rather than assuming scope.
- **The image was never a 404.** The script already pointed at HowToGalaxy, but
  as a `blob` URL — `200 text/html`, does not render. Now `?raw=true`. The
  allowlist entry was deleted: that URL appeared in no source file, so it held a
  green check over nothing.
- **A correctly-declined false positive**: `tutorial_4_group_scale.py:608` looks
  truncated but its path continues on the adjacent string literal; a line-scoped
  regex would have corrupted it.

## Root cause

`markdown/` is built by `generate_markdown.py` over a curated subset, really
executing each script — a **different tool** from the `generate.py` that builds
`notebooks/`. Anyone following the documented regeneration step rebuilds
`notebooks/` and silently misses `markdown/`. That is how the sibling HowToFit
fix for this same bug shipped with a stale markdown mirror, and how HowToGalaxy
came to publish a page documenting a mask section its script no longer had
(~400 of ~413 changed `.md` lines in #76 were that catch-up, isolated in its own
commit).

## Absorbed follow-ups

Filed as separate prompts, then folded in on the human's instruction rather than
deferred (all three retired with their own records):

- `howto_paths_orientation_block_parity` — far smaller than filed. Both repos
  already had a `__Directories__` block; only the clone URL was missing (and
  `config/` in HowToLens). Not new authorship.
- `tutorial_searches_writes_into_chapter_2` — three of four searches wrote into
  `output/howtolens/chapter_2/`; fixed with their four print strings in one commit.
- `generate_markdown_leaks_worktree_paths` — shipped as PyAutoHands#281.

## Process notes

- `worktree_check_conflict` fired on HowToFit and HowToLens; **both claims were
  residue** (HowToFit's leg already merged; HowToLens's entry named a branch no
  worktree was on). It also reported one claim on HowToFit when `active.md` held
  three. HowToLens was taken as a deliberate parallel worktree with the file sets
  proved disjoint.
- Heart was YELLOW; the human acknowledged the exact reason set, none of which
  this change could affect.
- `navigator / Catalogue staleness` on #76 merged with a stuck `in_progress`
  status field whose `conclusion` was `success` with a completion timestamp —
  a GitHub metadata glitch, not an unfinished check.

## Still open

- **HowToFit** `markdown/chapter_1_introduction/tutorial_1_models.md:104` still
  reads `PyAutoLabs/autofit_workspace` — the original report's own repo. It
  belongs to the unmerged HowToFit#58: on HowToFit's `main` both the `.py` and
  the `.md` are stale, so branching off main would duplicate that PR. Prompt
  `draft/docs/howtofit/markdown_mirror_missed_by_url_fix.md` stays open.
- **HowToLens** `markdown/chapter_1_introduction/tutorial_0_visualization.md` is
  hand-patched: the worktree render leaked and was corrected by hand. Content is
  right, but it is not byte-identical to generator output. Re-render now that
  PyAutoHands#281 has landed.

## Original prompt

# HowTo tutorials still describe themselves as living inside the *_workspace repos

Type: docs
Target: workspaces
Repos:
- HowToGalaxy
- HowToLens
Themes:
- howto
- tutorials
Difficulty: medium
Autonomy: safe
Priority: medium
Status: workspace-dev
Consequence: notify
Witness: No `<workspace>/{output,config,dataset}` path or clone/download URL in
HowToGalaxy or HowToLens refers to the HowTo repo's own files; the
HubbleTuningFork image renders from its HowToGalaxy home and its
`.url_check_allowlist.txt` grandfather entry is gone; genuine cross-references
to sibling workspace *examples* are untouched.
Review-minutes: 20
Unattended: ready
Filed: 2026-09-14
Issued: 2026-09-14
Issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/75

The HowTo lecture series were split out of the `*_workspace` repos into their
own `HowToFit` / `HowToGalaxy` / `HowToLens` repos. The prose did not move with
them: tutorials still tell the reader their working directory, config, dataset
and output folders live inside the workspace repo, and HowToFit's `__Paths__`
block sends a reader who wants to clone HowToFit to `autofit_workspace`.

User-reported (2026-09-14), from HowToFit tutorial 1:

> If you don't have a HowToFit clone, you can download it here:
> https://github.com/PyAutoLabs/autofit_workspace

## The distinction that governs every edit

Two classes of `*_workspace` reference live in these repos. Only the second is
stale, and the fix must not flatten them together:

- **KEEP — cross-references.** "See `autolens_workspace/*/guides/modeling/chaining.py`",
  "all examples in the `autogalaxy_workspace` use Nautilus", "the workspace
  scientific workflow example". These point at the sibling workspace as the
  reader's *next destination* and are correct post-split. There are dozens of
  them. Do not touch them.
- **FIX — self-location.** Text that assumes the HowTo tutorials live *inside*
  the workspace repo: clone/download URLs, and `<workspace>/{output,config,dataset}`
  paths that are now `<HowToRepo>/{output,config,dataset}`.

## Scope

HowToFit is **out of scope** — see "HowToFit was fixed elsewhere" below.

- @HowToGalaxy — 15 hits. `tutorial_2_practicalities.py` (`path_prefix`
  described as `autogalaxy_workspace/output/howtogalaxy/chapter_2`; "checkout
  the `autogalaxy_workspace/output` folder" x3; "`config`: the files in
  `autogalaxy_workspace/config`"), `tutorial_3_realism_and_complexity.py`
  (2 print strings), `tutorial_2_data.py:338`
  (`autogalaxy_workspace/dataset/imaging/howtogalaxy/`),
  `tutorial_0_visualization.py:33,102`
  (`autogalaxy_workspace/dataset/...`, `autogalaxy_workspace/config/visualize`).
- @HowToLens — 14 hits. `tutorial_2_practicalities.py`
  (`autolens_workspace/output` x4), `tutorial_3_realism_and_complexity.py`
  (2 print strings), and five `scripts/simulator/*.py` — `lens_x2`, `lens_x3`,
  `lens_sersic`, `lens_extra_galaxy`, `no_lens_light__mass_sis` — each saying
  "The dataset can be viewed in the folder `autolens_workspace/dataset/imaging/...`"
  when the script writes into `HowToLens/dataset`.

Counts are from a 2026-09-14 grep of `scripts/` only; re-run the survey across
each repo before editing, since `README.md`, `start_here.py`, `welcome.py`,
`llms.txt` and `llms-full.txt` may carry the same class of reference.

## Separate bug, same root cause (@HowToGalaxy)

`scripts/chapter_1_introduction/tutorial_1_grids_and_galaxies.py:9` links the
Hubble tuning fork image at
`https://github.com/PyAutoLabs/autogalaxy_workspace/blob/main/scripts/chapter_1_introduction/HubbleTuningFork.jpg`.
That URL has been broken since the move; the file now lives at
`HowToGalaxy/scripts/chapter_1_introduction/HubbleTuningFork.jpg`. Rather than
being fixed, it was grandfathered into `HowToGalaxy/.url_check_allowlist.txt`
so the weekly `url_check.yml` cron stays green.

Fix the link **and delete the allowlist entry**. Leaving the entry behind keeps
a green check over a fixed URL and re-hides the next breakage.

## Derived artefacts

Every prose fix lands in three mirrors per tutorial — `scripts/*.py`,
`notebooks/*.ipynb`, `markdown/*.md` — and `workspace_index.json`, `llms.txt`
and `llms-full.txt` carry some of the same links. Regenerate derived artefacts
through each repo's own regeneration convention rather than hand-editing the
notebook/markdown mirrors. ~90 edits total.

## HowToFit was fixed elsewhere (2026-09-14)

HowToFit's only stale block — the `__Paths__` download URL in
`scripts/chapter_1_introduction/tutorial_1_models.py:93` — was fixed by a
parallel session on `feature/howtofit-tutorials-1-3` (commit `6f335b2`,
pushed) while this prompt was being surveyed. It now reads
`https://github.com/PyAutoLabs/HowToFit`.

**One gap remains on that branch:** the fix landed in `scripts/` and
`notebooks/` but not in `markdown/chapter_1_introduction/tutorial_1_models.md:104`,
which still reads `https://github.com/PyAutoLabs/autofit_workspace`. The
markdown mirror was not regenerated. That single line is the only HowToFit work
left; it belongs to `feature/howtofit-tutorials-1-3`, not to this task.

## Registry state this task had to correct (2026-09-14)

`worktree_check_conflict` fired on HowToFit and HowToLens. Both claims were
residue, and the guard also under-reported:

- `howtofit-mode`'s HowToFit leg had already **merged** (`409f562`, HowToFit#55);
  its worktree is clean and 0 commits ahead.
- `model-figures-rollout-lens` registers HowToLens on
  `feature/model-figures-rollout-lens`; the worktree is actually on
  **`feature/model-figure-prose-lens`**. active.md has the wrong branch.
- The guard reported one claim on HowToFit when `active.md` carries three
  (`howtofit-mode`, `model-figure-prose-simplify`, `howtofit-tutorials-1-3`),
  and HowToFit has five live worktrees.

## Delivery

One issue (HowToGalaxy, primary), **two PRs** — one per repo, independent. Run
`/prm` once, after both are green and merged; a single `/prm` per PR would close
the issue and advance the prompt prematurely.

HowToLens is taken as a **deliberate parallel worktree** off `origin/main`,
recorded as a `parallel-claim:` block on the `active.md` entry. Of this task's
seven HowToLens target files, exactly one overlaps
`feature/model-figure-prose-lens` (`scripts/chapter_2_lens_modeling/tutorial_2_practicalities.py`);
that branch's change there is model-figure prose, this task's is the four
`autolens_workspace/output` strings — different lines, and its tree is clean
with the work committed. A parallel worktree is preferred over a fold because a
fold shares the branch, not just the directory.

## Out of scope

Adding a `__Paths__` orientation block to HowToGalaxy and HowToLens for parity
with HowToFit. It is a real gap — those two repos have no "here is your working
directory, here is where to clone" section, which is why their stale paths are
scattered through prose instead of concentrated in one block — but it is new
authorship, not a correction. File it as a follow-up prompt.
