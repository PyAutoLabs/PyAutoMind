# Reusable style resource for scientific Python tutorials

Issued: 2026-10-24

Create a canonical, callable @PyAutoBrain resource for editing Python script and
notebook documentation in the style established by the first AI COSMOS Ring
example. Decide whether this should extend the existing `/docs` entry point,
become a documentation agent or faculty, or live as a reusable skill/reference,
then wire the smallest coherent public surface without duplicating the existing
README/setup-page writing guidance.

## Request (verbatim)

> This prompt describes the tone and style we hit when we made a good update to a python script / notebook documentation, in particular the first-AI-COSMOS-Ring example, can you turn this into a go to callable resource? Maybe use a skill but I think it could be part of PyAutoBrain as an agent or as part of its docs agent or something, which I think recently also got a github README.md style update: 
> Aim for the tone of a knowledgeable person guiding someone through a picture or experiment: direct, patient and precise, without sounding formal, promotional or childish.
>
> Writing principles:
> - Use plain language and short, connected paragraphs.
> - Start with what the reader can see or do, then explain what it means.
> - Introduce each technical term only when it becomes useful. Explain it in everyday language at first use.
> - Prefer concrete descriptions: “50 smooth ellipses”, “the light left after subtracting the foreground galaxy”, “small differences consistent with noise”.
> - Keep the science accurate. Simplify the explanation, not the underlying meaning.
> - Avoid jargon about implementation when it does not help the reader understand the science.
> - Avoid vague or distracting words such as “blob”, “speckles”, “payoff” and “headline number”.
> - Avoid hype, rhetorical questions, forced analogies and repeated reassurance.
> - Use British English.
>
> For each section:
> 1. Orient the reader to the image, question or task.
> 2. Explain the relevant idea and why it matters.
> 3. Say what running the next code cell will do.
> 4. Explain what to look for in the output and how to interpret it.
>
> For code:
> - Keep the narrative focused on the scientific purpose.
> - Put incidental implementation details in concise Python comments.
> - When appropriate, tell readers which settings they can change and which they can leave alone.
> - For experiments, explain the starting values, suggest specific changes, describe the expected effect and provide a clear way to reset.
> - Distinguish loading or evaluating an existing model from fitting a new one.
>
> Preserve important distinctions:
> - Subtracting a foreground galaxy’s light is different from undoing the gravitational bending of the source’s light.
> - A reconstruction is inferred from a model; it is not a direct photograph.
> - A plausible measurement does not establish that a model fits well.
> - A single best model does not by itself describe uncertainty.
> - Attribute figures, data and models to their actual sources.
>
> Adapt to the audience:
> - For introductory tutorials, introduce fewer concepts and keep numerical methods out of the main narrative.
> - For advanced tutorials, retain the necessary technical detail but explain its purpose before its mechanics.
> - Do not remove useful detail merely to make the prose shorter.
>
> Editing boundaries:
> - Preserve scientific claims, numerical values, code behaviour, links, citations and required formatting unless I explicitly authorise changes.
> - Flag scientific inaccuracies or misleading wording rather than silently preserving or replacing them.
> - Do not invent provenance, results, performance claims or certainty.
> - Respect any protected text blocks byte-for-byte.
>
> Work iteratively:
> - Review one coherent block at a time.
> - Show proposed wording and briefly explain only the significant changes.
> - Wait for my feedback before applying it.
> - Carry agreed terminology and tone forward consistently.
> - Edit canonical source files rather than generated notebooks or documentation, then run the project’s required regeneration and validation steps.
>
> Ask AI / Gemini:
>
> - At opportune moments in the example or tutorial, put an "Ask AI / Gemini:" thing in bold font with a suggested follow up
> question the reader can ask the AI.

## Intended outcome

- A single callable entry point for tutorial/script/notebook documentation work.
- The supplied guidance is canonical and automatically consulted by that entry point.
- README/setup-page prose continues to use the existing people-facing writing
  guide; tutorial science narrative uses the new guidance, with shared rules
  linked rather than copied.
- The iterative review/apply boundary remains explicit and is not weakened by
  the general development workflow.
- Tests or validation cover command discovery and any generated agent/skill
  surfaces that change.

## Follow-up decisions (2026-10-24)

- The human approved the skill-based architecture: `/docs` remains the callable
  entry point, backed by a new canonical tutorial-writing guide rather than a
  new Brain conductor or faculty.
- Every notebook uses the single callout label `**🤖 Ask AI:**`; do not use a
  Gemini-specific variant.
- Include the established notebook-source format in the guidance: an opening
  `__Contents__` list and top-level `"""__Section__"""` narrative docstrings,
  pointing to the existing canonical format rather than copying a competing
  template.
- Approved branch: `feature/tutorial-documentation-style`.
- The older unregistered PyAutoBrain worktree on
  `feature/pyautodna-stack-management` is acknowledged and must remain
  untouched.
