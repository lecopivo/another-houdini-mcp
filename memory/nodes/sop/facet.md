# Facet (SOP)

## What This Node Is For

`facet` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/facet.txt`)
- Example set reviewed: yes (`examples/nodes/sop/facet/FacetVariations.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: facet variation network branch output 1508 pts / 40 prims.
- Live tweak: enabled `cusp`; topology stayed stable in tested branch while shading/point-sharing behavior changes.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- facet pipeline stages interact; understand order (normals, unique/consolidate, cusp) before tuning.
