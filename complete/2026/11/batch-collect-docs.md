## batch-collect-docs
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/596
- completed: 2026-11-22
- prs:
  - https://github.com/PyAutoLabs/PyAutoMind/pull/597
  - https://github.com/PyAutoLabs/PyAutoHeart/pull/362
- Mind: `batches/AGENTS.md` marks the fields only collect wrote as `legacy` and describes the integration flow as history; the digest is appended by the watcher's first tick after `review-at:`; `batches/packets/{AGENTS,TEMPLATE}.md` document the archived pages (opt-in `packet: yes` → `digest.html`); `REFERENCE.md` no longer says "appended at collection".
- Heart: `pyauto-heart freeze` help and `REFERENCE.md` list only `vitals` and `/prm` as freeze readers.
- Witness: `git grep -n "batch collect"` in Mind returns only history, drafts about the retirement, the generated dashboard and the retirement sentences.

## Original prompt

# Docs in PyAutoMind and PyAutoHeart still describe the retired batch collect

Type: docs
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoHeart
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Issued: 2026-11-22
Consequence: notify
Witness: `git grep -n "batch collect"` in both repos returns only history (`complete/`, `queue.md` footer) and sentences that say it was retired.
Review-minutes: 0
Unattended: ready
Lane: any

Docs in PyAutoMind and PyAutoHeart still describe the retired batch collect

Type: docs
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoHeart
Lane: any

`pyauto-brain batch collect` (and its `--integration` / `--push` flags) was removed in PyAutoBrain#701; a shift is now a brief the watcher runs and its digest is the report. These pages still describe it as live. In @PyAutoMind: `batches/AGENTS.md` (around lines 115-120, `collect --integration` and `--push`), `REFERENCE.md` (around line 189, "`batch collect` carries one line" about the Heart freeze), `batches/packets/TEMPLATE.md` (the page a `batch collect` emits). In @PyAutoHeart: `bin/pyauto-heart` help text (around line 332, the same freeze sentence). Rewrite each to the brief-only flow or remove it; the `integration/*` sweep rule stays for refs already published. The `queue.md` footer entry "batch collect" is history and stays.

Witness: `git grep -n "batch collect"` in both repos returns only history (`complete/`, `queue.md` footer) and sentences that say it was retired.

<!-- formalised by the Intake (Conception) Agent on 2026-11-22 from file:/tmp/claude-0/-home-user/8f120f5d-ca18-5874-ae34-519506e9751b/scratchpad/prompts/3.txt -->
