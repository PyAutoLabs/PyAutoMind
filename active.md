# Active Tasks

## jax-default-dependency
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/702
- status: shipped-awaiting-release-followups — ALL ELEVEN PRs merged 2026-08-19 (human-authorized):
  six library (PyAutoHeart#150, PyAutoNerves#150, PyAutoFit#1503, PyAutoArray#450, PyAutoGalaxy#574,
  PyAutoLens#703) + five workspace (autolens_workspace#486, autogalaxy_workspace#212,
  autofit_workspace#139, HowToLens#71, HowToGalaxy#67; pending-release hold waived by human — prose-only,
  few-hour docs-ahead window until the nightly). Worktree removed, claims released, branches deleted.
- nojax CI leg caught two real bugs day one: unmarked jax-requiring autolens test (94d8f54ba);
  NumPy-scalar misrouting in autofit Beta/Gamma/Normal message dispatch (19c679583).
- jax cap stays <0.11 (widen reverted 848a254; jax 0.11 bug prompt:
  draft/bug/autofit/jax_011_message_log_partition_tuple_shape.md).
- NEXT (release-blocked; nightly 02:00 UTC): (1) bump intra-family floors `>=2026.7.29.2` → first
  promoted version in all five pyprojects, then move this task to complete/; (2) later, make
  unittest-nojax a required check once it has green history.
- prompt: active/jax_default_dependency.md

## notebook-quotes-string-literal
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/244
- prompt: active/notebook_quotes_string_literal_closing_delimiter.md
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/notebook-quotes-string-literal
- registered: 2026-08-20 via /start_dev; no worktree conflict (worktree_check_conflict exit 0).
- confirmed live on origin/main before planning: `add_notebook_quotes.py:152` prefix test matches a
  code string literal's column-0 closer, inverting every later cell boundary (code cell becomes a
  SyntaxError; following code emitted as markdown). Latent workspace-wide — the only file with the
  shape, autolens_workspace_test/gallery/gallery_build.py:42, sits outside `scripts/`.
- `strip_env_declarations:51` shares the prefix assumption but is NOT a live defect (verified);
  migrated as hardening only. Zero-diff workspace regen is the proof that migration is safe.
- repos:
  - PyAutoHands: feature/notebook-quotes-string-literal

## transformed-message-factor-gradient-unpack
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1501 (issued 2026-08-19)
- prompt: active/16_transformed_message_factor_gradient_unpack.md
- status: HOLD — do not start dev. Fix-or-delete hangs off the PyAutoFit#1498 logpdf-contract
  decision (parked #1500 design bundle); dead code (zero production callers), crashes on first
  call if ever exercised.
- external: community PR https://github.com/PyAutoLabs/PyAutoFit/pull/1502 (@trexfr-ops) targets
  this exact unpack — review via /community before any local work; the #1498 adjudication decides
  whether the method should exist at all.
- registered: 2026-08-19 by the wake_up session — the issuing session (claude/autofit-priors-messages-audit-ylvenv)
  filed the prompt + issue but not this entry, tripping Lifecycle Drift on main.
- repos-none-claimed: this entry claims NO repos — one line deliberately, not 2-space bullets.

## vincken-2026-bib-placeholder
- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/39
- session: claude --resume 084ed603-054f-433c-9b87-e5cfc5506059
- prompt: active/add_vincken_2026_wiki_and_cite_in_euclid.md
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/vincken-2026-bib-placeholder
- registered: 2026-08-20 via /start_dev; no worktree conflict (worktree_check_conflict exit 0).
- rescoped at plan approval: prompt's arXiv link (2503.22657) is Shajib 2025 dolphin, NOT Vincken —
  and dolphin is already in PyAutoMemory (`Shajib2025dolphin`, #34/#36 pass), missing only a log.md
  line. Vincken 2026 (Euclid DR1 lens-finding ML paper) is real but unpublished, so this task lands
  a GENERIC placeholder only — public repo, EC-internal draft, human chose no draft-verbatim title.
- DEFERRED, not in this task: the `\citep{}` edit into "…only recently automated (Vincken 2026),".
  That sentence is in no file under PyAutoLabs; the Euclid paper's .tex lives outside the workspace.
- FOLLOW-UP owed after ship: refresh `Vincken2026` with verified title/arXiv ID/DOI/authors once the
  paper is public, and replace the placeholder `**Supports:**` bullet with real claims.
- repos:
  - PyAutoMemory: feature/vincken-2026-bib-placeholder
