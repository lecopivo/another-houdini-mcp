# Add (SOP)

## What This Node Is For

`add` creates points/primitives or rewires existing points into new primitive patterns.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/add.txt`)
- Example set reviewed: yes (`examples/nodes/sop/add/AddItUp.txt`)
- Example OTL internals inspected: yes (`AddItUp.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from lightweight point generation to pattern/group-driven polygon creation and point-only extraction.
- Observed:
  - Live repro `/obj/academy_add_live`: baseline input passthrough kept grid topology (`100 pts / 81 prims`);
  - Setting `keep=1` and `remove=0` produced point-only output (`100 pts / 0 prims`), matching docs.
  - Example `/obj/academy_AddItUp` confirms multiple practical modes: by pattern, by group, null-path construction, and point-only workflows.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_add_live/grid1 -> add1 -> OUT_ADD`
- Key parms: `keep`, `add`, `group`, `inc`, `closed*`, pattern fields.
- Verification: `probe_geometry` primitive-count drop when point-only mode enabled.

## Key Parameters and Interactions

- `keep` controls delete-geometry-keep-points behavior.
- `add` mode chooses pattern/group connection strategy.
- `remove` can unintentionally cull needed points when combined with point-only workflows.

## Gotchas and Failure Modes

- Point-order dependence makes results sensitive to upstream topology reorder.
- Aggressive point removal can produce empty outputs unexpectedly.

## Related Nodes

- `group`
- `merge`
- `fit`
