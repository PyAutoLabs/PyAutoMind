# Build ic50_assistant from autofit_assistant for EP/graphical IC50 analysis

Type: feature
Target: ic50_assistant
Repos:
- autofit_assistant
- ic50_assistant
- PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

/mnt/c/Users/Jammy/Science/ic50_workspace contains a number of scripts for our
work on IC50 analysis, including real data and simulated IC50 data.

Can you look at autofit_assistant, and build us an ic50_assistant, which I will
then use to perform ic50 analysis using the examples and scripts in that
workspace (which you can assume in terms of stats and functionality work). This
assistant will be using Expectation Propagation (EP), graphical models and other
autofit features.

The goal will be:

- To demonstrate it can recover input solutions using the simulated datasets.
- Fit the simulated data with graphical / EP, showing that EP can scale to more
  datasets once the dataset is large enough.
- Do EP / graphical fits to the real datasets showing the same scaling
  performance.
- Compare to the random forest and other methods in the workspace, to show
  hopefully that EP extracts more information.

You would benefit from finding some IC50 papers to put in the assistant context
/ wiki.

Once we have the ic50 assistant, we will then convert this workspace into a
separate science project with a closed github repo. Make sure all of this can
run on RAL and its HPC via the HPC link. Try and find some papers relevant to
this IC50 use case to use as part of the assistant training.

## Classification notes (intake hand-fix)

- The auto-classifier resolved Target=PyAutoFit because the prompt names "autofit
  features / EP / graphical models". Corrected: this builds a **new domain
  assistant cell (`ic50_assistant`) seeded from `autofit_assistant`** — it is not
  a PyAutoFit library change. PyAutoFit is a consumed dependency (EP, graphical
  models, aggregator), not an edit target. (Known pattern: bare library mentions
  steal Target from assistant repos.)
- Source cell confirmed present: `autofit_assistant/`. Science workspace confirmed
  present: `/mnt/c/Users/Jammy/Science/ic50_workspace` (AGENTS.md, scripts/, hpc/,
  dataset/, notebooks/, config/, output/). No `ic50_assistant` exists yet — this
  is a fresh assistant cell.
- This is an **assistant-cell clone/seed** task: at `/start_dev` time it should
  route through the Clone Agent (`/clone`) to decide exact-clone vs sibling vs
  seed, and repo creation is a human interactive gate (do not `gh repo create`
  unprompted).
- **Large / phased.** Expect to split into phased PRs at start_dev time.

## Scope sketch (to be firmed at start_dev / clone-agent time)

1. Seed `ic50_assistant` from `autofit_assistant` structure (AGENTS.md, skills/,
   wiki/, config), stripping autofit-specific domain content.
2. IC50 domain wiki: gather relevant IC50 / dose-response / pharmacology-fitting
   papers into the assistant's literature wiki as training context.
3. Wire the assistant to the `ic50_workspace` scripts/datasets (simulated + real),
   which are assumed statistically/functionally correct.
4. Demonstrations the assistant must support:
   - recover input solutions on simulated datasets;
   - graphical/EP fits on simulated data showing EP scaling with dataset count;
   - graphical/EP fits on real datasets showing the same scaling;
   - comparison vs random forest / other workspace methods (information extracted).
5. RAL/HPC: ensure all of the above runs on RAL via the HPC link (see
   `ic50_workspace/hpc/` + the AGENTS.md HPC-access section).

## Downstream (out of scope for this prompt, noted for sequencing)

- Later: convert `ic50_workspace` into a standalone **closed** GitHub science
  project repo. File as a separate follow-up prompt when the assistant is in place.
