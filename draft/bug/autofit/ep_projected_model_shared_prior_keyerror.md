# autofit: EP projection (Result.projected_model) raises KeyError for a prior shared across paths

Type: bug
Target: autofit
Repos:
- @PyAutoFit
Themes:
- expectation-propagation
- samples
- factor-graph
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: a unit test fits/constructs Samples for a model with one prior shared by two paths (e.g. two Gaussians with the same `centre` prior object) and `result.projected_model` returns a model whose shared prior is projected once, with no KeyError; and `Science/development/ep_gnfw_slope` `python scripts/ep.py --total 3 --max_steps 2 --smoke` (MGE source, 20 Gaussians sharing one centre/ell_comps prior) gets past the first factor's projection and completes both EP sweeps.
Review-minutes: 10
Unattended: never
Lane: any
Filed: 2026-11-13

Found 2026-11-13 in the `ep_gnfw_slope` science project's first EP smoke test (50
stellar + gNFW twins of Euclid DR1 lenses, one shared inner slope). Blocks that project.

## What happens

`Result.projected_model` (`autofit/non_linear/result.py`, ~line 500) loops over
`self.samples.model.path_priors_tuples` and calls `self.samples.values_for_path(path)`,
which does `sample.kwargs[path]` (`samples/samples.py` ~line 247). For a prior shared by
several paths, `path_priors_tuples` names it by its **first** path, but `Sample.kwargs`
holds it only under its **last** path (dict overwrite when the kwargs are built). Result:

```
KeyError: ('galaxies', 'galaxy_1', 'bulge', 'profile_list', '0', 'centre', 'centre_0')
```

after the factor's Nautilus search completes (kwargs carry `profile_list.19.centre.centre_0`).
Any EP `AnalysisFactor` whose model has an MGE source triggers it, because
`al.model_util.mge_model_from` ties one `centre` and one `ell_comps` prior across all
Gaussians. So EP with an MGE source has never been able to complete a factor step.
Ordinary (non-EP) fits never call `projected_model`, which is why nobody hit it before.

Repro (local PyAutoFit main 362ee746a == origin/main):

```python
import common  # ep_gnfw_slope/scripts
from autofit.non_linear.samples.sample import Sample
m = common.model_from(common.simulated_twin_from(common.sample_lens_ids()[0]))
s = Sample.from_lists(m, [list(m.physical_values_from_prior_medians)], [0.0], [0.0], [1.0])[0]
# path_priors_tuples -> ...profile_list.0.centre.centre_0 ; s.kwargs -> ...profile_list.19.centre.centre_0
```

## Fix direction

Same root cause as the sibling draft `samples_with_paths_shared_prior_factor_graph.md`
(kwargs keep only the last alias of a shared prior). Prefer one root fix that both inherit:
make `Samples.values_for_path` (and the kwargs lookup used by `parameter_lists`) accept any
alias of a shared prior, via `model.all_paths`, instead of patching `projected_model` alone.
Add a unit test with a prior shared across two paths covering `values_for_path` and
`projected_model`.
