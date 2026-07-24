# Centralise shared community and governance documents

Type: docs
Target: pyautoscientist
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Make @PyAutoScientist the canonical home for the PyAutoLabs-wide community and
governance documents that are currently duplicated across repositories.
Inventory all registered repositories before fixing the scope. Move the shared
`CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` content to PyAutoScientist, then keep
small repository-root pointer files at the conventional filenames so GitHub
and contributors can still discover the canonical documents. Identify any
other duplicated repository-level files that belong to this same remit, while
distinguishing genuinely shared policy from repository-specific instructions.

Design the central layout so a forthcoming shared AI statement can follow the
same canonical-document plus repository-pointer pattern. Do not draft the AI
statement as part of this task unless needed only to establish its location or
link structure.

## Inventory findings

- `PyAutoLabs/.github` already provides public organization-wide default
  `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` files, issue forms, and a pull
  request template. It should remain the GitHub-native distribution layer,
  with its two policy files reduced to pointers to the full canonical documents
  in @PyAutoScientist.
- Fourteen registered repositories have a local `CODE_OF_CONDUCT.md`, seventeen
  have a local `CONTRIBUTING.md`, and twenty repositories have at least one of
  the two. Replace those full local copies with short, uniform pointers. Repos
  with no local override will inherit the `.github` pointer automatically.
- Eight repositories carry the same legacy Markdown bug/feature issue
  templates, which suppress the newer organization-level YAML forms. Remove
  those local duplicates so the organization defaults take effect.
- Keep licenses and scientific citation files local. Record `SECURITY.md`,
  `SUPPORT.md`, and `GOVERNANCE.md` as future candidates for the same shared
  community-health architecture; none currently exists locally to migrate.
- The forthcoming `AI_STATEMENT.md` is not a GitHub-native default community
  file, so its later rollout will need explicit repository pointers or links
  from one of the inherited standard files.

## Original request

> The repos all share and duplicate CODE_OF_CONDUCT.md, CONTRIBUTING.md, can we move their up to PyAutoScientist and have each repo level on just direct to that? We will add an AI STATEMENT next which follows the same logic. Check if anything else falls in this remit
