# Setup-oriented inference evidence and navigation

Type: feature
Target: pyautoinsight
Repos: PyAutoInsight, autolens_inference, autolens_assistant, PyAutoMemory
Difficulty: too-large
Consequence: judge
Autonomy: human-required
Priority: high
Filed: 2026-10-08

## Approved direction

Human approved the researched five-phase design and then said "ok begin".
This umbrella records intent; bounded phase prompts each own an issue and PR.
No compute, scientific baseline acceptance, release or merge is authorized.
Tier: judge — merge mode: human /prm.

1. PyAutoInsight: versioned setup and baseline-to-experiment read contract,
   reader compatibility, validation and tests. Ship reader before producer.
2. autolens_inference: catalogue/exporter, reproducible baseline-stage references,
   setup-oriented leaves (scripts/imaging/delaunay/baseline_slam.py and sampler
   leaves), shared model construction, updated path-based wall budgeting and
   driver references. Preserve original evidence/output identities and archives.
3. PyAutoInsight: Pulse-style project → dataset family → model/setup navigation;
   setup pages open in new tabs, key baseline/evidence information at top,
   sampler disclosures, filtered history/comparisons below. Adopt shared sizing,
   imagery, prompt/copy and table conventions; verify responsive presentation.
4. Project setup wiki summaries and autolens_assistant lookup against pinned
   machine-readable evidence; exact/approximate/absent matches and qualified
   runtime/reliability advice. Retain cross-cutting campaign/Cortex history.
5. PyAutoMemory literature pairing and Insight sampler-candidate section with
   verified public sources, expected applications, limitations, implementation
   and trial status, copyable investigation prompts. Publish curated public
   summaries, never private Memory references.

Coordinate contract adoption with the existing search-extensibility epic's
autofit_inference B2/B3 work, without claiming or duplicating that harness.

## Contract decisions approved in conversation

- Stable setup IDs independent of script paths; dataset family/model/instrument
  are navigation facets, exact dataset/model/prior identities remain explicit.
- SLaM baseline prepares inherited model/prior/adapt products and supplies
  reviewed reference likelihood, parameters and posterior evidence. Completed
  execution alone is not scientific acceptance.
- Experiments reference an exact baseline run and stage (currently mass_total[1]),
  prepared artifacts, protocol and provenance; compare recovery and posterior
  diagnostics as well as cost. Maximum likelihood alone is insufficient.
- Cold sampler start: baseline-prepared problem, no posterior/best-fit reuse for
  sampler initialization. Warm start: explicit reused positions/samples/covariance
  or other state and source run. Resume: separate checkpoint-continuation mode.
- Sampler initialization is separate from JIT compilation and cache warmth.
  Record initialization/preparation costs separately from sampling, with clock
  definitions; unknown is not zero. Compare like-for-like starts by default.
- Count likelihood evaluations, iterations, retained samples and ESS separately;
  retain seeds, failure cases, hardware, precision and measured revisions.
- Historical unknowns remain unknown; archived runs are never silently promoted
  to current reference evidence. Do not rewrite source result provenance.

## Original request (verbatim)

- The formatting and structure updates should match PyAutoPulse, which includes making the prompt at the topnext to a 
icon for copying, making the format match size of other dashbaords, sort out image on dashboard, similar work on the table.

- I think we want to do the same clickable drop down style, so again first clickable dorp down is "autolens",
then we pick from the options in the scripts folder (e.g. imaging, interferometer), meaning as a user weve chosen
our dataset (more intuitive). I think for imaging and interferometer the next
click should be the type of likelihood function we want to look at results for (e.g. delaunay, rectangular, mge). This
would then bring up all relevent information for that setup, for example if I click delaunay I can see its summary
information for the baseline search in a SLam run in mass[1] using Nautilus with key summary information. I can then be
like "ok so for Deluanay I should expect 20000 iterations and a clock time of 2 hours on CPU". The drop down menu
would then have all samplers that have run (e.g. SMC, NUTS). I guess any other infor on that sampler would then be displayed
in there, this means the huge "Historical project results" section which is way too information dense is now easier to
digest as it shows once the user has chosen the setup they are investigating. Same for "Comparisons and parity groups"

At this point, one is left wondering if we need a _inference refactor, as the above design would be scripts/imaging/delaunay/nautilus.py (for example)
whereas currently we have scripts/imaging/searches. I think this would be an ok sized endeavor, but I think it would be worth it
as it means in the long term the repo navgiation matches what to me feels most intuitive. This is also closer to how autolens_workspace is packaged
with features in dediciated folders. I suspect this would then lead a redesign and refactor of the research wikis, campaigns etc, but I think this makes
obvious sense as a large scale refactor. Give me your opinion after reseaerching this. This mirrors what we have done recently on PyAutoPulse.
I think that for each setup (E.g. imaging/delaunay) we always have a baseline_slam.py file which does the main SLaM (e.g. what son workspace),
which will give us the models set up and baseline results (noting that sometimes its on CPU, or A100, other other GPU). search investigations
will then extend from that, so after baseline has run we may extend mass[1] to use SMC, NUTS, etc so each file in this folder would be like
smc.py, nuts.py. I think this is an ok design for now,I think we will need to extend it sooner or later but this feels more extensible.

The other long term goal of _inference repos is for the autolens_assistant (or other assistant) to read them and give the user a recommended setup
in terms of mdoel (E.g. if the model has 50 parameters use a gradient thing, maybe nautilus is ok for 10 parameters) and an estimate of number of
iterationsrun time. I think that having the structure above is probably more conducive for this, as the assistant will know what its dataset and model 
is and then just need to find the right folder on the repo, and can access all the key information within (e.g. different serarches).

I want this to have a pair with PyAutoMemory, whereby PyAutoMemory looks for papers which are samplers or searches
which could be added to PyAuto and PyAutoInsight should have a tab section with all of these and prompts to add them,
with a bit of research as to where their expected strength or use would be.

Many formatting improvements has been made across dashboards and in PyAutoPulse since wrtiign the above. In particular,
PyAutoPulse is now an even better model for how PyAutoInsight should navigate, including clicks taking one to a
new tab when you go to a page with search information and how to put key information at the top of that page
with drop downs for more detailed information further down.

## Follow-up requests (verbatim)

Sounds good, i like this **baseline-to-experiment contract** as I agree we will run baseline to get results (e.g. max likelihood value and parameters) we trust and then would often just run samplers on mass[1] to see if any sample faster but we need that baseline to be sure they are right. It makes sense SLaM is baseline, as we often need adapt images and stuff set up.

ok thats all good, remember also we need to distinguish between cold start and warm start for samplers which I guess also is part of the contract

ok begin

## Phase 1 handoff — 2026-10-08

Reader contract implemented in Insight PR14 (issue13), commit 4f8eaec.
157 tests, Ruff and offline check pass; hosted lint/refresh pending at handoff.
Phase 1 merged via human /prm. Continue producer/catalogue/script migration. The live registry
remains v1. No baseline scientific acceptance or runs were performed.
Bounded prompt: complete/2026/10/inference-setup-contract.md. Full scope remains the five
approved phases above; at that initial handoff only phase1 had been implemented.

## Continuing authorization — 2026-10-08

Human: "prm, and continue through all phases autonomously to the end".
This grants implementation and in-turn merge/close-out of the approved remaining
phases when their tests, independent review and CI pass. No compute/release or
scientific acceptance is authorized. Preserve Heart gates and data products.

## Implementation status — 2026-10-08

- Phase1 contract: complete/2026/10/inference-setup-contract.md (Insight#14 merged).
- Phase2 producer: complete/2026/10/inference-setup-producer.md (autolens_inference#21 merged de37acfe). Catalogue preserves56historical records across11setups; zero existing prepared problems and no accepted baseline. Future verified baseline export and sampler investigation are implemented.
- Phase3 browser: active/inference_setup_browser.md (Insight#16 awaiting merge on77e4d21). Captured producer de37acfe;168tests and fixture/actual-producer Chromium checks; independent CLEAN. Root must confirm merge and live deployment before completion.
- Phase4 assistant advice: complete/2026/10/inference-setup-advice.md (autolens_assistant#158 merged cea768a). Pinned lookup, immutable citations and qualified matches;252tests/1skip and36focused tests, independent CLEAN.
- Phase5a literature/curation: complete/2026/10/inference-sampler-literature.md (Memory#125 merged13499c3). Public-source candidates and on-demand curation guidance; no installation, compute or benchmark. Prerequisite complete/2026/10/memory-board-header-contract.md (Memory#127 merged).
- Phase5b public candidate publication is included in the pending browser work and remains unclosed until merge/deployment evidence is confirmed.

No new scientific acceptance or sampler promotion; Heart STALE rehearsal gap remains explicit. Worktrees are retained under root's coordination instruction pending reviewer/dependency cleanup.
