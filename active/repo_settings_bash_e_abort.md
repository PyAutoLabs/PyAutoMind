# repo_settings.yml aborts silently under GitHub's `bash -e`

Type: bug
Target: pyautobrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-26
Issued: 2026-08-26

Regression in PyAutoBrain#292 (merge `475d292e0`), filed the same day it shipped.
The weekly schedule fires Sunday 06:40, so it fails every week until fixed.

## The bug

GitHub runs a `run:` block as `/usr/bin/bash -e {0}`. `repo_settings.yml` sets
`set -uo pipefail` and never disables `-e`. The per-repo read is:

    before=$(gh api "repos/$slug" --jq '.delete_branch_on_merge' 2>/dev/null)

For an unreadable repo that assignment returns non-zero, so under `-e` the
script aborts **instantly**, and because stderr goes to `/dev/null` it aborts
**silently**. The `case "$before" in ... *)` unreadable handler is dead code in
production, and with it the whole in-org (error) vs out-of-org (warning)
failure-policy split that #292 was partly written to add.

Latent second instance: `[ "$hard" -eq 1 ] && failed=1` is the last statement of
`visit()` in two branches. With `hard=0` the compound returns 1, so the function
returns 1 — which under `-e` aborts on the first out-of-org repo.

The PATCH path is unaffected: `if gh api ...; then` is `-e`-safe.

## Evidence (confirmed, not inferred)

- Run <https://github.com/PyAutoLabs/PyAutoBrain/actions/runs/32992618192>
  (`mode=audit`) failed in 20s with **no stdout at all** between
  `##[endgroup]` and `##[error]Process completed with exit code 1`. The log's own
  env block prints `shell: /usr/bin/bash -e {0}`.
- Reproduced locally: extract the `run:` block, stub `gh` so one repo read
  fails. `bash body.sh` prints the `::warning::` then `::error::` and exits 1
  (graceful, as designed). `bash -e body.sh` exits 1 with **zero output** —
  byte-for-byte the CI signature.

**Corollary: at least one repo read genuinely failed in that run.** The fixed
version must name it; we still do not know which repo, and that is a second
finding hiding behind this one.

## Why it shipped — the actual lesson

#292 *was* control-tested, across 7 scenarios, before merge. The harness ran
`bash <script>`; GitHub runs `bash -e <script>`. **The harness did not match
production**, so it validated a shell mode that never executes. A control test
that does not reproduce the caller's invocation proves nothing about the caller.

## Sibling sweep — already done at filing

Audited every `run:` block in PyAutoBrain. `branch_archive.yml` and
`branch_sweep_all.yml` both **explicitly** `set -e` and use no `2>/dev/null`;
abort-on-error is what they want, so they are consistent, not defective.
`branch_sweep.yml`, `brain_board.yml`, `docs.yml`, `nightly-release.yml` have no
matching pattern. `repo_settings.yml` is the **only** block with no `e`-flag
statement combined with a swallowed stderr. Scope is one file.

## Fix

1. `set +e` immediately after `set -uo pipefail`, commented with why — GitHub's
   default `-e` would abort on the first unreadable repo and skip this script's
   own per-repo reporting. Preferred over sprinkling `|| true`, because the
   script's whole design is to survive per-repo failure and report it.
2. Both `[ "$hard" -eq 1 ] && failed=1` occurrences become `if` blocks, so
   `visit()` never returns non-zero spuriously.
3. **Regression-proof it**: a test that extracts the workflow's `run:` block and
   asserts the unreadable-repo path emits its `::warning::` and the right exit
   code **under `bash -e`**, matching GitHub's invocation. This is the leg that
   was missing. stdlib + PyYAML only, no network — stub `gh` on `PATH`.

## Acceptance

Re-dispatch `repo_settings.yml` in `audit` mode after merge. It must go green
**and** name any repo whose read fails. A green run that names nothing is only
acceptable if every one of the 46 reads genuinely succeeded.
