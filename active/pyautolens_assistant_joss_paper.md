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

## Original request verbatim

> ok, the second paper is PyAutoLens-Assistant and its title is PyAutoLens-Assistant: Using Natural Language and AI to Analyse Gravitational Lenses, make another JOSS paper and template
