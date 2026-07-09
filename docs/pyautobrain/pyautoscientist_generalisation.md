# Generalise the organism into PyAutoScientist: adoption assessment + unified docs

Type: docs
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoMemory
- PyAutoBuild
- PyAutoHeart
- PyAutoLens
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Assess how the organism repos (@PyAutoBrain, @PyAutoMind, @PyAutoMemory,
@PyAutoBuild, @PyAutoHeart) can be generalised so other people can adopt the
PyAutoScientist agentic dev workflow: audit what is Jammy/lensing-specific vs
generic, propose a single unified ReadTheDocs (working name **PyAutoScientist**)
replacing the AI-written per-repo READMEs, and give an opinion on whether this
can become a standalone open-source offering **without splitting off** from the
repos in daily use. Note the domain-specific layer (the lens-modelling library,
its workspace/assistant/test/HowTo satellites) is baked into the design, so the
assessment must cover generalising that pattern too (e.g. a template
PyAutoProject + autoproject_workspace + assistant/HowTo skeletons).

## Original request (verbatim)

PyAutoBrain, PyAutoMind, PyAutoMemory, PyAutoBuild (soon to be Hands) and PyAutoHeart make up an AI development ecosystem resembling a organism or a PyAutoScientist. some aspects of these repos might be specific to my workflow, how I develop PyAutoLens and over domain specific aspects of what I do. furthermore they are not documented and their GitHub repos Readme.md are long text and very AI written. could you do an assessment of how we generalise these repos so other people can adopt the PyAutoScientist AI agentic dev workflow and maybe put together docs for all repos (but just one readthedocs maybe called PyAutoScientist). Happy for your opinion on if thus can become a standalone open source repo others user can come in and if this can be done without splitting off from the repos I use  also not that the design of domain specific things like PyAutoLens, autolens_workspace, autolens_assistqnt and the test and HowTo things are built into the PyAuto design so even these may need to be Generalised? (e.g. an example PyAutoProject, autoproject_workspace and so on)

<!-- formalised by the Intake (Conception) Agent on 2026-07-09 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs-PyAutoMind/ebd42158-6295-466c-9407-20d3e6d1a824/scratchpad/intake_raw.txt -->
