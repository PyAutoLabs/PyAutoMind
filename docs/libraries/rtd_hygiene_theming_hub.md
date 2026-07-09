# Docs infrastructure: RTD hygiene, shared PyAuto theming, GitHub Pages hub

Type: docs
Target: libraries
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## Original request (verbatim)

> We've done lots of sweeps of high level functionality or design to ask Fable whether it
> could be improved. This focused on the AI workflow and other things. We haven't asked it
> about how our docs for each project (PyAutoFit, PyAutoGalaxy, PyAutoLens) are set up and
> the link with readthedocs. Can you do a review and census of that and offer feedback?
> Could this be something we move entirely to GitHub pages? Not saying we should but making
> them more PyAuto-bespoke would be cool.

Decision after the review: **middle path** — keep ReadTheDocs hosting, fix the hygiene
findings, make the docs bespoke via shared Furo theming, and add a bespoke hub on GitHub
Pages. Then:

> Ok I don't want to use money for this currently, so I guess set up the github stuff but
> in a way that doesn't cost so I can easily retrofit it with money later.

**Zero-cost constraint:** everything ships on free infrastructure now
(`*.readthedocs.io` + `pyautolabs.github.io`). Custom domains
(`docs.pyautolens.org` etc. — all of pyautolens/pyautofit/pyautogalaxy/pyautolabs/pyauto
`.org` were verified unregistered on 2026-07-09) are a later config-flip retrofit: register
domain → RTD dashboard custom-domain setting per project → Pages CNAME + DNS. Nothing in
this task may hard-bake the `pyautolabs.github.io` hostname in a way that makes that
retrofit require restructuring (use relative links inside the hub; the RTD sites keep
their canonical `*.readthedocs.io` URLs regardless).

## Census findings driving this task (2026-07-09 review)

1. **pyautofit.readthedocs.io has not built since 2026-05-06.** The RTD project points at
   `rhayes777/PyAutoFit.git`; its webhook/connection did not survive the org migration.
   16 docs commits (incl. the Jammy2211→PyAutoLabs URL audit #1265 and the Latent cookbook
   migration) have never reached the live site. PyAutoGalaxy/PyAutoLens RTD point at old
   `Jammy2211/...` URLs but their webhooks survived and build fine (built 2026-07-09).
2. **No docs build in CI** in any repo, and all three `.readthedocs.yaml` set
   `fail_on_warning: false` → docs rot silently (the stale `plot.rst` / PyAutoLens#592 is
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
   (`github_version: "master"`) Furo never reads; only PyAutoLens has brand colors
   (`#7C4DFF`).
5. Only `latest` is published (no `stable`/tags) — acceptable under nightly releases;
   record as a deliberate decision, not in scope to change.

## Scope

### Phase A — RTD hygiene

- **Human legs (RTD dashboard, walk the user through them):** reconnect the `pyautofit`
  RTD project to `PyAutoLabs/PyAutoFit` and confirm a fresh build goes live; update the
  `pyautogalaxy`/`pyautolens` RTD repo URLs to the PyAutoLabs org.
- Delete dead configs: `PyAutoFit/readthedocs.yml`, `PyAutoGalaxy/readthedocs.yaml`,
  `PyAutoFit/docs/requirements.txt`.
- Converge the three `docs/conf.py`: fix the `nnumpydoc` typo, remove dead `html_context`
  blocks, align the autodoc/numpydoc/typehints configuration on the Galaxy/Lens variant
  (verify PyAutoFit API pages still render before/after), fix or create the missing
  `_static` assets.
- Add a docs CI job to each of the three repos: build the Sphinx docs on PRs touching
  `docs/` or the package (at minimum `sphinx-build`; ideally `-W` once the existing
  warning baseline is triaged — if `-W` is not immediately achievable, fail on
  warning-count regression instead).

### Phase B — shared bespoke theming

- One shared PyAuto brand layer for Furo across PyAutoFit/PyAutoGalaxy/PyAutoLens: palette
  (start from Lens's `#7C4DFF`, give each project an accent), logo/wordmark in the
  sidebar, consistent `html_theme_options`, a single `pyauto.css` replicated (or
  vendored via `_templates`) into each repo's `docs/_static/`.
- Light + dark variables both styled (Furo supports both natively).
- Keep the AI-assistant note framing per the existing user-docs convention.

### Phase C — hub on GitHub Pages (zero-cost)

- New repo `PyAutoLabs/pyautolabs.github.io`: a bespoke static landing page — the PyAuto
  front door — linking to the three RTD doc sites, the workspaces, HowToFit/Galaxy/Lens,
  and autolens_assistant. Plain static HTML/CSS (no build framework needed), same brand
  layer as Phase B.
- Deploy via GitHub Pages from the repo (Actions or branch deploy — simplest that works).
- Include a short `RETROFIT.md` recording the paid-domain upgrade path (registrar → DNS →
  RTD custom domain per project → Pages custom domain + CNAME).

## Out of scope

- Migrating doc hosting off ReadTheDocs.
- Versioned/`stable` docs activation.
- The `plot.rst` content rewrite (PyAutoLens#592) and any API-page staleness fixes beyond
  what the CI warning baseline forces.
- PyAutoArray/PyAutoConf public docs (they have none; unchanged).

## Cross-references

- PyAutoLens#592 — stale plot API docs (separate content task).
- `PyAutoHeart/heart/checks/url_check_live.py` — existing RTD URL liveness/rewrite checks;
  a Heart check for "RTD last-build recency" would have caught finding 1 (nice-to-have,
  may be split out to a Heart task).
