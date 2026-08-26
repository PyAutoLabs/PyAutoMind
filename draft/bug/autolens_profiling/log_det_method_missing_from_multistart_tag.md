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

FIX (decided 2026-08-26) — a PATH SUFFIX, not an identifier change.

Do **not** touch `AbstractMultiStartGradient.__identifier_fields__` or anything
else in PyAutoFit. `arm_unique_tag` (`_samplers.py:90`) is already just
`"_".join(non-None parts)`, and the tag it returns sits in `output_path` above
`name` — so it *is* the path suffix. Add one more part, mirroring the
`bijector_tag` line directly above it:

    log_det = os.environ.get("SEARCHES_LOG_DET_METHOD")
    log_det_tag = None if not log_det else f"ld_{log_det}"
    ...
    return arm_unique_tag(seed_tag, pos_tag, bijector_tag, log_det_tag)

Tag on the **env override only**, never on the W8-resolved default. The
resolver at `_runner.py:744` falls back to slogdet-on-GPU for every arm alike,
so tagging the resolved value would add a suffix to cells that never had one
and break byte-identity with recorded output paths. An unset
`SEARCHES_LOG_DET_METHOD` must keep returning exactly today's tag. Read the env
directly in `_samplers.py` rather than importing the resolver — `_runner`
imports `_samplers`, so the other direction would be circular.

Scope note: the same class of gap may exist for other likelihood-affecting
knobs outside `__identifier_fields__`. Report anything found; do not fix it in
this change.

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cc3c117a-bb7b-499c-aa8c-f3e8f65d1bb5/scratchpad/prompts/p1.md -->
