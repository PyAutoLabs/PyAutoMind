# docs: generated "Where to file" block routes user reports to the Discussions hub

Every public AGENTS.md now tells an agent that a report from a user or collaborator (a question, an idea, a bug, a result) goes to the org Discussions hub, not to a repo's Issues, and that the agent drafts the post for the human rather than running `gh issue create`. It came from a collaborator's question on Slack on 2026-09-27. Sam asked: "is there a flag in the agents.md files for this so that if I use Claude to raise an issue it will automatically see that the issue should go there and not through GitHub?" There was none.

- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/442
- completed: 2026-09-27
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/443
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/425
- heart-ack: "manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml; manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source"

## Shipped

- Both PRs merged on 2026-09-27:
  - [PyAutoMind#443](https://github.com/PyAutoLabs/PyAutoMind/pull/443) at `bf4f8db7` (branch head `9450973e`)
  - [PyAutoBrain#425](https://github.com/PyAutoLabs/PyAutoBrain/pull/425) at `64861372` (branch head `62514c6f`)
  - At close-out, both branch heads were proven ancestors of `origin/main`.
- **Policy:** `policy/where_to_file.md` (11 lines) is the *what*. It names the hub, the categories (Help & Questions, Ideas & Proposals, Bugs & Errors, Show and tell; Announcements is maintainers-only), forbids `gh issue create` for such reports, and exempts the dev flow. `policy/community_surface.md` stays the *why*.
- **Generator:** `scripts/repos_sync.py` gained a `repos_sync:filing` block:
  - `load_filing_policy`
  - `check_filing_blocks`, which reports a missing copy rather than skipping it, and says which of three states it is in: stale, missing with deliverable markers present, or no markers at all
  - `insert_filing_markers`, which inserts the block itself under the deliverable block
  - `write_filing_blocks`, a narrow writer
  - the check label "where-to-file blocks (generated)"
- **Rollout (human-approved: a bot push, not a PR wave):** `session_hook_propagate.yml` calls `write_filing_blocks` and stages `AGENTS.md`. It writes this block only and never the map blocks, and it is also triggered by `policy/where_to_file.md`.
- **Firewall gate:** the `hookpr` step gained an independent `filing_pr` output. On a policy PR it pins PyAutoMind's own block first, then skips the where-to-file leg with a loud banner. The hook and filing skips combine when both fire, and nothing is skipped on a push to main.
- **Exemption:** `repos.yaml` records `filing_block: false` for euclid_assistant, a private single-user assistant outside the propagation job's reach. It is neither written nor reported.
- **Skills:** Mind `skills/create_issue` stops before `gh issue create` on a user-facing report and drafts the Discussion instead. Brain `skills/intake` routes outsider reports the same way; intake files a Mind prompt only once the maintainer decides to act on one.

## Validation

- **Suites:**
  - Mind: 617 passed after the rebase.
  - Brain: 1078 passed on the full suite; 212 passed on `-k "intake or skill"` after the rebase.
  - Gate tests (`test_session_hook_sync.py`): 59 passed.
- **Mutation checks** (each one had to make the named tests fail):

  | Mutation | Tests that failed |
  |---|---|
  | Stale copy not reported | 2 |
  | Missing-with-deliverable state skipped | 2 |
  | No-markers state skipped | 2 |
  | Marker insertion removed | 3 |
  | Leg unregistered | 1 |
  | Gate: filing `--skip` dropped | 6 |
  | Gate: `filing_pr` forced false | 5 |
  | Gate: compensating `-k` broken | 4 |
  | Exemption ignored | 1 |

- **CI on the PRs:** the firewall gate passed on #443, and the filing skip fired on its first real run (compensating step `1 passed, 20 deselected`, then the skipping drift check). Brain pytest 3.12 and 3.13 passed.
- **Pre-merge check mode:** "where-to-file blocks (generated): 36 mismatch(es)". All 36 were siblings in the "run --write" state; none needed markers placed by hand.

## Rollout snapshot (16:21Z, one look)

- Propagation run 36332804243 finished `completed success` on `bf4f8db7`. Its log shows 36 `AGENTS.md` diffs pushed and 36 marker insertions, with no warnings or errors.
- The post-merge firewall push run 36332804151 on `bf4f8db7` finished `completed success`.

## Notes

- The parallel claim with eyes-organ-order (PyAutoMind#439) was human-approved. The two tasks touched disjoint regions, and this task shipped first.
- Organ repos are not released to PyPI, so no `pending-release` label or lines were added.

## Original prompt

# docs: "Where to file" block in every public AGENTS.md — route user reports to the Discussions hub

Type: docs
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Lane: any
Issued: 2026-09-27

## Request (2026-09-27, from the collaborator Slack)

> Jam: All issues for any project should be posted here
> https://github.com/orgs/PyAutoLabs/discussions and NOT on their individual
> GitHub Issues page. When posts go there we will be notified about it here on
> SLACK.
>
> Sam: is there a flag in the agents.md files for this so that if I use Claude
> to raise an issue it will automatically see that the issue should go there
> and not through GitHub?

There is no such flag. `policy/community_surface.md` (PyAutoMind#403/#411/#426)
already decides that users go to the one org Discussions hub, and the README
"Community & Support" sections and issue choosers were regenerated from it —
but no `AGENTS.md` or `CLAUDE.md` in the workspace mentions Discussions (grep
over the root, every organ, every library, workspace and assistant checkout),
and the only issue-filing recipe an agent sees is `create_issue`'s
`gh issue create` on the target repo. A contributor's Claude reading their
clone of PyAutoLens today opens a repo issue.

## Ask

Add a generated **"Where to file"** block to every public repo's `AGENTS.md`,
single-sourced from a Mind policy file exactly like the never-rewrite-history
and end-at-deliverable blocks (`scripts/repos_sync.py`, one source, N copies,
drift check), stating:

- questions, help with code or analysis, ideas/proposals, bug reports and
  results from users and collaborators — or an agent acting for one — go to
  <https://github.com/orgs/PyAutoLabs/discussions> in the matching category
  (Help & Questions, Ideas & Proposals, Bugs & Errors, Show and tell;
  Announcements is maintainers-only), **not** to the repo's Issues;
- an agent never runs `gh issue create` for a user-facing report: it drafts
  the post (title, category, body) and hands it to the human, since sessions
  have not been able to create Discussions (measured on the policy page);
- the organism's own development flow — Mind prompt → `/start_dev` →
  `/create_issue` → one issue per task → PR — is the only thing that opens
  issues on these repos (policy sentence two; unchanged).

Make `create_issue` and `intake` state the same rule for user-facing reports so
the Mind flow does not become the loophole.

## Constraints

- Terse: the block rides in every repo's AGENTS.md and is paid in context in
  every session. Prohibition + hub link + categories + the dev-flow exemption.
- Keep `policy/community_surface.md` the source of *why*; the new policy file
  is the *what* an agent needs at filing time. Link, don't duplicate.
- The rollout to the ~48 AGENTS.md copies is its own decision: PR wave versus
  extending `session_hook_propagate.yml` to bot-push this one block.
