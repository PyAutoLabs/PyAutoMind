# Docs infrastructure phases B+C: shared PyAuto theming + GitHub Pages hub

Type: docs
Target: libraries
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised

Phase A (rtd_hygiene, PyAutoFit#1341) merged 2026-07-09 — this prompt graduates.
Phase A carried the census findings and the RTD/CI hygiene scope; this prompt holds the
decision record and phases B/C.

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

## Scope (phases B+C; phase A in rtd_hygiene.md)
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
