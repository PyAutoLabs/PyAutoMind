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

Stage IV weak-lensing surveys, such as Euclid and the Vera C. Rubin Observatory, are delivering measurements for increasingly large samples of galaxies, while strong-lensing searches are identifying rapidly growing numbers of galaxy-, group-, and cluster-scale lenses. These systems are observed using diverse datasets, including optical and infrared imaging, radio interferometry, point-source measurements of lensed quasars and supernovae, and weak-lensing shear catalogues. Together, these observations enable studies of cosmology, dark matter, galaxy formation, and the early Universe. Software packages such as PyAutoLens provide mature, well-documented, open-source tools for performing these analyses, but constructing a bespoke analysis from their many examples and capabilities can remain time-consuming.

PyAutoLens-Assistant allows scientists to use natural language to describe the gravitational-lens analysis they want to perform, reducing the time required to translate scientific goals into working and reproducible software. It provides a domain-specific interface to the documented and tested capabilities of PyAutoLens, supporting simulations, ray-tracing calculations, probabilistic modelling, strong- and weak-lensing analysis, result interpretation, and visualization. The assistant can be used through a conversational AI interface, such as ChatGPT, to answer questions and develop workflows interactively, or through agentic coding tools, such as Claude Code or Codex, that inspect data, write and execute scripts, diagnose errors, analyse outputs, and iteratively refine an analysis. It is grounded in curated, version-controlled documentation, examples, scientific reference material, and task-specific instructions, and produces explicit Python code and inspectable analysis products.

## Original request verbatim

> ok, the second paper is PyAutoLens-Assistant and its title is PyAutoLens-Assistant: Using Natural Language and AI to Analyse Gravitational Lenses, make another JOSS paper and template
