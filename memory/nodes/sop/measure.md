# Measure (SOP)

## What This Node Is For

`measure::2.0` computes geometric metrics (area, perimeter, volume, curvature, gradient, laplacian, integrals) and writes them to attributes.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/measure.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/measure/MeasureArea.txt`, `help/examples/nodes/sop/measure/MeasureLaplacian.txt`)
- Example OTL internals inspected: yes (`MeasureArea.hda`, `MeasureLaplacian.hda`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Produce measurement attributes on points/primitives.
  - Area and Laplacian examples emphasize attribute-driven downstream operations.
- Observed (live scene/params/geometry):
  - `MeasureArea` example `/obj/academy_MeasureArea/geo1/measure1` outputs primitive `area` attribute.
  - Switching `measure1.measure` from `area` to `perimeter` and setting `attribname=perim_test` produced primitive attribute `perim_test`; restoring returned `area`.
  - `MeasureLaplacian` example uses measure-in-loop pattern (`measure11`, `measure12`) over `Cd` and writes `laplacian`, then transfers/smooths.
  - Probes confirm expected attribute-class changes in loop outputs (`prim Cd/laplacian` then point-domain variants downstream).
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - Area: `/obj/academy_MeasureArea/geo1/... -> measure1 -> group/color/extrude chain`
  - Laplacian: `/obj/academy_MeasureLaplacian/geo1/attribfrommap2 -> repeat_begin -> measure -> wrangle -> repeat_end`
- Key parameter names and values:
  - `measure1.measure=1` (Area)
  - test variant: `measure1.measure=0`, `measure1.attribname=perim_test`
  - Laplacian nodes: `measure11.measure=6`, `srcattrib=Cd`, `attribname=laplacian`
- Output verification method:
  - `probe_geometry` attribute presence checks before/after measure changes.

## Key Parameters and Interactions

- `measure`: selects metric family.
- `attribname`: output attribute name to drive downstream ops.
- `grouptype`/`integrationdomain` and `pieceattrib`: per-element vs per-piece behavior.
- `srcattrib`/`srccomp`: source selection for gradient/laplacian/integrals.

## Practical Use Cases

1. Build procedural masks (area/curvature thresholds) for modeling and shading.
2. Drive iterative smoothing/sharpening with Laplacian-based loops.

## Gotchas and Failure Modes

- Open surfaces can make volume results non-meaningful.
- Wrong element class (point vs primitive expectations) can break downstream wrangles/groups.
- Complex Laplacian loops are sensitive to step size and iteration count.

## Related Nodes

- `attribpromote`
- `group`
- `attribwrangle`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
