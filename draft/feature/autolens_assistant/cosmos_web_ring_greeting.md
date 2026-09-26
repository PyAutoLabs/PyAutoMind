# COSMOS-Web Ring greeting: replace the Abell 1201 demonstration on the website, benchmark and Colab

Type: feature
Target: autolens_assistant
Repos:
- autolens_assistant
Themes:
- assistant
- benchmarks
- website
- colab
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 30
Unattended: needs-input
Supersedes: active/add_an_abell_1201_central_point_mass.md (autolens_assistant#133)
Filed: 2026-09-26

## Request (verbatim)

We have been doing work to make my website (/mnt/c/Users/Jammy/Professional) more
fancy by implmenting a abell_1201 greeting where they measure a SMBH. I want to undo
some of this work and shift it, but the main premise still stands. However, I want to
just do this with the cosmos-web ring example which is already used in thr PyautoLens
assiastant. for the following reasons: 1) The Cosmos web ring is more "immediate" in
terms of a user know its a less and uderstanding the basic lensing analysis; 2) Its
computationally quicker to analyse; 3) I can then link it to the COWLS survey which I
led. So, first remove the abell 1201 stuff from autolens_asistant, but make the cosmos
web ring one of the benchmarks we now routinerun against. Next, like we did for Abell
1201, model the system (here locally) and find two example fitds (good and bad but not
terrrible) which a user using the specific starting prompt which trrigger the asssitant
are described). Then put the cosmos web ring (with the pretty picture from the
autolens_assistant repo) on my website with the starting prompt and finally include a
dedicaded Google Colab that allows a reason to use AI to analyse the system but in a
Notebook style with more text, which on my website gives people two routes but also
helps on the autolens_assistant to illustrate and promotes this as another recommended
method to use the assistant, especially if you are learning PyautoLens and want to see
the API. A follow up issiue will further refine the assistant in the context of Google
colab here and throughout.

## Survey (2026-09-26, Fable session)

- Abell 1201 material merged on autolens_assistant origin/main via PR #134
  (issue #133 still open, Mind task `abell-1201-point-mass` awaiting-input):
  `dataset/imaging/abell_1201/` (10 FITS + manifest + README), `scripts/abell_1201/`
  (5 scripts + README), `benchmarks/prompts/oneshot/abell-1201-setup/` (card + score),
  `autoassistant/tests/test_abell_1201_{setup,posterior}.py`, README "Benchmarks"
  paragraph, `modes/maintainer.md` clone-boundary line, `benchmarks/README.md` table
  row, `VERSIONS.lock` entry, `test_benchmark.py` card set, `config/priors/mass/point/smbh.yaml`.
  Wiki literature pages (`entities/abell-1201.md`, `smbh-from-lensing.md`, `smbh-vlbi.md`)
  are literature, not demo material.
- Canonical checkout is 11 commits behind origin/main; untracked `dataset/abell_1201/`
  and `scripts/cluster_model_composition.py` spilled locally. Retained worktree
  `.worktrees/abell-1201-point-mass` holds 4.2 MB of ignored plots.
- COSMOS-Web Ring already ships: `dataset/imaging/cosmos_web_ring/wavebands/{F115W,F150W,F277W,F444W}`,
  README figure `docs/images/cosmos_web_ring_dataset.png`, vendored COWLS RGB
  `docs/images/sources/cosmos_web_ring_6_rgb.png`, existing one-shot card
  `oneshot-smoke` (grounding only, no fit), retired conversational card
  `easy_cosmos_web_ring.md`.
- Website page: `website/natural_language/{draft.md,render.py,index.html,page.css,prompt.js}`,
  image `website/assets/images/abell_1201_astrobites.{png,md}`; not a git repo.
