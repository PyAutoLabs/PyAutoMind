# Abell 1201 guided SMBH demonstration and Gemini Colab follow-on

Type: feature
Target: workspaces
Repos:
- autolens_assistant
Difficulty: large
Autonomy: supervised
Priority: normal
Memory: wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md; wiki/galaxies/sources/massive-ellipticals.md
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-input


## Current scope — mobile handoff, 2026-09-20

This section supersedes the earlier inference-first acceptance criteria and the
previous prohibition on showing a model without a black hole. Historical requests
below are retained for traceability. The deliverable is a guided demonstration
in @autolens_assistant plus a Google Colab notebook with a Gemini-led, opt-in
measurement extension. No new library API is planned.

Latest user request (verbatim):
> ok, can we add abell_1201 to the autolens_profiling repo dataset folder, and then come up with a plan which I will hand off to mobile in a bit. The plan overall that exists is good but these are additional requirements: 1) I dont want the example to perform inference, at least not to the point that the user gets a measurements. I think we would probably have the user be exposed to two models, one without a SMBH and one with it, which we have "tuned" from preivous inference, and the AI takes them through the two. The end point of the guide could be then to encourage them to do inference thereafter. 2) I would like there to also be a Google colab notebook with this, which encourages the user to measure the SMBH mass with Gemini to illustrate the ntural language aspect.

### High-level plan

1. Establish the data provenance and retrieve two previously inferred, tuned
   model snapshots: without an SMBH and with an SMBH.
2. Build a short, conversational tour of the observed image, each model's
   prediction and residuals, and the central region that distinguishes them.
3. Keep the tour at fixed parameters: no sampler, posterior, fresh mass
   measurement or uncertainty estimate. End by inviting the user to try inference.
4. Provide a Colab notebook containing the same tour, then an explicit opt-in
   Gemini-assisted SMBH mass measurement exercise with natural-language prompts.
5. Retain the website image work: a faithful, attractive data image with caption,
   alt text and provenance, ready for a separately approved website update.
6. Validate the tour from a clean checkout and the notebook in a fresh Colab
   runtime; record evidence separately for the tour and measurement extension.

### Phase 1 — data and fixed reference models

Completed locally during planning:
- Copied all 40 files (29,847,119 bytes) from
  `autolens_assistant/dataset/abell_1201/` to
  `autolens_profiling/dataset/abell_1201/`.
- Verified every copied file byte-for-byte using SHA-256. Both F390W and F814W
  trees, auxiliary images, masks and positions are preserved unchanged.
- Data publication follow-up: all 40 files are committed in `autolens_profiling`
  on branch `codex/abell-1201-data`, commit
  `9a65b1ea58269274984040f028b7ed3ef2d63108`. This explicitly stages the ignored
  files; the source assistant directory remains untracked. Data bytes are unchanged.
- Dataset: https://github.com/PyAutoLabs/autolens_profiling/tree/9a65b1ea58269274984040f028b7ed3ef2d63108/dataset/abell_1201
- From an existing profiling checkout, fetch the branch with
  `git fetch origin codex/abell-1201-data`. Read or export
  `dataset/abell_1201/` from the pinned commit, without changing the current
  source branch. Alternatively clone with
  `git clone --single-branch --branch codex/abell-1201-data https://github.com/PyAutoLabs/autolens_profiling.git`.
  With GitHub tools, read files at that commit/ref. Do not assume main has the data.

Implementation:
- Inspect the variants before selecting inputs: there are original, scaled,
  padded and lens-light-subtracted images plus different noise products. Do not
  silently pick a variant or treat all image/noise pairs as interchangeable.
- Prepare `dataset/abell_1201/README.md` and a machine-readable manifest with
  selected image/noise/PSF/mask filenames, checksums, filter, units, pixel scale,
  coordinate conventions, redshifts, preprocessing and data provenance.
- Agree a stable, versioned public download or deliberately tracked data bundle
  for the assistant and Colab, with redistribution terms and checksum validation.
  Preserve the requested profiling copy; user-facing code belongs in the assistant.
- Retrieve the actual previous inference outputs or scientist-approved parameter
  exports for BOTH models. Record model family, parameters, source treatment,
  dataset variant, mask, original run/paper and software version in proposed
  `examples/abell_1201/models/{without_smbh,with_smbh}.json` plus provenance.
  These are proposed paths; confirm against repo conventions at implementation.
- Do not manufacture a no-SMBH best fit by zeroing the SMBH in the other model.
  Any such perturbation must be separately labelled as an illustration.
- Plot and inspect the real data with the scientist; confirm contaminant handling
  and mask extent before composing fit evaluations. Parameter values, band choice
  and preprocessing remain open until the reference material is identified.

### Phase 2 — assistant-guided fixed-model tour

Proposed files: `examples/abell_1201/README.md`,
`scripts/abell_1201/guided_demo.py`, `skills/al_abell_1201_tour.md`, and the
matching entry in `skills/README.md` / generated discovery adapters.

- Opening prompt: "Guide me through Abell 1201 using the two prepared lens
  models, without and with a central supermassive black hole. Show me what
  changes in the images and residuals, without running inference."
- Stages: inspect data and mask; explain strong lensing and the counter-image;
  show the tuned no-SMBH model; show the tuned SMBH model; compare observations,
  predictions and residuals with matched scales and central-region zooms.
- Explain which parameters were inferred previously and what each plot shows.
  A stored SMBH mass is a reference-model input, never a newly measured result.
- Prefer stored source solutions or fixed forward calculations. If a linear
  source reconstruction is unavoidable, disclose that conditional solve and
  demonstrate that it does not estimate SMBH mass or launch a non-linear search.
- Avoid Bayes factors, detection-significance claims or claims to reproduce the
  full discovery. Explain the role of assumptions and limitations of two snapshots.
- End with a natural-language invitation to measure the mass, linking Colab.
- Keep the guided teaching flow separate from the existing one-shot benchmark
  protocol. Optional automated checks can verify deterministic outputs; a new
  full inference benchmark is deferred, not an acceptance gate for this tour.

### Phase 3 — Colab and Gemini measurement extension

Proposed notebook: `notebooks/abell_1201.ipynb`, generated from the established
notebook source format if the owning repo provides one. Add an Open in Colab
link to the tour and assistant README. Keep the notebook and tour on the same
versioned data/model assets and supported PyAutoLens environment.

- The main notebook runs the fixed-model tour without inference, including
  when the reader chooses Run all. The measurement extension needs an explicit
  opt-in control whose default is off.
- Add short, copyable Gemini prompts that ask it to explain the data, compare
  fixed models, describe the measurement plan, help configure and run inference,
  and interpret convergence, residuals and mass uncertainty after a valid run.
- Ground generated code in the notebook's installed API and supplied examples.
  Verify current Colab Gemini access/UI and account availability during authoring;
  do not promise universal access or an undocumented integration.
- Present the extension as a real measurement exercise. Specify mass prior,
  point-mass unit conversion, position treatment and fixed/free nuisance
  parameters from the reference setup. If conditioning on fixed parameters,
  explicitly label the resulting uncertainty as conditional.
- Provide runtime expectations, interruption/resume guidance and a small setup
  check. No fabricated posterior, uncertainty or success claim for a smoke run.
- Run a representative full extension only after agreeing compute budget. Keep
  the two validated states distinct: tour tested versus mass inference tested.

### Phase 4 — presentation and acceptance

Retain the original website-image follow-up below. Generate the image from the
verified telescope data, with a reproducible plotting script and display settings.
Website publication itself is outside this implementation plan.

Acceptance checks:
- A fresh checkout can obtain the versioned data and both reference models with
  matching checksums; each snapshot's prior-inference provenance is documented.
- The default guide executes without a sampler or a new SMBH measurement and
  produces finite, reproducible model/residual arrays and correctly labelled plots.
- Colab setup and the fixed tour execute in a fresh runtime; Run all does not
  start the optional inference. Links/assets resolve without local-only paths.
- The Gemini instructions are manually checked in Colab; availability limitations
  and any unexecuted full inference are recorded honestly.
- A completed inference exercise reports diagnostics and qualified mass/uncertainty;
  absence of a full run does not become a claimed measurement.

### Resume instructions and branch survey

Planning only: no issue created, no implementation claim made, no source or
notebook edited, no model fit or inference run. The data copy above is complete.
The revised implementation plan awaits review in the next session.

Survey on 2026-09-20: assistant main was at `18c353d` with untracked
`dataset/abell_1201/` and `scripts/cluster_model_composition.py`; existing worktree
`feature/mass-field-sibling-sweep` must be rechecked for overlap. Profiling main
was at `8789511`, clean apart from ignored datasets; existing profiling worktrees
include fixed-light-numba-s5, fixed-light-numba-s5b, hst-gpu-residue-p1 and
mass-field-profiling-live. Mind's primary checkout had unrelated changes and was
left intact; this handoff uses an isolated `codex/abell-1201-guide-plan` branch.
No matching Abell 1201 task was found in active/planned registries.

Brain's Feature Agent recommends workspace routing and phased execution. On
mobile, read this prompt, recheck claims and current branches, obtain approval
for the implementation plan, then use start-dev -> start-workspace with proposed
branch `feature/abell-1201-guided-tour`. Register/issue through Mind's existing
primitive; do not assume this draft claims the assistant repository. Readiness
and the normal ship-workspace gates apply when implementing/shipping.

The dataset is available from the pinned profiling commit above. The remaining
scientific dependency is the two previously tuned model exports; those have not
been identified or published by this handoff.

## Historical intake — superseded where it conflicts with current scope

Add an Abell 1201 central point-mass fitting benchmark to @autolens_assistant

Type: feature
Autonomy: supervised

Original user request (verbatim):
"2. It has not, but it has reproduced a similar dark matter analysis, maybe we should make the Abell 1201 prompt a benchmark and add it data to the repo, in which can intake that, I think its a great opening science prompt which isnt supported yet, but we should also make sure the prompt detail is good."

Context:
The personal website's Natural Language & AI draft currently illustrates reproducing James Nightingale's Abell 1201 black-hole analysis. The user confirms this has NOT yet been demonstrated by the assistant; a similar dark-matter analysis has been reproduced. This task enables a future evidence-backed showcase, not a claim of an existing result.

User scope correction (verbatim):
"Also make the intake prompt only fit th epoint mass, lets not do the whole model compaerison thing"

Scope (the correction above is authoritative):
- Inspect the existing benchmark protocol and science reference material before defining this benchmark.
- Identify the intended published Abell 1201 study, appropriate baseline lens/source model and reference point-mass results with the scientist; do not invent them.
- Add analysis-ready Abell 1201 data to the assistant repository, or its established data distribution mechanism if size requires it, with provenance, redistribution permission, units, pixel scales, noise maps, PSFs and required masks/configuration documented.
- Develop a concise public-facing opening prompt plus a frozen, scientifically explicit benchmark specification. Specify a single baseline model containing a central point mass, its priors, position treatment and necessary lens/source assumptions from the intended reference study. Explicitly distinguish fixed baseline parameters from any nuisance parameters needed for a valid point-mass uncertainty; do not expand into alternative model families. Define which choices the assistant must clarify with the scientist.
- Fit the central point mass representing the black hole and report its mass and uncertainty, with fit/residual diagnostics. No model without a black hole, evidence ratios, detection significance or model-comparison campaign. This benchmark does not claim to reproduce the full published analysis or establish the need for a black hole.
- Reuse the benchmark harness and record runnable commands, environment, compute requirements, scoring rubric, reference tolerances and failure criteria. Separate a cheap setup/smoke check from the full point-mass fitting run.
- Record full-run evidence before marking the point-mass fit validated or recommending a website claim. Avoid launching expensive compute during intake; agree budget at development time.
- Treat this as one coherent benchmark addition, not a library refactor or website edit.

Acceptance:
A new user can find the data and prerequisites, submit the documented prompt and follow an auditable workflow; the frozen benchmark measures the validity and reference agreement of the point-mass fit rather than merely successful execution. The public example asks for a point-mass fit, not reproduction of the entire discovery or model comparison. Missing data or unperformed full runs remain explicitly marked.

<!-- formalised by the Intake (Conception) Agent on 2026-09-19 from user-intake -->

## Website image follow-up

User request (verbatim):
"put imrpoving the image as an intake in autolens assistants task, then get this draft webpage live so I can review it"

As part of the same Abell 1201 demonstration, produce a more attractive,
scientifically faithful image for the Natural Language & AI webpage from the
original telescope data. The current placeholder is the Astrobites featured
image credited to Nightingale et al. (2023):
https://astrobites.org/wp-content/uploads/2023/04/Screen-Shot-2023-04-05-at-8.58.48-AM.png

Use a considered colour map, intensity stretch, framing and minimal labels
to make the lens and arc clear to public readers. Preserve real structures;
do not invent or remove astronomical features or imply the black hole is
directly visible. Keep the source data unchanged, save the plotting script
and display settings, and provide a web-ready export with alt text, a plain
language caption and source credit. Distinguish observed data from any model
output. This presentation work does not expand the point-mass benchmark into
model comparison.
