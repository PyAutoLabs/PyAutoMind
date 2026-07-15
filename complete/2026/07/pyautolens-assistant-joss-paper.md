## pyautolens-assistant-joss-paper (JOSS paper #2 scaffolded next to the software — SHIPPED)
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/69 (CLOSED)
- completed: 2026-07-15
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/71 — MERGED (fa1aaa6, merge commit 3b5349f). wiki-currency CI green.
- summary: created `autolens_assistant/paper/` (paper.md 1309 words, paper.bib, README.md, .gitignore), mirroring the `PyAutoLens/paper_jax/` sibling. The author's four drafted sections (Summary / Statement of need / software design / benchmarks) existed ONLY inside the Mind prompt file — this consolidated them into a real manuscript. Title: "PyAutoLens-Assistant: Using Natural Language and AI to Analyse Gravitational Lenses".
- unblocked: had sat in planned.md since 2026-07-14 blocked-by benchmark-calibration (#59) holding the autolens_assistant repo claim. #59 closed → claim released → shipped from its own worktree. The block was recorded as an issue comment, which is where the resume context lived.
- bibliography provenance (REUSABLE PATTERN): extracted all 6 entries VERBATIM from `wiki/literature/bibliography/autolens_literature.bib` (1037 entries) via a brace-matching python extractor, rather than writing bib entries from memory. Fabricated/mistyped citations are the one failure mode a paper cannot absorb, and the repo already had verified entries. Cited: Nightingale2021 (PyAutoLens JOSS), Casey2023 (COSMOS-Web), EuclidCollaboration2025 (Q1 lensing), LSSTDarkEnergyScienceCollaboration2012, Vegetti2010 + Minor2021 (SDSSJ0946+1006 subhalo + high-concentration claim).
- decisions: benchmarks framed "three representative examples" (repo ships 4 prompts; hard_group_multi deliberately undescribed — author chose reframe over a 4th paragraph; framing recorded in paper/README.md so prose+prompt set can't drift). Author block mirrors the JAX paper (sole corresponding author). Renamed SLACS0946+1006 → SDSSJ0946+1006 to match the cited papers + the literature wiki.
- contract deviations (both surfaced, both evidence-backed): (1) NO pending-release label — it does not exist on autolens_assistant, ensure_workspace_labels.sh does not cover the repo, and PRs #70/#68/#66 all merged unlabelled. It guards the library-first merge gate, meaningless for a docs-only PR with no upstream library PR. Creating it would have invented a convention. (2) NO smoke tests — ship_workspace's smoke step assumes a workspace repo with scripts/; this repo has none and the change touches no code. Ran the repo's OWN gates instead: `make validate-literature-citations` + `audit_skill_apis.py`.
- verified: citations resolve 1:1 (6 cited / 6 defined / 0 missing / 0 unused); body 1309 words inside JOSS 750-1750; YAML front-matter parses with all required keys; audit 58 files/120 symbols/0 broken. NOT verified: Inara PDF build (docker not installed locally) — left unchecked on the PR Test Plan rather than claimed.
- trap avoided: `audit_skill_apis.py` writes a dated report to `autoassistant/audit/` as a side effect, which `git add -A` would sweep up — already gitignored (.gitignore:30), commit stayed clean. See [[feedback_ship_workspace_binary_leak]].
- heart: shipped at YELLOW score 55 (no RED), author-acknowledged; both reasons ("workspace validation not passing (3 failed, 2026-07-09)"; "58 stale parked script(s)") pre-date the branch and are unrelated to a docs-only change. Ack recorded verbatim on the issue + in active.md.
- OPEN / needs author: `State of the field` + `Research impact statement` are commented stubs (JOSS requires both; neither draftable without author judgement). Benchmark-results prose stays FUTURE-TENSE because benchmarks/RESULTS.md records ZERO runs for all 4 benchmarks — despite #59 (first calibration campaign) being CLOSED. Either results exist un-ingested or the campaign closed without producing them; worth a look before submission.

## Original prompt

# Set up the PyAutoLens-Assistant JOSS paper

Type: docs
Target: autolens_assistant
Repos:
- autolens_assistant
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Request

Create a current-format JOSS paper template for PyAutoLens-Assistant with the
title:

> PyAutoLens-Assistant: Using Natural Language and AI to Analyse Gravitational Lenses

Place the manuscript in the `autolens_assistant` repository so that the JOSS
paper is hosted with the software it describes. Preserve all existing assistant
content and benchmark outputs.

## Summary draft supplied by the author

### Summary

Stage IV weak-lensing surveys, such as Euclid and the Vera C. Rubin Observatory, are measuring increasingly large samples of galaxies, while strong-lensing searches are discovering rapidly growing numbers of galaxy-, group-, and cluster-scale lenses. These systems are observed through optical and infrared imaging, radio interferometry, point-source measurements of lensed quasars and supernovae, and weak-lensing shear catalogues, enabling studies of cosmology, dark matter, galaxy formation, and the early Universe. Mature open-source software such as PyAutoLens supports simulations, lensing calculations, and strong- and weak-lensing modelling across these datasets, but constructing a bespoke analysis can still require substantial effort to locate, adapt, and combine the relevant examples using the correct Python API and syntax.

PyAutoLens-Assistant allows scientists to use natural language to describe the gravitational-lens analysis they want to perform. It provides a domain-specific interface to the documented and tested capabilities of PyAutoLens, supporting simulations, ray-tracing calculations, probabilistic modelling, data preparation, result interpretation, and visualization. Researchers can use it through a conversational AI assistant, such as ChatGPT, to ask questions and develop workflows interactively, or through agentic coding tools, such as Claude Code or Codex, which can inspect data, write and execute scripts, diagnose errors, analyse outputs, and iteratively refine an analysis. PyAutoLens-Assistant is grounded in curated, version-controlled documentation, examples, scientific reference material, and task-specific instructions, and produces explicit Python code and inspectable analysis products.

## Statement of need draft supplied by the author

### Statement of Need

Experienced PyAutoLens users often know exactly which scientific analysis they want to perform, but implementing it still requires substantial time assembling the appropriate Python workflow. An expert can quickly specify: “Perform multi-wavelength lens modelling of the F115W, F150W, F277W, and F444W JWST imaging of the COSMOS-Web Ring using a multi-Gaussian expansion lens-light model, a singular isothermal ellipsoid plus external shear mass model, and a Delaunay pixelized source reconstruction.” Translating this concise scientific specification into executable code requires locating and combining several examples, loading and configuring each dataset, composing the model components with the correct API, and adapting the workflow to the system being analysed. As models incorporate more datasets, cluster-scale mass distributions, or joint strong- and weak-lensing constraints, this implementation burden increases even when the underlying scientific choices are already clear. PyAutoLens-Assistant reduces this overhead by translating natural-language specifications into explicit, executable, and reproducible PyAutoLens workflows.

New users face a complementary challenge: they may not yet know which modelling approach, software abstractions, or examples are appropriate for the task they are learning. PyAutoLens has grown from galaxy-scale imaging analyses to support point-source lenses, group- and cluster-scale systems, weak lensing, interferometry, simulations, and joint analyses, accompanied by well over one hundred worked examples across the autolens_workspace. Navigating this material while simultaneously learning gravitational-lensing science, Bayesian inference, and the PyAutoLens API can be overwhelming. PyAutoLens-Assistant enables users to describe their immediate goal in natural language and receive targeted explanations, example code, and pointers to the relevant documentation. Its teaching mode also explains the underlying science and numerical methods, encourages follow-up questions, and supports learning rather than simply returning code.

## Software design draft supplied by the author

### How It Works

PyAutoLens-Assistant is a version-controlled knowledge and workflow layer that enables general-purpose AI systems to use PyAutoLens reliably. Its architecture separates three components: instructions define assistant behaviour, skills describe how to perform specific tasks, and wiki pages provide the underlying technical and scientific knowledge. For a given request, the assistant selects the relevant skill, consults the associated wiki material, and adapts tested examples from the `autolens_workspace` rather than generating PyAutoLens code from memory. Generated scripts follow the established workspace structure and can be checked against the installed API, reducing the risk of outdated or invented syntax.

Two reference wikis provide complementary context. The core wiki organizes the PyAutoLens API, modelling concepts, datasets, inference methods, and operational guidance, linking these to procedural skills and relevant workspace examples. The literature wiki provides scientific context through pages on lensing concepts, named surveys and systems, and bibliographies of published papers. Users can also ingest papers relevant to a project, after which they become part of the assistant’s persistent scientific context.

PyAutoLens-Assistant can be used through a browser-based conversational assistant or a local agentic coding tool. For systems such as ChatGPT or Claude, `llms.txt` acts as the machine-readable entry point: it asks the assistant to verify repository access and directs it through the canonical read order of instructions, skills, relevant wiki pages, and runnable workspace examples. In this mode, users can ask questions, receive scientific explanations, locate examples, interpret errors and figures, and generate draft end-to-end scripts, although the assistant cannot normally inspect local files or execute code.

For full computational workflows, PyAutoLens-Assistant can instead be used with agentic tools such as Claude Code or Codex. These tools load the repository instructions directly and can inspect datasets, write and run scripts, generate diagnostic plots, debug failures, and iteratively refine an analysis. The resulting Python code, configuration, outputs, and modelling decisions remain explicit and inspectable.

The assistant operates in two interaction modes. **Assistant mode** is intended for users who want a task completed efficiently, with concise explanations and support ranging from interactive coding to phased end-to-end analysis. **Teacher mode** prioritizes learning by explaining what each stage does and why, making assumptions explicit, and directing users to relevant documentation and examples. Both modes use the same scientific capabilities, reproducibility requirements, and safety checks.

For agentic work, each analysis can be stored in a separate project repository containing its data, configuration, scripts, results, and project journal. This separates the shared assistant knowledge base from the scientific project while preserving a complete record that can be shared with collaborators or released alongside a publication.

## Benchmark examples draft supplied by the author

### Benchmark Examples

PyAutoLens-Assistant is evaluated using three frozen benchmark prompts distributed with the repository. These represent progressively more demanding scientific workflows and are run using multiple conversational and agentic AI systems. Each benchmark records the full interaction, generated code, executed analysis where applicable, scientific outputs, and a rubric-based score, enabling direct comparison between different models, tools, and interaction modes.

The first benchmark uses **Teacher mode** to simulate Euclid-like imaging of a simple strong lens, fit the simulated data, and recover the lens model. The assistant must explain the purpose of each stage, including model composition, simulation, masking, non-linear inference, and interpretation of the recovered parameters. This benchmark tests whether the assistant can provide scientifically accurate guidance while helping a new user understand an end-to-end PyAutoLens workflow.

The second benchmark uses **Assistant mode** to model JWST imaging of the COSMOS-Web Ring. The assistant must inspect the supplied dataset, perform the required data-preparation steps, construct an appropriate lens-light and mass model with a pixelized source reconstruction, run the analysis, and present the reconstructed source and fit residuals. This benchmark tests the assistant’s ability to convert a concise scientific request into a complete and reproducible modelling workflow with limited user intervention.

The third benchmark requests a more autonomous analysis of the strong lens SLACS0946+1006. The assistant must reproduce a reported dark-matter subhalo detection through Bayesian model comparison, compare alternative subhalo mass profiles, preserve all intermediate models and results for inspection, and determine whether the analysis should run locally or on high-performance computing resources. This benchmark tests long-horizon planning, scientific decision-making, project-state management, and the ability to execute a complex analysis across multiple stages.

The benchmark suite is run across different AI systems and access modes, including browser-based conversational assistants and local agentic coding tools. Results will be reported using metrics such as task completion, scientific correctness, API validity, reproducibility, degree of autonomy, number of user interventions, wall-clock time, and computational cost. Together, the benchmarks test the two principal use cases of PyAutoLens-Assistant: teaching new users how to perform gravitational-lens analyses and enabling experienced users to execute complex workflows efficiently from natural-language specifications.

### Drafting note

The repository currently contains four frozen benchmark prompts. Before publication, either add the omitted `hard_group_multi.md` benchmark to this section or reframe these as three selected benchmark examples.

## Original request verbatim

> ok, the second paper is PyAutoLens-Assistant and its title is PyAutoLens-Assistant: Using Natural Language and AI to Analyse Gravitational Lenses, make another JOSS paper and template
