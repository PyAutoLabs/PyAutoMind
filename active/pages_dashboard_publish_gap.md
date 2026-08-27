# The Mind board goes stale precisely when the render is correct — `dashboard_refresh.yml` publishes only from its self-heal path

Type: bug
Target: ci
Repos:
- @PyAutoMind
Difficulty: low
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27

Found 2026-08-27 when the user reported a retired prompt
(`smoke_install_stale_jax_pin`) still rendering as a pickable chip on
https://pyautolabs.github.io/PyAutoMind/ — roughly 1.5 hours after the retirement
landed on `main`. `dashboard.html` on `origin/main` was already correct (0 hits);
only the *published* surface lagged, by four commits.

## The defect

`.github/workflows/dashboard_refresh.yml` dispatches the Pages publisher
(`gh workflow run pages_dashboard.yml`, line ~166) from **inside its self-heal
branch only**. The job's first act is:

```bash
if check; then
  exit 0
fi
```

so when the committed render is *already fresh* the workflow returns before ever
reaching the dispatch. The publisher is never asked, and `pages_dashboard.yml`'s
own trigger (`push: main`, `paths: [dashboard.html]`) cannot cover the gap
because the commit that landed the fresh page was pushed with `GITHUB_TOKEN`.

The full chain that stranded the board:

1. A session regenerates `dashboard.html` correctly on a `claude/**` branch and
   pushes.
2. `mind_ledger_merge.yml` merges it to `main` with `GITHUB_TOKEN` — GitHub's
   recursion guard fires no `push` event, so `pages_dashboard.yml` does not run.
   That workflow's own heal loop dispatches only `dashboard_refresh.yml` and
   `lifecycle_drift.yml`.
3. `dashboard_refresh.yml` runs on `main`, `check` passes, `exit 0` — publisher
   never dispatched.

Observed: `Pages Dashboard` last ran 2026-08-27T19:15:13Z (a real-credential
push); the ledger merges at 19:29, 19:30 and 20:09 produced `Mind Ledger Merge` /
`Dashboard Refresh` / `Lifecycle Drift` runs and **no** `Pages Dashboard` run.

## Why it matters

Two things make this worse than a lag.

- **It is not self-healing.** The nightly `cron: "20 3 * * *"` takes the same
  `exit 0` path, so a board stranded this way stays stranded until some push to
  `main` touching `dashboard.html` is made with a non-`GITHUB_TOKEN` credential.
  That is incidental, not guaranteed.
- **The failure is inverted.** The page goes stale *because* the session did its
  job properly. Had the session left the render stale, the self-heal would have
  fired and published. A correct upstream produces the broken outcome, which is
  why nothing downstream reads as wrong: `git show origin/main:dashboard.html` is
  perfect and every workflow run is green.

The user-visible cost is a re-pick: a chip for shipped work stays tappable, and
`/start_dev` gets launched on a task that is already closed. That has now
happened to `smoke_install_stale_jax_pin` twice
(`complete/2026/08/smoke-install-stale-jax-pin.md` documents the first).

This is the third bite of the same `GITHUB_TOKEN` trap. The fix for bite two
(`a305a293`, 2026-08-21) added the right dispatch on the wrong branch of the
flow — it addressed the self-heal case and left the already-fresh case open.

## Suggested scope

1. Make `dashboard_refresh.yml`'s contract *"after I run on `main`, Pages
   reflects `main`"* — dispatch the publisher on the already-fresh path too, not
   only after a heal. Keep PR runs dispatch-free (they must not publish).
2. Consider also adding `pages_dashboard.yml` to `mind_ledger_merge.yml`'s heal
   loop, so the publish does not depend on `dashboard_refresh` being reached at
   all. `pages_dashboard.yml` already declares `concurrency: group: pages,
   cancel-in-progress: true`, so a duplicate dispatch collapses rather than
   racing — confirm that is true of a deploy already in flight before relying on
   it.
3. Verify by replaying the real chain — land a ledger-only change through
   `mind_ledger_merge.yml` and assert a `Pages Dashboard` run appears for it —
   rather than inferring from a green `Dashboard Refresh`.
4. Leave a comment at the `if check; then exit 0; fi` site recording *why* the
   publisher is dispatched there, so the early return is not "simplified" back.

## Out of scope

The sibling boards. `PyAutoHands/release_board.yml`,
`PyAutoMemory/knowledge_board.yml` and `PyAutoScientist/organism_board.yml` each
render and `actions/deploy-pages@v4` in a *single* run, so they cannot desync.
PyAutoMind is the only board split into a renderer plus a separate publisher,
which is what creates the gap. PyAutoHeart has no board workflow. Checked
2026-08-27; no change needed in any of them.

## Diagnostic worth keeping

"The renderer is working" is not evidence the page published. Compare the
**publisher's** last run against the artifact's last commit:

```bash
gh run list --repo PyAutoLabs/PyAutoMind --workflow pages_dashboard.yml --limit 3
git -C PyAutoMind log -1 --format=%ci origin/main -- dashboard.html
```

Immediate unblock (already applied on 2026-08-27, run 33114834609):
`gh workflow run pages_dashboard.yml --repo PyAutoLabs/PyAutoMind --ref main`.

<!-- Sizing: declared low; the sizing faculty derives large (8) and recommends
     split-into-phases. Kept at low and NOT phased — the change is a handful of
     YAML lines in one workflow file plus a replay to verify. The prompt is long
     because the evidence chain is (three workflows, a token-recursion rule and a
     run-history comparison), not because the work is. Same call, and the same
     reason, as complete/2026/08/smoke-install-stale-jax-pin.md.
     The faculty's PyAutoMemory hits (wiki/cti "trap", wiki/methods "jax") are
     keyword collisions — neither is relevant here. -->
