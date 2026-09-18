# arXiv's Fastly edge refuses `urllib.request` outright — retrying a 406 only delays the failure

Type: bug
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- ci
- robustness
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: a probe script issuing the SAME **uncached** arXiv API URL (cache-busted — a fresh `max_results` or a unique whitespace variant per call, never a repeat) through `urllib.request` and through `requests`, from one host, interleaved. Current expectation: `urllib.request` 406s and `requests` returns 200. After the fix, `_get()` takes the working client and a live `--livecheck` from a clean IP returns PASS rather than `SKIPPED (network)`. Record the `via:` and `x-cache:` response headers for each attempt — a 406 with `via: 1.1 varnish` and no `1.1 google` proves the edge refused it and the origin never saw it.
Review-minutes: 5
Filed: 2026-09-18

Found while shipping PyAutoMind#412 (issue #410), which added `406` to the
retry ladder in `.github/scripts/arxiv_fetch.py`. That change is correct and
strictly better, but the investigation behind it turned up a bigger problem
that it does not solve.

## The finding

The 406 is **not transient**. It never reaches arXiv at all:

- A 406 response carries `via: 1.1 varnish` only — no `1.1 google`, no
  `server: Google Frontend`. **Fastly's edge refuses the request**; arXiv's
  application never sees it. A 200 for the same query carries both.
- Run live from a home IP on 2026-09-18, `--livecheck` exhausted the entire
  5/15/45/90/180 s ladder on 406 and gave up. So this is not specific to the
  shared GitHub Actions egress, which was the assumption #410 was written under.

**Headers are not the discriminator.** Ten combinations were tried across
`urllib.request` and raw `http.client`: bare and contact-bearing User-Agents,
`Accept: */*`, `Accept: application/atom+xml`, `Accept-Encoding: gzip` and
`identity`, `Connection: close` and `keep-alive`, and byte-for-byte copies of
curl's and `requests`' header sets. All 406 on **uncached** URLs.

Meanwhile `curl` (HTTP/2 and `--http1.1`, even carrying Python's exact UA and
headers) and `requests`/urllib3 returned **200** on cache MISSes where stdlib
`urllib.request` got 406. That leaves the **TLS/client fingerprint** — the
stdlib `ssl` ClientHello against urllib3's and curl's — as the leading
hypothesis: Fastly bot mitigation aimed at the stdlib client.

## The trap that makes this hard to measure

**Fastly caching confounds naive probing.** Repeating the same URL returns 200
as a cache HIT while every MISS 406s. An earlier probe in this investigation
concluded "headers are irrelevant, all combinations return 200" and was simply
reading its own cache hits. Any test here MUST use a fresh, uncached URL per
attempt and MUST record `x-cache:`.

Note also that probing escalates the mitigation: by the end of the session the
address was being rate-limited outright, and even `requests` began timing out.
Probe sparingly, from an address you are willing to have throttled.

## Why #412 is not enough

`_get()` now climbs the ladder on a 406 instead of dying on the first request,
and `_livecheck()` warns rather than failing the run. But if the edge refuses
*every* attempt — which is what a fingerprint-based block means — the ~5.5 min
ladder is spent for nothing, `fetch()` raises, and the digest still posts
nothing to Slack. It converts an instant failure into a slow one.

## What to do

1. Confirm the discriminator with the cache-busted witness above, from a clean
   address. If `requests` succeeds where `urllib.request` fails on uncached
   URLs, that settles it.
2. Move `_get()` off `urllib.request`. `requests` 2.32.3 / urllib3 2.4.0 are
   already present locally — confirm they are available in the workflow's
   Python step (it uses `actions/setup-python`, so check rather than assume; a
   `pip install requests` line may be needed).
3. Keep the 406 retry from #412 regardless. Even with a working client, 406
   remains a mitigation response worth backing off on rather than dying on.
4. Re-check `scripts/backfill_arxiv_refs.py` and `scripts/arxiv_refs.py` in
   **PyAutoMemory**, which use `urllib.request` against the same endpoint. They
   have stayed green only because they swallow every exception
   (`draft/bug/pyautomemory/arxiv_refs_swallows_every_api_error_silently.md`) —
   so they may already be resolving nothing, silently, for this same reason.
5. If the fingerprint hypothesis is confirmed, consider whether arXiv's API
   terms expect a declared client; a contact-bearing UA plus a mainstream HTTP
   client is the well-behaved combination, not an evasion.
