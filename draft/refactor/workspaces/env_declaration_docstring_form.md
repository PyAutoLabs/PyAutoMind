# __Env__ docstring form for user-workspace env declarations (Phase 1b follow-up)

Type: refactor
Target: workspaces
Repos:
- PyAutoHands
- autolens_workspace
- autogalaxy_workspace
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised

User feedback on the merged #187 migration (2026-07-23): the `# ENV:` comment
lines clutter user-facing teaching scripts and would leak into regenerated
notebooks; the declaration should follow the workspace docstring doctrine
(`__Section__` format), sit at the BOTTOM of the script so users don't notice
it, carry an explicit developer-only note, and be STRIPPED from generated
notebooks and markdown. `_test` repos keep the plain `# ENV:` comment (not
user-facing).

**The tasks:**
1. **Mechanism (PyAutoHands):** `read_env_declaration` additionally parses a
   docstring section headed `__Env__` containing an anchored `ENV: <tokens>`
   line. Both syntaxes valid; a file carrying both (or two of either) is a
   duplicate-declaration error. Validator inherits via the shared parser.
2. **Generation strip (PyAutoHands):** the script→notebook and script→markdown
   generators drop the entire `__Env__` docstring section, so rendered docs are
   byte-identical to the pre-declaration state. Check the navigator/contents
   validators tolerate (or are taught to ignore) the section.
3. **Migration (autolens_workspace 53 scripts, autogalaxy_workspace 36):**
   replace each `# ENV:` comment (+ its adjacent rationale comment) with a
   bottom-of-file `__Env__` docstring section using the standard template
   (developer-only note + rationale + `ENV:` line).
4. **Verification:** resolved-env diff per repo (empty base) must be IDENTICAL
   before/after (pure syntax move); generated notebook/markdown output for a
   sample of migrated scripts must contain no `__Env__`/`ENV:` content; full
   PyAutoHands suite green; validator all-strict 0 errors on both repos.

Notebooks have NOT regenerated since #187 merged, so no user-visible artifact
carries the comment form yet — this must land before the next pre_build.
