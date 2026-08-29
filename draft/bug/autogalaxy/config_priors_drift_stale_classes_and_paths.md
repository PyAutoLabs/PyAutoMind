# Config priors drift: stale class names, paths and params shared by PyAutoGalaxy and autolens_workspace

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- PyAutoFit
- autolens_workspace
- autogalaxy_workspace
Themes:
- config
- hygiene
Difficulty: small
Autonomy: safe
Priority: medium
Status: draft
Filed: 2026-08-29

Found by the euclid_strong_lens_modeling_pipeline config drift sweep (euclid#43 / PR #44,
2026-08-29). These findings reproduce **identically** in the packaged
`PyAutoGalaxy/autogalaxy/config/priors/` and in `autolens_workspace/config/priors/`, so they
were deliberately left alone in the euclid repo (fixing them there would fork files in parity)
and belong upstream. Mechanism that makes several of these silent: `JSONPriorConfig` matches
`cls.__module__ + cls.__name__ + param` by *suffix* against the yaml path relative to
`config/priors/`, so a file at the wrong path is dead, not an error — the packaged default wins.

User request (verbatim): "voronoi was removed so we should remove voronoi.yaml and things with
similar references. I guess this implies for the euclid repo we should do a general config drift
sweet" — the euclid-local half shipped in PR #44; this prompt is the upstream half.

## Findings (all verified against installed 2026.8.17.1 via `dir()` / `__init__` signatures)

| File | Key | Finding |
|---|---|---|
| `priors/light/operated/sersic.yaml` | `ersic` | Typo (leading `S` missing) — the operated `Sersic` priors are dead |
| `priors/mass/dark/nfw_truncated_mcr.yaml` | `NFWTruncatedMCRScatterLudlowSph` | path ≠ class module → dead |
| `priors/light/linear/chameleon.yaml` | `Chameleon`, `ChameleonSph` | path mismatch → dead |
| `priors/light/linear/eff.yaml` | `ElsonFreeFall`, `ElsonFreeFallSph` | path mismatch → dead |
| `priors/point_sources.yaml` | `PointSourceChi` | class no longer exists |
| `priors/cosmology.yaml` | `model.FlatLambdaCDM` | dotted key, no matching class path |
| `priors/mass/stellar/sersic_core.yaml` | `SersicCoreSph.mass_to_light_ratio` | param not in `__init__` |
| `priors/light/linear_operated/gaussian.yaml` | `Gaussian.intensity` | linear profiles have no `intensity` |
| `priors/mesh/README.md` | prose | still says "…Delaunay triangulation or Voronoi mesh" — Voronoi removed |
| `visualize/plots_search.yaml` | `dynesty:`, `emcee:`, `nautilus:`, `zeus:` | autofit reads only the three family-level sections; per-search blocks unread |
| `general.yaml` | `fits.flip_for_ds9` | no reader in any library or autonerves |

## Deliverable

- Fix or delete each row in the packaged PyAutoGalaxy (and PyAutoFit for `plots_search`/`general`)
  config, then propagate to `autolens_workspace` / `autogalaxy_workspace` `config/` so the copies
  stay in parity.
- Consider a small test in PyAutoFit/PyAutoGalaxy that walks `config/priors/**` and asserts every
  top-level key resolves to a class whose module path suffix-matches the file path and whose
  declared params are in `__init__` — the check that found these is ~40 lines and would stop the
  class of bug recurring.
