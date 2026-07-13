The project @z_projects/ic50_workspace is our IC50  use case which we are now aiming to scale up the EP framework
to the IC50 use case.

Can you perform a run of ep_sim.py, and perform a timing break down of all the different steps that go into
the overall EP run time, which would include things like:

1) Time spent doing each IC50 Hill curve fit in a FactorAnalysis using Dynesty, total time and time per EP iteration.
2) Time spent fitting the global model.
3) Time spent doing all non fitting boiler plate (e.g. PyAutoFit over heads seting up graph, iterations around the EP loop, and so forth).

Can you attempt to break 3) down into sub categories.

Given the time taken for 5 datasets in this example, present a proejction for how long 100, 1000, 10000 would take.

This will then form the basis of us optimizing and improving all EP functioanlity so it runs fast enough to scale up
to lsrger samples.