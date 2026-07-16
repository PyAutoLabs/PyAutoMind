# Aggregator profiling harness and result-loading speedups (sqlite follow-up)

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
- autolens_workspace
- autolens_workspace_test
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

The PyAutoFit Aggregator is used to load and inspection modeling results, including workflow variants
for .fits, .csv and .png files.

It is used heavily in /mnt/c/Users/Jammy/Science/euclid, where it was often loading results for 3000+ strong lenses
and making the catalogue of csv, fits, png files.

There are many variants of how to load results, aggregators may be skipped for small numbers of lenses, whereas
an sqlite database can be built for large sets (albeit I havent done this in a while and it may be buggy).

A good run through of loadin gresults in all the different ways is at autolens_workspace/scripts/guides/results

The goals of this task are the following:

1) Extend autofit_workspace_test and autolens_workspace_test to have the tools required to profile the speed of the aggregator
in different models, for differnt models and really work out "where does it scale poorly", "when is it too
slow to do sciecne", "is it model complexity, number of sampels or something else whjich sl;ows it down?". Ideally,
This will create output folders that mock real results, but it will do so in a fast way which does not run actual
samplers or do anything that is to slow.

2) Use these profiling tools to begin speeding up the existing Aggregators and other ways of loading reults, basically
target the low hanging fruit for now.

3) dont work on sqlite database builds on 1 or 2, but then do a follow upw here you use this functionality,
inevitably encounter and fix bugs for its use, and assess the code which writes directly to the sqlite database,
which has not been used in a long time and I'm sure is buggy. If its hard to fix dont bother, but its good to work out where its at.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/aa483bab-3f5b-4ffe-b121-c968ff80ffae/scratchpad/intake_aggregator_profiling.md -->
