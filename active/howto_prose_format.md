# Repair tutorial prose formatting

@HowToLens @HowToGalaxy

Wrap Chapter 3 prose to 115 columns, preserving wording, paragraph boundaries and executable code. Join consecutive top-level narrative string blocks in Chapters 2 and 3 when separated only by whitespace, so only executable code separates narrative cells. Regenerate notebooks and catalogues via PyAutoHands; verify prose word sequences and executable AST equivalence, notebook cell types and nonempty code cells.

Original requests:
> on chapter 3 I think th epthon text goes all the way to the right so it doesnt have page spaces and new paragraphs?
> Dont format tings eithout code between them like this triple-quote / blank / triple-quote / **Parameter Space**, iw ill break notebook generation and is not the standard style

The user clarified the formatting plan in the same session; existing PR/merge/local-update authorization persists. No science wording changes.

Issued: 2026-11-01
Issue: https://github.com/PyAutoLabs/HowToLens/issues/119
