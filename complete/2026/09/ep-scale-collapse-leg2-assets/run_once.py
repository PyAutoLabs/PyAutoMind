"""
One EP fit of the toy. Prints a single machine-readable RESULT line.

Env:
  TOY_SEED       data/run seed
  TOY_N          number of datasets (default 5)
  TOY_MAX_STEPS  EP sweeps (default 20 — the setting both measured COLLAPSEs hit)
  TOY_DELTA      if set, damping via SimplerUpdater(delta=...)
  TOY_OPT        'dynesty' (default) or 'laplace' for the per-factor optimiser
"""
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, "/workspace/ep_leg2")

import numpy as np
import autofit as af
from toy import make_data, build_graph, TRUE_SCATTER

SEED = int(os.environ.get("TOY_SEED", "0"))
N = int(os.environ.get("TOY_N", "5"))
MAX_STEPS = int(os.environ.get("TOY_MAX_STEPS", "20"))
DELTA = os.environ.get("TOY_DELTA")
OPT = os.environ.get("TOY_OPT", "dynesty")
UPDATER = os.environ.get("TOY_UPDATER")

start = time.time()
_, datasets = make_data(N, seed=SEED)
factor_graph, hf = build_graph(datasets)

if OPT == "laplace":
    # Swap the per-factor nested sampler for a deterministic optimiser on the
    # ANALYSIS factors — lever 2 of the prompt.
    for factor in factor_graph.model_factors:
        if hasattr(factor, "optimiser") and factor.optimiser is not None:
            try:
                factor.optimiser = af.LaplaceOptimiser()
            except Exception:
                pass

kwargs = {}
if UPDATER == "dynamic":
    # Per-VARIABLE damping: delta_i proportional to min_count / count(i), so the
    # parent hyperparameters (shared by 6 factors here) update at 0.5 while the
    # well-identified drawn centres (shared by 3) stay at 1.0. This targets the
    # over-shared variable specifically, unlike the uniform SimplerUpdater the
    # prompt's evidence found harmful.
    kwargs["updater"] = af.DynamicUpdater()
elif DELTA is not None:
    kwargs["updater"] = af.SimplerUpdater(delta=float(DELTA))

try:
    ep_result = factor_graph.optimise(
        af.LaplaceOptimiser(),
        paths=af.DirectoryPaths(
            name=os.path.join(
                "leg2",
                f"{OPT}_d{DELTA}_s{MAX_STEPS}"
                + (f"_u{UPDATER}" if UPDATER else "")
                + f"_seed{SEED}",
            )
        ),
        ep_history=af.EPHistory(kl_tol=0.05),
        max_steps=MAX_STEPS,
        **kwargs,
    )
except Exception as e:
    print(
        f"RESULT seed={SEED} outcome=CRASH scatter=nan err=nan "
        f"exc={type(e).__name__} secs={time.time() - start:.1f}"
    )
    sys.exit(0)

mf = ep_result.updated_ep_mean_field.mean_field
scatter = float(mf.mean[hf.sigma])
err = float(np.sqrt(mf.variance[hf.sigma]))
mean = float(mf.mean[hf.mean])

outcome = "COLLAPSE" if scatter < 0.4 * TRUE_SCATTER else "RECOVER"
print(
    f"RESULT seed={SEED} outcome={outcome} scatter={scatter:.4f} err={err:.4g} "
    f"mean={mean:.3f} secs={time.time() - start:.1f}"
)
