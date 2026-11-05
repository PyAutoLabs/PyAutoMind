# `ledger_merge.py sync`: bring a non-`claude/**` Mind branch up to date with main…

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
Themes:
- mind-workflow
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-11-05
Consequence: judge
Witness: tests drive a fixture repo — a session branch behind main with entry-level registry changes on both sides and conflicting renders — through `sync_with_base`: status `ready`, registries merged by entry, renders regenerated on the merged tree by the (injected) renderer, merge left staged; `up-to-date` is a no-op; a dirty tree is refused; a non-ledger conflict stops as `blocked` before rendering.
Review-minutes: 5
Unattended: ready

`mind_ledger_merge.yml` settles concurrent-push conflicts for `claude/**`, `codex/**` and
`chatgpt/**` branches (`ledger_merge.py resolve`, then re-render). Session branches (`ccr-*`) and
PR branches holding code get none of that: PyAutoMind#539 needed three rounds of hand conflict
resolution on `dashboard.md` / `dashboard.html` / `state.json` / `complete/index.md` as other
sessions pushed to main every few minutes, and one round kept main's stale index because the
manual regen was a dry run (red `drift` check). A `.gitattributes` merge driver does not help:
GitHub ignores custom drivers. Add `ledger_merge.py sync [--base origin/main]` — merge with
`--no-commit`, `resolve`, re-render the generated files on the merged tree, stage, let the caller
commit — and document it beside the workflow in REFERENCE.md "How the ledger lands".
Extending the auto-merge workflow to `ccr-*` branches is a separate policy decision (not here).

<!-- formalised by the Intake (Conception) Agent on 2026-11-05 from file:/tmp/claude-0/-home-user/ad8c6486-73f7-504b-b742-a7b629366ade/scratchpad/intake/c_sync.md -->
