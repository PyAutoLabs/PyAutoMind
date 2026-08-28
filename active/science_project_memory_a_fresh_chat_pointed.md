# Science-project memory: a fresh chat pointed at a project folder resumes…

Type: feature
Target: PyAutoBrain
Repos:
- autocti_assistant
- autofit_assistant
- autogalaxy_assistant
- autolens_assistant
- PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-08-28

# Science-project memory: a fresh chat pointed at a project folder resumes by default

Type: feature
Difficulty: large
Autonomy: supervised
Priority: high

Make "point a fresh agent chat at a science project folder and it works out where it got to, how to resume, and the project's history" true by default for projects scaffolded by the assistants' `start-new-project` skill.

Scope: autolens_assistant (reference copy), autofit_assistant, autogalaxy_assistant, autocti_assistant, and the pyautobrain clone conductor. The euclid assistant is a different design and is explicitly out of scope.

User's original request (verbatim): "I want to know how much memory of a project they truly have. Ideally, I can always load a new agent (e.g. claude) chat, and point it to a science project and it can quickly work out where it got to, how to resume and the general history of the science project. I feel like this would need more in the wiki than just the code run, so how much of this type of more persistant memory is avaialble? Is this something we should add, like an indexed tracker of tasks and work analogous to how organ repos and other tasks are easily resumeable?"

Findings verified 2026-08-28 (one real project scaffolded in July, two journal entries, one full run campaign):
1. The generated project AGENTS.md (from `skills/start-new-project.md`) has no session-start section; each assistant's own AGENTS.md step 2 reads `wiki/project/profile.md` only. Nothing reads the journal on arrival, so a fresh chat does not resume unless asked "what have we done?".
2. `autocti_assistant/wiki/project/state.md` is an orphan — no AGENTS.md or skill reads or writes it (the only precedent for a head pointer, and it is dead).
3. `results_summary.md` is consumed by the Publish phase (`gh release create --notes-file wiki/project/results_summary.md`, autolens_assistant `skills/start-new-project.md:381`) but is never templated or created by the scaffold.
4. `results/manifests/` is aspirational: empty after a full real campaign; the journal's run tables do the job.
5. `profile.md` conflates user-level facts (role, HPC/SSH access, automation consent) with the per-project science goal; a second project re-elicits everything.
6. The four copies of `skills/start-new-project.md` and `wiki/project/{README,_profile_template,_template}.md` have four distinct hashes (the autofit_assistant copy diverged by 343 lines). The clone conductor lists them as `_SHARED_GENERIC` (`agents/conductors/clone/_clone.py:69-81`) but only has a birth mode — nothing re-syncs after birth.

Deliverables, in priority order (A alone gets most of the value):
A. Session-start block in the generated project AGENTS.md, and in the assistants' AGENTS.md step 2: read `profile.md`, `wiki/project/state.md`, and the newest dated journal entry before answering. Verify the scaffold emits a CLAUDE.md that @-imports AGENTS.md so Claude Code actually loads it.
B. `wiki/project/state.md` (keep autocti_assistant's filename) — a small head pointer, rewritten not appended each session: Where we are now / In flight (runs, job IDs, what unblocks each) / Open, carried forward (struck when done) / Traps — don't repeat / one-line journal index. Wire it into the existing end-of-session "want a journal entry?" ritual: an entry is finished when state.md is rewritten. Markdown read by an LLM, not YAML — a science project is one repo with a handful of in-flight runs.
C. Template `results_summary.md` with a `covers_through: <date>` stamp so staleness is visible. Drop `results/manifests/` from the scaffold and the AGENTS text (delete the trap rather than document it).
D. Split `profile.md` at the user/project seam: the user half (who you are, HPC access, automation preference) seeded from the assistant clone's `profile.md` and free to diverge; the project goal moves to `state.md`.
E. Land via a clone-conductor `sync` mode that re-applies `_SHARED_GENERIC` files from autolens_assistant (reference) to the other three, rather than four hand edits. A human reviews the autofit_assistant divergence before any overwrite — some of it may be deliberate domain adaptation.

Out of scope: the library-repo anonymisation of a named science target is filed as its own small maintenance prompt in the data-reduction library.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/069a02ef-b14f-4a43-b0c3-92e461ddef66/scratchpad/intake_memory.md -->
