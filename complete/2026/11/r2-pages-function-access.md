Shipped 2026-11-09 in PyAutoLabs/ECLIPSE_lens_catalogue#5 (merge `1a38897`); issue #4 closed.

- **Pages Function.** The read-only `/files/*` function (`functions/files/[[path]].js`) reads the private R2 bucket through the `DATA` binding, set for both Preview and Production. It supports GET, HEAD, byte ranges and 304, and sends `Content-Disposition` for downloads. The bundled `docs/data_files/` is removed.
- **Full DR1 v5 catalogue.** The site lists 15,071 lenses: 15,007 modelled, plus 64 with dataset and RGB only.
  - `index.json` and the 200 px thumbnails are committed.
  - The per-lens JSON is in R2 at `_site/lenses/`, because a Pages deployment is capped at 20,000 files.
  - The thumbnails and lens files are the north-up versions (sky-orientation-p2, euclid_strong_lens_modeling_pipeline#120). The site data was rebuilt on RAL by job 414433, and check_links found 0 missing files.
- **Downloads page.** It lists `_release/dr1_v5_northup` (28 objects, 76.2 GB). The 2026-10-29 `_release/dr1_v5` was deleted with the human's OK.
- **Verified.**
  - The production deploy `ea4877c2` succeeded.
  - Unauthenticated requests for `/`, `/data/index.json` and `/files/_release/...` all return a 302 to the Access login.
  - The human confirmed that Production Access and the Production R2 binding are set.
- **Bucket rule.** The bucket root holds lens trees, `_release/` and `_site/`, so it is only ever updated with `rclone copy`, never `sync`.

## Original prompt

# ECLIPSE site: serve R2 lens files through a Pages Function behind Cloudflare Access

Type: feature
Target: eclipse_lens_catalogue
Repos:
- ECLIPSE_lens_catalogue
Themes:
- euclid
- catalogue
- website
Difficulty: small
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-10-29
Issued: 2026-10-29
Issue: https://github.com/PyAutoLabs/ECLIPSE_lens_catalogue/issues/4

## Original request (human, 2026-10-29)

> is there a way to collaborator can use the github mosaic page or something easier than rclone without sacrifying security?
>
> (after the proposal) yeah do it

## Context

- The site (`eclipse-lens-catalogue.pages.dev`) is gated by the Cloudflare Access app "ECLIPSE preview" (email policy "Invited", covers the pages.dev host and every preview subdomain). Verified 2026-10-29: every URL 302s to the Access login without a session.
- The R2 bucket `eclipse-lens-catalogue` is private (unsigned requests get HTTP 400; r2.dev off per 10-24 setup). The full DR1 per-lens tree (15,007 lenses, release full-tier file selection, 256-colour palette PNGs) is being uploaded to the bucket root from RAL on 2026-10-29 (euclid_dr1 `hpc/run_manifests/eclipse_r2_upload_20261029/`, jobs 413223 stage → 413224 upload).
- No domain yet, so the site cannot link to R2 directly; today ten lenses are bundled into `docs/data_files/`.

## Want

- A Pages Function that serves bucket objects through an R2 binding on the same host, so Access gates the data exactly as it gates the pages. Collaborators log in with their email, browse the mosaic and download; no rclone and no keys.
- GET/HEAD only, no listing, path validation, `Cache-Control: private` (never shared-cached), Range support for large FITS.
- Mounted at `/files/*` (not `/data/*`, which would shadow the static `docs/data/` JSON). Optional `DATA_PREFIX` env var (default empty = bucket root).
- `storage_base = /files`; site rebuilt on the 100 rehearsal lenses, with `data/` mirrored from the bucket so the download lists match the bucket exactly; `docs/data_files/` removed.
- Branch preview for a collaborator test; production stays as-is until the human reviews and merges.

## Human steps

- Pages project `eclipse-lens-catalogue` → Settings → Bindings → add R2 bucket binding `DATA` → `eclipse-lens-catalogue`, for **Preview** (and **Production** before merge).
