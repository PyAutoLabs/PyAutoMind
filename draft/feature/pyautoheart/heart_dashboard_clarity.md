# Heart dashboard: readable status and a systematic path to green

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: large
Priority: high
Autonomy: human-required
Status: draft

@PyAutoHeart owns this implementation. Planning only: awaiting Fable review and human approval.

## Original request (verbatim)

I want to imrpove the PyAutoHeart dashboard, make it more relevent and useable, and begin to work towards making it green. Look at my history of using it, which to be honest isnt too much. The Red / Yellow / Green for release and health works very well, the score will work well once I get it down. I think the main problems are that: 1) the "Evidence Gaps" are unclear what they are, but I think I probably just need to be in the habit of copy and pasting the "clean them all button", maybe clearer button placement would help. 2) I dont know why Libraries, Workspaces, Worktree drift are red or how to fix the (Worktree dirft has a claude button). 3) Colors could help at points, for example for "Import timing" having the number of seconds in a different color with bolder font would make it more readable, I also think the grey text small font through makes it hard to capture information. 4) Unit test timing is equally an information overload hard to read. 5) CI Wall clock is nice, graphs are cool, hard to read information. Overall, I think most the information we need is there but theres a lot of info and the small grey font can be hard to read, there is probably too much info at times, maybe drop down menus could help? I guess we need to balance this so it also works on mobile and is easy to read. I do also think a single "Fix all of the heart in one chat ttype prompt systematically" would be valuable, and I think we should get a Fred Again theme going and have it be at the top of the dashboard with the lyric *[these guys are giving me life]*. This all warrants a Fable review after a plan is up.

## Findings and limits of the history

Inspected repository implementation, Mind completion history and the published board.json; no browser click history or private chat history was available in this investigation.

- `complete/2026/08/stale-remedies-on-the-heart-board.md`: the user's earlier question was why Heart stayed stale. Since August 19 the cloud board commonly sat at STALE / 65, with test_unknown (10 points), install_unknown (10), validation_absent (15). August 25 added keyed remedies, `fix stale` and a clear-every-gap prompt. This request shows the action remains hard to understand/discover; adding more data alone is unlikely to help.
- `complete/2026/09/offtick-timing-legs-live.md`: September 5 brought import and unit timing into the existing panels via CI ingestion. Preserve that collection and its baseline rules.
- Live board retrieved September 30, snapshot `2026-09-30T10:53:48.253971+00:00`: STALE / 65; Libraries (6) and Workspaces (11) nominal, not currently red. Worktree drift came from the dev-box observation dated September 28: 14 orphan directories, zero missing, three dirty task worktrees. Correction (Fable review): a dev-box observation older than 48h (`DEVBOX_FRESH_SECONDS`) renders grey (“dev box last looked 2d ago”), so on the published board drift shows as *unobserved*, not red; it is red only on a dev box with a fresh tick. This is historical evidence, not a fresh inventory or permission to remove anything.
- `heart/dashboard.py`: `_repo_section` computes per-repository states but flattens details to strings. Targeted links/prompts exist for failing CI only; behind branches and old PRs can also make rows red. Drift details omit orphan/missing entries even though they contribute to the summary. `_shown_reasons` shows only the worst tier, hiding gaps when actual failures exist.
- `_EXTRA_CSS` makes all detail text muted monospace at .8rem; `_render_html` expands every detail list. CI sparklines are embedded in dense prose. Dev-box observations retain their age but can visually look as current as cloud data.

## High-level plan

1. Keep release verdicts and score prominent; add a short ordered action summary and a clear distinction between failed checks, missing evidence and advisory performance.
2. Explain each red/yellow repository or drift finding in plain language, with its observation age, evidence link and a named next action.
3. Replace the wall of detail with readable summaries and accessible disclosure panels. Keep urgent reasons/actions visible; collapse passing inventories and raw diagnostics.
4. Give import, unit-test and CI timings a consistent layout: bold duration, labelled baseline/change, source and coverage; retain readable graphs with text equivalents.
5. Add one prominent “Fix Heart systematically” copy prompt, plus a nearby “Refresh all missing evidence” action. They assemble current context and route work through existing Brain doors.
6. Add a restrained Fred Again inspired header with the exact supplied lyric, then validate desktop/mobile readability and unchanged health semantics. Obtain Fable plan review before implementation.

## Proposed page hierarchy

Header: PyAutoHeart with the italic lyric *[these guys are giving me life]* placed in the shared hero's `lede` (or one line directly under it), styled with type only (italic, larger size, existing family accent). No second palette: the theme reserves ok/warn/bad for verdict meaning and Heart's `_EXTRA_CSS` follows the family accent. Keep red/yellow/green reserved for status; do not imitate an album cover or introduce animation/audio. Open question for the human (decide in PR A): Heart's own accent is already red (#b50f1a / #ff6b73) so every heading and link is red-hued; optionally soften heading colour so red reads only as status.

First screen: authoritative verdict and score, snapshot age, concise blocker/gap counts, primary “Fix Heart systematically” button and secondary “Refresh all missing evidence” button. Brief explanation: “Missing evidence means a check has not run, has expired, or does not cover the current source. Refreshing it may reveal failures.” Show all applicable tiers, not only the worst one. Show the dev-box vantage and observation age on the first screen (today it sits in muted meta and the stale banner only covers tick age over 1h). Add a “why this score” disclosure fed by an additive per-key `penalties` breakdown from readiness; weights unchanged.

Next: “Needs attention”, ordered by release blockers, health warnings, evidence refreshes, then advisory performance. Every entry answers what happened, why it matters, where/when it was observed and the next action. Mark whether it affects release readiness. Avoid implying every red section blocks release.

Then: performance summaries (imports, tests, CI), with details disclosed on demand. Passing repository inventory and diagnostic metadata are collapsed. Desktop supports compact columns; mobile uses full-width stacked cards. Disclosure summaries retain counts and status so collapsing does not conceal a problem.

## Detailed implementation plan

### 1. Explain findings using structured data

In `heart/dashboard.py`, extend the Board/Section presentation model additively with structured entries (stable identity, subject, state, reason, evidence/source/age and action). Preserve existing `details`, markdown/terminal output and old-snapshot fallback for consumers. Inspect schema consumers before deciding whether a schema-version bump is required.

Refactor `_lib_row`/`_repo_section` to retain the actual contributing observations, not parse their formatted strings. Show failures first; retain per-repo status. Cover CI failure/unavailability, behind/ahead/dirty checkout and old PR reasons with appropriate existing doors; informational PRs are not failures. Expand drift presentation to distinguish dirty task worktrees, missing claimed paths, clean orphan directories and dirty canonical checkouts, with concrete paths. Freshness is independent of severity: retain an adverse last-known result while explicitly labelling its age and asking for refresh.

Keep existing readiness computation, score weights, timing thresholds, cloud/dev-box ownership and <30s tick unchanged. Heart still observes and emits context; it does not repair repositories.

### 2. Render a focused responsive dashboard

Update `_render_html`, `_shown_reasons` usage and `_EXTRA_CSS`. Use native `details`/`summary` for inventories and deep diagnostics; retain all-tier action counts. Scope visual overrides to Heart instead of modifying the shared Brain theme. Primary content at least 1rem, strong contrast (4.5:1 normal text), visible focus, buttons at least 44px, long names that wrap without horizontal page scrolling. Status must have words/icons in addition to colour. Copy controls get visible descriptive text and successful/failure feedback; preserve a selectable prompt fallback if clipboard APIs are unavailable.

Implement the header locally in Heart using the existing family theme. Use the exact user-supplied lyric only. No generated image asset is needed.

### 3. Make performance legible

Use existing unit/performance data behind `_unit_import_details`, `_unit_suite_details`, `_ci_timing_section` and `_performance_sections`; never extract numeric values from prose for styling. Show package/repo, bold current duration and labelled baseline/change. Neutral accent for time; yellow/red only when the existing metric classifies a regression. Explicitly preserve unavailable/failed imports and baseline-building states.

For unit timing, show suite wall-clock, Python leg, test counts and top three bottlenecks by default; disclose remaining tests/legs. Do not sum parallel legs into an invented elapsed time. Separate absolute slowness from measured regression.

For CI, lead with median duration, maximum, run count and date window. Replace/augment text sparklines with accessible labelled inline SVG where data supports it, with text values as a fallback. Preserve coverage and source distinctions, include all remaining gates under disclosure and never present missing samples as zero.

### 4. One systematic prompt, shared with the CLI

Add a pure prompt builder consuming the same board evidence, expose an additive `fix_plan` payload in JSON and a `pyauto-heart fix all` topic in `heart/fix.py` (inspect CLI dispatch/help wiring before implementation). Reuse existing `build_stale_plan` for the narrower evidence-only action. Dashboard and CLI must agree on scope and remedies.

The all-Heart prompt includes source timestamp, exact known findings and action routes, then instructs the receiving chat to:

1. Read current authoritative Heart evidence and reconcile old dev-box observations before acting.
2. Produce a deduplicated ordered checklist: real blockers, missing evidence, local drift, then advisory timing/score improvements. Preserve all findings even when the UI truncates a preview.
3. Use existing health, bug/start-dev, hygiene, repo-cleanup and release-rehearsal doors as appropriate. Distinguish release rehearsal from publication. Follow existing plan approvals and task claims; copying this prompt is not blanket merge, cleanup or release approval.
4. Complete authorized items systematically in that chat, refresh evidence after relevant completed work, and report remaining gates with concrete next steps. Stop at the session deliverable; never schedule background follow-up or promise GREEN.
5. Preserve user edits; a dirty worktree is not automatically disposable. Never lower thresholds, waive tests or change weights just to improve colour/score.

This is a complete contextual prompt, not a blind shell chain. If a finding lacks a supported remedy, explicitly request diagnosis instead of silently dropping it or inventing a command.

### 5. Validation and delivery

Extend `tests/test_dashboard.py` and the existing fix tests for mixed severity tiers, non-CI red repositories, drift categories, aged adverse observations, no-data/baseline-building timings, complete prompts beyond display limits, escaping and old snapshots. Assert identical verdict/score for identical source data and CLI/dashboard remedy parity. Run targeted tests, then the Heart suite required by the ship workflow.

Inspect rendered representative fixtures and the saved current snapshot at 375/390px and desktop width; test keyboard disclosures, 200% zoom, copy/fallback, contrast, long repo/test names and no horizontal overflow. Browser-based validation must be obtained in an environment that supports it before claiming visual acceptance; no browser automation capability was available during this planning session.

The Feature Agent classified this as large and recommended phases through start_library / ship_library. **Amended after Fable review to three sequential PRs** so the user's highest-value item (one systematic prompt) lands first:

- **PR A — `heart_dashboard_clarity_p1.md`** (small, ~150–250 source lines): readability CSS (≥1rem primary text, non-monospace summaries, structural bolding of durations already built from fields in `_unit_*_details`), the lyric in the hero lede, all-tier reasons/counts, prominent worded “Refresh all missing evidence” and “Fix Heart systematically” buttons, `<details>` disclosures for passing inventories, Heart-scoped copy-button override with success/failure feedback and a selectable `<pre>` fallback, and a v0 `fix all` (dashboard button + `pyauto-heart fix all` topic) built from the payloads that exist today: `blockers`, `stale_plan`, `Section.action`, drift and timing actions.
- **PR B — `heart_dashboard_clarity_p2.md`**: structured entries (`sections[].entries`), repo reasons aligned with the readiness rules, drift categories with paths, correct remedies for behind/dirty/branch rows, row actions for Release validation and Test run, score `penalties` breakdown, and the fix-all prompt upgraded to consume the structured entries.
- **PR C — `heart_dashboard_clarity_p3.md`**: timing presentation (imports, unit tests, CI) including the Import-timing false-green fix.

Each gets the relevant validation from step 5. This parent is the review packet, not a fourth implementation task. Actual library failures, cleanup or performance optimizations discovered through it become separately scoped work; this plan does not promise to turn the whole ecosystem green.

## Branch and workflow preflight

- Mind root: `/home/jammy/Code/PyAutoLabs/organs/PyAutoMind`, `main`, clean before this draft; fetched origin and checked current state.
- Heart root: `/home/jammy/Code/PyAutoLabs/organs/PyAutoHeart`, `main`, clean, one commit behind origin/main. Fast-forward before implementation setup. Only local branch listed: main.
- `worktree_check_conflict heart-dashboard-clarity PyAutoHeart` returned 0; no existing claim. Recheck at implementation time.
- Proposed branch: `feature/heart-dashboard-clarity`. Heart is organ tooling: use the FeatureDecision routing through start-dev, then its indicated worktree/ship path. No source edits or worktree created during planning.
- After Fable review and human approval, use Mind create_issue primitive with both plan levels, register the claim and set up the isolated worktree. Resolve worktree location using the canonical helper and applicable workspace constraints rather than creating an ad-hoc checkout.

## Fable review handoff

Fable review requested by the author (Codex session, 2026-09-30) and **completed the same day** — see “Fable review (2026-09-30)” below. Human approval of the amended plan is still pending; no implementation has started.

## First operational step toward green

The published September 30 board's score 65 reflects three missing-evidence penalties totalling 35: test report, install verification, current-source release validation. This is superseded for local diagnosis by the vitals consultation below. A repair session must reconcile published and local evidence before choosing remedies. No expensive verification, rehearsal, source repair or cleanup has been launched by this planning task.

### Newer local evidence from the FeatureDecision vitals consultation

`pyauto-brain vitals` refreshed the local tick and returned RED / score 25 at `2026-09-30T19:01:24.391641+00:00`. Exact red reasons:

- `PyAutoLens: 2 commit(s) behind origin`
- `release validation FAILED (stage integrate)`

Exact warning reasons:

- `workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)`
- `manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml`

Local Libraries and Workspaces are red with behind-origin checkouts; several CI runs are in progress. Drift refreshed to five orphan directories, zero missing and seven dirty task worktrees. Install verification has a passed TestPyPI observation; release validation has an actual integrate failure. These observations explain why the earlier published snapshot is insufficient for choosing the next operation. The dashboard should expose vantage and freshness, not blend these into an unexplained red row.

The next operational session should inspect the failed integration evidence and workspace timeout, reconcile checkout updates without disturbing active work, and address manifest drift through its owner. Re-read authoritative state at that time. The newly observed RED blocks development progression under start-dev unless the documented human development override applies; no override was requested or assumed. Planning artifacts were already prepared; this addendum records the new diagnosis rather than initiating repairs.

## Fable review (2026-09-30)

Fable session; the code cross-check ran in an Opus subagent against PyAutoHeart main `518ce45` (one README/timings commit behind origin). D = `heart/dashboard.py`. Nothing was edited in Heart.

### Verdict

The plan is sound and its findings are accurate; approve for implementation after the amendments below. Answers to the review questions:

- **Does the first screen say what needs doing?** Not yet as written: the plan explains rows but not *why the row colour disagrees with the verdict*, which is the user's actual confusion (finding 1). Fixed by amendment 1.
- **Are verdict / evidence / advisory distinctions honest?** Yes in intent; the plan must keep them out of `blockers` so Brain vitals do not misread them (amendment 3).
- **Is disclosure useful on mobile?** Yes: viewport meta, a 34rem card layout and 375/390px overflow guards already exist and must be preserved (amendment 11).
- **Is the systematic prompt complete without implying blanket authority?** Yes; the five numbered instructions are right. It must read uncapped sources (amendment 12) and its CLI wiring has three touchpoints, not one (amendment 5).
- **Scope for one PR?** No. Three PRs, with the systematic prompt in the first (amendment 4).

### Findings against the code

1. **Row colour disagrees with readiness (plan missed this).** `readiness.py:302-315` treats behind/dirty/branch as release-red for gated *libraries* only, but `_lib_row` (D:586-601) paints any repo FAIL for branch≠main, dirty, behind≥1 or a PR ≥30 days old. Today's local render shows Workspaces “11 repos, 11 need attention” in red while the verdict names only `PyAutoLens: 2 commit(s) behind origin`. This is the main reason the user cannot tell why Libraries/Workspaces are red.
2. **Behind-origin rows get the wrong door.** `_reason_item` (D:1517-1520) gives every red/yellow item `/bug Heart board: <text>`; for “behind origin” the remedy is an ff-pull of the canonical checkout plus `pyauto-heart tick`, and for dirty it is `fix dirty <repo>`.
3. **Confirmed plan claims:** `_repo_section` flattens rows to strings (D:571-613, 647); targeted links/prompts only for failing CI (D:630-641, capped `links[:4]`); drift details list only dirty and canonical_dirty, 5 each (D:724-730) while `fix drift` lists all three categories up to 20 (`fix.py:74-109`); `_shown_reasons` shows the worst tier only (D:1650-1659) and `tests/test_dashboard.py:1266-1276` deliberately locks that in, so the test must be rewritten on purpose; detail text is muted `.8rem` monospace (D:1836-1838); zero `<details>` elements; CI sparklines are unicode text in prose (D:1106-1108) and also travel in `performance.gates[].spark`, which the Brain reads.
4. **Partial: contrast already passes.** `--muted` is #59636e on white (≈6.3:1). The readability problem is size, monospace and density, not contrast; drop the contrast framing and keep the size/typeface goals.
5. **Partial: dev-box age is shown** in a muted `.ago` span (D:1569-1573) and rows grey out after 48h; the plan's live-board drift claim is corrected above.
6. **Import-timing false green (bug).** D:774-781 renders OK “0 imports within baseline” while the slice has 4 packages with no baseline and 1 unavailable. Fix in PR C with a regression test.
7. **The drift “claude button” copies a shell command**, `pyauto-heart fix drift`, which prints a Claude prompt to stdout; grey rows copy `pyauto-heart tick && pyauto-heart publish`. Libraries, Workspaces, Test run, Version skew, Install verify and Release validation have no action unless CI is failing — today's real blocker (release validation FAILED) has no button. Faces are glyph-only ⌨/📋.
8. **Copy buttons.** Theme JS (`PyAutoBrain/board/_theme.py:811-822`) always flashes ✓ even on failure; no selectable fallback, no aria-live; buttons are ~42px / ~35px in tables. The plan's feedback/fallback/44px goals therefore need a Heart-local `copyCmd` override, not a theme edit.
9. **board.json consumers.** `SCHEMA_VERSION = 3`; readers are `PyAutoBrain/board/_board.py:358-400` (`blockers[].{text,severity,repo,repo_url,run_url,prompt,command}`, `stale_plan`, `performance`), `agents/faculties/vitals/_vitals.py:121-130` (`worst(blockers)` — an unrecognised severity counts as YELLOW) and `agents/conductors/hygiene/_hygiene_ci.py:296`. None checks `schema_version`; all `.get()`. Additive fields are safe; a v4 bump is optional.
10. **Publishing.** `.github/workflows/heart-health.yml` renders `--cloud` HTML/JSON/badge and deploys to Pages from main on a 05:00 UTC cron or `workflow_dispatch`; theme CSS is inlined at render time. A merge is invisible until the next run or a manual dispatch.
11. **Local snapshot has empty timing slices** (`ci_timing`, `unit_timings`, `unit_test_timing`, `smoke_timings`, `no_run_census` all `{}`), so timing validation needs the published `board.json`, a `heart-health` artifact, or fixtures.
12. **Display caps that hide findings:** reasons `[:8]` html / `[:6]` md (D:1907), links `[:4]`, drift 5+5, `UNIT_DETAIL_CAP=6` (D:363). Terminal, md and md-brief renderers also use `_shown_reasons`.
13. **CLI wiring for a new topic** touches `heart/fix.py:251-277`, the case list at `bin/pyauto-heart:388` and `help_fix` at `bin/pyauto-heart:367-379`. There is no `tests/test_fix.py`; fix behaviour is tested inside `test_dashboard.py` (e.g. :1279-1286).
14. **Header.** Built by `t_.hero(BOARD_KEY, "Dashboard", _LEDE)` (D:1917) with a `lede_html` parameter — the lyric fits there with no theme edit.
15. **Score has no explanation.** `readiness.compute` applies `_WEIGHTS` (readiness.py:116-135, 702-707) but does not return per-key penalties.

### Amendments (applied to this packet and the phase prompts)

1. Carry `affects_release` per repo fragment, derived from the same rules as `readiness.py:302-315`; render workspace behind/in_progress as advisory, not blocker-red; test that a workspace with `behind=2` and a fresh verdict is not shown as blocking. (PR B)
2. Route behind-origin to ff-pull + tick, branch/dirty to `fix dirty <repo>`; notify the Brain that blocker prompts change (they flow straight to the Brain board). (PR B)
3. New data goes in `sections[].entries` and top-level `fix_plan`; never add entries or severities to `blockers`. (PR A/B)
4. Three PRs as described above; `fix all` v0 ships in PR A. (all)
5. Name the three CLI touchpoints and add `tests/test_fix.py` (or explicitly extend `test_dashboard.py`). (PR A)
6. Fix the Import-timing false green with a regression test. (PR C)
7. Heart-scoped `copyCmd` override with aria-live success/failure feedback and a selectable `<pre>` fallback for the two big prompts; 44px buttons as a Heart-scoped override; worded faces (“copy prompt” / “copy command”). (PR A)
8. Lyric in the hero lede, type-only styling, no second palette; heading-colour softening is a human decision. (PR A)
9. Additive `penalties` breakdown in readiness and a “why this score” disclosure. (PR B)
10. Timing validation uses published `board.json` / workflow artifact / fixtures; drift-red claim corrected. (PR C)
11. Keep the 34rem card layout and `a.out` wrapping (D:1839-1872); test long names in `<summary>` wrap. (PR A)
12. HTML and JSON adopt all-tier reasons in PR A; full md and terminal follow in PR B; `--md-brief` README strip stays one-tier. Fix-all builder reads uncapped sources; the caps in finding 12 are named test targets. Add row actions for Release validation and Test run. (A/B)
13. Ship steps dispatch `heart-health.yml` after merge so the Pages board reflects the change. (all)

## Human approval (2026-09-30)

The human approved the amended three-PR plan ("I approve"), following the recommendation of neutral headings with Heart identity accents. This authorizes implementation in phase order, not merge or release.
