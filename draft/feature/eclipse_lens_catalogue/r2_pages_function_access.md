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
