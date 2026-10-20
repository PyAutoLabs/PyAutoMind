# COSMOS-Web Ring walkthrough — phase 2: image-first greeting skill + assistant-wide rule

**Work type:** docs · **Target:** `lens/autolens_assistant` · **Consequence:** judge
**Epic:** [`cosmos_web_ring_guided_walkthrough.md`](cosmos_web_ring_guided_walkthrough.md).
Depends on phase 1 (vendored images, committed tracers, notebook sections).

## Scope

1. **`skills/al_greeting_cosmos_web_ring.md`:** Step 1 opens `docs/images/strong_lens_schematic.png`
   then `docs/images/cosmos_web_ring_rgb.png` with the platform opener (xdg-open / open /
   wslview / explorer.exe) **with no Python**, gives the rays→ring bridge and the two-sentence
   explanation, and asks the one background question. Step 3 routes every audience through the
   notebook's sections using shipped figures (arrows image for Preparing The Data; Mercier+24
   figure for What A Lens Model Looks Like) and ends at **Explore The Model** (see the epic's "Phase 1 outcome"): **evaluate** the
   committed ansofi tracer (seconds), show its fit, report θ_E and the mass from it, then offer
   to change the mass (Einstein-radius offset) or the lens light (scale) and look at the
   residuals, mirroring the shipped notebook's controls — no Sérsic "bad fit". Use F150W/F444W
   when talking colours, and the F150W/F444W Mercier figure. Full inference (`MultiStartProdigy`) only on explicit request, with the
   time cost stated first; the priors paragraph moves into that branch.
2. **`skills/_style.md`:** add the rule "show an existing figure before writing code; when
   code must plot, open the PNG for the user, don't just quote a path"; sweep `al_*` skills
   and `modes/*.md` for compliance (bounded: list offenders, fix the plot-path announcement
   wording where it conflicts).
3. **Benchmarks:** update `benchmarks/prompts/conversational/easy_cosmos_web_ring.md`, the
   `cosmos-web-ring-fit` card/truth and `autoassistant/tests/test_cosmos_web_ring_fit_card.py`
   so the scored behaviour is the no-search walkthrough; keep a separate "fit it yourself"
   expectation if the card needs one.
4. Regenerate the Claude/Codex skill adapters (`.claude/`, `.codex/`) as the repo's
   generator prescribes.

## Done when

A fresh greeting session shows two images before any code and reaches good-vs-bad with no
search; benchmark card and tests green; PR open.
