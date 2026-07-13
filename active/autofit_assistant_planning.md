# autofit_assistant planning — generic inference wiki + content migration

Type: research
Target: autofit_assistant
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Intent

An `autofit_assistant` repo will ultimately be created, following the
`autolens_assistant` pattern: a generic, public, stripped-of-personal-content
template with its own wiki. This prompt is the planning anchor for it, and
holds migration notes until the repo exists.

## Migration notes (content that moves to the generic wiki when it is made)

The following inference-methods content currently lives in the personal
`PyAutoMemory/methods_wiki/` and should be migrated (as public, generalised
rewrites — PyAutoMemory itself is personal and must never be referenced from
public repos):

1. **Expectation propagation** — the
   `methods_wiki/concepts/expectation-propagation.md` page being produced by
   Phase 1 of `research/graphical_ep/ep_framework_review.md` (formal EP
   equations as PyAutoFit implements them, moment matching, damping,
   pitfalls/findings).
2. **Searches / samplers wiki stuff**:
   - `methods_wiki/concepts/nested-sampling.md`
   - `methods_wiki/concepts/sampler-benchmarks.md`
   - `methods_wiki/concepts/hamiltonian-monte-carlo.md`
   - `methods_wiki/concepts/gpu-nested-sampling.md`
   - `methods_wiki/concepts/initialization-chaining.md`
   - `methods_wiki/sources/samplers.md` (source notes; strip personal
     reading-log framing)
   - related general pages as judged at migration time
     (`concepts/bayesian-inference.md`, `sources/bayesian-inference.md`,
     `sources/probabilistic-programming.md`)

Migration means: rewrite for a generic PyAutoFit user (no personal project
context, no PyAutoMemory links), keep the personal originals in PyAutoMemory
as the private superset.

## Planning scope (when this prompt is picked up)

- Decide repo layout by cloning the `autolens_assistant` template structure
  (`AGENTS.md`, `skills/`, `wiki/core|literature|project`).
- Decide which PyAutoFit demos ship as the assistant's worked examples
  (analogue of cosmos_web_ring / slacs0946 in autolens_assistant).
- Define the wiki's core page set: model composition, priors, searches,
  graphical/EP, result analysis.
- Sequence: do not start until the EP framework review
  (`research/graphical_ep/ep_framework_review.md`) has produced the Phase 1/2
  write-ups, since those seed the wiki's inference pages.
