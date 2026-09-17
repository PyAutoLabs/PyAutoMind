# Witness campaign — make the backlog reviewable by construction

Type: feature
Target: pyautomind
Repos:
- PyAutoMind
Themes:
- mind-workflow
Difficulty: medium
Autonomy: safe
Priority: high
Status: active
Consequence: judge
Review-minutes: 15
Unattended: ready
Filed: 2026-08-31
Issued: 2026-09-10

**Make every backlog prompt reviewable: a `Witness:` line on each draft.** A
witness is the machine-checkable claim whose truth settles the task — the thing
a reviewer reads first and, when it holds, often the only thing they need to
read. Today 151 of 153 backlog prompts grade `judge` because they carry none;
given one, the same backlog grades 33 `notify` / 104 `glance` / 16 `judge`. That
is the whole distance between "every task costs a PI's hour" and "a fifth of it
costs nothing", and it is a property of how prompts are written, not of how they
are scheduled: a witnessed prompt is cheaper to review whether it ships alone,
in a bundle, or under `--auto`. Measured from the other side too — the tasks
that reviewed in minutes on 2026-08-31 were the ones with pre-registered
witnesses.

## The work

Sweep the `Unattended: ready` prompts in `draft/`, adding a `Witness:` line —
a machine-checkable claim whose truth makes the task reviewable in minutes
("ids bit-identical", "31-rule byte-equality", "smoke suite green with the new
default", "Δlog-evidence < 5") — in passes of ~15 prompts, proposed
to the human for approval before any header is written.

**The no-invention rule stands and is the whole point: witnesses are
human-declared.** A pass proposes candidate witnesses where the prompt's own
text implies one; the human accepts, edits, or strikes each. A prompt whose
witness cannot be stated stays `judge` — that is a finding about the prompt,
not a failure of the sweep.

This is fill work: zero review-minutes of its own (the review *is* the human's
accept/strike pass, which is the approval itself), and every pass permanently
lowers the review cost of the prompts it touches.

## Done when

- Every `Unattended: ready` prompt either carries a human-approved `Witness:`
  or a one-line `Witness: none —` reason.
- The regrade (`sizing` faculty) is re-run and the glance/notify counts are
  recorded in this prompt, pass by pass, so the campaign's effect on the
  backlog's review cost is visible without re-deriving it.

## Campaign log

Counts are over `draft/` only, so the campaign's own prompt drops out of the
denominator once it moves to `active/` (110 → 109). Two readings are recorded
because they can disagree: **derived** is `estimate_consequence` re-run over the
prompt, **declared** is the `Consequence:` header, which is what `dashboard.md`
and the batch planner actually read.

### Method correction (2026-09-10, before pass 1)

The prompt above says "adding a `Witness:` line". That alone moves nothing on
most of the target set. 89 of the 110 `Unattended: ready` prompts declare
`Consequence: judge` in their header — 74 of them among the 89 unwitnessed —
and `effective_consequence` lets a declared value beat the derived one.

That declaration is not a human judgement the heuristic lacks; it is a cached
derivation. `PyAutoBrain/agents/conductors/intake/_intake.py` puts `consequence`
and `review-minutes` in the "DERIVED … hygiene set" that `intake formalise`
fills in, while deliberately excluding `witness` because nothing can derive one.
The stamp was correct when written (no witness → `judge`) and goes stale the
moment a witness lands. Striking it instead is not an option either: the
dashboard reads `header.get("consequence", "-")` (`_intake.py:1568`), never a
live derivation, so a struck field renders `-` and the planner keeps budgeting
20 review-minutes for a task that now costs 0 or 3.

**So each pass writes three fields together — `Witness:`, `Consequence:`,
`Review-minutes:` — and leaves `Unattended:` alone.**

### Baseline (2026-09-10, before pass 1)

| Reading | ready | witnessed | notify | glance | judge |
|---|---|---|---|---|---|
| derived | 110 | 21 | 5 | 12 | 93 |
| declared (dashboard) | 110 | 21 | 1 | 7 | 89 + 13 unset |

Fully witnessed, the same 110 would derive **28 notify / 74 glance / 8 judge**.
That is the campaign's ceiling, and it reproduces the 33/104/16 in the prompt
above (measured there over the whole 153-prompt backlog, not the ready subset).

### Pass 1 — `workspaces`, 15 prompts (2026-09-10, issue #398)

Chosen as the largest single-target group and the biggest `notify` yield. All 15
were pinned at `Consequence: judge` with no witness. Human accepted all 15 as
proposed.

| | notify | glance | judge | review-minutes |
|---|---|---|---|---|
| before | 0 | 0 | 15 | 300 |
| after | 7 | 8 | 0 | 24 |

Backlog after pass 1: 109 ready, 36 witnessed, 73 not — derived **12 notify /
19 glance / 78 judge**; declared **8 / 15 / 73** + 13 unset.

Two witnesses are weaker than the other thirteen and are flagged here rather
than in the prompts, so a later pass can revisit them without re-deriving the
doubt: `group_los_halos` and `group_subhalo_sensitivity` both gate on "the
imaging version needs improving and padding out first", a leg with no stated
done-condition anywhere. Their witnesses cover only the group leg. The honest
alternative was `Witness: none —` on both; the human chose to accept them.

Also worth a later look: seven of the fifteen grade `notify` (0 review-minutes)
via rule 5 — `docs` work-type, no library repo touched. Two of those seven
(`interferometer_dirty_images_call_sites`, `propagate_shear_galaxy_idiom_to_group_cluster`)
change figures across 11 and 4 lens examples and say in their own text that a
human should look at the figures. The heuristic cannot see that. Declaring
`Consequence: glance` on such a prompt is the documented way to hold it.

### Re-baseline (2026-09-17, before pass 2)

Whole `draft/`, today's faculty over today's tree. The backlog grew by 47
prompts since the pass-1 reading (mostly `euclid`, `autofit`, `autolens`
filings). Method note: pass 1's 109 / 36 re-derive today as 108 / 35 because
`repos.yaml` gained `autolens_inference` and one prompt now resolves an extra
repo; each reading stands as measured on its day.

| Reading | ready | witnessed | notify | glance | judge |
|---|---|---|---|---|---|
| derived | 156 | 64 | 17 | 36 | 103 |
| declared (dashboard) | 156 | 64 | 12 | 24 | 102 + 18 unset |

### Pass 2 — `autoarray`, 11 prompts (2026-09-17, issue #398)

The group was 11, not the 10 planned (two 2026-09-16 DR1 filings). Three
already carried a witness and needed only the restamp. Human accepted all 11
as proposed, including two flagged calls: the `mapping_overlay` override
(declared `glance` over a derived `judge` — the keyword hit is prose describing
the existing bug, the faculty's documented false-`judge` case; its duplicated
header block was collapsed in the same write) and `multiwavelength_inversion`
as the campaign's first `Witness: none —` (a placeholder prompt, stays `judge`).

| | notify | glance | judge | review-minutes |
|---|---|---|---|---|
| before | 0 | 1 | 10 | 173 |
| after | 1 | 9 | 1 | 47 |

Backlog after pass 2: 157 ready (one more landed between the re-baseline and
the write), 72 witnessed + 1 `none`, 84 not — derived **18 notify / 44 glance /
95 judge**; declared **13 / 32 / 94** + 18 unset.

Finding about the faculty, not the prompts: `_sizing.py` has no `none` rule.
`Witness: none — <reason>` is read as a witness, so `multiwavelength_inversion`
derives `glance` while its declared `judge` holds by precedence — the dashboard
and planner are right, the derived reading is not. The regrade script counts it
as witnessed for the same reason. A one-line rule (a witness whose value starts
with `none` is no witness) belongs in the sizing faculty; filed as a follow-up
for the Brain rather than widened into this pass.

Weaker witnesses, flagged here as in pass 1: `non_uniform_over_sample`'s 1.5x
compile bound is the sweep's number, not the prompt's; `sparse_operator_int32`'s
`notify` holds only if the precision-operator compression is lossless;
`over_sample_size_via_snr_from`'s pre-existing witness pins option 1 of the
prompt's "decide one of".

### Pass 3 — `autofit`, 26 prompts (2026-09-17, issue #398)

Bigger than the ~15 of a pass because most of it was mechanical: 14
unwitnessed prompts got a witness, 6 witnessed prompts got only the restamp
(5 stale `judge`, 1 unset), and 7 witnessed bug prompts that derived `judge`
solely on "raises " in prose describing the crash being fixed got the
declared-`glance` override. Human accepted all 26 as proposed. Two
`Witness: none —` (`ep_analytic_updates`, an umbrella of four work packages;
`ep_lbfgs_jax`, a placeholder); `skip_the_likelihood` left at `judge` on
purpose (large, changes what the sampler evaluates). Four duplicated header
blocks collapsed in the same write (`skip_the_likelihood`, `assertion_repr`,
`emcee_crashes`, `stale_enable_pytrees` — the intake artefact, twice over).

| | notify | glance | judge | review-minutes |
|---|---|---|---|---|
| before | 2 | 0 | 24 | 465 |
| after | 3 | 20 | 3 | 130 |

Backlog after pass 3: 157 ready, 83 witnessed + 3 `none`, 71 not —
derived **19 notify / 55 glance / 83 judge**; declared **15 / 52 / 74** +
16 unset.

Findings for the Brain, added to the `none`-rule follow-up: (1) the "raises "
keyword is endemic in bug prompts — 8 of the campaign's overrides so far are
prose describing an existing crash, and the faculty's own "Known limit"
predicts exactly this; (2) `emcee_crashes_in_autocorrelation_when_the_chain`
and item 2 of `mcmc_thin_zero_and_check_size_short_chain` are the same
defect — the two witnesses were written to agree (Emcee gains Zeus's guard),
but one of the two prompts should fold into the other at pick-up.

Decisions the accept pinned, flagged as in earlier passes: `mcmc_thin_zero`
(thin clamps to 1; guard, not a named error); `split_fitness_batch_size`
declared `glance` over a derived `notify` (two new public kwargs); `howtofit_chapter_3`
keeps its declared `notify` over a derived `glance` (two docstring strings).

### Pass 4 — `autolens`, 11 prompts (2026-09-17, issue #398)

Human pre-accepted the pass before seeing the candidates ("Continue i
accept"), so proposal and write landed in one turn, with every pinned decision
listed on the issue for after-the-fact strikes. No restamps this time (the one
witnessed `autolens` prompt already agreed with itself). `multi_plane_time_delays`
keeps `judge` on its own merits — declared over a derived `glance` (its
"raises" sits inside inline code, which the faculty masks): the task decides
whether a half-plane-bound `LensCalc` refuses or answers, a real error
contract, and the science is a large multi-plane formalism. Two repeated title
lines collapsed (`magnification_errors_posterior_draws`, `point_magnification_api`).

| | notify | glance | judge | review-minutes |
|---|---|---|---|---|
| before | 0 | 0 | 11 | 230 |
| after | 0 | 10 | 1 | 55 |

Backlog after pass 4: 157 ready, 94 witnessed + 3 `none`, 60 not —
derived **20 notify / 64 glance / 73 judge**; declared **15 / 62 / 66** +
14 unset.

Decisions the accept pinned, for a later strike if wanted: `one_construction_path`
declared `glance` over a derived `notify` (a new public accessor — the pass-3
`split_fitness` rule) and `witt_wynne_solver_library_home` declared `glance`
over a derived `judge` (the keyword hit is its deliverable naming a public API;
the bit-identical witness makes `glance` the honest tier); `magnification_errors_posterior_draws` is gated on phases 5-6 and its
witness assumes them (the pass-1 `group_los_halos` shape); `point_magnification_api`'s
parity decision (signed or |mu|) stays open — the witness accepts either,
documented; `quick_update_plotting_cost`'s witness covers only the
container-safe half its own triage split off — the measured numbers are local
work.

### Remaining passes

`autolens_workspace` (7) · `euclid` (6) · `autogalaxy` (5) ·
`autolens_profiling` (5) · then a tail pass over the ~30 singleton targets.
