# Aggregator reload of an in-memory sparse-operator interferometer fit silently falls back to the dense path

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Themes:
- interferometer
- sparse-operator
- aggregator
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: a fit run with `dataset.apply_sparse_operator(...)` and reloaded through `al.agg` / `ag.agg` rebuilds a dataset whose `sparse_operator` is not `None` (or raises a clear error), and the reloaded fit's inversion class matches the original.
Review-minutes: 3
Unattended: ready

Found 2026-09-30 in the Discussion #13 phase-2 survey. `autogalaxy/aggregator/interferometer/interferometer.py` `_interferometer_from`
rebuilds `aa.Interferometer(data, noise_map, uv, transformer_class)` and never re-attaches a sparse operator, so a reloaded sparse fit runs
`InversionInterferometerMapping`/w-tilde instead — a silent class change (cf. memory: assert the inversion class before blaming hardware).
Fix: persist a `sparse_operator` marker (settings json or `dataset.fits` header) in `save_attributes` and re-apply on reload; the array-free
case shipped in `complete/2026/09/streaming-p2-fit-save-reload.md` (PyAutoGalaxy#639 + PyAutoLens#758).
