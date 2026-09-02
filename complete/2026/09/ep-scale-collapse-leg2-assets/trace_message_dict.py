"""
Settle the leg-2 lead: is `_HierarchicalFactor.message_dict` — which drops the
base class's 1/(count-1) tempering — actually reached when the GLOBAL mean field
is built, or is it inert because FactorGraphModel inherits the tempered base?
"""
import sys
sys.path.insert(0, "/workspace/ep_leg2")

import autofit as af
from autofit.graphical.declarative.factor.hierarchical import _HierarchicalFactor
from autofit.graphical.declarative.abstract import AbstractDeclarativeFactor
from toy import make_data, build_graph

calls = {"hierarchical": 0, "base": 0}

original_hier = _HierarchicalFactor.message_dict.fget
original_base = AbstractDeclarativeFactor.message_dict.fget


def traced_hier(self):
    calls["hierarchical"] += 1
    return original_hier(self)


def traced_base(self):
    calls["base"] += 1
    return original_base(self)


_HierarchicalFactor.message_dict = property(traced_hier)
AbstractDeclarativeFactor.message_dict = property(traced_base)

_, datasets = make_data(5, seed=0)
factor_graph, hf = build_graph(datasets)

mean_field = factor_graph.mean_field_approximation().mean_field
print("after building the GLOBAL mean field:")
print("  _HierarchicalFactor.message_dict calls :", calls["hierarchical"])
print("  base (tempered) message_dict calls     :", calls["base"])

# Is the parent scale's initial message tempered or not?
sigma_prior = hf.sigma
counts = dict(factor_graph.prior_counts)
print("\nparent scale prior:")
print("  shared by n factors (incl. prior factor):", counts.get(sigma_prior))
print("  initial message in global mean field    :", repr(mean_field[sigma_prior]))
print("  untempered prior message                :", repr(sigma_prior.message))
