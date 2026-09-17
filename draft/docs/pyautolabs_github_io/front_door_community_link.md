# Front door: a Community link to the Discussions hub

Type: docs
Target: pyautolabs.github.io
Repos:
- pyautolabs.github.io
Themes:
- docs-hub
- community
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: the pyautolabs.github.io front door carries a "Community" entry that opens https://github.com/orgs/PyAutoLabs/discussions, with the policy's two sentences beside it, and no front-door text sends a question to an issue tracker.
Review-minutes: 5
Filed: 2026-09-17

Spawned by `policy/community_surface.md` (PyAutoMind#403), decision 4. The
front door is the first thing a search engine hands a new user; today it has
no community entry at all, so the first "how do I ask" lands on whichever
repo's tracker they click into. Add one entry (nav + a short block on the
landing page) with the policy paragraph:

> Questions, help with your code or your analysis, and ideas: the
> [PyAutoLabs Discussions](https://github.com/orgs/PyAutoLabs/discussions).
> Bug reports with a reproducer (a snippet, the traceback, your versions):
> an issue on the library's tracker. The Slack is for collaborators, by
> invitation.

Do after `draft/maintenance/community/migrate_user_threads_to_discussions.md`
has promoted the hub, so the org-level URL resolves.
