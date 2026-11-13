# Goals

What the human wants the organism working towards, **in order**: goal 1
outranks the rest. A shift brief copies this list into its `goals:` block
(`pyauto-brain batch brief --new <slot>`), and the dashboard shows it at the
top of the page.

**This file is public**, as all of PyAutoMind and its Pages dashboard are.
Write nothing here that should not be read by anyone.

It is written from the dashboard's Goals box (one goal per line, top first,
through `.github/workflows/dashboard_input.yml`) or by hand. Either way,
`scripts/lifecycle.py check` validates it: goals are numbered 1..n with no
gaps, there are at most 10, a goal is one line of at most 200 characters, and
the only fields are the three below. An empty list is valid.

The queue says *which tasks*, in order (`queue.md`); goals say *why*, and what
a brief's backlog dip should favour. The planner's ranking reads the queue,
not this file.

## Schema

```markdown
## <n>. <goal, one line, at most 200 characters>
- epics: <slug>, <slug>    # optional: epics.md slugs this goal advances
- tags: <tag>, <tag>       # optional: themes.md keywords
- note: <one line>         # optional
```

`batch brief --new` scopes the brief's backlog dip to the union of the goals'
`epics:` and `tags:` (`backlog: scoped`), or to `fill-idle` when no goal names
any. An `epics:` slug that `epics.md` does not list is a warning, not drift.
A goal edited on the dashboard keeps its fields when its text is unchanged,
even if it moved.

<!-- goals: the list starts below this line -->
