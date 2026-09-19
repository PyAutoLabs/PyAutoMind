# docs: distinguish implementation proposals from ideas

Type: docs
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Approved: 2026-09-19 (Codex conversation: "I approve")
Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/426

Update policy/community_surface.md with answerable Proposals, accepted-verdict closure and issue routing. Update draft/maintenance/community/migrate_user_threads_to_discussions.md to route #551 to Proposals, leaving five shipped threads in Ideas. Keep the support paragraph verbatim and align category-aware scan doctrine.

Branch: feature/community-surface
Validation: focused community tests for Brain; Markdown/YAML/link checks for docs and templates; static HTML and browser review for the website; independent diff review before PR creation.

## Original request

# Finish the community surface: the Proposals category, the Ears' category rule, and the user-facing doors

Type: docs
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoLens
- PyAutoGalaxy
- PyAutoFit
- PyAutoArray
- autolens_workspace
- autogalaxy_workspace
- autofit_workspace
- pyautolabs.github.io
Themes:
- docs-hub
- community
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: glance
Witness: `policy/community_surface.md` lists a seventh category, **Proposals**
  (answerable, opened by anyone), with the Ideas-vs-Proposals rule and the
  instruction that a settled proposal is closed by marking the verdict
  comment as the accepted answer; the migration prompt sends PyAutoArray#551
  to Proposals rather than Ideas; `pyauto-brain community` does not list an
  Announcements or Show and tell thread under awaiting-response when a
  non-self login commented last, and a test pins that; each of the seven
  user-facing READMEs and the pyautolabs.github.io front door carry the
  policy paragraph with the hub link and no "raise an issue to ask a
  question" line.
Review-minutes: 20

Context: PyAutoMind#403 shipped `policy/community_surface.md` (PR #411) and
PyAutoBrain#388 taught the Ears to read the hub. The hub is the org's
Discussions, source repository `PyAutoLabs/.github`. Read the policy page
first — it is the single source for both sentences and it records what a
session measured (creating, converting and answering a Discussion are the
human's clicks; GET is served, POST is 404, GraphQL is refused).

## 1. The Proposals category (policy + migration prompt)

The gap the maintainer named: a technically savvy outside contributor who
arrives with a *design* — an API sketch, or a reference implementation they
intend to land — has nowhere that fits. `Ideas` is for a request before
anyone has thought it through, and an issue is the development flow's own
ledger. PyAutoArray#551 (@HRSAstro, streaming visibilities for memory
efficiency, "proposal with a reference implementation, not yet committed
work" in the policy page's own manifest) is the live example, and the
migration prompt currently sends it to Ideas.

Add a seventh row to the category table in `policy/community_surface.md`:

| Category | Answerable | For |
|---|---|---|
| Proposals | yes | a concrete plan someone means to implement — design, API sketch or a reference implementation; further along than an Idea |

Write the distinction into the page in its own voice:

- **Ideas** is "it would be good if…" — no design, and no offer from the
  author to build it.
- **Proposals** is a design the author has thought through and usually
  intends to write. The thread argues the design; the issue, when the work
  is accepted, is still where the work is tracked.
- Proposals is **answerable** on purpose, and this is load-bearing rather
  than cosmetic: the Ears' awaiting-response rule keys off
  `answer_chosen_at` (`_community.py` ~189, ~429), so marking the verdict
  comment — "yes, open the issue" or a recorded no — as the accepted answer
  settles the thread with no code change. Say so on the page, so whoever
  answers a proposal knows the accept button is what stops it being chased.
- An accepted proposal gets its issue opened with a link back to the thread,
  exactly as a confirmed bug does today, and is routed through
  `/start_dev_for_user`.

Then update `draft/maintenance/community/migrate_user_threads_to_discussions.md`:

- step 1's category list gains Proposals (the human creates it while they
  are already in the settings page);
- in step 2's manifest, **PyAutoArray#551 → Proposals** (it is open, and it
  is a design, not a wish). The five shipped threads stay in **Ideas** —
  they are the record of a request that closed, and moving them buys
  nothing;
- step 3's verification sentence still holds: `bin/pyauto-brain community`
  lists the #551 thread as awaiting our response, now under Proposals.

## 2. The Ears: the awaiting-response rule should read the category

Grounded in the merged code: `_community.py` captures `category` (~188,
~440) but the awaiting-response rule never consults it —
`entry["awaiting_response"] = actor is not None and actor not in
SELF_LOGINS` (~282) and `(not answered) and last not in SELF_LOGINS` (~447).

Proposals does not need this, because it is answerable. But Announcements
and Show and tell are not, so the first time anyone comments on a release
announcement the board raises a `/community triage` chip for a thread that
is ours to watch, not ours to answer. Fix it while the category work is
open:

- a module-level set beside `COMMUNITY_HUB`, e.g.
  `BROADCAST_CATEGORIES = {"Announcements", "Show and tell"}`;
- a thread in one of them never sets `awaiting_response` True on the
  last-word rule alone — use the "ours-to-watch" state the board already
  renders;
- `community triage <url>` still works on those threads and still emits the
  context surface; they are simply not chased.

Add cases to `tests/test_community_conductor.py` beside the +10 that PR #388
added: an Announcements thread with a non-self last comment is NOT in
awaiting-response; a Q&A thread with the same shape still IS; a Proposals
thread with an accepted answer is NOT, and without one IS.

## 3. The user-facing doors (two prompts already filed — do them)

- `draft/docs/workspaces/support_sections_point_to_discussions.md` — the
  seven READMEs' "Community & Support" sections and a
  `.github/ISSUE_TEMPLATE/config.yml` + `bug_report.md` per repo. One small
  PR per repo, PyAutoLens first. The prompt carries the verbatim paragraph.
  Add one contact link to the chooser beside the existing two: "Propose an
  implementation" → the hub's Proposals category, so a contributor arriving
  with a design meets it at the moment of filing.
- `draft/docs/pyautolabs_github_io/front_door_community_link.md` — the front
  door's Community entry. Its own prompt says to do it after the hub is
  promoted, so check that https://github.com/orgs/PyAutoLabs/discussions
  resolves before opening that PR.

The policy paragraph itself does not change — a user still goes to the hub;
Proposals is what a contributor finds once there. Do not rewrite it.

## 4. Order and gates

PyAutoBrain (the broadcast-category rule + tests) and PyAutoMind (the policy
page + the migration prompt) are one PR each and are independent of the
human's clicks. The seven README PRs and the front door follow in any order.

Human-required and NOT this task: creating the Proposals category itself,
and the six-thread migration — the Convert-to-discussion and
Transfer-discussion buttons are UI-only.



OTHER THINGS:

Can we have Discussions clickable on each repo but direct to the PyAutoLabs repo? Would be nice
Otherwise we can just disable Discussions everywhere but then people need to find PyAutoLabs
whcih isnt always easy.

On PyAutoLabs lets move PyAutoScientist down to the bottom, and put a clearer message that
its currently my (Jammy2211's) vibe coded AI software development ecosystem. Users are welcome
to check it out but its not currently expected contributors will use it.
