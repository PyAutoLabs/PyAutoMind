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

## Original request verbatim

> ok, the second paper is PyAutoLens-Assistant and its title is PyAutoLens-Assistant: Using Natural Language and AI to Analyse Gravitational Lenses, make another JOSS paper and template
