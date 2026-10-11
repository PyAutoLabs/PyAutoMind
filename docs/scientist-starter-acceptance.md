# Independent starter: local conversational acceptance

Task: [Mind #502](https://github.com/PyAutoLabs/PyAutoMind/issues/502)

Epic: scientist-adoption-pilot

Observed: 2026-10-11

This bounded check exercises the minimal local Claude pilot: an independently
named Scientist, its own minimal Mind, one existing synthetic project, and a
second fresh conversation. It is not acceptance of the full development/release
workflow, other harnesses, independent hosting, or a real collaborator setup.

## Inputs

| Source | Revision |
|---|---|
| PyAutoMind | `e6efa4a4f323fc27d9c94fefbb6123ca46e9a828` |
| PyAutoBrain | `7ef9e23420c18d2602d99caec52a8fe40e08d8ac` |
| PyAutoScientist | `f0d5d12fb2363d4079a9e1e40991650cbffcf1ec` |

Claude Code 2.1.296; runtime reported `claude-opus-5-5` (no model override).
Brain and Scientist were copied using `git archive HEAD`, not edited or linked
back to the maintainer checkouts. Mind came from `spawn.py --minimal-mind`.
This run uses the merged instruction-isolation fix from Mind #501 and local
discovery from Brain #518. Reporting PRs Brain #519 and Scientist #70 are not
prerequisites or acceptance inputs.

The fixture uses Mira Scientist, `ExampleResearch/ResearchPlans`, and an
initially empty project catalogue with `organs: {}`. The existing `spectra/`
directory contains a README and a saved note about baseline spectrum selection A.
The same research intent is recorded in the generated Mind's `ideas.md`.
All identities are fictional; no repository existence or access is implied.

## Evidence and criteria

- Supported discovery produced 40 relative workspace-local skill links;
  `starter-check` reported 40 skills, zero missing.
- The first conversation invoked `Skill(sizing)`. The harness-injected skill
  message identified **`<fixture>/.claude/skills/sizing`** as its base directory;
  that link resolves to **`<fixture>/PyAutoBrain/skills/sizing`**. This establishes
  runtime provenance for the sampled skill, beyond a model's claim or a visible
  skill name. The sizing procedure itself was not run.
- That conversation read the local instance handoff, Mind instructions,
  registries and saved idea, project schema, profile and source notes. It added
  the explicitly supplied identity `spectra: ExampleResearch/Spectra` and the
  public `spectra` project with software resource `spectra-code`.
- SHA-256 comparison of 529 regular fixture files found exactly two changes:
  `PyAutoMind/repos.yaml` and `instance/projects.json`. There were no added or
  removed regular files. Framework files, research notes, task records and
  `instance.json` remained unchanged.
- Owner commands `--check-instance`, `--check-projects`, `--html` and `--json`
  exited successfully. The JSON projection has one project, the intended source
  URL and `boards: []`; HTML contains Mira Scientist and the Spectra source link.
  No assistant or optional organ was added.
- A fresh second conversation recovered the instance name, existing source
  relationship, empty task state and baseline-A idea by reading saved files. It
  correctly identified assistants/organs as optional and made no edits. The
  initial hash comparison also detected three new renderer bytecode caches:
  those were created by the intervening validation, not the conversation; all
  529 original file hashes were unchanged.
- Resumption was repeated in a third fresh process against a new baseline taken
  after validation. **All 532 regular-file hashes were unchanged**, no files
  were added/removed, and discovery still reported 40 skills, zero missing.
  The tool trace contains only Read/Glob/Grep despite the same narrowly allowed
  write tools remaining available. It recovered the same saved intent and
  connection without initialization or duplication.
- All three processes completed successfully with distinct session IDs and no
  permission denials. The resume prompts supplied neither the Scientist/project
  names nor the saved research note. Both responses separated configuration
  from validation and did not claim to have run tests.

**Result:** the bounded local connection/resumption criteria passed. The
limitations below remain; this does not certify an entire adopter harness.

## Reproduce the boundary

Use a new disposable workspace; never point this recipe at user records. Keep
raw session logs private. The prompts below are test inputs; identities and
visibility must come from the actual owner during real adoption.

1. Archive the pinned Brain and Scientist revisions into flat `PyAutoBrain/`
   and `PyAutoScientist/` directories. From the pinned Mind source run:

   ```sh
   python3 scripts/spawn.py --minimal-mind --write <fixture>/PyAutoMind
   ```

2. Set the generated Mind's identity map to these explicit fixture entries:

   ```yaml
   categories:
     organ: {}
     science: {}
   repos:
     PyAutoBrain:
       github: ExampleResearch/PyAutoBrain
       category: organ
     PyAutoMind:
       github: ExampleResearch/ResearchPlans
       category: organ
     PyAutoScientist:
       github: ExampleResearch/MiraScientist
       category: organ
   ```

3. At the fixture root initialize the instance and discovery:

   ```sh
   python3 PyAutoScientist/scripts/starter.py instance --repos PyAutoMind/repos.yaml \
     --name 'Mira Scientist' --repo PyAutoScientist \
     --pages-url https://example.invalid/mira/ --apply
   python3 PyAutoBrain/bin/project_discovery.py starter-write --root .
   python3 PyAutoBrain/bin/project_discovery.py starter-check --root .
   ```

   Add `spectra/README.md` describing a synthetic existing optical-spectra
   project, `spectra/notes.txt` with the baseline-selection note, and that intent
   in `PyAutoMind/ideas.md`. Hash every regular file before launching the conversation; validate and
   record the discovery link targets.

4. Start a fresh session at the fixture root with `PYAUTO_ROOT`, `PYAUTO_MIND`
   and `PYAUTO_BRAIN` explicitly pointing into it; remove inherited
   `PYAUTO_MAIN` and `PYAUTO_WT_ROOT`. Use the installed authenticated CLI:

   ```sh
   claude -p --setting-sources project,local \
     --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
     --settings '{"disableAllHooks":true}' \
     --tools Read,Glob,Grep,Edit,Write,Skill \
     --allowedTools 'Read,Glob,Grep,Skill(sizing),Edit(./instance/projects.json),Write(./instance/projects.json),Edit(./PyAutoMind/repos.yaml),Write(./PyAutoMind/repos.yaml)' \
     --permission-mode dontAsk --no-session-persistence \
     --output-format stream-json --verbose
   ```

   Supply stdin and save stdout/stderr to private files **outside** the fixture.
   Bound each process to 180 seconds; do not launch background sessions.
   No shell, network, MCP, delegation or publication tools are exposed. Hook
   execution is disabled. The two permitted configuration files are the only
   preapproved write targets. No global installer or auth changes are involved.

   First-session request:

   > This is an approved synthetic acceptance task, not a new development task.
   > Load sizing with the Skill tool only to establish provenance; do not run its
   > procedure. Read instance/SETUP.md, local Mind instructions and records,
   > the canonical identity map, PROJECTS.md, profile, project catalogue and
   > spectra source notes. Connect Spectra, a scientific_project comparing optical
   > spectra, repo key spectra, fictional GitHub ExampleResearch/Spectra,
   > category science. The owner permits public:true for this project and its
   > software resource spectra-code. Explain then apply only the two approved
   > configuration edits. Preserve every other file. No assistant or optional
   > organ is needed. Do not delegate, start workflows, publish, install, change
   > access or claim tests ran; the parent task validates independently.

5. Parse the tool transcript, not just its final answer. Require the local skill
   base-directory message, successful permitted edits, and no permission denials.
   Compare all file hashes: only the two approved paths may differ. Independently
   run the Scientist renderer with explicit instance/map/Brain paths and the four
   flags listed above; inspect the JSON relationships and HTML source link.

6. Take a **new hash baseline after validation**, including any Python bytecode
   caches created by the renderer. With the same persisted fixture and tool
   restrictions, start another fresh
   process **without** `--resume` and without supplying the previous transcript:

   > Resume this Scientist from saved files. Read instance/SETUP.md and the local
   > Mind instructions/registries, identity map, profile, catalogue and connected
   > local project notes. Identify the Scientist, its project/source relationship,
   > saved research notes and task status. Is an assistant or another organ
   > required? Explain the smallest next step without doing it. Preserve existing
   > configuration; do not initialize again, duplicate records or replace files
   > with examples. No workflows, delegation, publication, install or external
   > access. Cite files and do not claim validation ran in this conversation.

   Require a distinct session ID, correct recovery from file reads, and zero
   file-hash changes and successful `starter-check` for all discovery links. Write tools remain available under the
   same narrow permissions; preservation is observed behavior, not merely a
   read-only-tool consequence.

## Limits and next steps

The fixture is nested inside a maintainer workspace with an already authenticated
CLI. Explicit local resolution and the sampled Skill result prove the observed
source path; they do not prove a pristine user installation or absence of all
ancestor instructions/user customizations. Only one of 40 skills was invoked. This is application-state resumption in a
new conversation, not a test of Claude's transcript `--resume` feature.
Hooks were disabled and no dev workflow, GitHub task creation, Heart shipping
procedure or release was exercised. Source is synthetic; no science was run.

The local preview and conversational configuration connection are the acceptance
scope. Optional organ activation must still establish prerequisites, owner-specific
validation and resumability. Framework upgrades/rollback must preserve records.
Independent deployment and an actual collaborator's access/harness remain
separate milestones in the adoption epic. Do not call the whole starter or
release workflow production-validated from this report.

Raw evidence is intentionally uncommitted: task worktree
`PyAutoMind/tmp/acceptance/` contains prompts, runner commands, JSONL tool
transcripts, revisions, before/after hashes and rendered previews. After merge,
archive it under canonical Mind `tmp/scientist-starter-acceptance/` before
removing the worktree. The public report records only synthetic findings.
