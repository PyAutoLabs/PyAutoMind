# Deep audit of autolens_assistant skills prose and tooling robustness

Type: feature
Target: autolens_assistant
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Phase 2 of the reference-assistant audit (phase 1: issue #33 / PR #34 — README/AGENTS
cleanup and the two-mode model). Phase 1 deliberately did not read the individual skill
bodies or the tooling; this prompt is that deep pass. Run it with a strong reviewing model
(Fable): the skills themselves are executed by whatever model the user has, so the review
standard is "would this recipe steer a *weaker* model correctly?", not "can a strong model
fill the gaps?".

**Prerequisite:** PR #34 merged, so the two-mode (teacher/assistant) model is settled text.

**Expect to split into phased PRs at start_dev time** — suggested cut:

## PR A — skill prose review (highest value)

- Read every **mature** skill body end-to-end against `skills/_style.md` and the live
  installed API (source-of-truth order in AGENTS.md; the code gate protects symbols, not
  reasoning).
- Tighten the Orient → Ask → Branch → Combine arcs: weak phrasing, buried decisions,
  missing "when NOT to use this", stale workspace-example pointers.
- Judge each recipe as instructions for a weaker model: are the steps executable without
  inference leaps? Are failure modes and checks explicit? Fix in place; keep skill names
  and frontmatter contracts stable.
- `skills/_style.md` itself gets the same treatment (phase 1 only touched one sentence).
- Optionally promote 1–2 stubs from the pending queue to full recipes if the review pass
  makes them cheap (`al_subhalo_detect` first — README example 3 exercises it); do not
  mass-fill stubs.

## PR B — tooling robustness

- `autoassistant/audit_skill_apis.py`: error paths, exit-code contract, and the
  version-check UX — a version skew currently prints the same multi-paragraph
  WorkspaceVersionMismatchError three times (once per library import); it should report
  once, short, with the two remedies. Found while validating phase 1.
- The PreToolUse code-gate hook: review wiring, bypass ergonomics, false-positive/negative
  behaviour on the current stack.
- `activate.sh`, `Makefile` targets, `config/` defaults, sandbox/cache env-var handling
  (`NUMBA_CACHE_DIR`, `MPLCONFIGDIR`, `PYAUTO_SKIP_WORKSPACE_VERSION_CHECK`).
- Refresh the pinned version baseline against the installed 2026.7 stack (the standing
  Heart skew finding) or record why it must wait for the next release.

## PR C — workflow skills + wiki spot-checks

- `start-new-project.md` end-to-end review — the highest-stakes skill (it scaffolds user
  repos); verify the copy/never-copy lists, lifecycle stages, and refer-back contract
  against the actual template behaviour.
- `contribute-upstream.md`, `init-slam.md`, `_bootstrap_skill.md` same treatment.
- Spot-check `wiki/core/` operational pages (installation, hpc, sandbox, dataset) against
  the installed stack; flag — don't rewrite — scientific content issues in
  `wiki/literature/`.

## Constraints (unchanged from phase 1)

- AGENTS.md stays canonical; no parallel instruction files; safety invariants untouched.
- Small reviewable diffs per skill; no renames; no premature generalisation — respect the
  template-boundary notes in `modes/maintainer.md`.
- Validate each PR: `audit_skill_apis.py` symbol audit, `make
  validate-literature-citations`, link sweep; draft PRs, merge stays human.
