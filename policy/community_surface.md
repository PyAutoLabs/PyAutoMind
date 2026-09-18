# The community surface: users on Discussions, the development flow on issues

Decided 2026-09-17 (PyAutoMind#403, from
`draft/research/pyautobrain/community_surface_users_vs_dev_flow.md`). This
page is the single source for *where an outsider goes* and *where the
organism's own work lives*. The Ears (`pyauto-brain community`) read it as
doctrine; the README "Community & Support" sections, the issue-template
contact links and the pyautolabs.github.io front door are generated from the
same two sentences.

## The two sentences

1. **Users go to one Discussions hub** —
   <https://github.com/orgs/PyAutoLabs/discussions>, hosted on the org's
   profile repository `PyAutoLabs/.github` (GitHub backs org Discussions
   with one source repo; a neutral one keeps every thread URL free of a
   library's name). Questions, help with code, help with a scientific
   analysis, feature ideas, results to show: all of it, for every library
   and workspace — PyAutoFit and PyAutoCTI as much as PyAutoLens — in one
   place.
2. **The development flow stays exactly where it is** — one GitHub issue per
   task on the target repo, opened by the Mind's prompt lifecycle, closed by
   its PR. Nothing about `/start_dev`, the ship skills, `/prm`, the Heart's
   issue links or the `pending-release` labels changes.

The only thing that moves is the audience. The trackers were never a problem
for the development flow; they were a problem for a user reading them.

## Why (the evidence at filing, 2026-09-15)

Last 90 days across the four libraries, the lens workspace and the Mind: 447
issues closed, **427 of them opened by the maintainer's own development flow**
(lens 49/42, galaxy 42/39, fit 129/128, array 78/72, lens workspace 109/107,
Mind 40/39). Every open issue on the lens, galaxy and fit libraries is the
maintainer's. The trackers are ~95 % development flow. On 2026-09-17 the
externally-authored *open* issues across the seven user-facing repos number
two, both on PyAutoArray.

## The five questions, answered

### 1. Which surface for users — per-repo Discussions, one hub, or external?

**One hub, on GitHub, at the org level, for every repo.** Rejected
alternatives:

- *Per-repo Discussions.* Fragments a community of a few dozen active users
  across six repos and reproduces the "which repo do I post in?" question
  that already sends PyAutoArray bugs to the PyAutoLens tracker. It also
  repeats the bulking problem: six thin boards instead of one live one.
- *An external forum or chat (Discourse, Zulip, Discord, the Slack).* Another
  service to run and moderate, invisible to a search engine or to someone
  arriving from the README, and a second login. The Slack stays what it is —
  invitation-only, for collaborators — and is not the public surface.
- *Hosting the hub on PyAutoLens.* It already has Discussions on (since
  2026-07-10, one Announcements thread) and is where most users are, but
  every thread's URL would read `PyAutoLabs/PyAutoLens/discussions/N`, which
  tells a PyAutoFit or PyAutoCTI user they are on the lens board. Threads
  never move when the org's source repository is switched later, so the
  host is chosen once, before the first migration: the org profile repo
  `PyAutoLabs/.github`, whose only job is org-wide material.

Promotion (Organization settings → Discussions → source repository =
`.github`) gives the hub the org-level URL and the "Discussions" tab on the
org page. PyAutoLens's one announcement thread is transferred there and
PyAutoLens's Discussions switched off; every other repo keeps Discussions
**off**, with README and issue chooser pointing at the hub.

**Categories** (GitHub's defaults plus one):

| Category | Answerable | For |
|---|---|---|
| Announcements | no | releases, breaking changes (exists) |
| Q&A | yes | installation, usage, "why does this error", help with code |
| Scientific analysis | yes | lens modelling, inference, "is this result right" — the ask that never fitted an issue |
| Ideas | no | feature requests and proposals, before anyone commits to work |
| Show and tell | no | results, papers, figures |
| General | no | everything else |

### 2. Does the development flow stay on library issues?

**Yes, unchanged.** Moving it (to Mind-only issues, to a private tracker, to
PRs-only) would touch every ship skill, `/prm`, the Heart's per-repo issue
links, the workspace `pending-release` labels and every completion record's
`Issue:` line, for no user-visible gain once users have their own surface.
The trackers become what they honestly are: the organism's work ledger,
public but not addressed to users.

**Where a user's bug report goes.** A report with a reproducer (a snippet or
script, the traceback, the versions) is dev work and is welcome as an
**issue** on the target repo — that is exactly what `/start_dev_for_user`
picks up. Anything short of that ("this doesn't work", "how do I", "is this
right") is a **Discussion**; if it turns out to be a bug, the Ears open the
issue with a link back and mark the thread answered with the issue link.
Each user-facing repo's issue chooser (`.github/ISSUE_TEMPLATE/config.yml`)
carries the two contact links and one bug-report template so the choice is
made at the moment of filing; blank issues stay enabled because the
development flow files by API and the maintainer occasionally by hand.

### 3. How do the Ears scan the hub and route bugs back?

`pyauto-brain community` (the scan) lists the hub's open discussions through
the REST endpoint `repos/PyAutoLabs/.github/discussions` (read-only, and
served to a remote session — see "Measured" below) alongside the external
issues and PRs it already hears. A thread is **awaiting our response** when it
has no accepted answer and its last word is not a self login; the board
renders each such thread as a `/community triage <url>` chip.
`pyauto-brain community triage <discussion url>` emits the same
context-sufficiency surface as for an issue, with the route: **answer in the
thread** (drafted in the session, posted by the human), or, for a confirmed
bug, **open the issue** with a link back and route it through
`/start_dev_for_user`, then mark the thread answered with the issue link. The
hub is `COMMUNITY_HUB` in the conductor (default `PyAutoLabs/.github`).

### 4. What the READMEs and the front door say

Every user-facing README's **Community & Support** section, and the
pyautolabs.github.io front door, say the two sentences in this order:

> Questions, help with your code or your analysis, and ideas: the
> [PyAutoLabs Discussions](https://github.com/orgs/PyAutoLabs/discussions).
> Bug reports with a reproducer (a snippet, the traceback, your versions):
> an issue on the library's tracker. The Slack is for collaborators, by
> invitation.

Follow-ups filed: `draft/docs/workspaces/support_sections_point_to_discussions.md`
(the seven READMEs and issue choosers) and
`draft/docs/pyautolabs_github_io/front_door_community_link.md`.

### 5. Migration of the external threads

The threads worth moving are the **user-filed feature requests and
proposals** — they are conversations about direction, which is what Ideas is
for, and a hub that opens with real requests and their outcomes is a hub
people post to. Bug reports (fixed or open) stay issues: a fixed bug is a
record, an open one with a reproducer is dev work.

Move them with GitHub's native **Convert to discussion** (issue sidebar). It
keeps the author, every comment and every timestamp, and locks the issue
with a redirect; nothing else does — the REST Discussions API is read-only,
`createDiscussion` is GraphQL, and a GraphQL copy would be posted under the
maintainer's name and lose the thread. Conversion lands in the issue's own
repo, so a non-hub repo's thread is converted there (Discussions enabled
for the minute it takes) and then **Transfer discussion** moves it to the
hub; discussions never move when the org's source repository changes, which
is why the host repo is decided *before* the migration, not after. Manifest (all → **Ideas**; the two
closed-as-shipped ones keep the shipped status in their last comment):

| Thread | Author | State | Why Ideas |
|---|---|---|---|
| PyAutoArray#551 — Streaming visibilities for memory efficiency | @HRSAstro | open | proposal with a reference implementation, not yet committed work |
| PyAutoArray#499 — Sparse interferometer inversion with linear function lists | @HRSAstro | shipped (#500) | request → shipped; shows the loop closes |
| PyAutoLens#631 — Yang+2024 SIDM profile as default for subhalos/LOS halos | @mwiet | shipped (PyAutoGalaxy#556, #691) | request with deferred items still open for discussion |
| PyAutoLens#564 — Kaplinghat, Tulin & Yu (2016) cored-NFW profile | @mwiet | shipped (PyAutoGalaxy#471) | request → shipped |
| PyAutoLens#542 — end-to-end `jax.jit`/`vmap` multi-plane substructure simulator | @mwiet | shipped (jax_substructure series) | request → shipped |
| PyAutoGalaxy#419 — External potential (Powell 2022) | @Sketos | shipped (PyAutoGalaxy#422) | request → shipped |

Stays an issue: PyAutoArray#535 (@ClarkGuilty, `imshow_origin` overlay
mirror — open, full reproducer, dev work); the fixed bug reports
PyAutoLens#724, autolens_workspace#524, PyAutoArray#521/#459, PyAutoLens#495/#470,
PyAutoGalaxy#451. Follow-up filed:
`draft/maintenance/community/migrate_user_threads_to_discussions.md`
(human-required: the button is UI-only).

## Measured, 2026-09-17, from a Claude Code remote session

Recorded so nobody re-derives them:

- `api.github.com/repos/<in-scope repo>/...` **is served** to a remote
  session through the proxy with the session token (`GH_TOKEN`), including
  `.../discussions` and `.../discussions/<n>/comments` (GET). This is the
  path `gh api` would take; the 403s recorded in
  `PyAutoBrain/skills/GITHUB_ACCESS.md` on 2026-08-27 do not reproduce for
  repos attached to the session.
- `POST .../discussions` is 404 (GitHub: the REST Discussions API is
  read-only), `api.github.com/graphql` is refused by the proxy for every
  query, `search/issues` is refused (org-wide search is not
  repository-scoped), and `github.com/...` HTML is 403. **No session can
  create, convert or answer a Discussion**; those are the human's clicks.
- `GET repos/<repo>` reports `has_discussions`: true on PyAutoLens only. The
  session token has admin on every attached repo, so `PATCH` could enable
  Discussions elsewhere — deliberately not done (decision 1).
  `PyAutoLabs/.github` is public but cannot be attached to a session (its
  name begins with a dot), so enabling Discussions there is a UI step.
