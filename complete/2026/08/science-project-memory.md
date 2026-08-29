## science-project-memory
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/315
- completed: 2026-08-29
- library-pr: PyAutoBrain#316 (merged 8f5f769 -> main), autocti_assistant#27 (merged 0242d7b -> main), autofit_assistant#31 (merged d5df11f -> main), autolens_assistant#116 (merged 010378d -> main), autogalaxy_assistant#20 (merged 5938bcc -> main)
- classification: library (five independent assistant/organ repos; no workspace follow-up — the assistants are their own workspaces)
- what shipped: "point a fresh agent chat at a science project folder and it works out where it got to, how to resume, and the project's history" is now true by default for projects scaffolded by the assistants' `start-new-project` skill. Phase 1 (PyAutoBrain) — a `sync` mode on the clone conductor: given a reference assistant and a commit range it takes the reference's diff over the `_SHARED_GENERIC` file set and applies it to each sibling as a three-way patch, reporting per file/per sibling applied / rejected-hunks / absent / unchanged; dry-run by default, `--apply` writes, a rejected hunk is a human decision and is never auto-resolved. Phase 2 (autolens_assistant, the reference copy) — deliverables A-D: a session-start block in the generated project `AGENTS.md` plus a project `CLAUDE.md` that `@`-imports it; `wiki/project/state.md` as the head pointer (templated, scaffolded, rewritten-not-appended each session, wired into the end-of-session journal ritual); a templated `results_summary.md` with a `covers_through:` stamp; `results/manifests/` deleted from the scaffold and from every sentence that promised it (delete the trap, don't document it); `profile.md` split at the user/project seam. Phase 3 — propagated through the new sync to autocti_assistant and autogalaxy_assistant with the rejected hunks hand-resolved (autocti's orphan `state.md` reconciled into the template, not deleted).
- folded-in follow-up: the maintenance follow-up `finish-the-science-project-memory-propagation` was worked as part of THIS issue, not re-filed — see `complete/2026/08/science-project-memory-followup.md`. Leg B: the clone conductor's rename table became one shared `name_substitutions()` used by both birth and sync, carrying the UPPERCASE package rule birth omitted plus `DOMAIN_NOUNS` / `DOMAIN_ALIASES`; unknown target science = no domain rule + a warning, never a guess. Leg A: autofit_assistant synced (`--since ee306ac`), all four rejected files hand-resolved.
- validation: PyAutoBrain suite 627 -> 634 passed (clone-sync tests 9 -> 16); autofit_assistant 56 tests pass, boundary complete.
- scope: `euclid_assistant` is a different design and was OUT OF SCOPE throughout — never opened, never synced.
- ci-note: the last two PRs (autolens_assistant#116, autogalaxy_assistant#20) were merged with the `wiki-currency` leg RED, on explicit human acknowledgement. The failure is pre-existing `wiki/core` / skill-audit drift these branches do not touch — autolens "Symbol audit (--scope all) exited 1" (missing/broken: 1); autogalaxy the same plus "Citation paths (--check-citations) exited 1" (`wiki/core/operations/sandbox.md` cites `PyAutoGalaxy:autogalaxy/plot/plot_utils.py`, absent from the source tree). The same leg failed on both repos' previous PRs (#115, #19 — pynufft residue phase 2, 2026-08-23), which were merged anyway. No code was modified to make the leg pass. Filed as its own task: `draft/maintenance/pyautobrain/fix_wiki_currency_ci_drift_in_the.md`.
- heart-ack: human authorisation 2026-08-28 — "open prs under red and merge i acknowledge". Heart RED reason acknowledged verbatim: "release validation FAILED (stage integrate)". YELLOW reasons acknowledged verbatim: "workspace validation not passing (2 failed, cloud#33179766004: autolens_test scripts/imaging/rectangular_mge.py, rectangular_mge_rtu.py)"; "manifest drift: session-start hooks (generated) — 32 mismatch(es) vs PyAutoMind/repos.yaml". None of these reasons is caused by this task.
- supporting commit already on Mind main before the close-out: 2b764e48 (tenant-firewall allowlist).
- reported not-fixed (human domain adaptation, not substitutions): autocti_assistant's lensing *example strings* (slacs_subhalo, the SLaM run row, README filename examples) and three more `.claude/skills/` real-file copies.
- merge note: autolens_assistant#116 and autogalaxy_assistant#20 were squash-merged, so `--is-ancestor` reads UNMERGED for their heads; merge proven from `state=MERGED` plus the squash commits 010378d / 5938bcc carrying the branches' 7-file diffs.

## Original prompt

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
