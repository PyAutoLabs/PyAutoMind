# Release docs polish + 3-ways-to-learn (PyAutoLens / Galaxy / Fit)

Type: docs
Target: PyAutoLens
Repos:
- PyAutoFit
- PyAutoGalaxy
- PyAutoLens
- autolens_assistant
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

I am readying for a PyAuto release and want to do the following on PyAutoLens docs:

(i) make sure API docs are clean and up to date (do this also for PyAutoGalaxy and PyAutoFit);

(ii) clusters and weak lensing are now working and mature and thus can be explained to users as things they can go and use (e.g. no "in development" flags); make sure this is also reflected on autolens_workspace;

(iii) in overview_2_new_user_guide.md, the equivalent location in autolens_workspace, and the README.md files of PyAutoLens and autolens_workspace, explain that there are 3 ways to learn to use PyAutoLens:
  (i) reading workspace guides;
  (ii) asking questions to an AI assistant like ChatGPT, which uses the llms.txt interface, giving an example of how a user does that (there is an example somewhere in the source code; the user points to the URL for the autolens_assistant);
  (iii) fully agentic AI use via Claude, Codex, pointing to autolens_assistant for more information.

Put these 3 options as a subsection after this sentence: "The autolens_workspace contains a suite of example Jupyter Notebooks, organised by lens scale and dataset type", with the first option being "manual navigation" flagging the questions below that are about to follow.

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b7b89cda-1dac-48c9-8880-7d467cd91f58/scratchpad/intake_input.txt -->
