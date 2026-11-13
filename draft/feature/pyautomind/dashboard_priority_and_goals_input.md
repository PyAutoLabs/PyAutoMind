# Mind dashboard: a priority tick on each task and a written Goals box, from a phone

Type: feature
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: judge
Witness: (a) tapping a task's ★ on the published `dashboard.html` and submitting adds or moves one `kind: prompt` entry in `queue.md` in one bot commit, `python3 scripts/lifecycle.py check` stays green, and the input issue is closed with a "queued at #n" comment; a ref that resolves to no prompt gets an error comment and no commit (workflow test on fixtures); (b) the dashboard marks queued tasks ★ with their position and shows `goals.md` at the top (golden-HTML test in PyAutoBrain intake); (c) `pyauto-brain batch brief` prefills `brief.goals:` from `goals.md` and `batch brief --check` passes on the result
Review-minutes: 25
Unattended: never
Lane: any

Original request (human, 2026-11-13): "I rarely look in that repo… an actual input thing on the PyAutoMind dashboard, which with html could be a more visual and easy to read and change thing… a priority 'tick' next to PyAutoMind dashboard tasks and entries… and having a written 'Goal' type input."

**Fixed points.** `queue.md` stays the machine-readable store the planner reads (schema `queue.md:42-50`; "order is priority"; M2.3 keeps it validated). The UI only writes into it. The dashboard is static: rendered by `PyAutoBrain/agents/conductors/intake/_intake.py:2600` (`render_dashboard_html`), published by `PyAutoMind/.github/workflows/pages_dashboard.yml`. Goals go to a new `goals.md` (ordered `## n. <goal>` + optional `epics:`/`tags:`), which `batch brief` copies into the brief's required `goals:` (`_brief.py:214`, schema `batches/AGENTS.md:183`).

**Options.**
1. **GitHub issue forms, launched from the dashboard.** Each task row gets a ★ link to `issues/new?template=queue.yml&ref=<path>` (prefilled), with fields position (top / after #n / bottom / remove) and note; a Goals link opens `goals.yml`. A Mind workflow on `issues: opened` (label `queue-input`) validates with `lifecycle.py check`, edits `queue.md`/`goals.md`, commits as the bot (precedent: `dashboard_refresh.yml` self-heal), comments and closes.
   + works in the GitHub app and any browser with the human's existing login; no secret on a device; every change has an issue as its history; the watcher's network surface is untouched.
   − two taps plus a submit, on a GitHub page rather than the dashboard itself; coarse reordering; the bot commit must rebase against concurrent Mind pushes.
   Variant: one pinned "Priorities" issue whose checklist the refresh regenerates; ticking a box (`issues: edited`) syncs. More tick-like, but a regenerate can clobber a concurrent tick.
2. **claude.ai Artifact with a shared database.** A visual page: ticks, drag order, a Goals text box.
   + the nicest UI, on the phone in claude.ai.
   − the store is outside git; reading it needs a Claude session (the laptop watcher and Actions cannot), and the task list must be re-published into the page by a session after each Mind change. Two sources of truth until a session syncs them.
3. **Pages form + `repository_dispatch`.** Ticks on `dashboard.html` itself, POSTing to the dispatch API.
   + one tap, on the dashboard.
   − a static page has no server, so it needs a GitHub token stored in the phone's browser (a Mind-write credential in localStorage) or an OAuth backend that Pages cannot host.

**Recommendation: option 1**, with the dashboard carrying the read side visually (★ position, goals at the top). It is the only option with no new credential, no second store and no watcher change. Revisit option 2 at M5/M6, when a cloud session runs every shift anyway and could sync it.

**Re-check before building:** that issue-form prefill by query parameter works when opened from the GitHub mobile app (field `id` = query key).

Tier judge: a design choice for the human, and it creates a new write path into `queue.md`.
Programme: before M3.1 (the live shifts pick from `queue.md`); a side lane of M3.

<!-- drafted 2026-11-13 by the REL intake session (scratch/intake_2026-11-13) -->
