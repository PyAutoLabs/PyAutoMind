- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/211 (closed on merge)
- completed: 2026-08-08
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/212 (squash-merged as `f4e9341`); Mind bookkeeping PyAutoMind#156
- summary: the `feature`, `bug` and `refactor` selection modes all failed silently — each rooted prompt discovery at `mind/<work-type>/`, dead since the lifecycle split (#71) closed 2026-07-13 and prompts moved under `draft/<work-type>/<target>/`. 86 backlog prompts were invisible to the three front doors. Fixed with one shared `discover_prompts(mind, work_type)` in the sizing faculty plus three thin delegations, an 11-test regression suite, and a docs leg correcting stale Mind paths. CI green on both pytest legs (3.12/3.13); 261 tests pass locally (250 existing + 11 new).

## Key findings

- **The shipped fix for this exact bug class was half a fix.** `brain-lifecycle-path-fixes` (PyAutoBrain#128, complete/2026/07) taught the *reader* — `parse_prompt` strips the `draft/` state folder — but never the *discoverer*. Specific mode (`feature <path>`) has been correct throughout; only selection was dead. Its folded prompt explicitly warned "assume the parser is shared or copied"; the sweep caught `parse_prompt` and stopped there. **When a path assumption is found in one place, grep for the operation, not the function** — `parse_prompt` was fixed, `discover()` was three doors down.
- **It failed silently, which is why it survived ~4 weeks.** Each verb printed a plausible "no prompts found" and exited 4. A human reads that as an empty backlog, not a broken root. The regression test that now guards it is the end-to-end one — each conductor's selection surface must be non-empty on a `draft/`-layout Mind — not the unit tests on `discover_prompts` itself.
- **Second latent bug fixed on the way:** `bug health` probed `mind/bug/health_fixes/` and so reported health-fix prompts `absent`. They exist at `draft/bug/health_fixes/`; it now reports `present`. Same root cause wearing a different symptom, found only by sweeping the stale path strings rather than stopping at the code.
- **The sizing heuristic mis-sized its own bug report.** Intake scored this `large` (8) — +4 for prompt verbosity, +2 for the word "architectural", +2 for a second repo — for a change that is four functions in one repo plus a test file. The header was overridden to `small`/`safe` at filing with the rationale recorded inline. Worth remembering when reading `Difficulty:` on any *detailed* prompt: the heuristic partly measures how much was written, not how much must be done.

## Decided scope

- **`active/` is deliberately not discovered.** It is flat (its paths carry no work-type to filter on) and holds issued, in-flight work, whereas selection answers "what should I start next". In-flight prompts referenced from `active.md` / `planned.md` stay handled by the existing down-rank.
- **The silent-empty failure mode was left out of scope** — making an empty backlog distinguishable from a broken root is a real improvement but separate work. Not filed; file it if the pattern recurs.

## Verified, no change needed

`_referenced_paths` / `_referenced_bug_paths` regexes (`[\w./-]*feature/…`, `[\w./-]*bug/…`) already match `draft/`-prefixed paths, so in-flight down-ranking worked as soon as discovery did.

## Debt left behind

`planned.md` still lists `brain-lifecycle-path-fixes` as planned/blocked, though it shipped 2026-07-16 with its record in `complete/2026/07/`. Stale entry for the next `planned.md` sweep — deliberately not touched here to keep this task to one change.

## Environment note

Shipped from a cloud/web session, so there was no `~/Code/PyAutoLabs-wt/` worktree layout: work ran directly in the PyAutoBrain checkout on the session-designated branch `claude/automind-task-planning-tj0sdn` rather than `feature/<task-name>`. Tests ran via `uv run --python 3.11 --with pytest --with pyyaml pytest tests/` — the sandbox's `pytest` is a uv tool install with an isolated venv lacking `pyyaml`, which `_sizing.py` needs for the body map.

## Original prompt

# Conductor discovery predates the lifecycle split — feature/bug/refactor selection is dead

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised

<!-- Header corrected from the IntakeDecision at filing time (2026-08-08):
     difficulty large -> small, autonomy supervised -> safe, and PyAutoMind
     dropped from Repos. The sizing heuristic scored 8 off prompt verbosity
     (+4 words), the word "architectural" (+2 risk) and a second repo (+2) —
     it was measuring this prompt's detail, not the change. The change is four
     functions in one repo (a new shared discover_prompts plus three thin
     delegations), one new test file, and doc-string path corrections; no
     behaviour outside the three conductors' selection modes. PyAutoMind is
     read by the fix but not modified by it, so it is not a claimed repo. -->

The `feature`, `bug` and `refactor` selection modes are all broken and fail
silently. Reproduced 2026-08-08 on PyAutoBrain main (83b65f1):

| Command | Prints | Real backlog |
|---------|--------|--------------|
| `bin/pyauto-brain feature` (bare, `select --impact`, `select --difficulty easy`) | `feature agent: no feature prompts found in PyAutoMind.` | 39 prompts |
| `bin/pyauto-brain bug` (bare, `select`) | `bug agent: no bug prompts found in PyAutoMind/bug/.` | 43 prompts |
| `bin/pyauto-brain refactor` (bare, `candidates`) | `no prompts under refactor/` -> `Backlog (0)` | 5 prompts |

## Root cause

Three copies of the same pre-#71 assumption — discovery roots at
`mind/<work-type>/`, but prompts have lived under `draft/<work-type>/<target>/`
since the lifecycle split (PyAutoMind#71) closed 2026-07-13:

- `agents/conductors/feature/_feature.py:186` — `feat = mind / "feature"`
- `agents/conductors/bug/_bug.py:305` — `bug = mind / "bug"`
- `agents/conductors/refactor/_refactor.py:108` — `root = mind / "refactor"`

This is unshipped residue of `brain-lifecycle-path-fixes` (PyAutoBrain#128,
complete/2026/07). That task fixed the *reader* — `parse_prompt` strips the
`draft/` state folder, and specific mode is correct today (verified by passing
an explicit draft-layout prompt path). It never touched the *discoverer*. The folded prompt warned "assume the parser is shared or copied";
the sweep caught `parse_prompt` and stopped there.

It fails silently: each path prints a plausible "nothing found" and the shell
sees exit 4, so a human reads it as an empty backlog rather than a broken root.

## Fix

Follow the doctrine #128 established — one definition in the shared sizing
faculty, not three patches.

1. `agents/faculties/sizing/_sizing.py` — add `discover_prompts(mind, work_type)`
   beside `parse_prompt`. Scans `draft/<work-type>/**/*.md`; keeps legacy flat
   `<work-type>/**/*.md` resolving (matching `parse_prompt`'s third path
   regime); excludes `complete/` and `complete/archive/`; filters `README.md`
   (hoisted from the bug agent's ad-hoc filter); de-dupes.
2. `_feature.py` / `_bug.py` / `_refactor.py` — the three `discover*()`
   functions become thin delegations to it.
3. `tests/test_conductor_discovery.py` — new, on the `tests/test_sizing_paths.py`
   tmp_path-Mind pattern. Lock draft/, legacy flat, `complete/` exclusion,
   README exclusion, and one end-to-end assertion per conductor that `select()`
   returns non-empty — the regression that would have caught this.
4. Docs leg — stale Mind paths in prose and user-facing messages:
   `_bug.py:421,422,432,502`, `bug.sh:75`, `BUG_TAXONOMY.md:9,82,108`,
   `skills/bug/bug.md:16`, `refactor/AGENTS.md:12`, and the "Scan `feature/**`"
   line in `feature/AGENTS.md`. `health_fixes/` is real but now lives at
   `draft/bug/health_fixes/`.

## Decided scope

- **`active/` is NOT discovered.** It is flat and by definition already started;
  selection answers "what next". Excluding it also avoids parsing every file to
  recover a work-type the path no longer carries. In-flight prompts referenced
  from `active.md` / `planned.md` stay handled by the existing down-rank.
- **The silent-empty failure mode is out of scope.** Making an empty backlog
  distinguishable from a broken root is a real improvement but is scope creep
  here; file separately if wanted.

## Verified, no change needed

`_referenced_paths` / `_referenced_bug_paths` regexes (`[\w./-]*feature/…`,
`[\w./-]*bug/…`) already match `draft/`-prefixed paths, so in-flight
down-ranking works once discovery is fixed.

<!-- filed 2026-08-08; found by running /feature to pick a task and hitting the dead selector -->

<!-- formalised by the Intake (Conception) Agent on 2026-08-08 from file:/tmp/claude-0/-home-user/a776a449-cbea-5069-9c29-7ed6fa93a291/scratchpad/conductor_discovery.md -->
