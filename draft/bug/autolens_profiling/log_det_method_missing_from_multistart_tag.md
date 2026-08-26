# log_det_method is missing from the MultiStart search tag, so arms collide

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Two Phase 8B arms that differ only in `log_det_method` resolve to the same
autofit output directory and identifier, so the second silently returns the
first's completed fit.

`autolens_profiling/scripts/misc/searches/_samplers.py::multi_start_unique_tag`
composes seed + positions + bijector into the tag — its docstring explains, at
length, why each of those three had to be added — but it does not compose
`log_det_method`. `AbstractMultiStartGradient.__identifier_fields__` is only
`("clipper",)`, so `log_det_method` enters neither the identifier hash nor the
output path.

PROOF (RAL job 340576, 2026-08-25): the Phase 8B array submitted 20
`delaunay_adapt_split` arms — cholesky x10, slogdet x10 — and they produced
only 10 autofit output dirs (`n16_s3000_seed{0-4}` and `..._bij_log_reg`). The
knn half, whose 15 arms are all `log_det=auto`, correctly produced 15 dirs.

CONSEQUENCE: on rerun the second of each cholesky/slogdet pair hits the
`.completed` short-circuit and returns its sibling's fit, while the results
JSON basename still differs (config-name carries log_det) — so the campaign
would report 20 rows of which 10 are duplicates, with nothing in the artifact
revealing it. This is the same defect class the docstring already documents
for positions and for the bijector.

Blocks 20 arms / ~80 GPU-h of Phase 8B (autolens_profiling#162). The knn half
was submitted on 2026-08-26 as job 341845; the delaunay half is held pending
this fix.

FIX: compose a log_det tag into `multi_start_unique_tag`, in the same shape as
the existing seed/positions/bijector tags, preserving the rule that the
default/"auto" value adds no tag so recorded output paths stay byte-identical.
Then audit for any OTHER likelihood-affecting knob that sits outside both
`__identifier_fields__` and the tag.

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cc3c117a-bb7b-499c-aa8c-f3e8f65d1bb5/scratchpad/prompts/p1.md -->
