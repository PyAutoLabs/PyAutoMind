# Questions

Parked questions from shift workers, waiting for the human (M3.5,
PyAutoBrain#645). The shift watcher adds entries through its one Mind writer;
a `/questions` chat (PyAutoBrain `skills/questions`) answers, defers or drops
them with `scripts/questions_edit.py`. Never edit by hand: the section an
entry sits under is its state, and `lifecycle.py check` validates the file.
An answer releases the parked task: the next shift resumes it with the answer
in its prompt. Kind `ruling` is filed by the readiness pass (PyAutoBrain
`batch ready`, M3.3) for a gate on a queued task: it carries `gate:`, may have
no `issue:`, never holds or releases a parked task, and answering it records
the ruling on the prompt.

```markdown
### Q<n>. <task> — <short ask>
- task: draft/<work-type>/<target>/<name>.md
- issue: https://github.com/<owner>/<repo>/issues/<n>
- kind: question
- gate: <kebab-case slug>         (kind ruling only; a ruling may have no issue:)
- ask: <one line>
- options: (a) <first> · (b) <second>
- shift: <slot>
- asked: <YYYY-MM-DDTHH:MMZ>
- worker: <session key>
```

## Open

## Deferred      <!-- entries add: - until: YYYY-MM-DD (absent: until the next sitting) -->

## Answered      <!-- entries add: - answered: <time> by <login> (chat|issue), - answer:, - answer-comment: <url> -->

### Q3. dataset_model_free_grid_offset_pytree_roundtrip — PyAutoFit is claimed by ep-projected-model-shared-prior (#1773). No f…
- task: active/dataset_model_free_grid_offset_pytree_roundtrip.md
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1777
- kind: question
- ask: PyAutoFit is claimed by ep-projected-model-shared-prior (#1773). No files overlap. Allow a separate worktree off main for this fix?
- options: (a) Override: separate worktree off main now (recommended) · (b) Wait until #1773 merges · (c) Drop: blocks nothing today
- shift: 2026-11-16-pm
- asked: 2026-11-16T18:38Z
- worker: b778571d
- answered: 2026-11-16T18:42Z by Jammy2211 (issue)
- answer: Use 1: (a) override — separate worktree off main for this fix alongside #1773, since no files overlap.
- answer-comment: https://github.com/PyAutoLabs/PyAutoFit/issues/1777#issuecomment-6925624924

### Q1. cluster_regime_narrative — The `features/extended_source/` example and the `autolens_workspace_t…
- task: active/cluster_regime_narrative.md
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/670
- kind: question
- ask: The `features/extended_source/` example and the `autolens_workspace_test` script are parked with a question on the issue (`awaiting-input`): which data, how the mass model is handed off, and whether…
- shift: 2026-11-14-pm2
- asked: 2026-11-14T17:56Z
- worker: a033837e
- answered: 2026-11-18 by Jammy2211 (chat)
- answer: Not now — cluster extended sources will not be developed for a while. The questions moved unanswered to draft/feature/workspaces/cluster_pixelized_analysisfactor.md ("Deferred"); prose half merged as autolens_workspace#671.
- answer-comment: https://github.com/PyAutoLabs/autolens_workspace/issues/670#issuecomment-6974154944

## Dropped       <!-- entries add: - dropped: <date> by <login> — <why> (task shelved) -->

### Q2. markdown_regeneration_sigma_min — The human answered "do 1" (real regeneration off the laptop) at 18:32…
- task: draft/docs/autolens_workspace/markdown_regeneration_sigma_min.md
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/669
- kind: question
- ask: The human answered "do 1" (real regeneration off the laptop) at 18:32Z, but neither machine for option 1 can be used unattended, so the human has to choose (a) laptop GPU with them there or (b) RAL w…
- shift: 2026-11-14-pm3
- asked: 2026-11-14T20:23Z
- worker: a8222e1a
- dropped: 2026-11-16 by Jammy2211 — Lets retire this markdown feature (the human on autolens_workspace#669, 2026-11-16 09:13) (task shelved)
