# Move PyAutoReduce lensing prototypes to flat fields

Type: maintenance
Target: PyAutoReduce
Repos:
- PyAutoReduce
Epic: mass-field
Status: draft
Autonomy: supervised
Filed: 2026-09-19
Issued: 2026-09-19

## Original user request

> We have been doing work which updates workspaces and lots more to a fields API, can we review where the updating te API for everything got too (E.g. I dont think we have done HowToLens) and continue all of that until its done?
>
> yes do all that, note that autolens_jax_joss is deleted more recently. But lets go

## Scope

Migrate the two live PyAutoReduce prototypes `prototypes/b1938_lens_fit.py` and `prototypes/slacs1430_parity_fit.py` from galaxy-attached ExternalShear to top-level `fields=` using `al.MassField`. Preserve the SLACS result's shear summary via `mp.fields.shear`.

This is the PyAutoReduce slice of `draft/maintenance/autolens_profiling/mass_field_flat_adoption_science_repos.md`. No library import is introduced into the `autoreduce` package; prototype scripts already use PyAutoLens.
