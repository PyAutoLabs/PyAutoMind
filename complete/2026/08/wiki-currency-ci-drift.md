## wiki-currency-ci-drift
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/317
- completed: 2026-08-29
- library-pr: autolens_assistant#117 (merged cc8dd2b -> main), autogalaxy_assistant#21 (merged aa00fb1 -> main)
- classification: library (two assistant repos; docs-only, no workspace follow-up — the assistants are their own workspaces)
- what shipped: the `wiki-currency` CI leg, RED on `main` in both assistants since 2026-08-23, is green again. Root cause was upstream: PyAutoArray `f9aceea3` (PyAutoArray#461) split the rectangular adaptive mesh family into Bilinear (rank-CDF) and RTU (kernel-CDF) variants and retired the unqualified `Rectangular*Adapt*` names, and PyAutoGalaxy `247e4a3a` deleted `autogalaxy/plot/plot_utils.py` as a byte-identical duplicate of `autogalaxy/util/plot_utils.py`. Every symbol was re-grounded against the RELEASED stack the CI job installs (2026.8.23.1), not a local source-tree `PYTHONPATH`.
  - autolens_assistant#117: `wiki/core/stack/autolens.md` — retired `al.mesh.RectangularAdaptImage` -> `RectangularBilinearAdaptImage`, with the split stated. `wiki/core/concepts/inversions_and_pixelizations.md` — the mesh-choice table named four symbols that do not exist; replaced with the four real adaptive classes plus the Bilinear-vs-RTU guidance taken from the upstream docstrings. `--scope all` missing/broken 1 -> 0.
  - autogalaxy_assistant#21: three sites (`skills/ag_multi_dataset.md`, `skills/ag_pixelization.md`, `wiki/core/stack/autogalaxy.md`) moved from the retired `ag.mesh.RectangularAdaptDensity` to `RectangularBilinearAdaptDensity` — Bilinear rather than the pure-rename RTU, because the split made Bilinear the fast CPU default and it is what the workspace scripts use (77 call sites vs 2), which is what these pages were recommending. `wiki/core/operations/sandbox.md` re-cited to `autogalaxy/util/plot_utils.py` in both the frontmatter `sources:` list and the `PYAUTO_FAST_PLOTS` prose. `--scope all` 1 -> 0; `--check-citations` 2 missing paths -> 0.
- pinned_commit deliberately unchanged in `sandbox.md`: `PYAUTO_FAST_PLOTS` is present in `util/plot_utils.py` at that same pin (65b14d77, verified), so the citation pointed at the wrong one of two identical copies rather than at something that moved. Bumping the pin would have claimed a move that did not happen.
- provenance: every edited `wiki/core/` page carries a `content_sha256` and was re-stamped with `--write-provenance --page`; `last_updated` bumped. An unstamped body edit is itself a CI error.
- validation: per repo, in a clean venv on the released stack with `PYTHONPATH` unset — `--check-version`, `--scope all`, `--lint-idioms`, `--check-provenance`, `--check-citations` all clean, plus (lens only) `chat_bundle.py --check` OK. On the merged heads CI reported `wiki-currency` PASS and `clone-boundary` PASS on both PRs.
- prompt claim measured FALSE: the originating prompt stated autolens_assistant's `llms-chat.txt` and `chat_pack/01_api_surface.md` were stale on `main`. They are not. `chat_bundle.py --check` is OK against the released stack (2026.8.23.1) — the same result CI reported. The FAIL reproduces only against a local source-tree `PYTHONPATH`, where regenerating would DOWNGRADE the committed version stamp to 2026.8.17.1 and inject unreleased `autofit` Bijector symbols. Regenerating would have introduced drift rather than removed it, so both files were left untouched. This is the second time a chat-bundle "stale" reading has come from the wrong stack; check the version stamp before believing it.
- scope: `euclid_assistant` is a different design and was never opened. No check was weakened to pass; no library source was touched.
- heart-red-at-ship: "PyAutoArray: 2 commit(s) behind origin" — verbatim from `pyauto-heart readiness --json` at 2026-08-29T01:56:44Z. Pre-existing and unrelated (markdown-only changes in two other repos). Human acknowledged and authorised PR-open; merge authorised separately.
- merge note: both PRs were squash-merged to match the repos' convention (autolens_assistant#116 / autogalaxy_assistant#20, merged hours earlier the same day, are single-parent squashes). `--is-ancestor` therefore reads UNMERGED for both heads; merge proven from `state=MERGED` plus the squash commits cc8dd2b / aa00fb1.
- follow-on: this task closes the red leg that `complete/2026/08/science-project-memory.md` recorded as knowingly merged over (autolens_assistant#116, autogalaxy_assistant#20).

## Original prompt

# Fix wiki-currency CI drift in the lens and galaxy assistants

Type: maintenance
Target: PyAutoBrain
Repos:
- autogalaxy_assistant
- autolens_assistant
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: medium
Status: issued
Issued: 2026-08-28

# Fix wiki-currency CI drift in the lens and galaxy assistants
Type: maintenance
Difficulty: small
Autonomy: safe
Priority: medium

The `wiki-currency` CI leg is red on main for autolens_assistant and autogalaxy_assistant (Actions runs 33226180760 and 33226182888, 2026-08-28). The symbol audit run with `--scope all` reports 1 missing or broken symbol in each repo, out of 67 files and 141 symbols scanned. autogalaxy_assistant additionally fails its citation-path check: `wiki/core/operations/sandbox.md` cites the galaxy library's `plot/plot_utils.py` module, which no longer exists in the sources checkout. autolens_assistant's `llms-chat.txt` and `chat_pack/01_api_surface.md` are also stale on main.

Task: regenerate the stale generated surfaces and re-cite the dead path so the `wiki-currency` leg goes green again on both repos. Note that PRs #115 and #116 (autolens_assistant) and #19 and #20 (autogalaxy_assistant) were merged over this drift on human acknowledgement, so the red leg predates and survives those merges.

Related: PyAutoBrain#315.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/069a02ef-b14f-4a43-b0c3-92e461ddef66/scratchpad/intake_wiki_currency.md -->
