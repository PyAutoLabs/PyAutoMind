# Dashboard titles two drafts "Filed: 2026-11-05 (…" because their header sits above the H1

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
Themes:
- dashboard
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: after the fix and `pyauto-brain intake --apply dashboard`, `grep -c '>Filed: 20' dashboard.md dashboard.html` prints 0 for both (4 each on main at e9c34daa4), and every `draft/**/*.md` outside an epic's `*_reviews/` folder has a `# ` heading as its first non-blank line
Review-minutes: 2
Unattended: ready
Verified: 2026-11-16 98f42277 (PyAutoMind)
Lane: any
Filed: 2026-11-16

## Reproduce

On PyAutoMind main (e9c34daa4):

```
grep -c '>Filed: 20' dashboard.md dashboard.html     # 4 and 4
grep -o '>Filed: 2026-11-05 ([^<]*' dashboard.md | sort -u
# >Filed: 2026-11-05 (found by the autolens_profiling#519 worker-route…
# >Filed: 2026-11-05 (phase 2 of autolens_profiling#519; Pulse task…
```

Both rows appear in Recent and in Backlog with that text as the task title.

## Expected

The rows show the drafts' real titles: "Sibson serial kernel (the one every Nautilus
worker runs since #677) is ~1.25x slower…" and "Re-measure the DelaunayNN numba
Optimal cell on the Nautilus worker route…".

## Actual

Two drafts open with `Filed:` and `Lane:` lines *above* their `# ` heading:

- `draft/bug/autoarray/sibson_serial_kernel_loses_allocation_hoisting.md` (lines 1-2)
- `draft/feature/autolens_profiling/delaunay_nn_numba_optimal_remeasure_after_677.md` (lines 1-2)

The `Filed:` line was written first when the drafts were filed (f4a8fc046,
2026-11-05) and the Lane backfill (beebefb6f, 2026-11-13) added `Lane: any` beneath it.
`REFERENCE.md`'s header convention ("Prompt file format") puts `# Short task title` first. The renderer's
`_title` takes the first non-blank line, so these titles come out as the `Filed:` line.

## Likely fix location

PyAutoMind only: in each of the two drafts, move the `Filed:` and `Lane:` lines from
above the `# ` heading into the header block below it, keeping their values, then
regenerate `dashboard.md` and `dashboard.html`. (Separately, PyAutoBrain `_intake._title` has a docstring
that says "first markdown heading, else first non-empty line" but does not look for a
heading first. That is a Brain hardening item and is out of scope here.)
