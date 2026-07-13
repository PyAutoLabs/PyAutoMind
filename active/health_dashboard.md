# One unified health dashboard — GitHub web + CLI/venv + mobile, one renderer

Type: feature
Target: PyAutoHeart (+ PyAutoBrain Health Agent rendering; PyAutoHeart README / GitHub Pages surface)
Repos:
- PyAutoHeart
- PyAutoBrain
Status: planned
Difficulty: large
Autonomy: supervised
Priority: high
Milestone: M5 — the unified health dashboard. Supersedes and expands the
one-line "M5 = polish of the mobile UX" placeholder in
`feature/pyautoheart/release_validation.md` (line ~219): mobile polish is now
*one of three surfaces* of a single dashboard, not a standalone milestone.
Depends on M1–M4 (all merged): the release-validation report + readiness hard
gate + the full Stages 0–3 orchestrator already produce the signals this
dashboard surfaces.

## Why

Heart already computes everything a health dashboard needs — `state.json` (per
repo × per check), `release_ready.json` (the green/yellow/red verdict + score +
reasons), and `validation_report.json` (the release rehearsal). But those
signals are surfaced in **scattered, inconsistent places**:

- `pyauto-heart status` / `readiness` — colour terminal output, dev box only.
- `pulse-health.yml` — a daily cloud job that opens/updates a single
  `[heart-health]` tracking **issue** when red, closes it when clean. Good for
  alerting, but it is an issue thread, not an at-a-glance board, and it only
  covers the two cloud-safe checks (ci_status, open_prs).
- The `watch`/`live` daemon — a rich live board, but only while you are staring
  at that one terminal.
- Mobile (`pyauto-brain health`) — the Health Agent reads `readiness --json`,
  but renders nothing dashboard-shaped.

There is **no single place** a human (or the Health Agent) can look and see the
whole organism's health at a glance — least of all from a phone or a freshly
opened shell. The Health Agent's entire purpose is to drive this board to all
green; right now there is no board. M5 builds it: **one dashboard, one
renderer, three surfaces that cannot disagree.**

Concretely, the ask is: *"I want one unified health dashboard — live on a
GitHub webpage for PyAutoHeart, on my CLI when I open my venv, and on my phone —
all showing the same thing, which is what the Health Agent is trying to make all
green."*

## Design

### 1. One renderer, many formats (the crux)

The invariant that makes this "unified" rather than "three dashboards that drift
apart": **a single render function** consumes the SAME cached snapshot the
terminal already uses and emits every surface's format. Nothing recomputes; the
web page, the CLI line, and the mobile card are all projections of one
`state.json` + `release_ready.json` (+ `validation_report.json`).

Add `heart/dashboard.py` with:

```
render(snapshot, verdict, validation, *, fmt) -> str
    fmt = "term"     # the full colour board (what `status` + `readiness` show today, unified)
        | "oneline"  # compact: "PyAuto ● RED 35  5 blockers  (tick 4m ago)"  [venv/prompt]
        | "md"       # GitHub-flavoured markdown (step summary / issue body / README block)
        | "html"     # standalone self-contained HTML page (GitHub Pages)
        | "json"     # the machine surface the Health Agent + mobile consume
```

`render` must be **pure** (snapshot in → string out, no I/O), mirroring
`heart/readiness.py::compute` / `render_block` and `heart/status.py::render`, so
it stays trivially testable on the stdlib-only footprint (Heart's test rule).
Refactor today's `status.render` / `readiness.render_block` to delegate to the
`fmt="term"` path so there is exactly one source of truth for what "the board"
looks like. Colour rules stay the `c_ok/c_warn/c_fail` helpers; `md`/`html` map
green/yellow/red to the same three states (badge colours / cell backgrounds).

The board shows, at minimum: the top-line verdict + score; the 5 libraries'
repo_state + CI; workspace CI; version skew; the release-validation report
(profile / testpypi_version / commit_shas freshness / per-stage status); and the
**dashboard's own age** (last tick `ts`) with a staleness flag — a cached board
that does not advertise its own staleness is a footgun.

### 2. Surface A — GitHub web (a real page, for PyAutoHeart)

Primary: **GitHub Pages.** A scheduled workflow renders `fmt="html"` to
`index.html` and publishes it to the `gh-pages` branch (or Pages artifact), so
`https://pyautolabs.github.io/PyAutoHeart/` is the live board. Self-contained
HTML only (inline CSS, no external assets) so it renders anywhere.

Complementary, cheap, same renderer:
- **`$GITHUB_STEP_SUMMARY`** — the scheduled job writes `fmt="md"` to its run
  summary, so every run's board is visible in the Actions tab with zero hosting.
- **README badge + block** — a shields.io-style endpoint badge (verdict colour)
  at the top of `README.md`, and an auto-updated `<!-- heart:begin -->…<!-- heart:end -->`
  markdown block the workflow commits (into PyAutoHeart's OWN README — never a
  foreign repo).
- **Keep `pulse-health.yml`'s `[heart-health]` issue** as the *alerting*
  channel (it pings on red, closes on green); the dashboard is the *at-a-glance*
  channel. They are complementary, not duplicative.

Reuse/extend `pulse-health.yml` rather than adding a parallel workflow: it
already runs the cloud-safe checks daily and has `issues: write`. Add the render
+ publish steps (Pages needs `pages: write` + `id-token: write`). **Cloud-safe
caveat:** the cloud job only has ci_status + open_prs (no local working tree),
so the published board must clearly mark the local-only checks (repo_state,
worktree_drift, script_timing, test_run, version_skew) as "dev-box only /
not observed here" rather than silently showing them green. A fuller board can
optionally be pushed from the dev-box `watch` daemon (it has the full snapshot)
to the same Pages target — decide during implementation whether the canonical
web board is cloud-only-honest or dev-box-pushed-complete.

### 3. Surface B — CLI / venv (the shell-open glance)

- **`pyauto-heart dashboard`** — a new subcommand that prints `fmt="term"`: the
  ONE unified board (today's `status` + `readiness` + the validation report
  folded into a single screen). `--oneline`, `--md`, `--html`, `--json` select
  the other formats. It reads the **cached** snapshot (no tick) so it is instant.
- **venv / shell-open hook** — ship a tiny sourceable snippet (e.g.
  `heart/shell/heart_prompt.sh`, or extend the existing bashrc-started `watch`
  pattern the README already documents) that on venv activation prints exactly
  the `fmt="oneline"` summary from cached state. Hard requirements:
  - **Never runs a tick** on shell open (reads cache only) — must add <100 ms and
    never block the prompt.
  - **Never errors** if state is absent/stale — degrade to a one-line
    "heart: no fresh state (run `pyauto-heart tick`)" hint.
  - Honours `NO_COLOR`; opt-in via an env flag so it does not surprise anyone.
  - Shows the board's age; if stale beyond a threshold, nudges a tick rather than
    implying the stale numbers are live.

This is what the user means by "running a bash script when I open a venv" — a
cached, instant, one-line vital sign, with `pyauto-heart dashboard` for the full
board on demand.

### 4. Surface C — mobile (the original M5 mobile-UX polish, folded in)

The Brain **Health Agent** (`agents/health/`) already reads
`pyauto-heart readiness --json`; give it the `fmt="json"`/`"md"` dashboard view
so `pyauto-brain health` renders the same compact card on a phone — verdict,
score, the top blockers, and the release-validation state — instead of raw
verdict JSON. No new agent, no boundary change: the Health Agent stays strict
read-and-reason. This subsumes the "polish of the mobile UX" that was M5 in
`release_validation.md`.

### 5. Register the capability (so the Brain agents surface it)

Add a `dashboard` capability (+ the published Pages URL and the `dashboard`
CLI/`--json` surface) to `health_agent/capabilities.yaml` and the
`HEART_CAPABILITIES.md` cross-reference. The manifest-driven Health Agent then
picks it up with no Brain code change (same pattern M2 used for the `validate`
capability).

## Boundary (unchanged, non-negotiable)

Heart stays an **observer**. Everything M5 writes goes ONLY to: PyAutoHeart's own
`gh-pages`/README/`[heart-health]` issue (its own repo), the job's step summary,
or `~/.pyauto-heart/`. **No** writes into any other repo, **no** build/workflow
dispatch, **no** new credentials beyond the auto-provisioned `GITHUB_TOKEN`
`pulse-health.yml` already uses. The venv hook is read-only over cached state.
The Health Agent remains read-and-reason. The dashboard *shows* health; it never
*acts* on it.

## Scope of this milestone (M5)

- `heart/dashboard.py` — the one pure renderer (`term`/`oneline`/`md`/`html`/`json`),
  with `status.render` / `readiness.render_block` refactored to delegate to it.
- `pyauto-heart dashboard` subcommand + the sourceable venv/shell one-line hook.
- Extend `pulse-health.yml` to render + publish the board (Pages + step summary +
  README badge/block), keeping the tracking-issue alerting.
- Health Agent renders the dashboard card for mobile; manifest + capabilities
  updated.
- Tests: renderer snapshot tests for each `fmt` (stdlib-only), a staleness path,
  and a "cloud-only-honest" path that marks local-only checks as unobserved.

## Out of scope (later)

- Historical time-series / trend graphs of the score (a v2 — needs a data store
  beyond the single `state.json`; the `validation_history/` archive is a seed).
- Slack/email push or any non-GitHub notification channel.
- Per-repo drill-down pages (the single board first; deep links later).

## Open design decisions (resolve during implementation)

1. **Canonical web board = cloud-only-honest vs dev-box-pushed-complete?** The
   cloud job lacks the local-only checks. Either publish an honest partial board
   from cloud, or have the dev-box `watch` daemon push the full snapshot to Pages.
   Recommend: cloud-only-honest as the always-on baseline, with an optional
   dev-box push that *enriches* the same page — never two competing pages.
2. **Pages vs README-block as the primary "webpage"?** The ask says "GitHub
   webpage," which points at Pages; the README block is the zero-hosting
   fallback. Recommend shipping both from day one (same `md`/`html` renderer) and
   letting the badge be the entry point.

## Validation

- `pytest tests/` in PyAutoHeart stays green; add `tests/test_dashboard.py`
  covering each `fmt` and the staleness / unobserved-check paths.
- Manually: `pyauto-heart dashboard` (+ `--oneline`/`--md`/`--html`) renders from
  a cached snapshot; source the venv hook in a fresh shell and confirm it adds a
  single instant line and degrades cleanly with no state.
- The scheduled workflow publishes a Pages board + step summary + README badge on
  a dispatch, and the Health Agent card renders on `pyauto-brain health`.
- All four surfaces show the SAME verdict/score for the same snapshot (the unify
  invariant) — assert it in a test that renders `term`/`oneline`/`md`/`json`
  from one fixture and diffs the extracted verdict/score.

## PR

One PR: "PyAutoHeart: unified health dashboard (GitHub Pages + CLI/venv +
mobile) — M5". Note the README/Pages/manifest surface changes and confirm the
observer boundary is preserved (writes only within PyAutoHeart's own repo/state).

## Provenance

Drafted in the M4 release-validation-orchestrator session, immediately after M4
(PyAutoBrain #8) merged, when a live `pyauto-brain health` run went RED purely
because every repo was on the dev branch — a vivid reminder that the health
signal exists but has nowhere unified to *appear*. Expands the M5 placeholder in
`feature/pyautoheart/release_validation.md` from "mobile UX polish" to the full
one-dashboard-three-surfaces design the user asked for.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
