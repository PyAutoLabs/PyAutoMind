## eceb-editorial-revision (ECEB wiki rules — EC A&A template assets — MERGED)
- issue: https://github.com/Jammy2211/euclid_assistant/issues/6 (CLOSED)
- completed: 2026-07-14 (human-directed PR + merge in /morning session; docs-only)
- pr: https://github.com/Jammy2211/euclid_assistant/pull/8 — MERGED (squash, 2f4f2ee) 2026-07-14; branch deleted.
- summary: Editorial revision of `wiki/rules/acknowledgements.md` and `wiki/rules/references.md` to reference the bundled official EC A&A template assets under `knowledge/sources/euclid_assets/`. acknowledgements.md documents `\AckDatalabs` (ESA Datalabs macro) and replaces the stale "euclid.sty not present" open question with guidance to use the macros + refresh the style file from the ECEB template. references.md documents the A&A acknowledgements → references → appendices ordering.
- validation: both factual claims verified against the tracked assets before shipping — `\AckDatalabs` at `euclid.sty:361`, appendix-after-references at `blank.tex:529`. Docs-only prose; no code paths touched.
- note: the private manuscript companion (`/mnt/c/Users/Jammy/Science/euclid/paper`) is a separate deliverable outside this repo and was not part of this PR.
