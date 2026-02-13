# Spline Curve Clay (SOP)

## What This Node Is For

`curveclay` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/curveclay.txt`)
- Example set reviewed: yes (`examples/nodes/sop/curveclay/CurveClayBasic.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: example produced 6164 pts / 1 prim in method1 network; curveclay nodes found in two method branches.
- Live tweak: tweaked `refine` on `curveclay_profile`; example remained stable and cooked cleanly.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- works on spline surfaces; not polygon-mesh replacement for clay.
