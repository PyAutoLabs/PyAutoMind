"""
Toy hierarchical EP diagnostic
==============================

Cheap CPU reproduction of the slope_hierarchy goal-2 pathology:
EP recovers the parent MEAN but reports a parent SCATTER that is too low with
error bars that are orders-of-magnitude too tight.

Known-answer toy (HowToFit chapter 3 hierarchical dataset):
  - N Gaussians, each centre drawn from parent N(mean=50, sigma=10)
  - TRUE parent mean   = 50.0
  - TRUE parent scatter= 10.0   <-- FAR from the sigma->0 boundary (the key contrast
                                     with slope_hierarchy whose truth was 0.1)
  - per-Gaussian normalization = 0.5, sigma = 5.0 (fixed at truth to keep the joint
    nested-sampler fit cheap and to isolate the parent-scatter question)

Run from the HowToFit repo root.
"""
import os
import sys
import numpy as np
from os import path

import autofit as af
from autofit.graphical import mean_field_summary, check_sigma_collapse

# ---- config ---------------------------------------------------------------
TOTAL_DATASETS = int(os.environ.get("TOY_N", "5"))
MAX_STEPS = int(os.environ.get("TOY_MAX_STEPS", "20"))
RUN_JOINT = os.environ.get("TOY_JOINT", "1") == "1"
OUT_TAG = os.environ.get("TOY_TAG", f"ep_toy_n{TOTAL_DATASETS}_s{MAX_STEPS}")

TRUE_MEAN = 50.0
TRUE_SCATTER = 10.0

print(f"=== TOY EP DIAGNOSTIC  N={TOTAL_DATASETS}  max_steps={MAX_STEPS} ===")
print(f"TRUE parent: mean={TRUE_MEAN}  scatter={TRUE_SCATTER}")

# ---- data -----------------------------------------------------------------
data_list, noise_map_list = [], []
for i in range(TOTAL_DATASETS):
    dp = path.join("dataset", "example_1d", "gaussian_x1__hierarchical", f"dataset_{i}")
    data_list.append(af.util.numpy_array_from_json(file_path=path.join(dp, "data.json")))
    noise_map_list.append(af.util.numpy_array_from_json(file_path=path.join(dp, "noise_map.json")))

analysis_list = [af.ex.Analysis(data=d, noise_map=n) for d, n in zip(data_list, noise_map_list)]

# ---- per-dataset models: only `centre` free (nuisances fixed at truth) -----
model_list = []
for _ in range(TOTAL_DATASETS):
    g = af.Model(af.ex.Gaussian)
    g.centre = af.TruncatedGaussianPrior(mean=50.0, sigma=20.0, lower_limit=0.0, upper_limit=100.0)
    g.normalization = 0.5
    g.sigma = 5.0
    model_list.append(g)

# ---- EP fit ---------------------------------------------------------------
dynesty = af.DynestyStatic(nlive=100, sample="rwalk")
analysis_factor_list = [
    af.AnalysisFactor(prior_model=m, analysis=a, optimiser=dynesty, name=f"dataset_{i}")
    for i, (m, a) in enumerate(zip(model_list, analysis_list))
]

hierarchical_factor = af.HierarchicalFactor(
    af.GaussianPrior,
    mean=af.TruncatedGaussianPrior(mean=50.0, sigma=10.0, lower_limit=0.0, upper_limit=100.0),
    sigma=af.TruncatedGaussianPrior(mean=10.0, sigma=5.0, lower_limit=0.0, upper_limit=100.0),
)
for m in model_list:
    hierarchical_factor.add_drawn_variable(m.centre)

factor_graph = af.FactorGraphModel(*analysis_factor_list, hierarchical_factor)

laplace = af.LaplaceOptimiser()
try:
    ep_result = factor_graph.optimise(
        laplace,
        paths=af.DirectoryPaths(name=path.join("ep_toy_diagnostic", OUT_TAG)),
        ep_history=af.EPHistory(kl_tol=0.05),
        max_steps=MAX_STEPS,
    )
except Exception as e:
    print(f"\nOUTCOME: CRASH  ({type(e).__name__}: {str(e).splitlines()[0][:80]})")
    print("DONE-SENTINEL")
    sys.exit(0)

mean_field = ep_result.updated_ep_mean_field.mean_field
ep_mean = mean_field.mean[hierarchical_factor.mean]
ep_mean_err = float(np.sqrt(mean_field.variance[hierarchical_factor.mean]))
ep_sigma = mean_field.mean[hierarchical_factor.sigma]
ep_sigma_err = float(np.sqrt(mean_field.variance[hierarchical_factor.sigma]))

print("\n================ EP RESULT ================")
print(f"parent mean    : {ep_mean:.4f} +/- {ep_mean_err:.4g}   (truth {TRUE_MEAN})")
print(f"parent scatter : {ep_sigma:.4f} +/- {ep_sigma_err:.4g}   (truth {TRUE_SCATTER})")
# outcome tag: COLLAPSE if scatter << truth, else RECOVER
_tag = "COLLAPSE" if ep_sigma < 0.4 * TRUE_SCATTER else "RECOVER"
print(f"OUTCOME: {_tag}  scatter={ep_sigma:.4f}  err={ep_sigma_err:.4f}  mean={ep_mean:.3f}")
print("\n--- mean_field_summary ---")
try:
    print(mean_field_summary(mean_field))
except Exception as e:
    print("mean_field_summary failed:", e)
print("\n--- check_sigma_collapse ---")
try:
    print(check_sigma_collapse(mean_field))
except Exception as e:
    print("check_sigma_collapse failed:", e)

# base-space (untransformed) sigma message: is it near the sigma->0 boundary?
try:
    base_msg = mean_field[hierarchical_factor.sigma]
    print("\n--- parent-sigma message (base space) ---")
    print("  repr:", repr(base_msg))
    for attr in ("mean", "sigma", "scale", "variance", "natural_parameters"):
        v = getattr(base_msg, attr, None)
        if callable(v):
            try:
                v = v()
            except Exception:
                continue
        if v is not None:
            print(f"  {attr}: {v}")
except Exception as e:
    print("base sigma message introspection failed:", e)

# ---- JOINT nested-sampler fit of the SAME graph ---------------------------
def weighted_percentiles(values, weights, qs=(0.16, 0.5, 0.84)):
    order = np.argsort(values)
    v = np.asarray(values)[order]
    w = np.asarray(weights)[order]
    cw = np.cumsum(w)
    cw = cw / cw[-1]
    return np.interp(qs, cw, v)

if RUN_JOINT:
    print("\n================ JOINT NESTED-SAMPLER FIT (SAME graph) ================")
    joint_model = factor_graph.global_prior_model
    print("joint dims (prior_count):", joint_model.prior_count)
    search = af.DynestyStatic(
        name=path.join("ep_toy_diagnostic", OUT_TAG + "_joint"),
        nlive=150,
        sample="rwalk",
    )
    joint_result = search.fit(model=joint_model, analysis=factor_graph)
    samples = joint_result.samples

    ordered = samples.model.priors_ordered_by_id
    params = np.array(samples.parameter_lists)
    weights = np.array(samples.weight_list)

    def marg(prior):
        col = [i for i, p in enumerate(ordered) if p.id == prior.id][0]
        lo, med, hi = weighted_percentiles(params[:, col], weights)
        return med, lo, hi

    jm_med, jm_lo, jm_hi = marg(hierarchical_factor.mean)
    js_med, js_lo, js_hi = marg(hierarchical_factor.sigma)
    print("\n---------------- JOINT RESULT (percentile 16/50/84) ----------------")
    print(f"parent mean    : {jm_med:.4f}  [{jm_lo:.4f}, {jm_hi:.4f}]   (truth {TRUE_MEAN})")
    print(f"parent scatter : {js_med:.4f}  [{js_lo:.4f}, {js_hi:.4f}]   (truth {TRUE_SCATTER})")

    # ---- side-by-side verdict table ----
    print("\n================ EP vs JOINT ================")
    print(f"{'param':10s} {'truth':>7s} {'EP':>22s} {'JOINT':>26s}")
    print(f"{'mean':10s} {TRUE_MEAN:7.2f} {ep_mean:8.4f}+/-{ep_mean_err:<10.3g} "
          f"{jm_med:8.4f} [{jm_lo:.3f},{jm_hi:.3f}]")
    print(f"{'scatter':10s} {TRUE_SCATTER:7.2f} {ep_sigma:8.4f}+/-{ep_sigma_err:<10.3g} "
          f"{js_med:8.4f} [{js_lo:.3f},{js_hi:.3f}]")
    joint_sigma_err = 0.5 * (js_hi - js_lo)
    ratio = joint_sigma_err / ep_sigma_err if ep_sigma_err > 0 else float("inf")
    print(f"\nscatter error ratio JOINT/EP = {ratio:.1f}x  "
          f"(EP err {ep_sigma_err:.4g}  vs  JOINT half-CI {joint_sigma_err:.4g})")

print("\nDONE-SENTINEL")
