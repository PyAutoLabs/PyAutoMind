# HowToFit — surface the Colab entry point on the README, rename chapter 3 to chapter_advanced

Type: docs
Target: HowToFit
Repos:
- HowToFit
- autofit_workspace
Themes:
- docs-hub
- autofit
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: no
Filed: 2026-09-14

Original request (verbatim):

> for HowToFit, can we generate the Jupyer Notebooks?
> Ok great, can you make it so the Google Colab link is clear and visible on the HowToFit GitHub Readme
> Also make chapter 3 become chapter_advanced

Notebook regeneration was checked first and is a no-op: a throwaway regen in a
detached scratch worktree produced a byte-identical tree against `main`
(70bfcfa), `Catalogue written: llms-full.txt, workspace_index.json (19 scripts)`.
The committed notebooks are exactly what the current scripts produce, so this
prompt is only the README/Colab work plus the chapter rename — but each of those
does require a regen to propagate.

## 1. Colab visibility on the root README

`README.md` mentions Colab once, buried at line 44 ("every tutorial can be
opened directly in Google Colab via the links in each chapter's `README.md`").
No badge, no direct link. `autofit_workspace/README.md` puts a Colab badge on
line 3, directly under the title — mirror that convention.

- Add a Colab badge immediately under the `# HowToFit` title, pointing at the
  root `start_here.ipynb` (it carries Colab setup cells), pinned to the current
  tag `2026.9.11.1`.
- Add a "Start Here on Colab" entry to the header link row.
- Replace the line-44 sentence with a prominent "Run in Google Colab (no
  installation)" subsection under *Getting Started*, presenting Colab as a
  first-class option alongside the local install rather than an afterthought.

`PyAutoHands/autohands/bump_colab_urls.sh` already covers the `HowToFit` repo
and sweeps `*.md` at any depth, so pinned-tag URLs in the root README are
auto-bumped at each release. Use the canonical
`colab.research.google.com/github/PyAutoLabs/HowToFit/blob/<tag>/...` form or the
bumper silently skips them.

## 2. The chapter indexes lie about Colab coverage

Both chapter READMEs claim "**Colab** links to every tutorial are included".
Neither is true:

- `scripts/chapter_1_introduction/README.md` — tutorials 1-5 have real Colab
  URLs; **tutorial 6 (gradients), 7 (the details), 8 (scientific workflow) and
  the optional Bayesian formalism** use relative `../../notebooks/...` paths,
  which on GitHub open a raw notebook view, not Colab. Convert all four.
- `scripts/chapter_3_graphical_models/README.md` — tutorials 1-5 have Colab
  URLs; the **two optional tutorials** (`tutorial_optional_hierarchical_ep`,
  `tutorial_optional_hierarchical_individual`) are not listed at all despite
  having notebooks. Add both as Colab rows.

Chapter READMEs are authored in `scripts/` and copied into `notebooks/` by
`generate.py`, so edit the `scripts/` copies and regenerate.

## 3. Rename chapter 3 -> chapter_advanced

`scripts/chapter_3_graphical_models/` -> `scripts/chapter_advanced/` (human
decision 2026-09-14: unnumbered `chapter_advanced`, not `chapter_2_advanced` —
it kills the confusing 1-then-3 gap and names what the chapter is rather than
where it sits). Prose "chapter 3" becomes "the advanced chapter".

Blast radius, measured 2026-09-14:

- **HowToFit — 30 files** reference `chapter_3_graphical_models` / "chapter 3",
  including `AGENTS.md`, `README.md`, `scripts/README.md`,
  `notebooks/README.md`, `start_here.py`, `start_here.ipynb`,
  `scripts/simulators/simulators.py`, and chapter 1's `tutorial_1_models.py` and
  `tutorial_8_scientific_workflow.py`. `llms-full.txt`/`workspace_index.json`
  are regenerated, not hand-edited.
- **autofit_workspace — 3 source files with hard `main`-pinned URLs that break
  on rename**, plus their generated `.ipynb`/`.md` twins:
  - `scripts/features/graphical_models.py:24`
  - `scripts/features/expectation_propagation.py:432`
  - `scripts/overview/overview_3_statistical_methods.py:29`
- **PyAutoHands** hardcodes no chapter folders (`generate.py` derives grouping
  from whatever top-level folders exist in `scripts/`), so the tooling needs no
  change.
- HowToLens / HowToGalaxy matches are their own chapter 3s — out of scope.

Use `git mv` so history follows the files. Regenerate notebooks + catalogue in
both repos and commit them alongside the source edits (HowToFit's `AGENTS.md`
requires notebook twins in the same PR; so does autofit_workspace's).

## Out of scope — file separately

`PyAutoFit` carries two prose-only "HowToFit chapter 3" mentions with no URLs:
`autofit/messages/truncated_normal.py:328` and
`test_autofit/graph_spec/graphical_doubles.py:81`. Including them would pull a
library PR and the library-first merge gate in for two lines of prose (human
decision 2026-09-14). File as a trivial `docs/autofit` follow-up prompt.

## Verification

- Every Colab URL in both repos resolves (HowToFit CI has `url_check.yml`).
- `navigator_check.yml` passes — the regenerated `llms-full.txt` +
  `workspace_index.json` must be committed or it fails.
- `notebooks/chapter_1_introduction/tutorial_8_scientific_workflow.ipynb` still
  has **zero** code cells, including no Colab setup cell (prose-only by design).
- No `chapter_3_graphical_models` string survives in either repo.
