- completed: 2026-08-23
- release: autonerves/autofit/autoarray/autogalaxy/autolens 2026.8.23.1
- nerves source released: 0ecefa0 (PRs #154 stamp, #155 header comment, #152 jax cap <0.12.0)

Released from the CLI after two cloud sessions could not gate it. Every instrument
that was blind in the web session measured here: `gh` authenticated, 25 repos
scanned, `version_skew` resolved 7 floors (the cloud reported "0 floors"), and
no reason read "status unknown".

**THE PARKED "UNKNOWN LOCAL BLOCKER" IS DIAGNOSED.** It was not the handoff
prompt. `pyauto-heart readiness` returns the verdict string `stale`, and
`PyAutoBrain/agents/conductors/build/build.sh` maps only `unknown` onto YELLOW
(`eff="yellow"` at the `[[ "$verdict" == "unknown" ]]` line). `stale` matches no
case arm, falls through to `*)`, and aborts with exit 4 and the blocker
"Could not obtain a readiness verdict ('stale')." **`--force` is unreachable from
`stale`** — it is only consulted inside the `yellow)` arm. So a stale Heart cannot
be forced past, only cleared. Any future session that hits this must run the
validation stages, not reach for `--force`.

Clearing it required the full Stages 0-3 path, and both stages were needed:
- Stage 2 alone (`release rehearse`) left `profile '?' is not 'release'` — the
  rehearsal artifact carries no profile field.
- Stage 3 (`release-integrate.yml`, ~65min) supplies `profile: release` and the
  passing integrate stage. Note `pyauto-heart validate --ingest` REPLACES the
  stored report, so ingesting Stage 2 alone destroyed the pre-existing passing
  integrate report and moved the reason rather than clearing it. Ingest both
  stages from ONE directory.
- A stage report's embedded `commit_shas` is applied last-writer-wins over the
  `--commit-shas` seed, so Stage 3 must be re-run (not just Stage 2) whenever the
  captured SHAs go stale.

**THE VERSION DATE ROLLS AT UTC MIDNIGHT.** `release.yml` computes the version
from the runner's UTC date, so `minor_version` is not stable across a long
validation window: the first cycle resolved 2026.8.22.2, and after the UTC
rollover the correct input became `minor_version=1` for 2026.8.23.1. Re-check
`date -u` immediately before every dispatch.

**PRE-EXISTING, NON-BLOCKING: `run_smoke_tests` red does not stop a release.**
The 21h-earlier run (32542888112) is recorded as `failure` but its five `release`
jobs all succeeded — that run is what published 2026.8.22.1. The `release` job's
`needs:` is only `resolve_mode, release_test_pypi, version_number`; workspace
integration moved to Heart. The failure is
`autolens_workspace/scripts/imaging/modeling.py:641`, which guards on
`files/tracer.json` existing and then reads a different file,
`image/tracer.fits`, that TEST_MODE never writes. Guard present since April,
script untouched since 2026-08-04. It is TEST_MODE-specific: Stage 3 ran the same
script at release fidelity and passed. Filed separately.

**Payload control-tested before publishing**, not assumed: writing through
`hdu_list_for_output_from` + `write_hdu_list` produced `SMALLDAT` as a genuine
FITS boolean (`True`/`False`, not the string that `bool("F")` would invert),
<= 8 chars, correct under both regimes, and `PIXSCALE`'s comment came back `''`
confirming #155 removed the `[']` literal.

The workspace smoke suite was deliberately NOT run in full here (deferred to an
overnight run); Stage 3 covers the same surface at release fidelity, 672p/0f.

**Follow-up opened in the same session:** PyAutoArray#481 bumped the floor from
`autonerves>=2026.8.22.1` to `>=2026.8.23.1`, verified against the published
wheel in a clean venv rather than the source tree. The shape fallback,
`_is_capped_at_the_current_cap`, and the duplicated `"SMALLDAT"` literal were all
deliberately left alone, and the PyAutoLens#687/#702 comment was added to rather
than replaced.

**Reconciled 2026-09-04 — #481 was superseded, not merged.** The same floor bump
landed on `main` through the task recorded in
[`bump-autonerves-floor.md`](bump-autonerves-floor.md)
([PyAutoArray#482](https://github.com/PyAutoLabs/PyAutoArray/issues/482) ->
[PyAutoArray#483](https://github.com/PyAutoLabs/PyAutoArray/pull/483), merged
`0f75c3d278066c4337c9186c16a7770769fe8c5f` 2026-08-23), which reached the same
conclusion on the `"SMALLDAT"` literal and rewrote the comment that named the
old floor. `pyproject.toml` on `main` carries `autonerves>=2026.8.23.1` today, so
the shipped state is exactly what #481 proposed.
[PyAutoArray#481](https://github.com/PyAutoLabs/PyAutoArray/pull/481) was
therefore **closed unmerged as superseded**; its branch
`claude/autonerves-floor-regime-stamp` carries nothing `main` does not.
