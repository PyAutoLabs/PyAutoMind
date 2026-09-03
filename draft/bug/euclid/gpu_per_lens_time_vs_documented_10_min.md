# GPU route takes 74 min per lens with the committed config, not the documented ~10 min

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- jax
- hpc
Difficulty: medium
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Epic: euclid-dr1-prep
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-09-03

Found during the RAL acceptance runs of Mind phase 4 of the euclid-dr1-prep epic
(`euclid_strong_lens_modeling_pipeline#49`), which measured both submission routes
end to end for the first time from the pipeline repo's own scripts.

## The finding

The repository documents `scripts/initial_lens_model.py` as fitting a lens in
"around 10 minutes on a GPU, around 20 minutes on an 8-core CPU"
(`README.md`, `start_here.py`). Measured on RAL on 2026-09-03, on the committed
example lens `q1_walsmley/102018665_NEG570040238507752998`, with the committed
`config/`:

| Route | Allocation | `vis_lp` | `vis_pix` | Total |
|---|---|---|---|---|
| GPU (`hpc/batch_gpu/submit_initial_lens_model`, job 342248_0) | one A100 80GB PCIe, 1 core | 31.5 min | 42.5 min | 1 h 14 min |
| Two-stage CPU (`hpc/batch_cpu/submit_initial_lens_model_two_stage`, job 342244_0) | 8 cores, 8 pool workers | 25.5 min | 2 h 51 min | 3 h 17 min |

Both jobs COMPLETED, and the GPU job's fail-fast guard printed `JAX backend: gpu`,
so this is a real GPU run rather than the CPU-fallback case that the same phase's
MIG-mode incident produced. The GPU figure is roughly 7x the documented one, and
the CPU figure roughly 10x.

The documented figures come from the DR1 science runs, which used their own
`config/` tree, so they are not necessarily wrong — but nothing in the repository
says so, and a new user following `hpc/README.md` gets the measured numbers.
Phase 4 has already replaced the route-table figures with the measured ones and
attributed the ~10 min claim in `README.md` / `start_here.py` to the science-run
configuration; this prompt is about closing the gap rather than describing it.

## Candidate causes

1. **The science configuration.** `hpc/README.md` "Config for large runs" already
   names three `config/general.yaml` keys the DR1 runs set differently:
   `output.samples_to_csv: false`, `hpc.hpc_mode: true` (no GUI visualisation or
   screen logging) and `numba.cache: false`. The committed config runs a quick
   update roughly every 2.5 min at about 14 s each, so visualisation overhead alone
   is only about 10% — not a 7x gap. Whatever else the science tree's `config/`
   changed (sampler settings in particular) has not been diffed against the
   committed tree, and that diff is the first thing to do here.

2. **The sparse-operator drift on the JAX path.** `scripts/initial_lens_model.py`
   lines 341-344 read:

   ```python
   if use_cpu:
       dataset = dataset.apply_sparse_operator_cpu()
   else:
       dataset = dataset.apply_sparse_operator()
   ```

   The science tree's copy
   (`/mnt/c/Users/Jammy/Science/euclid/scripts/initial_lens_model.py`, lines
   210-211) has no `else` branch: on the JAX path it applies no sparse operator at
   all. So the public repo does extra work on exactly the route whose measured time
   is 7x the documented one. This was flagged for review in phase 4 and deliberately
   not changed there. Whether the `else` is a correctness fix or an accidental
   addition is unresolved, and it is the reason PyAutoLens may turn out to be
   implicated — do not add it to `Repos:` until the operator itself is in question.

These are not exclusive: the answer may be some of each.

## Acceptance

- The ~10 min per-lens GPU figure is either reproduced (naming the exact `config/`
  changes that get there, which then belong in `hpc/README.md`'s "Config for large
  runs" list) or retired from `README.md` and `start_here.py` in favour of a
  measured number.
- A verdict on `apply_sparse_operator()` in the `else:` branch: a bug to remove, or
  correct and to be kept with a comment saying why the JAX path needs it. If it is
  removed, re-measure the GPU route on the same lens and record the new time.
- `hpc/README.md`'s route table carries whatever the final numbers are.
