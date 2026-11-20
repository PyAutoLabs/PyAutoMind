# A compound-prior model reloaded from model.json has a different prior order…

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoNerves
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: for the reproducer's model, the model reloaded through `to_dict` / `from_dict` has the same ordered list of prior paths and the same `identifier` as the built model, and `instance_from_vector` of one vector gives equal instances from both
Review-minutes: 3
Unattended: ready
Lane: any

Found 2026-11-20 in the science project stars_dm_slope, after PyAutoFit #1783 made compound-prior models serialisable. The project's P1 lens model (a `Collection` of galaxies in which a stellar profile takes `(1 - f_dm) * m_ap` and a dark profile takes `f_dm * m_ap`, with other priors replaced after construction and the light fixed) round-trips through `autonerves.dictable.to_dict` / `from_dict`, the route `paths.save_all` uses for `model.json`, with the same set of prior paths and the same `prior_count` (9) but a different order: built order starts `dark.inner_slope, bulge.mass_ap.m_ap, dark.mass_ap.m_ap, bulge.mass_ap.self.self.f_dm, dark.mass_ap.f_dm`, reloaded order starts `bulge.mass_ap.self.self.f_dm, dark.mass_ap.f_dm, bulge.mass_ap.m_ap, dark.mass_ap.m_ap, dark.inner_slope`. The identifiers differ (48d99f56... versus 566fd61f...), which contradicts #1783's witness for this model, and the same physical vector gives a different lens (inner_slope 0.3 becomes 0.325, kappa_s 0.154 becomes 0.137). Instances built by name agree. Consequence: anything that maps stored samples or a raw parameter vector through a reloaded model (aggregator, resumed searches, database loads, EP factor reloads) silently assigns parameters to the wrong priors for such models; a resumed search would also get a new identifier and start again.
Reproducer: `/home/jammy/Science/Science/development/stars_dm_slope/scripts/scratch/repro_compound_prior_reload_order.py` (needs that project's `scripts/` on the path; read-only for the fixer). A minimal two-component compound-prior `Collection` does NOT reproduce it (order and identifier survive), so the first step is to isolate the trigger: candidates are priors replaced after construction (cf. the #1783 follow-up "modified priors set directly on a model reload"), the prior-id based ordering when the reloaded model creates its priors in a different sequence, or the galaxy / basis nesting.
Fix: make prior ordering after reload identical to the built model (persist the order or the prior ids, or derive the order from paths deterministically on both sides), and add the isolated case to the #1783 round-trip tests, asserting ordered paths, identifier and vector-mapped instances.

**Cause isolated (added 2026-11-20).** No compound priors are needed. A model's free parameters are ordered by prior id, i.e. creation order (`priors_ordered_by_id`); the model rebuilt by `from_dict` gets fresh priors created while walking the model, so its order is the walk order. The two differ whenever a prior was created out of walk order, which is what replacing a prior after construction does. Minimal case: `model = af.Collection(g=af.Model(af.ex.Gaussian)); model.g.centre = af.UniformPrior(lower_limit=-10.0, upper_limit=10.0)`, then `from_dict(json.loads(json.dumps(to_dict(model), cls=NumpyEncoder)))`. Built paths: `g.normalization, g.sigma, g.centre`; reloaded: `g.centre, g.normalization, g.sigma`; the same vector gives (centre, normalization, sigma) = (8.0, 1.6e-5, 12.5) from the built model and (1.6e-5, 12.5, 8.0) from the reloaded one. In this minimal case the identifiers are equal; the identifier change above is specific to the compound-prior model, so there may be two effects to separate. Since most user scripts replace priors after building a model, check first which code paths map vectors (rather than named columns) through a reloaded model: that decides how far the consequence reaches. Second reproducer: `/home/jammy/Science/Science/development/stars_dm_slope/scripts/scratch/repro_reload_order_minimal.py` (standalone, no project imports).

<!-- formalised by the Intake (Conception) Agent on 2026-11-20 from file:/tmp/claude-1000/-home-jammy-Science/4543c7f0-9e90-432b-a76f-76d0789fa7b1/scratchpad/intake/8_compound_prior_reload_order.md -->
