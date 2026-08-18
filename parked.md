# Parked tasks

Tasks that were started or scoped but are not currently in flight. Listed
here so they remain visible across machines instead of disappearing into
unindexed worktrees or stashes. Move an entry back to `active.md` (or to
`planned.md` if re-scoping is needed) when work resumes; on shipping,
write the dated `complete/<YYYY>/<MM>/<slug>.md` record instead.

## matplotlib-inline-standalones
- prompt: active/matplotlib_inline_standalones.md
- parked: 2026-08-08 — surfaced by the orphaned-prompt triage; VERIFIED INCOMPLETE, not shipped
- classification: refactor (autolens_workspace + autogalaxy_workspace)
- remaining: the prompt calls for removing five standalone `# %matplotlib inline` comments.
  At least TWO survive on autolens_workspace main —
  `scripts/interferometer/features/advanced/potential_correction/start_here.py:36` and
  `scripts/imaging/features/advanced/potential_correction/start_here.py:56`.
  The autogalaxy_workspace half was not counted; do that first to confirm how many of the
  five are left.
- note: do NOT broaden into the old `pyprojroot` bootstrap sweep — the prompt is explicit
  that the dependent AutoCTI follow-up owns that.

## pyautoreduce-slacs1430-acs-comparison
- prompt: active/pyautoreduce_slacs1430_acs_comparison.md
- parked: 2026-08-08 — surfaced by the orphaned-prompt triage; STATE UNVERIFIED
- classification: test (PyAutoReduce + autolens_assistant)
- why unverified: the comparison targets a collaborator dataset at
  `/mnt/c/Users/Jammy/Science/subhalo/dataset/slacs/slacs1430+4105`, which this session cannot
  see. Confirm from the laptop whether the reduction and parity fits were ever run.
