# ECLIPSE catalogue website: private prototype on ten DR1 lenses

Issue ECLIPSE_lens_catalogue#1. Merged 2026-10-24 via /prm. Repo created this day: `PyAutoLabs/ECLIPSE_lens_catalogue` (private, `lens/ECLIPSE_lens_catalogue`, in `repos.yaml`).

## What shipped
- **ECLIPSE_lens_catalogue#2** (`0e7e2e1`, 7 commits): the COWLS catalogue site design rebuilt for the Euclid per-lens bundle.
  - `docs/`: gallery paginated at 100 rows with filter/sort/view/page in the URL and only the current page in the DOM; grade and inspection filters; name/tile search; `lens.html?lens=<tile>` fetching its own JSON with summary, mass/Sérsic tables (1σ), per-band fluxes + AB magnitudes, captioned figures, downloads; `about.html` documenting the 24 results files and the dataset folder; `papers.json` empty; landing/citation slots marked as human placeholders.
  - Every file URL derives from the single `storage_base` in `docs/data/config.json`.
  - `scripts/pull_lenses.sh` (RAL rsync of results + dataset per tile), `scripts/build_site_data.py` (config, slim `index.json`, one JSON per lens, 200 px thumbnails cropped from the left panel of `rgb.png`, `--synthetic N`), `scripts/sync_storage.sh` (rclone → R2), `scripts/check_links.py`, people-first README with the Cloudflare human-step checklist.
  - Preview mode: the ten lenses' files are committed at `docs/data_files/<tile>/` with `storage_base = data_files`, so the Cloudflare Pages Access policy covers the data. Replaced by R2 behind a custom domain at launch prep.

## Hosting decisions (human, 2026-10-24)
- GitHub Pages/raw cannot carry DR1 (~95 GB full tier, 15,071 lenses; the COWLS repo is already 9.3 GB). Site → Cloudflare Pages (deploys from the private repo, no bandwidth cap); per-lens files → Cloudflare R2 behind a custom domain (r2.dev is rate-limited); Cloudflare Access (Zero Trust Free) gates both until launch; Zenodo later for archival zips + DOI (100 files per record). Free tier for wiring; human pays (~$1.50/month at 100 GB) before public launch; domain purchase deferred.
- Human set up: R2 subscription, bucket `eclipse-lens-catalogue`, account API token (rclone remote `r2`, credentials in Bitwarden), Pages project `eclipse-lens-catalogue` (output dir `docs`, no build), Access application on `eclipse-lens-catalogue.pages.dev` + wildcard with an email policy. Preview verified working by the human.

## Validation
- Local preview with real data: gallery, lens, about, papers pages at 1200/400 px, no broken images; `check_links.py` 10 lenses, 403 files, 0 missing; synthetic 15,000-row gallery renders in 40–100 ms.
- Merge gate: the Cloudflare Pages deployment check (the repo has no test workflows) green; PR MERGEABLE/CLEAN. Heart YELLOW at start_dev (release yellow, monitoring red).

## Follow-ups (not blocking)
- Buy a domain → attach `data.` to the bucket and the site to Pages → delete `docs/data_files/`, rebuild `--storage-base https://data.<domain>`, sync `data/`.
- Pages caps a deployment at 20,000 files: per-lens JSON (or thumbnails) move to R2 at 15k lenses.
- Full DR1 upload from RAL via rclone once the v5 catalogue tree lands; swap `ECLIPSE_RAL_RESULTS` to it.
- About-page grade/score/inspection-consensus wording inferred from column names: human to check. Upstream quirk: some 1σ bounds equal the median exactly.
- Before public: $10 billing alert, one rate-limiting rule on the data hostname, remove the Access policy, Euclid Consortium data-rights sign-off.

## Original prompt

# ECLIPSE catalogue website: private prototype on ten DR1 lenses, COWLS design, Cloudflare Pages + R2

Type: feature
Target: euclid
Repos:
- ECLIPSE_catalogue (new private repo, PyAutoLabs org, cloned design from Jammy2211/COWLS_COSMOS_Web_Lens_Survey)
- euclid_strong_lens_modeling_pipeline (read-only: bundle layout, RAL inspect tree)
Themes:
- euclid
- catalogue
- website
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: a private Cloudflare Pages deployment, gated by Cloudflare Access, renders the index, lens page and about page for ten real DR1 per-lens bundles whose PNG/FITS/JSON are served from an R2 bucket behind a custom domain; the index stays responsive with a synthetic 15,000-row index JSON; the storage base URL is a single config value.
Review-minutes: 15
Unattended: no
Epic: none (first phase of the ECLIPSE catalogue site; DR1 full build is a later phase)
Filed: 2026-10-24
Issued: 2026-10-24

## Context

The COWLS catalogue website (static site in `docs/`, `scripts/build_site_data.py`, deployed by
GitHub Pages, images and `.fits` hot-linked from raw.githubusercontent.com) is the approved design.
It cannot be reused as-is for Euclid: the DR1 full tier is ~95 GB (15,071 lenses, ~32 GB of
256-colour PNGs, ~45 GB of results FITS, ~19 GB of per-lens input data, 21 bundle files + a
`dataset/` folder per lens — see `catalogue/README.md` in the pipeline repo), which no git
repo or GitHub Pages site can carry. The COWLS repo is already 9.3 GB on GitHub.

Hosting decision (conversation 2026-10-24):
- Site: **Cloudflare Pages**, deployed from a **private** GitHub repo (GitHub Pages cannot serve
  a private repo on the free plan; Cloudflare Pages has no bandwidth cap, which matters for a
  public DR1 launch).
- Per-lens files: **Cloudflare R2** public bucket behind a **custom domain** (the `r2.dev`
  hostname is rate-limited and not for production). Free tier (10 GB) for the prototype; the
  human upgrades/pays before public launch. Storage ~$1.50/month at 100 GB, egress free.
- Both gated by **Cloudflare Access** during development (free up to 50 users). Going public
  = removing the Access policy.
- Archival zips + DOI: **Zenodo** later (100 files per record, so zips only).
- Euclid Consortium data rights: check before any public exposure; the prototype is private.

The site is **ECLIPSE**, not DR1-specific: DR1 is its first catalogue; naming (repo, domain,
about page) must not bake in DR1.

Ten real DR1 bundles are available now without waiting for the v5 catalogue rebuild: one on the
laptop (`/mnt/c/Users/Jammy/Science/active/euclid_dr1/inspect/compression_example_20261024/original`)
and the rest in the RAL inspect tree (rsync ~70 MB). No Q1 modelling.

## Scope of this phase

1. New private repo `PyAutoLabs/ECLIPSE_catalogue` (name to confirm) seeded from the COWLS
   `docs/`, `scripts/build_site_data.py`, README pattern and `pages.yml` replaced by a Cloudflare
   Pages deploy.
2. Pull ten complete DR1 bundles (21 files + `dataset/`) from RAL into a local, git-ignored
   data tree; commit only the derived JSON/thumbnails.
3. Build step: 200 px thumbnail per lens; slim gzipped index JSON (table/filter columns only);
   one per-lens JSON with the full record; file list per lens from the data tree, not git.
4. Site changes vs COWLS: paginated/virtualised index built for 15k; per-lens JSON fetched on
   click; `STORAGE_BASE` single config value (prototype → R2 custom domain); ECLIPSE naming.
5. Cloudflare wiring (human-performed steps called out explicitly: account, domain, Access
   policy, Pages project, R2 bucket + custom domain): rclone sync script from the data tree to
   the bucket; Pages deploy from the repo.
6. Synthetic 15k-row index test for responsiveness; local preview check; Access-gated deploy.

Out of scope: the full DR1 upload, Zenodo, public launch, Euclid data-rights sign-off.

User request (verbatim, conversation 2026-10-24):

"""
We have just done amazing work making the COWLS catalogue website clean:
https://github.com/Jammy2211/COWLS_COSMOS_Web_Lens_Survey . We are also building a full euclid_dr1
catalogue, containign 15072 lenses all with results and other information. I now want us to build
the catalogue website for ECLIPSE and euclid_dr1. Really, I am happy with the design of the COWLS
catalogue, the main challenge is what is the right solution to hosting the Euclid data given that
the catalogue is curently 100GB total, so just using github pages is not feasible, I think?

[...] tbh Cloudflare R2 seems fine I can prob claim it, can I pay yearly? and what about paying for a URL?

[...] this plan is good, are we able to build a free template using like, only 10 euclid lenses
(make them q1 lenses which are public)? dont start yet just working out our options, I guess the
github repo should be closed for now

Its ECLIPSE, not specific to DR1. Can we get this going in a fully private way on ten DR1 lenses,
once the catalogue is built (or start assuming itll be built). If not its fine but trying to avoid
faff with q1 lens modeling

Does this solution cope with 100s of people going to the wbeiste when DR1 goes live? It could
attrack a lot of public interest

Sounds great, before this goes public I'll prob pay for cloudflare but for initial wiring use free.
I think we can plan and begin?
"""
