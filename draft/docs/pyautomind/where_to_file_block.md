# docs: "Where to file" block in every public AGENTS.md — route user reports to the Discussions hub

Type: docs
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Lane: any

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
