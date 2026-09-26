- issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/12 (closed)
- completed: 2026-09-26
- workspace-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/13 (MERGED)
- epic: organ-cockpit (feeds: PyAutoBrain#416, Hands#289, Memory#104, Brain#418)
- heart-ack: "Heart YELLOW (score 100): `manifest drift: hub organism blurb (organs present) — 7 mismatch(es) vs PyAutoMind/repos.yaml`; `manifest drift: organism-map blocks (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml` — pre-existing; live human 'ack and merge' 2026-09-26"
- witness: Pages deploy 36253613207 green; https://pyautolabs.github.io/cockpit/ , manifest.webmanifest (application/manifest+json, standalone, start_url /cockpit/) and sw.js all 200; hub index carries the Cockpit link. Human legs pending: cards populate, install prompt / Lighthouse installable, 🔔 + notification on a status change.
- gotchas: feeds are absolute URLs so a localhost preview shows live data (Pages sends access-control-allow-origin: *); Pages CDN caches state.json 600 s so fetches carry a `?t=` buster besides cache:"no-store"; installed Android PWAs need notifications via the service worker's showNotification, not `new Notification`; the hub has no CI and no headless browser exists locally — the visual check is human; the hub's AGENTS "inline everything" rule has two platform-mandated exceptions (manifest + sw.js), now documented there.
- follow-ups (not filed): Eyes/Gut/Nerves feeds (need a minimal board workflow each) so the grey cards fill; start_dev Heart-RED gate reading the Heart feed; tray-dot script; Claude Code status line; the 7-mismatch hub organism-blurb drift (regenerate the organism card from repos.yaml).
- summary: Installable organ cockpit PWA at https://pyautolabs.github.io/cockpit/ — one self-contained page reading every organ's state.json feed (ORGANS list, Heart pinned, canonical order, grey cards for feed-less organs), 60 s polling with last-good fallback, app badge + title red count, local notifications on status transitions, manifest + shell-only service worker; hub nav link + README/AGENTS section.

## Original prompt

# Organ cockpit: installable cockpit page on the hub reading the organ feeds

Type: feature
Target: pyautolabs.github.io
Repos:
- pyautolabs.github.io
Difficulty: medium
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: python3 -c 'import json; json.load(open("cockpit/manifest.webmanifest"))' passes; the page opened locally over file:// renders nine cards with the six live feeds populated (screenshot on the PR); Chrome's install prompt appears at https://pyautolabs.github.io/cockpit/ after deploy and Lighthouse reports the page installable; a status change in any feed between two polls produces a local notification.
Review-minutes: 3
Unattended: ready
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/pyautolabs.github.io/issues/12
Filed: 2026-09-26
Epic: organ-cockpit

Six organs now publish the v1 cockpit feed at https://pyautolabs.github.io/<Organ>/state.json (Brain, Heart, Hands, Memory, Mind, Cortex; contract board/state_schema.json in the Brain, validator board/_state.py). The human still manages the ecosystem from a pile of browser tabs. This prompt builds the one cockpit page that replaces them: a Progressive Web App on the hub site that reads every feed, pins the Heart first, badges each organ, and installs as its own window on the laptop and a home-screen icon on the phone.

1. cockpit/index.html on pyautolabs.github.io: self-contained (inline CSS/JS, no external assets, light/dark via prefers-color-scheme, matching the hub's tokens). A status strip with the Heart pinned first, then one card per organ in canonical organ order (Brain, Mind, Cortex, Memory, Eyes, Heart, Hands, Nerves, Gut — organs without a feed yet render as a grey 'no feed' card): status colour, headline, updated age, item list with severity dots, each item's link and a copy button for its prompt payload (same one-tap-copy pattern as the boards). Polls every 60 s (and on visibility change); shows 'unreachable' rather than stale data when a fetch fails; keeps the last good feed per organ in localStorage.
2. PWA: cockpit/manifest.webmanifest (name, standalone display, theme colours, an inline SVG data-URI icon) and cockpit/sw.js (cache the shell only, never the feeds). navigator.setAppBadge with the count of red items across organs when supported; the Notification API asks permission on first tap of a bell control and fires a local notification when any organ's status changes between polls (client-side complement to the Heart ntfy push; no server).
3. A 'Cockpit' link in the hub index.html nav and a short section in AGENTS.md/README.md explaining the cockpit and the feed contract it reads. All feed URLs derive from one ORGANS list at the top of the page (organ, repo, feed URL) so a new organ is one line.

Out of scope: any server; embedding the ntfy topic; editing any organ's feed; start_dev Heart-RED gate; tray dot; status line.

Witness: python3 -c 'import json; json.load(open("cockpit/manifest.webmanifest"))' passes; the page opened locally over file:// renders nine cards with the six live feeds populated (screenshot on the PR); Chrome's install prompt appears at https://pyautolabs.github.io/cockpit/ after deploy and Lighthouse reports the page installable; a status change in any feed between two polls produces a local notification.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->
