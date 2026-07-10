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
