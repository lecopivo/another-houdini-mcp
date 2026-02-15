# Convert (SOP)

## What This Node Is For

`convert` Converts geometry between primitive representations.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/convert.txt`)
- Example set reviewed: yes (`examples/nodes/sop/convert/ConvToTrimSurface.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: based on node docs/example description and sticky-note guidance.
- Observed: official example `ConvToTrimSurface` instantiated and cooked; representative display output was `16 pts / 1 prims` at `material1`.
- Mismatches: none observed in this pass.

## Minimum Repro Setup

- Example loaded: `/obj/academy_seq3_*_convert` (instantiated one-by-one, then deleted before next node).
- Verification: asset installs, instantiates, and display network cooks without errors.

## Key Parameters and Interactions

- Primary behavior is driven by node-specific core parameters shown in the example network.
- Crowd/path nodes depend on stable clip libraries, agent definitions, and motion-path contracts.

## Gotchas and Failure Modes

- Legacy/alternative nodes (`cookie`, `copy`) can diverge from newer counterparts; verify intended tool variant.
- Crowd motion-path nodes are sensitive to clip naming/state graph consistency.

## Companion Finding (from PolySoup study)

- `convert` is the practical exit path from polygon soup back to regular polygons for editing/compatibility.
- In a live soup branch (`112 pts / 1 PolySoup prim / 112 verts`), converting back produced `112 pts / 108 Polygon prims / 432 verts`, preserving key primitive attribute `classid`.
- Use this to verify semantic preservation after soup optimization, while accepting increased primitive/vertex overhead in editable polygon form.

## Related Nodes

- `attribwrangle`
- `group`
- `merge`
