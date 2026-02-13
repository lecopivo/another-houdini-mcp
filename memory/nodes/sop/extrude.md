# Extrude (SOP)

## What This Node Is For

`extrude` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/extrude.txt`)
- Example set reviewed: yes (`examples/nodes/sop/extrude/ExtrudeFont.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: font example output 2468 pts / 638 prims.
- Live tweak: changed `depthxlate` 0 -> 0.2 on `extrude_font`; topology unchanged, extrusion placement changed.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- extrude is great for text/surfaces; for polygon face workflows prefer polyextrude.
