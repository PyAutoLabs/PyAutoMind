## natural-language-first-docs
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1587
- completed: 2026-09-09
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1588
- workspace-pr: https://github.com/PyAutoLabs/autofit_assistant/pull/32
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1588

PyAutoFit's docs now lead natural-language first. The Overview toctree reads
Inference with Natural Language → Scientific Workflow → Statistical Methods →
The Python API, and `docs/index.md` leads with the assistant route instead of
the Python API.

- `docs/overview/the_basics.md` → `docs/overview/python_api.md` ("The Python
  API", anchor `(python-api)=`), tracked as a rename so history follows. It now
  opens as the under-the-hood companion to the natural-language page.
- `docs/overview/natural_language.md` (human-authored) entered the toctree — it
  had been an orphan page. Gained a teacher-mode section under HowToFit and a
  Scientific Context section on populating the assistant's literature wiki.
- `docs/index.md`: the ~90-line Gaussian walkthrough under `## API Overview`
  was cut to pointers at the two overview pages (it survives in full on the
  Python API page); `autofit_assistant` is now the first Getting Started bullet.
- `autofit_assistant/README.md`: the same walkthrough fills the previously
  empty `### Using PyAutoFit Assistant`, Science Project was rewritten, and
  "Choosing Your AI Tool" was corrected from PyAutoLens to PyAutoFit.

**User-visible URL change:** readthedocs `overview/the_basics.html` becomes
`overview/python_api.html`. The old URL 404s — raised with the human and
accepted. Every in-repo link was updated; the `autofit_workspace` notebook
links (`overview_1_the_basics.ipynb`) point at another repo and were left.

## Traps worth remembering

- **The Sphinx baseline is a count, not a list.** `docs/sphinx_warning_baseline.txt`
  holds a bare integer and CI fails when the count exceeds it. Deleting the
  orphaned `backup.md` removed one warning, so the baseline was ratcheted
  31 → 30 — but only after building `main` in the same environment and
  confirming it produced exactly 31. Ratcheting on the new count alone would
  have risked a CI failure from an environment difference.
- **The Brain classified this `combined` off an out-of-scope mention.** The
  prompt named `@autofit_workspace` only to exclude it; the Feature Agent read
  the `@RepoName` reference and planned a workspace follow-up PR. Overridden to
  library-only. A repo named in an "out of scope" section still reads as an
  affected repo.
- **The assistant README was adapted from `autolens_assistant`** and still
  carries its traces: it links to four `docs/setup/*.md` pages that do not
  exist in `autofit_assistant` (no `docs/` dir at all), and `#free-ai-tools` /
  `#conversation-assistants` anchor at sections since removed. Flagged in the
  PR, not fixed — porting them needs PyAutoFit-specific rewriting.
- **Teacher mode's trigger is `Teacher mode.`** `autofit_assistant/README.md:95`
  says "Teacher model." — a typo; the working example at line 98 and
  `modes/teacher.md` both use `Teacher mode.`
- Heart was RED at ship time on `release validation FAILED (stage integrate)`
  (organism-scope, the release chain). Acknowledged by the human: both branches
  are docs-only and nothing in them is in the release chain.

## Original prompt

# PyAutoFit docs go natural-language first: `natural_language` becomes the main overview page, "The Basics" becomes "The Python API"

Type: docs
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- documentation
Difficulty: small
Autonomy: supervised
Priority: high
Status: issued
Witness: `docs/index.md`'s Overview toctree reads `overview/natural_language`, `overview/scientific_workflow`, `overview/statistical_methods`, `overview/python_api` in that order; `docs/overview/the_basics.md` no longer exists and `docs/overview/python_api.md` is titled "The Python API" with anchor `(python-api)=`; no in-repo link still points at `overview/the_basics`; the landing page leads with the natural-language/assistant framing; Sphinx build produces no new warnings against `docs/sphinx_warning_baseline.txt`.
Consequence: judge
Review-minutes: 15
Unattended: needs-slicing
Filed: 2026-09-09
Issued: 2026-09-09
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1587

Original request (verbatim):

> I ave made some updatesto the PyAutoFit docs I want to work into main via a
> PR, I want the main overview page to be the "natural_language.md", I want
> "the basics" to be renamed "the Python API" and be fourth down understand
> scientific workflows and statistical methods. We are going NAtural language
> first.

## Starting state

The human has uncommitted work in the canonical @PyAutoFit checkout on `main`:
a new `docs/overview/natural_language.md` (staged, then further edited in the
worktree) and a deleted `docs/overview/backup.md` (staged deletion; it was an
old "Extending Models" draft superseded by the new page). Both must be carried
onto the task branch — nothing is committed on `main`.

## Changes

- **Overview toctree order** in `@PyAutoFit/docs/index.md` becomes
  `natural_language` → `scientific_workflow` → `statistical_methods` →
  `python_api`. `natural_language` is the main overview page.
- **Rename** `@PyAutoFit/docs/overview/the_basics.md` →
  `docs/overview/python_api.md` (git mv, so history follows): heading
  `# The Basics` → `# The Python API`, MyST anchor `(the-basics)=` →
  `(python-api)=`. Confirmed with the human: the readthedocs URL changes from
  `overview/the_basics.html` to `overview/python_api.html`; the old URL will
  404 and that is accepted.
- **Update every in-repo link** to the renamed page: `docs/api/model.rst`,
  `docs/api/priors.rst`, `docs/api/analysis.rst` (readthedocs `the_basics.html`
  links) and the two `the_basics.html` links inside
  `docs/overview/natural_language.md`, which already call the page "The Python
  API". Links to the *workspace notebook* `overview_1_the_basics.ipynb` in
  `docs/index.md`, `docs/api/*.rst` and `README.md` point at
  @autofit_workspace and are **out of scope** — leave them alone.
- **Landing page (`docs/index.md`)** is reframed natural-language first,
  confirmed with the human: lead with the assistant / natural-language pitch,
  and cut the long Python "API Overview" Gaussian walkthrough down to a
  pointer at the Python API overview page. Getting Started / Support /
  HowToFit sections and all other toctrees stay.
- Light copy-edit of the human's `natural_language.md` typos where they are
  unambiguous (`instlal`, `advanced[Statistical`, `taksk`, `scienist`,
  `customizeable`) — no rewriting of their argument or structure.

## Out of scope

- @autofit_workspace notebook/script renames (`overview_1_the_basics.ipynb`)
  and any Colab badge URLs.
- The `[Find 1D example of a random model to the data, maybe from HowToFit]?`
  placeholder the human left in `natural_language.md` — flag it in the PR, do
  not invent an image.

## Acceptance

- `cd docs && make html` (or the repo's documented build) succeeds with no new
  Sphinx warnings versus `docs/sphinx_warning_baseline.txt`.
- `grep -rn "the_basics" docs/` returns only the @autofit_workspace notebook
  links.
