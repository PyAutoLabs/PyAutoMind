#!/usr/bin/env python3
"""Shortlist the day's non-strong-lensing arXiv papers into arxiv_interest_candidates.json.

The sibling of ``arxiv_fetch.py``, and deliberately its opposite. That script
asks a narrow question — *which of today's papers are about strong lensing?* —
and answers it with a keyword query precise enough that Claude only has to drop
the odd false positive. This one asks a broad one: *of everything announced
today, which ten would this reader most want to see?* Broad is the point (the
reading interest is black holes, dark matter, galaxy formation, statistics, and
whatever else is good), so there is no query narrow enough to answer it, and no
budget to hand Claude the whole day's astro-ph either.

So the work is split the way it always is here — a deterministic, testable
stage that RANKS, and a Claude stage that JUDGES:

1. Fetch the whole announcement band across the reading categories, paging
   until the band is covered (a band is a few hundred papers, not the handful
   the lensing query returns — hence ``fetch(..., start=)``).
2. Score each paper against the interest profile below: term hits in the title
   count triple, in the abstract once, and the best-scoring topic becomes the
   paper's suggested reading-queue section. Papers scoring nothing are dropped.
3. Write the top :data:`CANDIDATE_CAP` with full abstracts. Claude reads that
   file, drops what the keywords oversold, and picks the final ten.

The scoring is a shortlist, never a verdict: it exists to get the candidate
list down to something one prompt can read closely, and it is generous on
purpose — recall first, exactly as the lensing query is.

**Strong lensing is not excluded here, only flagged.** Those papers have their
own list (``arxiv_papers.yml`` → PyAutoMemory's ``arxiv-inbox.md``) and must
not appear twice, but a *deterministic* exclusion would open a gap: a dark
matter paper that mentions a lensing constraint in passing matches the lensing
net, gets dropped by the lensing digest as off-topic, and then falls through
both lists. So each candidate carries ``strong_lensing``, and the prompt drops
the ones genuinely about it — one judgement, in the place that can make it.

Window and band maths are ``arxiv_fetch.py``'s, imported rather than restated:
the two digests must take the same band or a paper can land in the seam.

Usage:
    python3 .github/scripts/arxiv_interests.py [--selftest]
"""
import datetime as dt
import json
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arxiv_fetch  # noqa: E402

#: The reading categories. astro-ph.HE carries the black-hole and transient
#: work that .CO/.GA do not; .IM carries the instrumentation and methods
#: papers. `cat:` matches cross-lists, so a stats-heavy paper whose primary
#: category is stat.ME is still caught when it cross-lists to astro-ph.
CATEGORIES = ("astro-ph.CO", "astro-ph.GA", "astro-ph.HE", "astro-ph.IM")
QUERY = " OR ".join(f"cat:{c}" for c in CATEGORIES)

#: How many papers the final list holds. The human asked for ten a day.
PICK_COUNT = 10

#: How many the prompt gets to choose from. Enough that ten good ones are
#: reliably in there, small enough that one prompt can read every abstract
#: closely — the whole reason for the scoring stage.
CANDIDATE_CAP = 60

#: Paging: the API caps a page at ~200 and a 3-day Monday band is several
#: hundred papers. The cap is a runaway guard, not an expected limit; hitting
#: it is reported rather than swallowed.
PAGE_SIZE = 200
MAX_PAGES = 12

#: The interest profile. Each topic's terms are matched case-insensitively as
#: substrings against title and abstract; the topic that scores highest becomes
#: the paper's suggested reading-queue section, so these names are
#: PyAutoMemory `reading-queue.md` section headers, verbatim — a name that
#: matches nothing there falls back to `## Interests` on the Memory side rather
#: than stranding the paper.
#:
#: Generous by design. A term that pulls in the occasional off-topic paper
#: costs one line of a 60-paper shortlist that Claude then ignores; a term
#: missing costs a paper that never appears at all. Recall first.
INTERESTS = {
    "SMBHs": (
        "black hole", "black holes", "supermassive", "smbh", "agn",
        "active galactic nucle", "quasar", "blazar", "accretion disc",
        "accretion disk", "tidal disruption", "event horizon",
        "binary black hole", "gravitational wave", "pulsar timing",
        "nanohertz", "m-sigma", "reverberation mapping", "jet",
        "eddington", "seed black hole", "intermediate-mass black hole",
        "little red dot", "sgr a*", "event horizon telescope",
    ),
    "Dark Matter": (
        "dark matter", "wimp", "axion", "sterile neutrino", "self-interacting",
        "subhalo", "substructure", "halo mass function", "cold dark matter",
        "warm dark matter", "fuzzy dark matter", "ultra-light",
        "primordial black hole", "direct detection", "annihilation",
        "dark energy", "modified gravity", "mond", "stellar stream",
        "dwarf spheroidal", "core-cusp", "missing satellites",
        "cosmological simulation", "n-body",
    ),
    "Galaxy Formation / Evolution": (
        "galaxy formation", "galaxy evolution", "star formation",
        "stellar population", "initial mass function", "quenching",
        "quiescent", "feedback", "outflow", "circumgalactic",
        "interstellar medium", "morphology", "bulge", "disc galaxy",
        "disk galaxy", "elliptical galaxy", "early-type galaxy",
        "merger", "high-redshift", "high redshift", "jwst", "cosmic noon",
        "reionization", "reionisation", "stellar halo", "globular cluster",
        "metallicity", "chemical evolution", "ifu", "integral field",
        "scaling relation", "stellar mass function", "dust",
    ),
    "Stats": (
        "bayesian", "inference", "posterior", "likelihood", "mcmc",
        "nested sampling", "sampler", "hamiltonian monte carlo",
        "variational", "simulation-based inference", "neural ratio",
        "normalizing flow", "normalising flow", "emulator",
        "gaussian process", "machine learning", "deep learning",
        "neural network", "transformer", "diffusion model",
        "uncertainty quantification", "model selection", "evidence",
        "hierarchical model", "systematics", "calibration",
        "probabilistic programming", "differentiable", "jax",
        "convolutional", "anomaly detection", "interpretab",
    ),
}

#: Weights: a term in the title is what the paper is ABOUT; the same term in
#: the abstract may be one sentence of context.
TITLE_WEIGHT = 3
ABSTRACT_WEIGHT = 1

#: The strong-lensing net, borrowed whole from the other digest so the two
#: cannot drift apart on what "strong lensing" means. Used only to FLAG.
LENSING_TERMS = tuple(t.lower() for t in (arxiv_fetch._ABS + arxiv_fetch._TI))


def score(title: str, abstract: str) -> tuple[int, str | None, dict]:
    """``(total, best_topic, per_topic)`` for one paper against the profile."""
    lo_title, lo_abs = title.lower(), abstract.lower()
    per: dict[str, int] = {}
    for topic, terms in INTERESTS.items():
        n = 0
        for term in terms:
            if term in lo_title:
                n += TITLE_WEIGHT
            if term in lo_abs:
                n += ABSTRACT_WEIGHT
        if n:
            per[topic] = n
    if not per:
        return (0, None, per)
    best = max(per, key=lambda k: (per[k], k))
    return (sum(per.values()), best, per)


def is_lensing(title: str, abstract: str) -> bool:
    """Whether the strong-lensing digest's own net would catch this paper."""
    text = f"{title}\n{abstract}".lower()
    return any(term in text for term in LENSING_TERMS)


def rank(papers: list[dict], cap: int = CANDIDATE_CAP) -> tuple[list[dict], int]:
    """Score, drop the unscored, sort, cap. Returns ``(candidates, scored)``.

    Ties break on the arXiv id rather than input order, so a re-run of the same
    band produces the same shortlist — a digest whose output moves when nothing
    moved is one nobody can debug.
    """
    scored = []
    for p in papers:
        total, topic, per = score(p["title"], p["abstract"])
        if not total:
            continue
        scored.append({**p,
                       "topic": topic,
                       "score": total,
                       "topic_scores": per,
                       "strong_lensing": is_lensing(p["title"], p["abstract"])})
    scored.sort(key=lambda p: (-p["score"], p["url"]))
    return (scored[:cap], len(scored))


def arxiv_id(url: str) -> str:
    """`http://arxiv.org/abs/2608.21253v1` → `2608.21253`."""
    return url.rsplit("/", 1)[-1].split("v")[0]


def collect_band(band_start, band_end) -> tuple[list[dict], bool]:
    """Every paper announced in the band, paging until it is covered.

    Returns ``(papers, truncated)`` — truncated when :data:`MAX_PAGES` ran out
    before the band did, which is a real (if unexpected) loss of the band's
    oldest papers and is reported rather than swallowed.
    """
    seen: set[str] = set()
    out: list[dict] = []
    truncated = True
    for page in range(MAX_PAGES):
        raw = arxiv_fetch.fetch(QUERY, PAGE_SIZE, start=page * PAGE_SIZE)
        root = ET.fromstring(raw)
        entries = root.findall(f"{arxiv_fetch.ATOM}entry")
        if not entries:
            truncated = False
            break
        oldest = None
        for paper in arxiv_fetch.parse(raw, band_start, band_end):
            if paper["url"] in seen:
                continue
            seen.add(paper["url"])
            out.append(paper)
        for entry in entries:
            published = entry.findtext(f"{arxiv_fetch.ATOM}published")
            if published:
                oldest = dt.datetime.fromisoformat(published.replace("Z", "+00:00"))
        if oldest is not None and oldest <= band_start:
            truncated = False
            break
    return (out, truncated)


def _selftest() -> int:
    """Scoring and ranking, no network."""
    failures = 0

    def check(label, ok):
        nonlocal failures
        failures += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {label}", file=sys.stderr)

    total, topic, _ = score("A tidal disruption event in a quiescent nucleus",
                            "We report an accretion disc flare around a "
                            "supermassive black hole.")
    check(f"black-hole paper scores ({total}) and routes to SMBHs ({topic})",
          total > 0 and topic == "SMBHs")

    _, topic, _ = score("Constraints on ultra-light dark matter",
                        "We use stellar streams to bound the axion mass.")
    check(f"dark-matter paper routes to Dark Matter ({topic})",
          topic == "Dark Matter")

    _, topic, _ = score("Simulation-based inference with misspecified models",
                        "A normalizing flow posterior over nuisance "
                        "parameters, validated by nested sampling.")
    check(f"methods paper routes to Stats ({topic})", topic == "Stats")

    _, topic, _ = score("Quenching of massive galaxies at cosmic noon",
                        "JWST spectroscopy of the stellar populations of "
                        "quiescent galaxies.")
    check(f"galaxies paper routes to Galaxy Formation ({topic})",
          topic == "Galaxy Formation / Evolution")

    total, _, _ = score("A new species of Antarctic lichen",
                        "Nothing here is astronomy at all.")
    check("an unrelated paper scores zero", total == 0)

    # The title carries the topic; the abstract only mentions it.
    title_hit, _, _ = score("Dark matter in dwarf galaxies", "Unrelated prose.")
    abs_hit, _, _ = score("Unrelated title", "We mention dark matter once.")
    check(f"a title hit outweighs an abstract hit ({title_hit} > {abs_hit})",
          title_hit > abs_hit)

    check("a lensing paper is flagged, not dropped",
          is_lensing("An Einstein ring in COSMOS", "A strongly lensed source."))
    check("a non-lensing paper is not flagged",
          not is_lensing("A quiescent galaxy at z=5", "JWST spectroscopy."))

    papers = [
        {"title": f"Dark matter paper {i}", "abstract": "dark matter halo",
         "url": f"https://arxiv.org/abs/2608.{i:05d}"} for i in range(20)
    ] + [{"title": "Unrelated", "abstract": "nothing", "url": "x"}]
    top, scored = rank(papers, cap=5)
    check(f"rank drops the unscored and caps ({len(top)} of {scored})",
          len(top) == 5 and scored == 20)
    check("rank is deterministic", rank(papers, cap=5)[0] == top)
    check("every candidate carries a topic and a lensing flag",
          all(p["topic"] and "strong_lensing" in p for p in top))

    print(f"selftest: {'PASS' if not failures else f'{failures} FAILURE(S)'}",
          file=sys.stderr)
    return 1 if failures else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()

    now = dt.datetime.now(dt.timezone.utc)
    override = os.environ.get("LOOKBACK_HOURS", "").strip()
    if override:
        mode = "lookback"
        band_start, band_end = now - dt.timedelta(hours=float(override)), now
    else:
        mode = "announcement-band"
        band_start, band_end = arxiv_fetch.announcement_band(now)

    uk_date = os.environ.get("UK_DATE") or now.strftime("%Y-%m-%d")
    band, truncated = collect_band(band_start, band_end)
    candidates, scored = rank(band)
    if truncated:
        print(f"::warning::paged out after {MAX_PAGES} pages without reaching "
              f"the start of the band — the band's oldest papers were not "
              f"considered today.", file=sys.stderr)

    out = {
        "uk_date": uk_date,
        "mode": mode,
        "since": band_start.isoformat(),
        "until": band_end.isoformat(),
        "categories": list(CATEGORIES),
        "pick": PICK_COUNT,
        "band_count": len(band),
        "scored_count": scored,
        "truncated": truncated,
        "count": len(candidates),
        "papers": [{"title": p["title"],
                    "authors": p["authors"],
                    "abstract": p["abstract"],
                    "url": p["url"],
                    "id": arxiv_id(p["url"]),
                    "primary_category": p["primary_category"],
                    "published": p["published"],
                    "topic": p["topic"],
                    "score": p["score"],
                    "strong_lensing": p["strong_lensing"]}
                   for p in candidates],
    }
    with open("arxiv_interest_candidates.json", "w") as f:
        json.dump(out, f, indent=2)

    print(f"mode={mode} band={band_start.isoformat()}..{band_end.isoformat()} "
          f"announced={len(band)} scored={scored} shortlisted={len(candidates)}",
          file=sys.stderr)
    for p in candidates[:15]:
        flag = " [lensing]" if p["strong_lensing"] else ""
        print(f"  {p['score']:>3}  [{p['topic']}]{flag} {p['title'][:64]}",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
