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
