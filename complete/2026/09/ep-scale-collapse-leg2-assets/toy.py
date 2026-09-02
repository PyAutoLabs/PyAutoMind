"""
Self-contained rebuild of the PyAutoFit #1405 hierarchical-EP toy.

The original (PyAutoMind complete/2026/07/ep_scale_collapse_assets/
ep_toy_diagnostic.py) loads the HowToFit chapter-3 dataset, which is gitignored
and ships with no data. The generative model is fully specified in that script's
docstring, so the data is regenerated here instead:

  N Gaussians, centre_i ~ N(mean=50, sigma=10), normalization=0.5, sigma=5.0,
  observed on a 1-D pixel grid with Gaussian noise.

TRUE parent mean = 50.0, TRUE parent scatter = 10.0 (far from the sigma->0
boundary — the key contrast with slope_hierarchy, whose truth was 0.1).
"""
import os
import numpy as np
import autofit as af

TRUE_MEAN = 50.0
TRUE_SCATTER = 10.0
NORMALIZATION = 0.5
GAUSSIAN_SIGMA = 5.0
N_PIXELS = 100
NOISE_SIGMA = float(os.environ.get("TOY_NOISE", "0.05"))


def make_data(n_datasets, seed):
    """Draw centres from the parent and simulate a noisy 1-D Gaussian each."""
    rng = np.random.default_rng(seed)
    centres = rng.normal(TRUE_MEAN, TRUE_SCATTER, size=n_datasets)
    xvals = np.arange(N_PIXELS).astype(float)

    datasets = []
    for centre in centres:
        gaussian = af.ex.Gaussian(
            centre=float(centre), normalization=NORMALIZATION, sigma=GAUSSIAN_SIGMA
        )
        model_data = gaussian.model_data_from(xvals)
        noise_map = np.full(N_PIXELS, NOISE_SIGMA)
        data = model_data + rng.normal(0.0, NOISE_SIGMA, size=N_PIXELS)
        datasets.append((data, noise_map))
    return centres, datasets


def build_graph(datasets, nlive=100):
    """The toy's graph: N AnalysisFactors + one HierarchicalFactor on `centre`."""
    model_list = []
    for _ in datasets:
        g = af.Model(af.ex.Gaussian)
        g.centre = af.TruncatedGaussianPrior(
            mean=50.0, sigma=20.0, lower_limit=0.0, upper_limit=100.0
        )
        g.normalization = NORMALIZATION
        g.sigma = GAUSSIAN_SIGMA
        model_list.append(g)

    dynesty = af.DynestyStatic(nlive=nlive, sample="rwalk")
    analysis_factor_list = [
        af.AnalysisFactor(
            prior_model=m,
            analysis=af.ex.Analysis(data=d, noise_map=n),
            optimiser=dynesty,
            name=f"dataset_{i}",
        )
        for i, (m, (d, n)) in enumerate(zip(model_list, datasets))
    ]

    hierarchical_factor = af.HierarchicalFactor(
        af.GaussianPrior,
        mean=af.TruncatedGaussianPrior(
            mean=50.0, sigma=10.0, lower_limit=0.0, upper_limit=100.0
        ),
        sigma=af.TruncatedGaussianPrior(
            mean=10.0, sigma=5.0, lower_limit=0.0, upper_limit=100.0
        ),
    )
    for m in model_list:
        hierarchical_factor.add_drawn_variable(m.centre)

    factor_graph = af.FactorGraphModel(*analysis_factor_list, hierarchical_factor)
    return factor_graph, hierarchical_factor
