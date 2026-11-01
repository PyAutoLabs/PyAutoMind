# Chapters 2 and 3: recovered demonstrations and notebook prose

User requested recovery of genuine missing code based on the full tutorial audit, preserving intentional prose-only sections and standard narrative block structure.

## Shipped changes

- Lens Chapter2 Tutorial3 prints saved search timer durations (handles missing timing and explains resumed interruptions).
- Lens Chapter2 Tutorial6 now overlays image positions; retained results/performance lessons describe their actual behaviour.
- Lens Chapter3 Tutorial8 overlays image-mesh points, reports actual mesh counts, and restores a three-source compactness/reconstruction experiment inside the existing tutorial.
- Lens Chapter3 Tutorial11 uses Hilbert-fed Delaunay meshes, displays source meshes and actual evidence comparisons with saved baselines; controlled weight-power/floor experiments hold other fit settings fixed.
- Lens Chapter3 Tutorial12 displays true Constant/Adapt regularization weights and measured evidence rather than historical constants.
- Corrected stale deleted-tutorial references, unsupported claims of universal improvement, and weight-floor algorithm description.
- Galaxy Chapter3 Tutorial2 recovers12 prose lines lost when closing quotes shared their line.
- Chapters2/3 contiguous narrative stays in one string; Chapter3 prose wraps in Python editors. Notebooks generated canonically.

## Validation

Full-resolution actual inversion/plot executions passed for Lens Chapter3 tutorials8,11,12. Tutorial8's19 figures captured; compact-source residual/source figures visually checked. Saved-timer string/float/missing cases and actual image-position overlay checked. Independent advanced-example review completed and its weight-floor finding corrected.

Source/notebook parity across27 Python tutorials: all319 narrative blocks preserved and executable ASTs match, excluding deliberate generated setup. Generation: Lens44/44, Galaxy29/29. Navigator, terminal-section completeness, search-memory and diff whitespace checks passed.

## Scope boundaries

The separately planned new Chapter2 Data and Likelihoods/replacement chaining lessons remain unfinished. Intentional conceptual sections were not padded with invented code. No new lesson was added. Demonstration evidence values are measurements for the specified examples, not scientific validation of real lenses.

Heart STALE after clean library fast-forwards, solely release rehearsal absent. Development permitted; no release performed.

## Merge receipts
HowToLens#122 merged 5fe12eb22ccf46e7e8d39e1711c95241d4160ceb (head a9588b3102d889dfe8e2c545eddfd0237dc00aea).
HowToGalaxy#100 merged 79b6c5f684fd489a391d1a0f6daf5d16542ce55f (head f30d6778d0b840c8a9d84f34f0325d0dcc169f64).
All16 CI jobs passed across6 runs, including Python3.12/3.13 smoke. Canonical main checkouts fast-forwarded to merged code.
Local Lens smoke: {'passed': 43}

## Original prompt

# Repair tutorial prose formatting

@HowToLens @HowToGalaxy

Wrap Chapter 3 prose to 115 columns, preserving wording, paragraph boundaries and executable code. Join consecutive top-level narrative string blocks in Chapters 2 and 3 when separated only by whitespace, so only executable code separates narrative cells. Regenerate notebooks and catalogues via PyAutoHands; verify prose word sequences and executable AST equivalence, notebook cell types and nonempty code cells.

Original requests:
> on chapter 3 I think th epthon text goes all the way to the right so it doesnt have page spaces and new paragraphs?
> Dont format tings eithout code between them like this triple-quote / blank / triple-quote / **Parameter Space**, iw ill break notebook generation and is not the standard style

The user clarified the formatting plan in the same session; existing PR/merge/local-update authorization persists. No science wording changes.

Issued: 2026-11-01
Issue: https://github.com/PyAutoLabs/HowToLens/issues/119

Recovery scope authorized 2026-11-01:
> re add code when missing based onthe audit let me know when things are recovered

Recover saved runtime comparison, missing overlays and weights plots, measured evidence comparisons and working Hilbert-driven mesh adaptation, plus compactness example inside existing tutorial8. Repair12 lost Galaxy notebook prose lines. Preserve intentional prose-only sections; no new lesson. Validate actual outputs and both notebook text/code preservation.
