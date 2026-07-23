# arXiv #papers digest missed a paper on recall, not on the window

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/92
PRs:
- PyAutoMind#93 (merged 2026-07-23)
Status: shipped

The user reported that #papers never carried arXiv:2607.19459, "Strong
Gravitational Lensing Posterior Sampling in Pixel-Space Using Diffusion Models
and Recurrent Inference Machines" (v1 2026-07-21T18:00:00Z, primary
`astro-ph.IM`, cross-listed `astro-ph.CO`).

## The diagnosis

This is the digest's second recorded miss, and it is a **different failure mode
from the first**. #79 was the window (submission-anchored, so announcement lag
dropped papers permanently). This one was **recall**:

- The Wed 2026-07-22 run's announcement band is
  `2026-07-20 18:00 → 2026-07-21 18:00 UTC`, and `parse()` keeps
  `band_start < ts <= band_end`, so the paper's 18:00:00 stamp is inside it.
- `cat:` matches cross-lists as documented; `cat:astro-ph.CO AND
  ti:"Recurrent Inference Machines"` returns the paper, so the `astro-ph.IM`
  primary category was irrelevant.
- None of the 17 `abs:` phrases matched the abstract, which says "strong
  gravitational **lenses**" and "gravitational **lensing** simulations" and
  never the literal "strong lensing".

**The two failure modes are indistinguishable from outside** — in both cases a
paper simply never appears. Check the band and the `cat:` clause before touching
the query.

## The fix

Added `abs:"strong gravitational lensing"`. Candidates were measured against the
live API over 2026-06-01 → 2026-07-23, where the query already returned 47:

| candidate | new papers | verdict |
|---|---|---|
| `"strong gravitational lensing"` | 5 — the target, an on-topic lensed arc, 3 adjacent | ~1 per 10 days, inside the budget the Claude step absorbs |
| `"gravitational lenses"` | 27 — mostly weak lensing, cosmic shear, GW lensing | rejected |
| `"strong lens"` | 1, off-topic | no recall gain |

This partly reverses the "deliberately omits *gravitational lensing*" decision
from the original build; the qualified phrase stays strong-lensing-shaped where
the bare catch-all did not, and the comment was amended to say so.

## Two findings worth keeping

1. **arXiv stems most singular/plural pairs in `_ABS`, but not all.**
   `lensed galaxy`/`galaxies`, `lensed quasar`/`quasars`, `Einstein
   ring`/`rings`, `lensed arc`/`arcs` each return identical sets — but
   `abs:"gravitational lens"` shares nothing with `abs:"gravitational lenses"`,
   which is why the existing singular term did not catch this paper. Never
   assume a singular term covers its plural; measure it.
2. **An offline "the term appears in the abstract" regression is invalid.**
   arXiv matched 2607.19459 by stemming "lensing" to "lenses"; the literal
   phrase `strong gravitational lensing` is *not* in the abstract, so a
   substring assertion would fail against a working query. This was the planned
   test in the issue and had to be replaced.

## The guard that replaced it

`--livecheck` intersects the production `QUERY` with `id_list` of every paper a
past query missed (#79's pair, plus this one) and fails if any is no longer
returned. `id_list` intersects `search_query`, so it asks arXiv directly "would
today's query return this paper?" — unlike a look-back over recent results, it
does not age out. It runs in the workflow immediately before the fetch, which
needs the same API anyway, so it adds no new failure mode. Verified
non-vacuous: with the new term removed it fails on 2607.19459 alone.

The offline `--selftest` retains only an assertion that the term is still in
`_ABS`.

## Post-merge

Backfilled with `workflow_dispatch lookback_hours=72` (run 29992352979, green):
3 papers posted to #papers including 2607.19459. The other two had already gone
out on the 07-22 run — all three share an 18:00:00 timestamp, so no smaller
look-back could isolate the target. The user accepted the duplicates.

## Original prompt

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
