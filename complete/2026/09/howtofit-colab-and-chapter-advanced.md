HowToFit's GitHub front page mentioned Google Colab exactly once, buried
mid-README with no badge and no link, and deferred to chapter indexes that both
falsely claimed "Colab links to every tutorial are included". The chapter folders
also ran 1 then 3, with no chapter 2.

Shipped:

- **Colab is visible.** A Colab badge sits under the `# HowToFit` title and
  `Start Here on Colab` leads the header link row, both pointing at root
  `start_here.ipynb`. A `Run in Google Colab (nothing to install)` subsection now
  opens *Getting Started*, ahead of the local-install path.
- **Both chapter indexes now tell the truth.** Chapter 1's tutorials 6, 7, 8 and
  the optional Bayesian formalism used relative `../../notebooks/...` paths that
  open a raw GitHub view rather than Colab — all four converted. The advanced
  chapter's two optional tutorials (`hierarchical_ep`,
  `hierarchical_individual`) were unlisted despite having notebooks — both added.
- **`scripts/chapter_3_graphical_models/` → `scripts/chapter_advanced/`** via
  `git mv` (renames tracked as `R`, history preserved), 16 "chapter 3" prose
  phrasings reworded, and the 3 `main`-pinned URLs in autofit_workspace that the
  rename would have broken fixed.

PRs: HowToFit#54 (merge `3a755c5`), autofit_workspace#155 (merge `5226f2f`).
Both proven merged by `git merge-base --is-ancestor`, not by PR state alone.

Verified before merge: no `chapter_3_graphical_models` string in either repo; no
stale "chapter 3" prose; `tutorial_8_scientific_workflow.ipynb` still exactly 1
markdown cell and 0 code cells (prose-only by design, no Colab setup cell); all
36 Colab URLs canonical on tag `2026.9.14.1`, the form `bump_colab_urls.sh`
rewrites, so the pin stays current automatically. Regens: HowToFit 19 scripts,
autofit_workspace 32 scripts. CI green on every run for each head sha —
`Catalogue staleness` confirms the regenerated catalogue matches the renamed
tree, and the smoke suites execute every tutorial script on 3.12 and 3.13.

Notebook regeneration, the original question, turned out to be a no-op: a
throwaway regen in a detached scratch worktree produced a byte-identical tree
against `main`, so the committed notebooks were already exactly what the scripts
produce.

Three things a later reader should know:

1. **Output directories changed.** Tutorial output moves from
   `output/chapter_3_graphical_models/...` to `output/chapter_advanced/...`.
   Existing results do not resume; they remain under the old name.
2. **`markdown/` pages were hand-edited, not regenerated.**
   `generate_markdown.py` executes every curated script for real and is an
   at-release tool — disproportionate for a URL/prose substring. The edits are
   byte-equivalent to what a regen emits for those lines, and
   `bump_colab_urls.sh` already performs this same class of in-place `*.md`
   rewrite.
3. **Merged under an explicit human override of Heart RED**
   (`release validation FAILED (stage integrate)`, unrelated to this work — it
   is autolens/autolens_test workspace validation, manifest drift and profiling
   drift). This was NOT the AUTONOMY.md corrective-PR exception, which covers
   only a PR repairing the defect the RED names. Recorded so the precedent is
   auditable and never read as policy-sanctioned.

Follow-up filed: `draft/docs/autofit/howtofit_chapter_3_prose_references.md` —
PyAutoFit's two prose-only "HowToFit chapter 3" mentions, split out to keep the
library-first merge gate out of workspace-only work.

## Original prompt

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
