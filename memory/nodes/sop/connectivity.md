# Connectivity (SOP)

## What This Node Is For

`connectivity` labels disconnected pieces with an id attribute (typically `class`), on points or primitives.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/connectivity.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/connectivity/ConnectedBalls.txt`)
- Example OTL internals inspected: yes (`ConnectedBalls.otl`, companion usage in `PartitionBall.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Generate per-piece ids for disconnected geometry.
  - Example uses generated ids to color independent pieces.
- Observed (live scene/params/geometry):
  - `Connectivity_SOP_Example/connectivity1` writes primitive attr `ball` (`connecttype=primitive`).
  - `PartitionBall/sopnet1/connectivity1` writes primitive attr `piece` consumed by downstream partition grouping.
  - Probes confirm primitive attr presence and stable topology counts through labeling stage.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_ConnectedBalls/Connectivity_SOP_Example/object_merge_DOPs -> connectivity1 -> primitive1`
- Key parameter names and values:
  - `connectivity1.connecttype=1` (Primitive)
  - `connectivity1.attribname=ball` (example variant) / `piece` (partition workflow)
  - optional local var map enabled (`createvarmap=1`)
- Output verification method:
  - `probe_geometry` for generated primitive attribute.

## Key Parameters and Interactions

- `connecttype`: point vs primitive domain.
- `attribname`: id channel consumed by partition/group/color workflows.
- `seamgroup` / `byuv`: alternate connectivity boundaries when needed.

## Practical Use Cases

1. Piece labeling before per-piece transforms, colors, or loops.
2. Prep for partition/name workflows in sim and fracture pipelines.

## Gotchas and Failure Modes

- Mixed/dirty topology can create unexpected extra pieces.
- Choosing point vs primitive domain incorrectly breaks downstream expressions.
- Seam/UV options can change piece count drastically; verify with quick visual checks.

## Related Nodes

- `partition`
- `assemble`
- `groupsfromname`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
