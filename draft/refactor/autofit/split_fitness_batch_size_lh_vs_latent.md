# Split `Fitness.batch_size` into `lh_batch_size` and `latent_batch_size`

Type: refactor
Target: PyAutoFit
Repos:
- @PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

`Fitness.batch_size` currently serves **two unrelated concepts**, which is
actively confusing when reasoning about GPU memory.

## The two meanings

1. **Likelihood / VRAM batching** — "how many model evaluations JAX performs
   simultaneously", the thing that drives VRAM. This is the user-facing meaning:
   - `analysis.print_vram_use(model, batch_size=search.batch_size)` constructs a
     `Fitness(..., batch_size=batch_size)` purely to profile VRAM, and its
     docstring is explicit: *"The `batch_size` sets how many likelihood
     evaluations are performed simultaneously. Increasing the batch size
     increases VRAM usage but can reduce overall run time."*
   - `af.Nautilus` exposes `@property batch_size -> self.n_batch`, and
     `af.MultiStartAdam`/`ADABelief`/`Lion` gained a `batch_size` with the same
     meaning (PyAutoFit#1373/#1374 — how many starts are evaluated per vmapped
     `value_and_grad`).

2. **Latent-sample chunking** — the *only* thing `Fitness.batch_size` is
   actually consumed for inside autofit:
   `updater.py` → `analysis.compute_latent_samples(latent_samples,
   batch_size=fitness.batch_size)` → `latent.py` chunks the batched JAX call
   over `range(0, len(parameter_array), batch_size)`.
   Note `Fitness._vmap` does **not** chunk with it — it is a plain
   `jax.vmap(jax.jit(self.call))`.

So one attribute is set for meaning (1) and consumed for meaning (2). A user
setting it to bound likelihood VRAM is really only changing latent chunking.

## What to do

**Split, do not just rename** — meaning (1) is legitimate and user-facing; only
the latent use is mis-named:

- `latent_batch_size` — the chunk size handed to `compute_latent_samples`
  (the current *actual* consumer; `updater.py` should pass this).
- `lh_batch_size` — the likelihood/VRAM batch ("simultaneous model
  evaluations"), what `print_vram_use` means and what the searches' own
  `batch_size` expresses.

Keep back-compat as appropriate (deprecate `batch_size`, or accept and route it).

## Related, worth deciding in the same pass

`search.batch_size` is a **de-facto generic contract** — "simultaneous model
evaluations", consumed by `analysis.print_vram_use(batch_size=search.batch_size)`
— but it is implemented only as a Nautilus property; the multi-start gradient
searches now also carry a `batch_size` attribute. Consider formalising it on
`NonLinearSearch` (default `None`) so `print_vram_use` has a real contract to
lean on rather than duck-typing, and so `lh_batch_size` and the search-level
knob line up by construction.

Historical note: the NSS `chunk_size` kwarg (PyAutoFit#1303/#1305, "chunked vmap
for inversion-heavy A100 likelihoods") was removed with NSS (#1356), so there is
currently **no** mechanism that chunks a search's likelihood vmap other than the
per-search `batch_size` added in #1374.

<!-- intaken 2026-07-15 from the pixelized multi-start OOM investigation (autolens_workspace_developer#100) -->
