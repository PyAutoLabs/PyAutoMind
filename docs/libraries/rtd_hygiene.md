# Docs infrastructure phase A: RTD hygiene across PyAutoFit/Galaxy/Lens

Type: docs
Target: libraries
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

Phase A of the docs-infrastructure middle path (census 2026-07-09; original request and
decision recorded in [docs_theming_and_hub.md](docs_theming_and_hub.md), the parked
follow-up). Repos: @PyAutoFit @PyAutoGalaxy @PyAutoLens.

## Census findings this phase fixes

1. **pyautofit.readthedocs.io has not built since 2026-05-06.** The RTD project points at
   `rhayes777/PyAutoFit.git`; its webhook/connection did not survive the org migration.
   16 docs commits (incl. the Jammy2211→PyAutoLabs URL audit #1265 and the Latent cookbook
   migration) have never reached the live site. PyAutoGalaxy/PyAutoLens RTD point at old
   `Jammy2211/...` URLs but their webhooks survived and build fine (built 2026-07-09).
2. **No docs build in CI** in any of the three repos, and all three `.readthedocs.yaml`
   set `fail_on_warning: false` → docs rot silently (stale `plot.rst` / PyAutoLens#592 is
   the proof; that content rewrite stays a separate task).
3. **Dead/duplicate configs:** PyAutoFit `readthedocs.yml` (py3.11) and PyAutoGalaxy
   `readthedocs.yaml` duplicate the live `.readthedocs.yaml` (py3.12) with drifted
   contents; PyAutoFit `docs/requirements.txt` (SQLAlchemy==1.3.20 etc.) is superseded by
   the pyproject `[docs]` extra RTD actually installs.
4. **conf.py drift:** PyAutoLens typo `nnumpydoc_class_members_toctree` (setting silently
   ignored → Lens runs different numpydoc config than Galaxy); PyAutoFit and PyAutoLens
   declare `html_static_path = ["_static"]` + `pied-piper-admonition.css` that do not
   exist on disk; PyAutoFit's autodoc block diverges wholesale from Galaxy/Lens (no
   `sphinx_autodoc_typehints` despite shipping it in the extra, different
   `autoclass_content`); all three carry a dead `html_context` block
   (`github_version: "master"`) Furo never reads.
5. Only `latest` is published (no `stable`/tags) — acceptable under nightly releases;
   recorded as deliberate, not in scope to change.

## Scope

- **Human legs (RTD dashboard — walk the user through them):** reconnect the `pyautofit`
  RTD project to `PyAutoLabs/PyAutoFit` and confirm a fresh build goes live; update the
  `pyautogalaxy`/`pyautolens` RTD repo URLs to the PyAutoLabs org.
- Delete dead configs: `PyAutoFit/readthedocs.yml`, `PyAutoGalaxy/readthedocs.yaml`,
  `PyAutoFit/docs/requirements.txt`.
- Converge the three `docs/conf.py`: fix the `nnumpydoc` typo, remove dead `html_context`
  blocks, align the autodoc/numpydoc/typehints configuration on the Galaxy/Lens variant
  (verify PyAutoFit API pages still render before/after), fix or drop the missing
  `_static` references.
- Add a docs CI job to each repo: build the Sphinx docs on PRs touching `docs/` or the
  package (at minimum `sphinx-build`; `-W` only if the existing warning baseline allows —
  otherwise fail on warning-count regression and record the baseline).

## Out of scope

- Theming, the GitHub Pages hub, custom domains → [docs_theming_and_hub.md](docs_theming_and_hub.md).
- `plot.rst` content rewrite (PyAutoLens#592) and API-page staleness beyond what the CI
  warning baseline forces.
- Migrating off ReadTheDocs; versioned/`stable` docs.

## Cross-references

- `PyAutoHeart/heart/checks/url_check_live.py` — existing RTD URL checks; a Heart check
  for "RTD last-build recency" would have caught finding 1 (candidate Heart follow-up,
  not in this phase).
