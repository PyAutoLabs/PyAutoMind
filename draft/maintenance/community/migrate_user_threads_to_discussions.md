# Finish migrating user threads to the Discussions hub

Type: maintenance
Target: community
Repos:
- PyAutoLens
- PyAutoGalaxy
- PyAutoArray
Themes:
- community
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Consequence: glance
Witness: the six feature-request threads retain their authors and comments in the hub's Ideas & Proposals category; reproducible defects have linked development issues; accepted answers settle resolved answerable discussions.
Review-minutes: 5
Filed: 2026-09-17

Spawned by `policy/community_surface.md` (PyAutoMind#403). Conversion and
transfer remain human actions in the GitHub UI; never copy a user's thread
under the maintainer's name or discard its original comments.

## Already verified, 2026-09-19

The org hub is live at https://github.com/orgs/PyAutoLabs/discussions.
The maintainer simplified the categories to five:

- **Help & Questions** (`help-questions`, answerable)
- **Ideas & Proposals** (`ideas-proposals`, answerable)
- **Bugs & Errors** (`bugs-errors`, answerable)
- **Announcements** (`announcements`)
- **Show and tell** (`show-and-tell`)

GraphQL verified names, slugs and answerability; HTTP 200 alone does not
verify a category because GitHub also serves unknown category URLs. The
category-creation gate on the support-link PRs is cleared.

The PyAutoLens announcement is on the hub as
https://github.com/orgs/PyAutoLabs/discussions/11.
PyAutoArray#551 (streaming visibilities, @HRSAstro) is already
https://github.com/orgs/PyAutoLabs/discussions/13 in **Ideas & Proposals**.
Do not convert or transfer those again.

## Remaining human steps

1. **Finish historical feature-request migration**, if retaining this
   history on the hub. Use *Convert to discussion* on the source issue,
   then *Transfer discussion* to `PyAutoLabs/.github`, category
   **Ideas & Proposals**. Enable Discussions temporarily on the source repo
   if necessary, then turn it off after transfer.
   - https://github.com/PyAutoLabs/PyAutoArray/issues/499 (@HRSAstro, shipped)
   - https://github.com/PyAutoLabs/PyAutoLens/issues/631 (@mwiet, shipped)
   - https://github.com/PyAutoLabs/PyAutoLens/issues/564 (@mwiet, shipped)
   - https://github.com/PyAutoLabs/PyAutoLens/issues/542 (@mwiet, shipped)
   - https://github.com/PyAutoLabs/PyAutoGalaxy/issues/419 (@Sketos, shipped)
   Keep shipped outcomes in the conversation. Since the combined category is
   answerable, mark the settling outcome as the accepted answer where
   appropriate so later comments do not reopen a response obligation.
2. **Correct the bug report's category.**
   https://github.com/orgs/PyAutoLabs/discussions/14 (`imshow_origin`) is
   currently in Ideas & Proposals. Move it to **Bugs & Errors**. It contains
   a reproducer; use `/community triage` to establish the appropriate
   PyAutoArray development issue and link it back. The original
   PyAutoArray#535 is now closed; do not assume it remains an open tracker.
3. **Finish the hub's navigation.** Keep repository Discussions off once
   migration is complete, with READMEs and issue choosers pointing at the
   hub. Pin a Help & Questions thread titled "How to get help" with the
   policy's support paragraph if it has not already been posted.
4. **Verify with the Ears:** `bin/pyauto-brain community` should show
   unanswered external threads awaiting response, while accepted answers
   settle Help & Questions, Ideas & Proposals, and Bugs & Errors.
   Announcements and Show and tell remain ours to watch.
   Retire this prompt with `scripts/lifecycle.py record` after the remaining
   migration is complete.

Replies are drafted in `/community` for human approval; this migration
does not authorize automatic replies or changes to GitHub category settings.
