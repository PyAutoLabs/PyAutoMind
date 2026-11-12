# Fred Again lyric at the bottom of every PyAutoLabs repo README

Type: docs
Target: workspaces
Repos:
- PyAutoLens
- workspaces
Difficulty: medium
Autonomy: safe
Priority: low
Memory: wiki/lensing/sources/dark-matter-substructure.md; wiki/galaxies/sources/massive-ellipticals.md; reading-queue.md
Status: formalised
Consequence: glance
Witness: a script over all PyAutoLabs repos finds the track URL on every README's last non-empty line.
Review-minutes: 3
Unattended: ready
Lane: any

Every PyAutoLabs GitHub repo README should end with the same Fred Again lyric
line that PyAutoLens's README already ends with (@PyAutoLens `README.md`, last
line):

```html
<sub><i><a href="https://open.spotify.com/track/6Ao5d7TMQ92h87jQqSHGyw">i found you, i found you, i found you beautiful, exploding, i found you</a></i></sub>
```

1. List every public PyAutoLabs repo and whether its README already ends with
   this line (match on the Spotify track URL).
2. For each repo missing it, append the line as the final line of the README
   (blank line before it), using the repo's README format (Markdown as above;
   for `.rst` use an equivalent raw-HTML or link line).
3. No other README changes.

Witness: a script over all PyAutoLabs repos finds the track URL on every README's last non-empty line.

<!-- formalised by the Intake (Conception) Agent on 2026-11-04 from file:/tmp/claude-1000/-home-jammy-Professional/e7f3429c-9309-4311-875f-b4af170b9807/scratchpad/lyric.md -->
