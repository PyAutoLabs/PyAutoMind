# cortex-checkin-p1-shed-review-slot

Phase 1 of the `cortex-checkin` epic: the review-slot and gate apparatus is
retired from the Cortex and from the Brain's cortex conductor.

## What shipped

- **PyAutoBrain#348** — merged `fc1cb32f6e226ddd2da24448769f1f77ebed6421`
- **PyAutoCortex#10** — merged `6cd6220e8e86711919c8261d3230564f22b09036`

Issue: PyAutoCortex#9 (closed completed 2026-09-04).

Gate grading is gone — the daily grading cron, the `--grade` / `--write` legs of
`gates`, and the `Gates-cleared:` / `Gate-override:` header keys with the three
`check` invariants over them. The plain `Gates:` header, the `gated` state and
the read-only `gates` listing stay; a gated phase is moved on by a human reading
the listing and typing `move <phase> ready`. Also retired: the batch record and
packet schema for the cortex kind (`batches/` becomes closed, append-only
history and `Batch:` becomes optional-historical), `rule --also`, the `Lane:`
header, and the hand-rolled restricted-YAML parser, which `yaml.safe_load`
replaces with the field validation kept. `collect` is decoupled from the batch
record. Recorded as schema decision 58 in `docs/schema_decisions.md`.

The measurement behind it: gate grading saw 2 gated refs and flipped 0 in its
lifetime; 0 review slots were opened by the conductor, 0 rulings came from a
packet, 0 partial reviews were filed and `review-minutes-actual` was never
filled — all 22 rulings were reached in a live session. `rule --also` was never
used, `Lane:` read `local-dev` on 32 of 32 phases, and the restricted parser's
own PyYAML-parity test proved it redundant.

## Merge notes

Merged Brain before Cortex: PyAutoCortex's `dashboard_refresh.yml` renders the
board through PyAutoBrain **main**, so the Cortex PR's `refresh` check stays red
until the matching Brain PR has landed. It went green on the re-run after #348.

PyAutoCortex#10 arrived at merge time `CONFLICTING`/`DIRTY`: `main` had moved
under the branch (`1a39784` self-healed the generated pages, `1815c69` graded
the gates and flipped `phases/euclid/dr1_prelim_10_lens_science_run.md` to
`ready`). The only conflicted paths were the two generated pages. Resolved with
a merge commit (`2ddb47b`) that keeps `main`'s gate flip, drops the
`Gates-cleared:` key this phase retires, and regenerates `dashboard.md` +
`dashboard.html` with the phase-1 renderer rather than hand-resolving them.
`cortex.py check` OK, `dashboard --check` current.

## Heart

RED at merge time, acknowledged by the human on 2026-09-04: "release validation
FAILED (stage integrate)"; "PyAutoArray: open PR 12d old". Both are
release-chain facts about other repos; neither PyAutoBrain nor PyAutoCortex is
in the release chain. No `pending-release:` obligation — both are organ repos,
not published libraries.

## Tests

Brain `test_cortex_conductor` 67 passed (13 new); full Brain suite 889 passed /
2 failed, both `test_branch_sweep` failures pre-existing and control-tested
unchanged on the base. PyAutoCortex `test_cortex` 95 passed (2 new).

## Original prompt

# Cortex: shed the review-slot and gate apparatus the check-in loop never uses

Type: maintenance
Target: pyautocortex
Repos:
- PyAutoCortex
- PyAutoBrain
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: high
Status: draft
Consequence: judge
Witness: in PyAutoCortex `grep -rn "gates_grade\|Gates-cleared\|Gate-override\|--also\|^Lane:\|review-minutes\|packets/" --include=*.md --include=*.py --include=*.yml . ` returns only `complete`-style history under `batches/reviews/` and `rulings/`; `.github/workflows/gates_grade.yml` and `batches/packets/` are gone; `scripts/cortex.py` imports `yaml` and has no `parse_projects` hand parser; in PyAutoBrain `grep -rn "plan_cortex\|cortex_plan_record\|carried_members\|CORTEX_CHIPS\|REVIEW_PART_RE\|_next_review_path" agents/ board/ skills/` returns nothing; `pyauto-brain cortex collect --pull --apply` runs with NO batch record and no `--phase` and scores every submitted/running phase; `pyauto-brain cortex dashboard --check` is current with no status box; Cortex `pytest -q`, Brain `pytest -q` and `cortex.py check` pass; the dashboard renders every existing section except the status box
Review-minutes: 20
Unattended: ready
Epic: cortex-checkin
Phase: 1
Filed: 2026-09-03
Issued: 2026-09-03

Phase 1 of `cortex-checkin` (ledger `draft/maintenance/pyautocortex/cortex_checkin_epic.md`).
Two PRs: PyAutoCortex (schema, scripts, workflows, tests, docs) and PyAutoBrain
(conductor, batch cortex kind, status box, skills). Deletion only, plus the one
decoupling the door needs (item 6). Keep every historical record readable.

## Delete — PyAutoCortex

1. **Gate grading**: `.github/workflows/gates_grade.yml`; in `scripts/cortex.py`
   the `gates --grade/--write` path (`_http_gate`, `fetch_gate_states`,
   `grade_gate`, `gates_report` ~L929-1092) and its tests; the
   `Gates-cleared:` / `Gate-override:` keys and the three `check` invariants
   that reference them (REFERENCE.md ~L148-157). KEEP the plain `Gates:`
   header, the `gated` state, `GATE_REF_RE`/`gate_url` and the read-only
   `gates` listing (no `--grade`): a gated phase is moved to `ready` by a
   human typing `move ready`. Update AGENTS.md/REFERENCE.md/schema_decisions
   (append a dated decision: "gate grading retired 2026-09-03; sequencing is
   prose `Ready when:` per decision 54").
2. **`rule --also`** fan-out (never used) — remove flag, code, tests, docs.
3. **`Lane:`** header — remove from the schema, `check`, `new` template, the
   32 phase files (one mechanical sweep), and the "laptop lane" prose in
   AGENTS.md. Brain's `_batch.py` lane filter for cortex kind goes with item 7.
4. **Restricted-YAML parser** (`parse_projects` ~L290-400 + the six parity
   tests): replace with `yaml.safe_load` and keep the FIELD validation
   (required keys, `status` values, path shape). Add `pyyaml` to whatever
   declares Cortex's deps (`cortex_check.yml` pip line, README install line).
5. **Batch record + packet schema**: delete `batches/packets/` (TEMPLATE.md,
   AGENTS.md, the three HTML files), the batch-record schema section in
   REFERENCE.md and `batches/AGENTS.md`'s slot/shift/review-at/review-minutes
   vocabulary and partial-review (`-r<N>`) rules, and `batch_problems` +
   `_review_section_problems` in `cortex.py` (~L772-893) with their tests.
   KEEP `batches/2026-*.md` and `batches/reviews/*.md` as read-only history
   (the human's verbatim words are cited by 13 rulings) — add a two-line
   `batches/AGENTS.md` saying exactly that, and make the ruling `Batch:`
   field optional-historical in the schema. Ledger-merge classification for
   `batches/` becomes "history: never modified, only added" or drop the path
   from the classifier — state which.
6. **Decouple `collect` from the record** (Brain side, but list it here so the
   Cortex side does not still document `--slot`): the door needs
   `collect --pull --apply` with no record: default scope = every phase in
   `submitted|running`, `--phase REL` narrows, `--slot` goes away.
   `apply_ops` keeps moving `running → pulled → awaiting-ruling`; the record
   rewrite leg is deleted.

## Delete — PyAutoBrain

7. In `agents/conductors/batch/_batch.py`: `plan_cortex`, `cortex_plan_record`,
   `carried_members` / `carried:` / `carried-from:`, `CORTEX_CHIPS` and the
   cortex packet rendering, `REVIEW_PART_RE` / `_next_review_path` (partial
   reviews, shipped as PyAutoCortex#7 / PyAutoBrain#342 — revert cleanly),
   `--kind cortex` on `plan`/`collect` entirely, the cortex lane gate
   (`detect_lane` stays for dev if dev uses it; delete if cortex-only), and
   `--push` integration for the cortex kind (`_integration.py`). Dev batching
   is untouched.
8. `agents/conductors/batch/_status.py`: the Cortex status box and the strip
   `_cortex.py` renders above "awaiting" (dashboard shows "No batch in
   flight" today). Delete the render call in `_cortex.py` too.
9. `agents/conductors/cortex/_cortex.py`: the `plan` verb (`plan`, `emit_plan`
   ~L972-1050), the `gates --grade --apply` wrapper (~L1856), `--slot` on
   `collect` (item 6). Keep `census`, `dashboard`, `collect` (decoupled),
   the payload builders (`_ruling_payload`, `launch_payload`, `_live_payload`,
   `_epic_payload`, `_project_payload`) — phase 2 and 3 build on them.
10. Skills/docs: `skills/batch/batch.md` science section (~L152-176) → one
    paragraph pointing at `/cortex` (phase 2); `skills/cortex/cortex.md` verb
    menu loses `plan` and `gates --grade`; `agents/conductors/cortex/AGENTS.md`
    and `batch/AGENTS.md` (~L545-600 rolling-board / carry prose) updated;
    `skills/COMMANDS.md` row for `/cortex` stays (phase 2 installs it).
11. Tests: delete the tests of the deleted things; keep every test of a kept
    thing green. Mind the `_batch` substring trap in `_cortex.py` noted in
    memory, and the tenant firewall (no real org/repo names in new fixtures).

Then: Cortex `pytest -q` + `python3 scripts/cortex.py check`; Brain `pytest -q`
(one known worktree-only failure: `test_cortex_conductor::test_a_fixture_tree_finds_the_schema_its_checkout_ships`);
regenerate the Cortex dashboard from inside the Cortex checkout
(`python3 ../PyAutoBrain/agents/conductors/cortex/_cortex.py dashboard --cortex . --apply`)
and confirm `--check` is current; open both PRs.
