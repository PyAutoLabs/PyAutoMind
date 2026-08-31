# Review-packet page template

Spec for emitting a slot-review page (the surface a `batch collect` — or the session driving one —
hands the human). Reference implementation: `PyAutoMind/batches/packets/2026-08-31-am.html`.

## File

- One self-contained HTML file: `PyAutoMind/batches/packets/<YYYY-MM-DD>-<slot>.html`
  (`<slot>` is the human's free-text label, e.g. `am`, `pm`, `night`).
- No wrappers (`<!DOCTYPE>`/`<html>`/`<head>`/`<body>`): `<title>` first, one `<style>`, markup,
  one `<script>` last. One external resource only: the IBM Plex Google-Fonts stylesheet link.
- Figures embedded as base64 data URIs, ≤ 720 px wide, JPEG q80; page ≤ 3 MB.
- The archive URL/path must stay **stable across refreshes** — the page's notes and decisions live
  in `localStorage` keyed by origin+page, and a moved file orphans them.

## Page structure, in order

1. **Header** — eyebrow (date · lane · what came back), title, one-sentence lede,
   mirror-note (where run outputs were pulled locally), stamp line
   (`Generated <ts> · refreshed <ts>`), `Permanent home: <code>path</code>`.
2. **Stat tiles** — members by health + `Est. review-minutes <sum>` with the addition shown.
3. **Inputs bar** — `Reviewed at` (text, auto-filled, editable) and `Review-minutes-actual`
   (number). Both persist; both go into the submit markdown.
4. **Most-important-finding callout.**
5. **Rulings needed** — a real `<ol>`, one line per decision, each linking to its member.
6. **Members** (sticky sidenav beside them), ordered: failures → rulings-required → clean →
   running → retrospectives. Cross-cutting sections and a closed `<details>` of packet-building
   notes follow the members.
7. **Fixed submit bar** — live progress (`Ruled r of N · decisions d of N`) + `Submit review`.

## Member block order

Question · Witness · Health evidence · Readout (tables in `overflow-x:auto` wrappers; figures) ·
**Ruling** (accent border, the one-line decision) · **Your review** (see below) · Follow-ups
(`[repo]`-tagged) · Where to look yourself (`<dl>`; local mirror paths; `RAL only` tag **only**
when the artefact genuinely cannot be mirrored) · Est. review-minutes chip.

**Your review** = radio chips `Accept / Tweak / Reject / Defer` (first chip renamed to fit the
member: `Leave to finish` for RUNNING, `Structure OK` for merged retrospectives) + one
auto-growing textarea. All state (chips, notes, Ruled ticks, the two top inputs) persists to
`localStorage` under one versioned key, every access in try/catch, saves debounced.

## PENDING members (evening dispatch → morning fill-in)

A member whose run had not finished at generation time is emitted as
`<section class="member pending" id="…">` with a `chip-pending` chip reading
`PENDING — refreshed during your read`, showing only Question, Witness and a status line.
The morning refresh **regenerates that section in place** (same `id`, full block set), bumps the
header's `refreshed` stamp, and republishes to the **same path** — never a new file, so stored
notes survive. Never touch other members' markup during a refresh.

## Submit markdown schema (parse-stable)

The submit button assembles exactly:

```markdown
# Batch review <YYYY-MM-DD>-<slot>

- packet: PyAutoMind/batches/packets/<YYYY-MM-DD>-<slot>.html
- reviewed-at: <free text>
- review-minutes-actual: <integer or (not given)>

## <member-slug> — <HEALTH>
- decision: accept|tweak|reject|defer|leave-to-finish|structure-ok|UNREVIEWED
- ruled: yes|no

<note verbatim, or (no note)>

## Follow-ups accepted
<!-- orchestrator: fill from the tweak notes and the packet's proposed follow-ups -->
```

One `## <member-slug> — <HEALTH>` section per member, in page order; slugs are stable
kebab-case identifiers chosen at generation (embed them in the page's `MEMBERS` JS array).
The orchestrator parses on those exact heading forms and the two `- key:` lines.

Delivery affordances, in this order: **Copy to clipboard** (always works; clipboard API with
`execCommand` fallback), **Download .md** (inert inside a Claude-artifact sandbox — say so in
small print), **Commit on GitHub** — a link to
`https://github.com/PyAutoLabs/PyAutoMind/new/main?filename=batches/reviews/<slot>.md&value=<urlencoded>`,
disabled with a use-Copy hint when the URL exceeds 7,500 chars. Close with: "tell the
orchestrator chat 'review submitted'." The committed file lands at
`PyAutoMind/batches/reviews/<YYYY-MM-DD>-<slot>.md`.

## Design tokens (brief)

Light on bare `:root`, dark redefined under `@media (prefers-color-scheme: dark)` guarded
`:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`; body background
always `var(--ground)`. Ground `#eef1f4` / surface white / ink `#17202b` / accent teal `#0f6e73`;
semantic (separate from accent): failed `#b3261e`, suspect `#a65f00`, healthy `#2c7a4b`,
running `#2f5fc4`, merged `#5b4bb5`, each with a `-soft` tint; dark equivalents lifted for
contrast. Type: IBM Plex Serif (headings) / Sans (body) / Mono (paths, ids, table numerals with
`tabular-nums`). No emoji, no decorative numbering; only real sequences get an `<ol>`.

## Standalone document (learned 2026-08-31)

An archived packet is served raw from Pages, with no wrapper. It MUST be a complete
HTML document — `<!DOCTYPE html>`, `<html lang>`, `<head>` with charset + viewport,
`<body>` — and its stylesheet MUST carry its own `[hidden] { display: none !important; }`
reset. A fragment relying on a host wrapper (the Claude artifact viewer injects both the
skeleton and that reset) renders in quirks mode here, and any element hidden via the
`hidden` attribute whose class sets `display:` stays visible — the submit modal did
exactly that on the first packet.
