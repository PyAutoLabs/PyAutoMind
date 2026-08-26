`log_det_method` entered neither `AbstractMultiStartGradient.__identifier_fields__`
(only `("clipper",)`) nor `multi_start_unique_tag`, so a cholesky arm and a slogdet
arm differing in nothing else resolved to one autofit output directory and the
second returned the first's `.completed` fit. RAL job 340576 proved it: 20
`delaunay_adapt_split` arms (cholesky x10, slogdet x10) produced only 10 output
dirs, while the knn half (15 arms, all `log_det=auto`) correctly produced 15. The
results JSON basename still differed because `--config-name` carries `log_det`, so
the campaign would have reported 20 rows of which 10 were duplicates with nothing in
the artifact revealing it.

Fixed as a PATH SUFFIX, not an identifier change. `multi_start_unique_tag`
(`scripts/misc/searches/_samplers.py`) composes a fourth `ld_<method>` part, tagged
on the `SEARCHES_LOG_DET_METHOD` **env override only** — the W8 resolver falls back
to slogdet for every GPU gradient-pixelized arm alike, so tagging the resolved value
would have suffixed cells that never had one and broken byte-identity with recorded
output paths. An unset env returns exactly the pre-fix tag. The env is read directly
in `_samplers.py` because `_runner` imports `_samplers`. PyAutoFit was deliberately
NOT touched: changing `__identifier_fields__` would move the identifier for every
recorded MultiStart run in the campaign.

Shipped in autolens_profiling PR #178 (merge commit `11d06e50`), 3 files: the fix,
5 new tests in `test_searches_log_det_and_nautilus_seed.py`, and the
`SEARCHES_LOG_DET_METHOD` README row. CI green — `ruff check`, `ruff format --check`
and `pytest scripts/misc/test/ -q`; 50 tests pass across the three searches suites,
with the bijector and positions suites acting as the byte-identity control.

UNBLOCKS Phase 8B (#162): the 20 held delaunay arms now resolve to fresh
`…_ld_cholesky` / `…_ld_slogdet` paths and cannot resume the poisoned dirs. The
in-flight knn job 341845 is unaffected (all arms `log_det_method=None`). OUTSTANDING
OPERATIONAL ITEM: the 10 output dirs and 20 result rows from job 340576 are
contaminated and must be quarantined before any Phase 8B harvest.

SCOPE-NOTE AUDIT (reported, not fixed — verified by comparing `paths.output_path`
AND `paths.identifier` on built searches, not inferred from docstrings): the same
gap exists for `SEARCHES_SCALER`, `SEARCHES_BATCH_SIZE`, and unseeded
`SEARCHES_N_STARTS`/`_N_STEPS` (seeded is fine — `seed_tag` carries them). Covered:
`SEARCHES_POSITIONS_FACTOR`/`_THRESHOLD` via `positions_arm_tag`, and the
Nautilus/NSS knobs via those classes' real `__identifier_fields__`.
`SEARCHES_NSS_CHUNK_SIZE` is benign (bit-identical at fixed seed, PyAutoFit PR#1492).
None of the three real gaps currently fires: no `hpc/batch_gpu/submit_*` varies
scaler or batch_size across arms, and every submit setting `N_STARTS` also sets
`SEARCHES_SEED`. `SEARCHES_DIAGNOSTIC_THETA_E_PRIOR` could NOT be decided — the
probe sees `paths.model is None` at build time, so it never exercises the model hash
a real fit attaches; flagged unverified rather than claimed either way.

PROCESS NOTES: shipped on explicit human authorization while Heart was RED on two
reasons unrelated to this repo (`autogalaxy_workspace_test: Smoke Tests failure on
main`, `release validation FAILED (stage integrate)`). Branch split mid-ship: this
task had been sharing worktree AND branch with #176, which committed ef1c44b (56
files) to `feature/log-det-multistart-tag` first, so #175 was rebranched off
`origin/main` as `feature/log-det-multistart-tag-175` in its own worktree and its 3
files were restored in the shared worktree, leaving #176 sole owner of both.

## Original prompt

# log_det_method is missing from the MultiStart search tag, so arms collide

Type: bug
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-08-26

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

SCOPE: **autolens_profiling only.** The fix, its test
(`scripts/misc/test/test_searches_log_det_and_nautilus_seed.py`) and the
submit that exercises it all live in this repo. No PyAutoFit worktree is
needed — do not claim one.

Scope note: the same class of gap may exist for other likelihood-affecting
knobs outside `__identifier_fields__`. Report anything found; do not fix it in
this change.

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/cc3c117a-bb7b-499c-aa8c-f3e8f65d1bb5/scratchpad/prompts/p1.md -->
