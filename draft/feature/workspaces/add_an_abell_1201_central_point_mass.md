# Add an Abell 1201 central point-mass fitting benchmark to @autolens_assistant

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
Unattended: ready

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
