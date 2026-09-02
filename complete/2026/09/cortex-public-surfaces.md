- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/385 (closed completed 2026-09-02)
- completed: 2026-09-02
- workspace-pr: PyAutoBrain https://github.com/PyAutoLabs/PyAutoBrain/pull/336 (`cf9efc5`, merge `eb59b44`) →
  pyautolabs.github.io https://github.com/PyAutoLabs/pyautolabs.github.io/pull/7 (`a573169`, merge `14df8f2`) →
  PyAutoScientist https://github.com/PyAutoLabs/PyAutoScientist/pull/27 (`f14a454`, merge `44a68f2`) →
  PyAutoCortex https://github.com/PyAutoLabs/PyAutoCortex/pull/6 (`f75d8e0`, merge `ef3522e`).
- classification: feature (pyautocortex) — epic `cortex-birth`, phase 6 of 7 (0–6), **the last**. Gates:
  phases 4 (SHIPPED #383) and 5 (SHIPPED PyAutoBrain#334) — met; "one real Cortex batch reviewed" — **not
  met**, so the retrospective landed as a stub naming what it waits for (the human's instruction for the
  overnight run). Prose and ledger only; no code.
- heart: n/a for a prose-only phase; YELLOW 65 at the time (manifest drift; CI status unavailable in the
  web container), recorded on the two earlier entries tonight.
- gate: docs build ✓ (local Sphinx 9.1 + myst, zero warnings, same as the baseline; the Brain `Docs` PR
  check) · `cortex check: OK` · smoke n/a · review: prose reviewed by the architect against the shipped
  repos (no adversary leg — no code, no witness to falsify) · CI: PyAutoBrain #336 `docs / docs-build` +
  pytest 3.12/3.13 green; PyAutoCortex #6 merge-gate job green (README is outside `cortex_check.yml`'s
  paths); **pyautolabs.github.io #7 and PyAutoScientist #27 have no PR checks configured** — merged
  on the human's standing /prm authorisation for the night, stated here rather than assumed green.

- summary: **the Cortex's public surfaces.** `PyAutoBrain/docs/organs/cortex.md` rewritten from its
  phase-0 stub ("born empty; phase 1 fills it") to the organ as shipped through phase 5: the ten-state
  model and who owns each edge (`move` for every edge but the three ruling states, which only `rule`
  reaches; `accepted` non-terminal, `dropped` terminal; `legacy`/`legacy_wrong` run states), the
  ruling-of-record rule, the `Gates:` grammar and the daily grading job, what the Cortex never does
  (dispatch, hold data, run under an autonomy level, read `sacct` as health), the cortex conductor verbs
  plus the batch conductor's `--kind cortex` doors and carry-forward, the board with the first image in
  the Brain docs (`docs/_static/cortex_board.png`, rendered with headless Chromium from the checkout's own
  generated dashboard), the adopter note. The docs hub's "Read how it works" links the organ page and the
  live board. The PyAutoScientist README gains its Cortex paragraph after the Ears paragraph (the generated
  organ table already carried the row). The Cortex README's walkthrough names the ten states and the batch
  doors. The epic ledger gains "What the first Cortex batch taught" as a **stub** — no batch has been
  planned and reviewed through the phase-5 door; neither 2026-08-31 record carries a numeric
  `review-minutes-actual:` — with the four questions to answer and the unblocker (the first
  `batch plan --kind cortex --apply` record closed with a review at the laptop), and "Deferred" with the
  five items and their reasons (Eyes fold-in after two batches; `hpc/sync` unification only if the
  retrospective shows cost; no template until a fork asks; the two-kind board strip is `batch_board.md`'s;
  no `cortex: true` flag — the phase-2 badge resolver reads the phases, a Mind flag would be a second
  source).

- decisions: **65** the prompt's witness ("the retrospective cites the first Cortex batch record's
  `review-minutes-actual:`") is recorded as **amended, not met**: no such number exists on any record;
  the stub names it as the unblocker rather than inventing evidence. **66** the organism overview and the
  index toctree already linked the page (phase 0) and there is no `llms.txt` census in PyAutoBrain — both
  Task-1 items are no-ops, stated rather than faked. **67** the board screenshot is taken from the local
  generated `dashboard.html`, not the live Pages host (the container's proxy CA is not trusted by
  Chromium); it will age with the counts and the prose quotes none of them.

- witness: Sphinx build of `docs/` → zero warnings (baseline zero), image copied to `_images/`;
  `cortex check: OK`; `lifecycle check: OK`; the four PRs green/merged as recorded above.

- lane notes: web-github session; PyAutoScientist and pyautolabs.github.io attached and cloned mid-session
  with push access (their session branch created from the default branch); PyAutoHeart cloned read-only
  for vitals. `/prm` local-only legs skipped — nothing to remove.

- follow-ups NOT filed (findable here): the retrospective proper, when the first conductor-opened Cortex
  batch closes with a review — its four questions are in the ledger; the screenshot re-render when the
  board's counts change materially.

- next: **the cortex-birth epic is complete** — phases 0–6 SHIPPED. `epics.md` marks it SHIPPED with this
  record. The first real Cortex batch through `batch plan --kind cortex` is the laptop's next act, and the
  retrospective follows it.

## Original prompt

# Cortex phase 6 — public surfaces and the retrospective

Type: feature
Target: pyautocortex
Repos:
- PyAutoBrain
- PyAutoScientist
- pyautolabs.github.io
- PyAutoCortex
Themes:
- docs-hub
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Consequence: glance
Witness: RTD organ page for the Cortex builds and is linked from the organism page; PyAutoScientist README lists eight organs; the retrospective section cites the first Cortex batch record's `review-minutes-actual:`
Review-minutes: 10
Unattended: ready
Epic: cortex-birth
Phase: 6
Parent: draft/feature/pyautocortex/cortex_birth_epic.md
Filed: 2026-09-01
Issued: 2026-09-02

Phase 6 of 7 in the PyAutoCortex birth epic — the last. **Gates: phases 4 and
5**, and **one real Cortex batch reviewed** (so the retrospective has evidence,
not intentions).

## Task

1. **RTD**: `PyAutoBrain/docs/` organ page for the Cortex in the register of
   the other six (what it owns, what it never does — dispatch, data, autonomy —
   the state model, the ruling-of-record rule, the gate grammar, one screenshot
   of the dashboard). Link from the organism overview page and the docs hub
   (`pyautolabs.github.io`). Update the `llms.txt` census if the organ pages
   are enumerated there.
2. **PyAutoScientist**: the README organ table is generated by
   `repos_sync.py` (phase 0) — verify it reads correctly and add the one
   paragraph the landing page carries per organ, in its voice.
3. **Cortex README**: the human-facing "how a science run moves through the
   Cortex" walkthrough (planned → gated → ready → submitted → running → pulled
   → awaiting-ruling → ruled), mirroring the Mind README's four-step lifecycle
   prose, with a link to the live dashboard.
4. **Retrospective**, appended to the epic ledger under "What the first Cortex
   batch taught": the first Cortex record's planned vs actual review-minutes;
   whether the rolling board removed the CARRIED pattern; whether any gate
   flipped automatically; what the human had to do by hand that the design
   said would be automatic. Facts, then at most three follow-up prompts filed
   through `/intake`, each with its issue created if it gates a Cortex phase.
5. **Deferred list**, recorded in the ledger so nobody re-derives it:
   - Eyes conductor fold-in (figure review as part of a science review) — open
     question, decide only after two Cortex batches.
   - `hpc/sync` unification across the three projects — file only if the
     retrospective shows the divergence cost review minutes.
   - Cortex template / `spawn.py` rule — only when a fork asks.
   - The batch board strip showing both kinds (`batch_board.md`).
   - Whether `PyAutoMind/repos.yaml` `category: project` rows
     (`autolens_profiling`) should carry a `cortex: true` flag for the badge
     resolver — decide from phase 2's implementation.

## Acceptance

- The witness above; every deferred item has a one-line reason; the epic's
  `epics.md` entry is marked SHIPPED with the completion record path.

## Out of scope

- Any code. This phase is prose and the ledger close-out.
- Acting on the deferred list.
