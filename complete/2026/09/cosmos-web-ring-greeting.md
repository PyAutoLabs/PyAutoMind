## cosmos-web-ring-greeting
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/136 (closed)
- completed: 2026-09-26
- brain-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/419 (merge 896c4fa3)
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/137 (merge 9d96bae1)
- merge-order: Brain first, assistant second (the assistant CI ran against `Brain-ref: feature/cosmos-web-ring-greeting`)
- supersedes: abell-1201-point-mass (autolens_assistant#133)
- summary: |
    The Abell 1201 demonstration is removed from autolens_assistant and replaced by the COSMOS-Web Ring as
    the assistant's greeting example: a new greeting skill plus general-reader audience routing, so a
    non-specialist first contact is walked through modelling the ring. Reference fits recover
    theta_E = 0.803" / 0.775" (effective), consistent with Mercier et al.'s 0.77-0.78". A
    `cosmos-web-ring-fit` benchmark card records runs 0 / 0 / 100. A Colab notebook ships with the
    walkthrough. PyAutoBrain's clone classifications retire the Abell 1201 domain path and add the
    COSMOS-Web Ring greeting paths. The website commit (Jammy2211.github.io 3597326) is pushed after the
    assistant merge.
- heart-red-override: "2026-09-26 live human, in direct response to the question naming this task, authorised the development-only override: push both branches and open the two PRs (no merge, no release, no CI bypass; merge via /prm on green checks). RED reasons: release validation FAILED (stage integrate); YELLOW: workspace validation not passing (4 failed, cloud#35579888156); manifest drift hub organism blurb 7; manifest drift organism-map blocks 1. Gates passed: assistant make test 128 passed 1 skipped + freeze-check OK; Brain clone tests 64 passed; check_boundary.py autolens_assistant complete; GPU smoke fit script 285 s; benchmark cosmos-web-ring-fit run 3 = 100."
- merge-authority: human "the fits look good so continue to proceed" (separate explicit merge grant this turn); every check green at the merged heads (Brain pytest 3.12/3.13; assistant boundary + wiki-currency).
- follow-ups: |
    - Run the Colab notebook in real Colab (not yet done) and tag-pin the Colab badge.
    - draft/feature/autolens_assistant/colab_refinement_throughout.md
    - draft/feature/pyautohands/bump_colab_urls_autolens_assistant.md
    - draft/refactor/workspaces/abell_1201_local_cleanup.md

## Original prompt

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
Status: issued
Consequence: judge
Review-minutes: 30
Unattended: needs-input
Supersedes: active/add_an_abell_1201_central_point_mass.md (autolens_assistant#133)
Filed: 2026-09-26
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/136

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
