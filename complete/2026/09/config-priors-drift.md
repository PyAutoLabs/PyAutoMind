## config-priors-drift
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/618
- completed: 2026-09-16
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/619
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/550
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/244
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/87
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/319
- summary: Fixed eleven dead rows in the packaged PyAutoGalaxy `config/priors/` (JSONPriorConfig suffix-matcher drift: `ersic` typo, `NFWTruncatedMCRScatterLudlowSph` under the wrong file, orphan linear chameleon/eff, `PointSourceChi`, dead `SersicCoreSph.mass_to_light_ratio` and linear-operated `Gaussian.intensity`, `EllipseMultipoleRelative`/`gaussian_limits`, empty `DelaunayNN`, Voronoi README) and added `test_autogalaxy/test_priors_config.py` (walker: every key resolves to a class, every param is an `__init__` arg; model-construction regressions). Re-synced autolens_workspace, autogalaxy_workspace, HowToLens, autolens_workspace_test `config/` to byte parity, replaced stale per-search `plots_search.yaml`, removed readerless `general.yaml::fits.flip_for_ds9`, deleted `autolens_workspace_test/config/priors/mesh/voronoi.yaml`.
- verification: red witness 4 failed on old config (9 dead keys, 2 dead params); green 5 passed; full `pytest test_autogalaxy` 1212 passed; `pyauto-heart smoke --root <wt>` 136/136; CI green on every leg of all five PRs.
- traps: intake drops `Type: hygiene` (use `maintenance`) and header-first input becomes the title; `pyauto-heart smoke --root` on real worktrees deleted tracked `autolens_workspace_test/output/.gitignore`; the plan assumed HowToLens/autolens_workspace_test shipped no priors — they carry full copies.
- follow-ups: `draft/bug/autogalaxy/sersiccoresph_has_no_mass_to_light_ratio.md`, `draft/maintenance/autogalaxy/linear_operated_sersic_has_no_prior_yaml.md`, `draft/maintenance/workspaces/sync_remaining_workspace_config_priors_copies.md` (HowToGalaxy, autogalaxy_workspace_test x2, autolens/autogalaxy/autocti assistants still carry the rows; euclid keeps its copy by design).

## Original prompt

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
Status: active
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-29
Issued: 2026-09-15

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
