The decision is recorded and the organism reads it.

**Shipped**

- PyAutoMind#411 — `policy/community_surface.md`: users go to one org-level
  Discussions hub hosted on `PyAutoLabs/.github`; the development flow stays
  exactly where it is, one issue per task on the target repo; a bug report
  with a reproducer is still an issue. The page carries the evidence at
  filing (447 issues closed in 90 days, 427 of them the maintainer's own dev
  flow), the five questions answered, the category list, the migration
  manifest of six user-filed feature threads, and what a session measured
  and can no longer re-derive: GET on discussions is served, `POST
  .../discussions` is 404, GraphQL is refused — creating, converting and
  answering a Discussion are the human's clicks.
- PyAutoBrain#388 — the Ears read the hub: `_community.py` scans
  `repos/<hub>/discussions` beside the user-filed issues and PRs, a thread is
  *awaiting our response* when it has no accepted answer and its last word is
  not a self login, `community triage <discussion url>` routes to answer-in-
  thread or open-the-issue, and the board renders unanswered threads as
  triage chips. `COMMUNITY_HUB` defaults to `PyAutoLabs/.github`.
  +10 cases in `tests/test_community_conductor.py`; pytest 3.12 and 3.13 green.

**Follow-ups filed (all still draft/)**

- `draft/maintenance/community/migrate_user_threads_to_discussions.md` —
  human-required, the UI clicks: promote the hub, add the Scientific
  analysis category, transfer PyAutoLens#603, convert-then-transfer the six
  threads into Ideas.
- `draft/docs/workspaces/support_sections_point_to_discussions.md` — the
  seven READMEs and issue choosers.
- `draft/docs/pyautolabs_github_io/front_door_community_link.md` — the front
  door, after the hub is promoted.

**Picked up on the way**

`tests/test_ledger_merge.py::test_the_real_registries_round_trip_through_split`
had failed on main since 2026-08-31 — every Mind PR's `privacy` leg with it.
Cause was one stray double blank line each in `planned.md` and `parked.md`,
which `split_entries` collapses. Deleted both: 456 passed, was 1 failed /
455 passed. Not part of this task; fixed because the leg was red.

**Not done, and deliberately so**

The migration itself. No session can create, convert or answer a Discussion
— measured, recorded on the policy page. It is the human's ten minutes at
github.com, and the `/community` verification in step 3 of that prompt is
what closes it.

## Original prompt

# Community surface: separate where users ask questions from the AI development flow

Type: research
Target: pyautobrain
Repos:
- PyAutoBrain
- PyAutoMind
- pyautolabs.github.io
Themes:
- docs-hub
- mind-workflow
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: active
Issued: 2026-09-17
Consequence: judge
Witness: A decision document exists in the Mind's policy directory naming (a) the surface where users bring questions, help requests and scientific-analysis asks and (b) the surface where the AI development flow (issues, PRs, Mind close-outs) lives; and the community conductor's scan reads the chosen user surface, verified by a scan that lists a thread posted there.
Review-minutes: 0

Decision task, not implementation: answer the questions below in a policy document and file the follow-up prompts it spawns (Discussions enablement, Ears scan change, README/front-door Support text, migration of the few external threads). Intake filed this at 2026-09-15; the heuristic classified it as a PyAutoLens bug and then re-targeted on bare repo mentions, so the header was set by hand.

Original request (verbatim): Given how much GitHub issues bulks out, should users put questions and whatnot elsewherE? Should All my AI dev work move elsewhere? ISsues doeesnt feel suited to building a community. basically how should we make it so that people can come to the PyAutoLens and other repos with questions, which could be bug reports or help with code but may also be asking for help with scientific analysis. Community basically, should we keep github issues what they are now a huge development flow? I feel like all the stuff I do and where users come in to chat and ask questions need to be sepaerate

Evidence at filing (2026-09-15, last 90 days, org trackers): 447 issues closed across the four libraries, the lens workspace and the Mind, 427 of them opened by the maintainer's own development flow (lens 49/42, galaxy 42/39, fit 129/128, array 78/72, lens workspace 109/107, Mind 40/39). Every open issue on the lens, galaxy and fit libraries is the maintainer's. GitHub Discussions is enabled on the lens library only. The trackers are ~95% development flow; external users account for a handful of threads.

Questions to answer: (1) which surface for users: GitHub Discussions per repo, one org-level Discussions hub, or an external forum/chat; (2) whether the development flow stays on library issues or moves (e.g. Mind-only issues with library PRs referencing them); (3) how the community conductor (the Ears) scans the chosen surface and routes bug reports back into issues; (4) what each README / docs Support section and the pyautolabs.github.io front door should say; (5) migration of the few external open threads. Deliverable is the decision document plus the follow-up prompts it spawns, not the implementation.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/098c4203-08b6-4d49-908d-e2cadaed6747/scratchpad/intake_community.md -->
