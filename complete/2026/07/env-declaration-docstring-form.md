## Outcome — SHIPPED, 12 PRs merged 2026-07-23/24

Issue: https://github.com/PyAutoLabs/PyAutoHands/issues/189 (closed). The
declaration syntax settled through two user-feedback refinements, each merged
same-day:

1. **#190 + 5 migration PRs** (al#327, ag#153, af_test#73, ag_test#90,
   al_test#208): `# ENV:` comments → standalone `__Env__` docstring blocks
   (user workspaces bottom + developer-only note; _test near top), with
   `strip_env_declarations` at the single shared generation layer
   (notebooks + markdown + navigator — future HowTo declarations covered).
2. **#191**: comment form removed LOUDLY (column-0 `# ENV:` raises with a
   migration pointer — a resurrected comment can never silently not-apply) +
   parser/strip generalized to the merged form; validator guidance strings
   updated.
3. **5 fold PRs** (al#328, ag#154, af_test#74, ag_test#91, al_test#210):
   standalone blocks folded INTO the adjacent docstring per doctrine (no
   close-then-reopen `"""` pairs) — 220 folded, 11 documented standalone
   fallbacks where code (not a docstring close) precedes the block.

## Final canonical form (docs/env_profile_redesign.md §10)

`__Env__` as the LAST SECTION inside an existing docstring — final docstring
for user-facing scripts + HowTo* (bottom, "Developer Only" note, stripped
from all generated output), module docstring for `*_test` (near top, short
template). Standalone `__Env__`-only docstring = fallback when no adjacent
docstring exists. Comment form = removal error.

## Gates that held at every step

- Resolved-env diff vs HEAD: IDENTICAL for every script at every stage
  (pure syntax moves; both forms parse to the same tokens).
- Structural: every fold eliminated exactly one delimiter pair; zero new
  close-then-reopen seams.
- Real notebook generation: no `__Env__`/`ENV:` leakage AND host-docstring
  prose preserved.
- All-strict validator (incl. --strict-declarations): 0 errors everywhere.
- PyAutoHands suite: 211 passing at the end.

## Gotchas

- Declarations are profile-agnostic and now doctrine-embedded — the parser
  detects a column-0 `__Env__` header ANYWHERE inside a bare-delimited
  docstring block; a docstring opened with inline content (`"""Title`) would
  not be scanned (convention uses bare delimiters; noted limitation).
- 11 fallback scripts end with code, not a docstring — fold there would be
  wrong; the preceding-line rule auto-detected all of them.
- The API gate false-positives on `al.` fixture strings when naming test
  files explicitly (bypass: PYAUTO_SKIP_API_GATE=1); full-suite runs unaffected.

## Follow-ups

- Phase 2 (mirror restructure + cull of autolens_workspace_test) — prompt
  drafted, UN-ISSUED, awaiting human go + YELLOW ack; restructure now
  near-free (declarations travel with files). Then eyes_gallery_repoint and
  test_results_relayout (both drafted).

## Original prompt

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
