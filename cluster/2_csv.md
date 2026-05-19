For autolens_workspace/scripts/cluster/simulator.py, can we make it so that all parameters are in .csv form
and loaded from there, to establish that the base way to interact with the autolens API for clusters
is via csv.

I thin kthe way to make this work is to write a guide, autolens_workspace/scripts/cluster/csv_api.py,
which illustrates how to set up lens models using the normal autolens API and then output them to csv,
and showing how all those featres linked together.

This csv file can then act as an "Auto Simulate" type siutation for simulator.py, which loads the csv outputsof this file.
The simulator will put the csv files int he lens it simulates at the end, meaning other scripts only need the
auto simulate performed here.

Things I am still unclear on that this guide could help with are:

Shouild main galaxies, extra galaxies and scaling galaies use their own csv files or can they all be combined into one?
I think it would be good if they could all be combined into one, but hiswould mean the .csv needs to know a lot more
than just parameters, but feasible mass profile class, lens name (e.g. when its used to name light and mass profiles in the Galaxy), redshift and
others. I think I like the idea of a single .csv API being used for all cluster interfaces.

The flip side is this could get complicated because if the same galaxy has light and mass profiles then the notion of column
heads breaks down, so maybe the rule is "one csv file per light or mass profile", and the reuse of light profile names, mass profile
names and galaxy names is exploited when building the model? Most cluster models will apply the same thing over loads
of galaxies so I think that works, so we can just build it in an extensible way.

This would mean it also needs the galaxy names, even though in simulator.py galaxies are not named when used in a Tracer
these names would be used for performing model composition, again the csv_api.py script could explain and cover this.

I would then go so far as to make it so that this guide also explains point_datasets.csv, which functionally looks a lot
more complete to me and just needs an explanation. I would explain this before doing galaxy API, as convention is normally load
dataset before modeling.

Do deep research when coming to this csv API and once you're happy with it make it the version used on all 3 cluster
scripts that exist.