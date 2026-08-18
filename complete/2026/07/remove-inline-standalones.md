## remove-inline-standalones
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/160
- completed: 2026-07-24
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/161; https://github.com/PyAutoLabs/autolens_workspace/pull/337
- summary: Removed five inert standalone `%matplotlib inline` comments from the AutoGalaxy and AutoLens top-level script/notebook pairs and the unpaired AutoLens SLACS dataset helper. Generated notebooks parse, targeted smoke passed 19/19, both PRs passed CI and merged. An unrelated AutoLens full-generator partial-tree failure was restored before commit, leaving no residual churn. Four AutoLens occurrences embedded in old `pyprojroot` blocks remain intentionally outside this task; the dependent AutoCTI bootstrap sweep follows.
- verified: 2026-08-18 — re-verified against the two workspace mains after the 2026-08-08
  orphaned-prompt triage wrongly parked this task as "VERIFIED INCOMPLETE". That triage grepped
  for `%matplotlib inline` without checking whether each hit was standalone, and counted the
  deliberately-excluded bootstrap survivors as remaining work. Ground truth on main:
  `autogalaxy_workspace` has **zero** `%matplotlib inline` occurrences; `autolens_workspace` has
  exactly **four**, all first-line of an old commented-out `pyprojroot` block
  (`{scripts,notebooks}/{imaging,interferometer}/features/advanced/potential_correction/start_here.{py,ipynb}`) —
  i.e. precisely the four this task's PR body records as out of scope. autogalaxy_workspace#160
  is closed-completed (2026-07-28) and both PRs merged. No standalone occurrence survives; nothing
  remained to do. The dependent `pyprojroot` bootstrap sweep shipped separately as
  `autocti-notebook-bootstrap`.

## Original prompt

# Remove standalone matplotlib-inline comments

Type: refactor
Target: workspaces
Repos:
- @autogalaxy_workspace
- @autolens_workspace
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Remove the five standalone `# %matplotlib inline` comments from the AutoGalaxy
and AutoLens workspaces. Keep each top-level script/notebook pair consistent;
the fifth occurrence is the unpaired AutoLens dataset helper. Do not broaden
this task into the old `pyprojroot` bootstrap sweep, which is tracked by the
dependent AutoCTI follow-up.

Behaviour-preservation witness: the change is comment-only. Validate the two
notebooks as JSON and assert that tracked Python/notebook files in these two
repos no longer contain a standalone `%matplotlib inline` occurrence outside
the separately identified old-bootstrap examples.

## Original request (verbatim)

> ok, lets get rid of the five standalones and then tackle all the CTI stuff
