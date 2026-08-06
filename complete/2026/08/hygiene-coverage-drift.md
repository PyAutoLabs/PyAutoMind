**Shipped 2026-08-05.** The hygiene conductor scanned a hardcoded list of repos
that had drifted from the body map, so it under-reported debt and reported
`clean` over repos it never opened. The sets are now derived from `repos.yaml`,
and a coverage check keeps them that way.

## PRs

- PyAutoBrain#200 — `fix(hygiene): derive the conductor's repo sets from the body map` (squashed `5cb1c73`)
- PyAutoMind#132 — `feat(repos_sync): check the hygiene conductor's repo coverage` (squashed `c0576aa`)
- Issue: PyAutoBrain#197

## What was wrong

`hygiene.sh` held `LIB_REPOS` (5), `ORG_REPOS` (4) and `DOC_REPOS` (3) as bash
arrays. The body map declares **6 libraries and 7 organs**, so PyAutoCTI and
PyAutoReduce were never scanned, PyAutoNerves was treated as a library where the
map calls it an organ, and 3 organs were uncovered.

The failure mode is the important part: **an unscanned repo produces no
findings, so the conductor reported `clean` and was believed.** Measured before
planning — `crlf` printed `5` `.py` with CRLF against a true `127`, 122 of them
in PyAutoCTI, which has an LF-only rule nobody was enforcing.

## Measured effect (17 repos scanned, was 9)

| mode | before | after |
|---|---|---|
| `crlf` cosmetic `.py` | 5 | 167 |
| `deps` manifests audited | 5 | 8 |
| `docs` repos | 3 | 4 |

## Traps and findings

- **Category alone is the wrong key, and getting this wrong re-creates the bug.**
  PyAutoNerves is `category: organ` yet ships a distribution, so mapping `deps`
  to `category: library` would have *dropped* it. `deps`/`docs` therefore key off
  what a checkout **contains** (`pyproject.toml`, `docs/api/`), not its category.
  This also picked up PyAutoCTI's docs, which the hardcoded triple never saw.
- **Leg A of the drift check is narrower than it looks.** The conductor reads the
  same `repos.yaml` the check does, so a manifest edit moves both sides together
  and they can *never* desynchronise — deriving is the whole point. Found by
  trying to make leg A fail and watching it pass. What it actually guards is the
  **reader**, specifically the PyYAML-free fallback used only where PyYAML is
  absent and verified nowhere else; a `--parser` flag was added so both readers
  run. A deliberately narrowed fallback regex made it report 4 dropped repos.
- **The tenant firewall could not have caught this.** Its entry for `hygiene.sh`
  *allowlisted* the stale names — it asked "are these names permitted here?" when
  the question was "does this cover the organism?". The entry is now **deleted**,
  not updated: the conductor names no instance fact at all, so re-adding one
  would re-permit the drift.
- **`unscanned` vs `clean`.** An empty scan root, or an unreachable body map,
  made every repo-array mode report `clean`. A zero from "nothing was examined"
  and a zero from "nothing was wrong" are indistinguishable to a reader, and only
  one is good news.
- **Scope the `unscanned` signal to the repo-array modes only.** The first cut
  applied it to every mode and broke 20 tests. `docstrings`/`refs`/`optdeps`/
  `extras`/`config` discover their own targets by walking the scan root and can
  legitimately find material the body map never names — suppressing them hides
  real findings. A real finding still leads the recommendation, with a
  partial-ranking caveat.
- **Do not filter `packaging` to repos with a `pyproject.toml`.** Tried, reverted:
  it narrowed detection for no benefit and broke a valid existing test. The
  existing ignore/untracked/depth guards already establish a hit. A comment in
  the source records this so it is not re-attempted.
- **Tests must not name repos.** They derive the expected sets from the body map —
  a test that hardcodes the list under test can only agree with itself, and a
  literal would be an instance fact in an organ test. Mutation-checked: reverting
  `LIB_REPOS` to the stale five fails 2 of the new tests.

## Verification

- PyAutoBrain 212 passed (3.12 + 3.13, the CI matrix); PyAutoMind 88 passed (3.12).
- Both drift-check legs driven with failing input before being trusted.
- `repos_sync.py --check` gains exactly one line, diffed against a stashed
  baseline to prove the tenant-firewall mismatches it still reports are
  pre-existing PyAutoHands drift. (A 7th appeared at merged main from
  PyAutoBrain#199's `test_health_conductor.py` — also not from this task.)

## Deliberately left open

- **The backlog this exposes is unfiled.** 167 cosmetic CRLF (122 in PyAutoCTI),
  41 dep caps across 8 manifests. The prompt scoped triage as a separate task.
- **`HYGIENE_PERF_LIBS` still defaults to `autoconf`**, the pre-rename name of the
  config package, so `perf` silently reports `n/a` for it. Same silent-under-report
  family, different defect — not repo-array coverage.

## Environment note

Cloud session: no worktree and no `gh` CLI, so the issue and both PRs went
through the GitHub MCP surface and work happened in the canonical checkouts on
the mandated branch. The PyAutoMind checkout was **shallow**, which made local
`main` look diverged from `origin/main` by 50 commits with no merge base (and
tripped a stop hook into proposing a 49-commit rebase over the user's own
commits). `git fetch --unshallow` reconnected the history and `main`
fast-forwarded — nothing was rewritten or discarded.

## Original prompt

# Hygiene under-reports debt by 25x because its repo arrays skip

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Hygiene under-reports debt by 25x because its repo arrays skip two libraries. The hygiene conductor scans a hardcoded list of checkouts in PyAutoBrain agents/conductors/hygiene/hygiene.sh. That list is stale: the LIB_REPOS array holds five entries where the body map (repos.yaml) has six, silently skipping the CTI and Reduce libraries, and it mislabels the config layer as a library; ORG_REPOS covers four of seven organs. The result is wrong output, not stale prose. On a real run the crlf mode printed '5 library .py w/ CRLF' when the true count is 127 — 122 of them in the skipped CTI library, breaking that repo's LF-only rule with nobody watching. The deps mode audits five pyproject.toml instead of six; tidy inspects nine of roughly seventeen managed checkouts. Every clean bill of health the conductor has issued understates reality. This is an internal inconsistency, since the sibling scanners _hygiene_config.py and _hygiene_refs.py already reach the CTI library. The drift checker cannot catch the gap: its tenant-firewall entry for hygiene.sh pins the current broken set as an allowlist instead of verifying coverage. The repair should derive the arrays from the body map rather than re-hardcoding them. Widening coverage will surface a large backlog of genuine new findings, so land the coverage repair and the triage of what it uncovers as separate tasks.

<!-- formalised by the Intake (Conception) Agent on 2026-08-05 from user-intake -->
