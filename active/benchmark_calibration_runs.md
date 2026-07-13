# First benchmark calibration campaign — run the 4 assistant benchmarks across models

Type: research
Target: autolens_assistant
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: filed

Follow-up to feature/autolens_assistant assistant_benchmarks (issue
https://github.com/PyAutoLabs/autolens_assistant/issues/57): the benchmark
package ships four frozen prompt cards (`benchmarks/prompts/`) and the
run/track harness (`autoassistant/benchmark.py`), but `benchmarks/runs/` is
empty. Run the first calibration campaign so the comparison tables have real
rows and the rubrics get validated against real transcripts.

Scope:

- Run at least the two cheap benchmarks (`teacher-basic-workflow`,
  `assistant-easy-cosmos-web-ring`) on 2+ model×harness combinations (e.g.
  Claude Code with two different models; add Codex/Gemini if convenient), per
  the protocol in `benchmarks/README.md` — fresh sessions, prompts verbatim,
  operator behaves like a real user, no coaching.
- Record every run (transcript, meta.yaml with hardware/duration, artifacts),
  score with evidence, regenerate `RESULTS.md`, commit + push.
- The medium/hard benchmarks are hours-scale: run at most one of them once,
  or explicitly defer them with a runtime note.
- Deliverable beyond the run records: a short calibration verdict on the
  rubrics themselves — were any rows unscoreable, ambiguous, or trivially
  gamed? File rubric fixes as `version`-bump proposals rather than editing
  cards in place.

Blocked until the assistant-benchmarks PRs are merged (the cards/harness must
be on main so runs execute against the published, frozen prompt versions).
