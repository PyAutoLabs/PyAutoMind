# Closing threads that are waiting on the contributor (21 days)

Decided 2026-11-17 in the /community chat (PyAutoBrain#658). First applied by
hand the same day, to [discussion #37](https://github.com/PyAutoLabs/.github/discussions/37)
after 27 days without a reply.

When we have asked a contributor something and they have not answered in three
weeks, we close the thread with a short, friendly message. It keeps the hub
honest about what is live, and the contributor can pick it up again at any time.

## When it applies

All of these must hold:

- **The thread is open and unsettled.** An open issue, or a Discussion with no
  accepted answer.
- **It is a contributor's thread.** An external person opened it. Not a PR, not
  our own thread, not a locked thread.
- **It is not a broadcast.** Announcements and Show and tell are never closed
  this way.
- **We spoke last.** The latest comment (nested replies included) is from one
  of our logins (`self_logins` in PyAutoEars `config.json`).
- **Three weeks have passed.** No reply from anyone else for 21 days or more.
  Bot comments do not reset the clock.
- **We are waiting on them.** Our last comment asked the contributor for
  something: a reproducer, a version, a test, a decision. If it said "we'll
  look at this" or accepted an idea, the next step is ours, and the thread
  stays open.

It **never** applies to a thread that is waiting on us.

Ears marks the candidates in its snapshot (`close_due`, with
`awaiting_contributor_since`; see PyAutoEars `REFERENCE.md`). Ears cannot read
what our last comment asked, so the last condition is the session's call when
it reads each thread.

## The message

Discussions:

> Hi @<author>, we're closing this for now because we haven't heard back in
> three weeks. Nothing is lost. If you're still <context>, reopen this
> discussion or just reply here <with what we asked for> and we'll pick it up
> again.

Issues (an issue's author cannot reopen an issue a maintainer closed):

> Hi @<author>, we're closing this for now because we haven't heard back in
> three weeks. Nothing is lost. If you're still <context>, reply here <with
> what we asked for> and we'll reopen it.

Fill in `<context>` (for example "seeing the zoomed panel cut off") and
`<with what we asked for>` (for example "with the script that makes the plot")
from the thread. Keep the rest as written.

## How it is done

1. `pyauto-brain community` lists the candidates under **Close due (21d)**,
   each with the message prefilled.
2. The session reads each thread, drops any that are not really waiting on the
   contributor, and fills in the two placeholders.
3. The human approves the batch once per session.
4. The session posts and closes each one:
   - Discussions: `addDiscussionComment`, then `closeDiscussion` with reason
     `OUTDATED`.
   - Issues: `gh issue close <n> -R <repo> --reason "not planned" --comment "<message>"`.

There is no GitHub Action and no unattended closing. Nothing is posted or
closed without the human's approval in that session. The commands are in
PyAutoBrain `skills/community/community.md` ("Close due").
