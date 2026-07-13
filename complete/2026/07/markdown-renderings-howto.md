## markdown-renderings-howto
- issue: https://github.com/PyAutoLabs/HowToLens/issues/24 (closed)
- completed: 2026-07-11
- prs: HowToFit#15 (62788e5) + HowToGalaxy#18 (3429dc5) + HowToLens#25 (93b520a) — all MERGED 2026-07-11
- summary: batch 2b executed-markdown for HowTo chapter_1 (6/6/9). FAST (ch1 = few/no searches). Surfaced+fixed 2 tutorials (tutorial_3_fitting, tutorial_7_fitting) MISSING setup_notebook → nbconvert CWD=notebook-dir broke relative paths; added line + regenerated notebooks. Broader audit filed bug/howto/missing_setup_notebook_audit.md. Calibration merged-unchanged. Completes the markdown-renderings rollout (phase1 + 2a + 2b, 8 PRs).

- completed: 2026-07-11
- issues: PyAutoBrain#84 + PyAutoBrain#85 + autolens_profiling#61 (closed)
- prs: PyAutoBrain#86 + PyAutoMind#60 + PyAutoHeart#59 + PyAutoBuild#145 + autolens_profiling#64 (all merged, merge commits)
- summary: Added Codex discovery across the PyAuto agent and workflow surfaces while preserving Claude commands and skill links. Phase 1 added thin `SKILL.md` wrappers for every public PyAutoBrain conductor/faculty and dual-harness installer coverage (30 tests; all 30 mandatory-load budgets pass). Phase 2 added `spawn`, `review-release`, `verify-install`, and `pre-build` wrappers plus explicit cross-harness ownership/routing (Heart 244 tests; Build 112 passed/1 skipped; composed installer and review clean). Phase 3 normalized `profile_likelihood` to Codex `profile-likelihood` while retaining Claude `/profile_likelihood`; profiling CI passed ruff, dashboard idempotence, links, and smoke. User explicitly directed PR+merge despite the ambient Heart YELLOW gate; no executable science or library API changed.

## Original prompt

# Markdown example renderings — batch 2b (HowTo trio)

Type: docs
Target: workspaces
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Follow-on to batch 2a (the three workspaces). Roll the executed-markdown
rendering system (PyAutoBuild generate_markdown.py, on main since 2026-07-10,
issue PyAutoBuild#134) out to the HowTo teaching series.

Scope (user-decided 2026-07-10): the full **chapter_1_introduction** of each of
HowToFit, HowToGalaxy, HowToLens — all tutorials in that chapter (HowToFit 6,
HowToGalaxy 6, HowToLens 9). Intro chapters are mostly visualization/fitting,
not full model-fits, so they render fast and showcase the teaching style with
images. Later chapters (modeling / pixelizations) are OUT of this batch.

Per repo: a config/build/markdown_examples.yaml listing the chapter_1 tutorials
in order, README links ("Browse the tutorials with output images"), a
git check-ignore verification on markdown/, and a real build (never TEST_MODE).
The HowTo repos each carry a Colab-style setup; confirm the pages render on
GitHub with images. Ship one pending-release PR per repo behind the four-leg
gate. Run this AFTER batch 2a merges (generator is repo-agnostic; no tooling
change expected). Operational traps are the same as 2a — see the phase-1 memory
[[markdown-example-renderings]].
