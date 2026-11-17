# Ears: report private or unreadable repos as excluded, not unavailable

Type: bug
Target: pyautoears
Repos:
- PyAutoEars
Difficulty: small
Status: active
Filed: 2026-11-17
Issued: 2026-11-17
Issue: https://github.com/PyAutoLabs/PyAutoEars/issues/33
Consequence: notify
Community: none

## Request

The Ears community snapshot shows Jammy2211/euclid_assistant and
PyAutoLabs/ECLIPSE_lens_catalogue (both private) as `unavailable`, which reads
as a collection failure. They should be reported as `excluded`, the status the
collector already uses for sources that are not public.

## Cause

The Ears Pages workflow collects with `github.token`, scoped to PyAutoEars, so
`GET repos/<private repo>` returns 404. `GitHub.get` in `ears/collect.py`
raises the generic `ReadError("GitHub read failed (permissions, rate limit or
endpoint)")` before `collect()` reaches its existing
`meta.get("private") is not False` -> `excluded` branch.

## Plan

- `ears/collect.py`: add `class NotFound(ReadError)`; in `GitHub.get`, when
  `gh api` exits non-zero and its stderr indicates HTTP 404 / Not Found, raise
  `NotFound("source not found or not visible publicly")` (bounded text, never
  the payload). In `collect()`, catch `NotFound` on the `repos/{repo}` metadata
  read -> status `excluded`, gap "source is not visible publicly (private or
  missing)", continue. Other ReadErrors (rate limit, 5xx, timeout) stay
  `unavailable`.
- `tests/test_ears.py`: fake API raising `NotFound` for the metadata read ->
  receipt `excluded`, `public_verified` False, no listing call; plain
  `ReadError` still -> `unavailable`; unit test of `GitHub.get` 404
  classification with a stub binary.
- `REFERENCE.md`: the status list says `excluded` also covers sources the
  collector cannot see (private or missing).
- Trade-off accepted: a deleted or mistyped repo also shows as excluded (still
  listed with its gap).
- Brain's adapter (`agents/conductors/community/_ears_feed.py`) only degrades
  partial/unavailable, so no Brain change.
