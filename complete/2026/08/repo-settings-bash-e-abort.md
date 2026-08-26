Regression in PyAutoBrain#292, found and fixed the same day by the acceptance
dispatch that #292's own close-out called for.

## The defect

GitHub runs a `run:` block as `/usr/bin/bash -e {0}`. `repo_settings.yml` set
`-uo pipefail` and never disabled `-e`, so the per-repo read

    before=$(gh api "repos/$slug" --jq '.delete_branch_on_merge' 2>/dev/null)

aborted the whole script on the first unreadable repo — silently, because that
stderr is discarded. The `case ... *)` unreadable branch, and with it the
in-org/out-of-org failure-policy split #292 had just added, was dead code in
production. A second instance was latent: `[ "$hard" -eq 1 ] && failed=1` ended
`visit()` in two branches and returns 1 when `hard=0`, so the function returned
1 and `-e` aborted on the first out-of-org repo.

## Why it shipped — the lesson worth keeping

#292 **was** control-tested, across seven scenarios, before merge. The harness
ran `bash <script>`; GitHub runs `bash -e <script>`. The harness did not
reproduce the caller's invocation, so seven green scenarios said nothing about
the only mode that actually runs. **A control test that does not reproduce the
caller's invocation proves nothing about the caller.**

## What shipped (PyAutoBrain#294, merge 8b48a93bd)

- `set +e` after `set -uo pipefail`, commented — explicit rather than `|| true`
  on the read, because the hazard applies to every guarded command in the block.
- Both trailing `[ ... ] && failed=1` compounds became `if` blocks.
- `tests/test_repo_settings_workflow.py` — extracts the workflow's `run:` block,
  stubs `gh` on `PATH`, and runs it **under `bash -e`**, the way the runner does.
  `test_the_step_does_not_override_the_shell` pins that assumption so it cannot
  rot silently. Verified non-vacuous: 3 of the 6 fail against the pre-fix
  workflow and pass against the fix.
- Sibling sweep: `branch_archive.yml` and `branch_sweep_all.yml` explicitly
  `set -e` and discard no stderr — intended there, left alone. No other `run:`
  block in the repo combines an inherited `-e` with a swallowed failure.

## Acceptance — passed, and it answered the open question

`audit` dispatch (run 32994175330) went **green** and named what the silence had
hidden:

    warning: Jammy2211/admin_jammy      — could not read the setting
    warning: Jammy2211/euclid_assistant — could not read the setting

That closes the loop. In-org repos are swept first; in `audit` with all 44
already `true` the run prints nothing, so it ran 20s in silence, reached the
first out-of-org repo, and `-e` killed it there. Both are personal-account repos
`PAT_PYAUTOLABS` cannot read — exactly the case the scope split exists for.

## Left open, now visible

The two personal repos are **outside the sweep's reach**. They are `true` today
(set by hand 2026-08-26) but nothing maintains them: either widen the PAT, or
accept them as manually managed. A human decision — the value of this fix is
that it is now a visible warning rather than a silent abort.

Verification: 554 tests pass (548 + 6 new); tenant firewall OK; 47/47 skill
budgets. Heart remained RED on `release validation FAILED` (unrelated, since
2026-08-23); shipped under the same standing human override as #292.

## Original prompt

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
