# Batch packets — the review pages, archived

One **self-contained** HTML page per slot: `<YYYY-MM-DD>-<slot>.html`. This is
the page the human actually opens to review a batch — every member with its
question, witness, health evidence, readout, ruling block, follow-ups, local
"where to look" pointers and figures — and, once the slot is over, the
permanent record of what they were shown. The batch record's `packet:` field
points here.

Rules (2026-08-31):

- **Self-contained means self-contained.** Figures are embedded as data URIs,
  styles and script are inline; the archive must render identically in ten
  years with no external fetch. Keep a page under ~5 MB; downsize figures.
- **Written at dispatch, refreshed at collect (retired flow).** The pages in
  this folder open with every member present — overnight runs as PENDING
  entries — and carry `generated:` / `refreshed:` stamps; the morning collect
  filled the PENDING members in. That collect step was retired in
  PyAutoBrain#701. Under a shift brief the page is opt-in (`packet: yes`) and
  the watcher writes it once, as `digest.html`, with the digest.
- **Never rewritten after the review is submitted.** The archived page plus
  the `batches/reviews/` file together are the audit pair: what was shown,
  what was ruled. A correction gets a new dated page, not an edit.
- **Pointers are local paths** (the laptop mirror each project's
  `hpc/sync pull` fills, e.g. `/mnt/c/.../Science/<project>/`), because the
  review happens at the laptop. A pointer may stay remote only when the pull
  cannot fetch it by design, and must say so.

**Visibility — ruled public, 2026-08-31.** The human ruled packets and reviews
public in this repository, served on its Pages site, aware that the science
numbers, figures and run paths in a packet are thereby on the open internet.
Pages land here as `<YYYY-MM-DD>-<slot>.html`; `pages_dashboard.yml` serves
them at `https://pyautolabs.github.io/PyAutoMind/packets/<name>.html`.
