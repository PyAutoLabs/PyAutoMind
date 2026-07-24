# Fix workspace-level `start_here.py` Colab links

Type: docs
Target: workspaces
Repos:
- PyAutoLens
- PyAutoGalaxy
- autolens_workspace
- autogalaxy_workspace
- euclid_strong_lens_modeling_pipeline
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Correct Google Colab URLs described as the introductory PyAutoLens or
PyAutoGalaxy Jupyter Notebook so that they open each workspace's root
`start_here.ipynb`, generated from the overall workspace `start_here.py`, not
the topic-specific `notebooks/imaging/start_here.ipynb`. Scan other `README.md`
and documentation files for the same incorrect target and update matching
introductory links, while preserving links that explicitly describe the
imaging-specific tutorial.

Verify that both root `start_here.py` sources use the correct product-specific
`setup_colab` call and that the corresponding generated `start_here.ipynb`
notebooks contain the same setup before routing users to them.

## Original request

> The URL to this should not be imaging/start_here.py but the overall workspace start_here.py, The introduction Jupyter Notebook on Google Colab: try PyAutoLens in a web browser (without installation)., update it and scan other README.md and docs for the same issue

> make sure the examples we are routing to has the right setup_colab

> this is prob requied for PyautoGalaxy too
