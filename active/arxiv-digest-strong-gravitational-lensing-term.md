# arXiv #papers digest misses papers whose abstract only says "strong gravitational lensing"

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: easy
Autonomy: safe
Priority: normal
Status: formalised

The #papers digest missed arXiv:2607.19459, "Strong Gravitational Lensing
Posterior Sampling in Pixel-Space Using Diffusion Models and Recurrent Inference
Machines" (v1 published 2026-07-21T18:00:00Z, primary `astro-ph.IM`,
cross-listed `astro-ph.CO`). The user reported the miss on 2026-07-23.

Unlike PyAutoMind#79 this is **not** a window bug, and not a category bug:

- The Wed 2026-07-22 02:00 UTC run's announcement band is
  `2026-07-20 18:00 → 2026-07-21 18:00 UTC`, and `parse()` keeps
  `band_start < ts <= band_end`, so an 18:00:00 timestamp is inside the band.
- `cat:` does match cross-lists as documented — `cat:astro-ph.CO AND
  ti:"Recurrent Inference Machines"` returns the paper. The `astro-ph.IM`
  primary category is not the cause.

Root cause: none of the 17 `abs:` phrases in `_ABS` match this abstract. It
says "strong gravitational **lenses**" and "gravitational **lensing**
simulations" — never the literal "strong lensing", never "gravitational lens"
in the singular. Verified against the live arXiv API: the production `QUERY`
returns 300 results without it. arXiv's phrase matching stems most of the
singular/plural pairs in `_ABS` interchangeably (`lensed galaxy`/`galaxies`,
`lensed quasar`/`quasars`, `Einstein ring`/`rings`, `lensed arc`/`arcs` all
overlap 100%), but `abs:"gravitational lens"` does **not** match "gravitational
lenses", so that term contributed nothing here.

Fix: add `"strong gravitational lensing"` to `_ABS`. Measured recall/noise cost
against the live API over 2026-06-01 → 2026-07-23 (current query returns 47
papers in that window):

| candidate term | new papers added | verdict |
|---|---|---|
| `"strong gravitational lensing"` | 5 — the target, a genuinely on-topic lensed arc, and 3 adjacent (SIDM in AREPO, SPT cluster SZ, massive-galaxy dynamics) | ~1 per 10 days, inside the existing false-positive budget the Claude step absorbs |
| `"gravitational lenses"` | 27 — mostly weak lensing, cosmic shear, GW lensing | too noisy, reject |
| `"strong lens"` | 1, off-topic | no recall gain |

This partially reverses the header comment's "deliberately omits the broad
catch-alls 'gravitational lensing' / 'weak lensing' / 'microlensing'" decision.
The qualified phrase stays strong-lensing-shaped where the bare catch-all did
not, so amend that comment rather than leave it contradicting the code.

Also update the module docstring's history paragraph to record this as the
second regression (the first being the #79 rolling-window bug), and add a
network-free regression to `_selftest` asserting that 2607.19459's abstract
text is matched by the term list.

After merge, `workflow_dispatch` the workflow with a `lookback_hours` override
(~72 h) to backfill 2607.19459 into #papers.

<!-- filed from a CLI session on 2026-07-23 after the user reported the miss -->
