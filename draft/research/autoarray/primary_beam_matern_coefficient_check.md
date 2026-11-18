# Primary beam: does the preferred Matérn coefficient shift when the beam is in the solve?

Type: research
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: low
Consequence: glance
Community: https://github.com/PyAutoLabs/.github/discussions/35
Filed: 2026-11-18

Promised to @HRSAstro on the closed thread (we said we'd post the result there). Agreed by the
human in the /community chat on 2026-11-18.

## Background

The primary beam on interferometer inversions (PyAutoArray#640 / #644) shipped in autoarray
2026.10.22.1. On the thread (2026-10-21) the proposer reported, from old non-lens mock tests in
PyUVimage, that with the beam in the solve the preferred regularisation coefficient moved:
down for a Matérn prior (and the evidence favoured the beam), slightly up for adaptive
regularisation (evidence about the same).

## What

1. On a simulated lensed interferometer dataset (SMA- or ALMA-like, with a beam that matters
   across the source), fit a pixelized source with and without the primary beam, for Matérn
   and for adaptive regularisation.
2. Record the preferred regularisation coefficient and the log evidence for each of the four
   cases.
3. Write a short note with the table; draft a thread reply on discussions/35 for human
   approval (posting stays with the human).

## Witness

A results table (coefficient and log evidence, beam on vs off, Matérn vs adaptive) on one lensed
mock, plus the drafted thread reply.
