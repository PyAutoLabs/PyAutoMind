Clear the 9 tenant-firewall mismatches by the decision rule + add PR-time gates so the drift cannot recur silently (issue #198; 9 → OK, and a green `--check` is only evidence for the organs actually checked out)

## Why it recurred in the first place

**No CI anywhere ran the firewall check.** All 9 findings merged through green
PRs between 2026-08-08 and 08-14. Heart's `manifest_drift.py` is exit-0,
local-only, folded into one YELLOW line, and invisible to the cloud health run.
The fix therefore had two halves: clear the 9 *by the rule*, then make the check
run in the PR that authors the drift.

The decision rule (from `complete/2026/08/autohands-firewall-allowlist.md`):
**derivable or arbitrary → refactor; genuine branded fact → declare the
surface.** The naive allowlist-all-9 clear was rejected — it would have grown
`FIREWALL_ALLOWLIST` by 8 entries, against a header that forbids growing it
casually. Net cost of the rule-following clear: **+2 entries**.

## PRs

Phase A + B, all 2026-08-17, merged in a deliberately staged order so every PR
in the arc was green at its own merge:

1. **PyAutoMind#199** (`0562f0d`) — allowlist +2, the `--only <leg>` selector,
   and a `check_heart` leg validating Heart's new `smoke:` block against the
   manifest.
2. **PyAutoHeart#147** (`642fa0d`) — `smoke.py`'s `WORKSPACES`/`IMPORT_NAMES`
   tables extracted to `config/repos.yaml` behind a strict loader; 2 test
   genericisations.
3. **PyAutoBrain#229** (`90d86b0`) — 3 test-fixture genericisations + the gate
   step in `tests.yml`.
4. **PyAutoMind#200** (`e9e99fc`) — the Mind-side `firewall_gate.yml`.

Phase A tail, 2026-08-18 (deferred at the time, see below):

5. **PyAutoHands#237** (`b7496ec`) — the last of the 9. `test_pre_build_staging.py`
   derives its five remaining repo literals from the already-parsed `SPECS`;
   `tests.yml` restructured to `path: PyAutoHands` + sibling PyAutoMind with the
   `--only` gate step.
6. **PyAutoMind#208** (`84dac42`) — adds the PyAutoHands checkout to
   `firewall_gate.yml`, which had deliberately omitted it.

## The deferral, and the trap in it

The Hands leg was deferred because PyAutoHands was claimed by the version-stamp
task (PyAutoHands#235). **That blocker had already cleared when the deferral was
written**: #236 merged at 2026-08-17 22:03 UTC; the comment declaring the leg
blocked was posted at 23:14 UTC, 71 minutes later. The leg then sat unblocked
and unnoticed for a day. Worth remembering when a task parks a leg behind
another repo's claim — re-check the claim before writing the deferral, not just
when picking it back up.

## Trap: a green `--check` is not evidence unless the organ is checked out

`check_tenant_firewall` **silently `continue`s past organs that are not present**
(`repos_sync.py:775`, `# not checked out in this environment`). A cloud container
holding only Mind + Brain reports `check tenant firewall (organ code): OK` while
a live finding sits on Hands `main`. This very nearly closed the task a day
early.

**Read a firewall OK as "OK for the organs present."** Verify against a
four-organ root, or read the count. The same property is what makes the gates
safe (`--only` gates exactly the organ whose PR is running), so it is load-
bearing, not a bug.

## The two "remaining" items were never independent

Heart's `manifest_drift.py` does not reimplement the check — it shells out to
`repos_sync.py --check` and parses the report lines. A full local workspace has
all four organs checked out, so the tenant-firewall YELLOW reason **could not**
drop while the Hands finding stood, no matter how many Heart ticks ran. Item 2
was gated on item 1. With #237 merged there is nothing left to do: the next
local Heart tick drops the reason on its own.

## Verification

- Four-organ root (`Mind + Brain + Heart + Hands`) →
  `check tenant firewall (organ code): OK`, exit 0.
- **Negative probes**, mandated by the allowlist record and re-run after the
  Hands clear: a bogus manifest name injected into a genericised file is flagged
  (exit 1); removing it returns `OK`. The check was not weakened into passing.
- The gate demonstrated itself three times: pre-#199 it failed organ PRs with
  `unrecognized arguments: --only`; pre-organ-merge the Mind gate listed exactly
  the 6 findings still on organ mains; and on #237 the new Hands step went green
  on the PR that added it.
- pytest green: Mind 139, Brain 349, Heart 469. Hands unchanged against pristine
  main in the verifying container (302 passed / 4 skipped / 7 failed both before
  and after — the 7 an environment gap, `ipynb-py-convert` has no wheel there).

## Out of scope, filed separately

- **Phase C** — teach `repos_sync --write` to stamp organ config surfaces from
  the body map, removing the hand-mirroring:
  `draft/feature/pyautomind/repos-sync-config-stamper.md`. The assessment's own
  endgame (§8-4, "the only real engineering in the whole plan").
- A separate open draft, unrelated to the 9:
  `draft/bug/pyautoheart/tenant_firewall_release_run_instance_fact.md`.

## Accepted-by-design notes from the final review

- A malformed `smoke:` spec crashes `check_heart` loudly rather than reporting a
  tidy mismatch — consistent with the strict-loader style.
- `--write` combined with `--only` still runs all writes; no caller does this.

## Original prompt

# Tenant-firewall drift: clear the 9 right + gate recurrence (Aug 2026)

Type: maintenance
Target: pyautomind
Difficulty: medium
Autonomy: supervised
Priority: normal

Heart's manifest-drift check is YELLOW: `PyAutoMind/scripts/repos_sync.py
--check` reports **check tenant firewall (organ code): 9 mismatch(es)**.
Deep-research pass (2026-08-17, three parallel agents over the design docs,
CI surfaces, and each finding) overturned the naive allowlist-all-9 clear and
set the scope to a two-phase arc, per the recorded decision rule
(`complete/2026/08/autohands-firewall-allowlist.md`): **"derivable or
arbitrary → refactor; genuine branded fact → declare the surface."**

## Original request (verbatim)

> sort this: - Heart's one real warning: manifest drift: tenant firewall — 9
> mismatches vs PyAutoMind/repos.yaml. This is the recommended next checkpoint
> to clear YELLOW.

> do deep research that this is the right approach long term to sort it all
> and stop recurrance of any issues

## Research conclusions (evidence in the issue)

- The allowlist reached its intended terminal state 2026-07-10 (72 files /
  262 tokens: "docstring examples + test fixtures + workspace-root defaults
  only", `complete/2026/07/pyautoscientist-4b.md`); it has since accreted to
  109 files / 430 tokens through six reactive drift patches. Growing it
  casually is what the header forbids.
- All 9 findings postdate the July clear; every one merged through a green PR
  because **no CI anywhere runs the firewall check** (organ test workflows
  are deliberately pytest-only; Mind's own CI never executes `repos_sync.py`;
  Heart's `manifest_drift` is exit-0 local-only monitoring invisible to the
  cloud health run). Recurrence is structural until a PR-time gate exists.
- Explicitly rejected shortcut (do not re-propose): teaching the checker to
  ignore comments/docstrings (`complete/2026/08/autohands-firewall-allowlist.md`).

## Phase A — clear the 9 by the decision rule

- `PyAutoHeart/heart/smoke.py`: **extract** `WORKSPACES` + `IMPORT_NAMES` to a
  `smoke:` block in `PyAutoHeart/config/repos.yaml` with a strict loader
  (twin precedents: Heart `version_skew`, Hands `autohands/config/
  workspaces.yaml`, both from `pyautoscientist-3b-config`). Reword the
  residual `--root` help string ("organism root"). Extend `check_heart` in
  `repos_sync.py` to validate the new block's repo names against the manifest.
- **Genericise fixtures** (synthetic names, verified non-load-bearing; add the
  convention comment so real names don't creep back):
  `PyAutoBrain/tests/test_worktree_conflict_guard.py`,
  `test_intake_dashboard.py`, `test_profiling_conductor.py`,
  `PyAutoHeart/tests/test_smoke.py`, `test_release_run.py`.
- `PyAutoHands/tests/test_pre_build_staging.py`: **derive in-file** — replace
  arbitrary repo literals with picks from the already-parsed `SPECS`; rename
  the `PyAutoLabs` fixture dir.
- **Allowlist only the 2 justified**: `_intake.py` +`autofit_workspace`
  (measured-noise docstring where names/counts are the evidence);
  `tests/test_intake_reconcile_ranking.py` (assertions pin resolution against
  the live body map). Net +1 entry / +1 token. Run the exactness/negative-probe
  audit the Aug 5 record mandates on any allowlist growth.

## Phase B — PR-time enforcement (stop recurrence)

- `repos_sync.py main()`: add an `--only <check-label>` selector (all-or-
  nothing today; an organ gate must fail only on the leg it can cause).
- `PyAutoBrain/.github/workflows/tests.yml`: add the firewall step (already
  checks out Brain+Mind side by side — the exact layout `--root` needs).
- `PyAutoHeart/.github/workflows/heart-tests.yml` and
  `PyAutoHands/.github/workflows/tests.yml`: restructure to path-based
  checkout + `PyAutoLabs/PyAutoMind` sibling, add the same step.
- Mind-side leg: run the firewall (four-repo checkout) on PRs touching
  `scripts/repos_sync.py`, so allowlist edits are themselves verified.

## Phase C — filed separately, not in this task

Draft prompt for the design's own endgame (assessment §8-4): teach
`repos_sync --write` to stamp organ config surfaces from the body map +
per-organ policy, removing hand-mirroring entirely.

## Verification

`repos_sync.py --check` → tenant firewall OK, all other legs unchanged;
pytest green in Mind/Brain/Heart/Hands (incl. the touched test files); Heart
`manifest_drift` → "identity in sync"; each organ's amended workflow passes on
its own PR (the gate step proving itself).
