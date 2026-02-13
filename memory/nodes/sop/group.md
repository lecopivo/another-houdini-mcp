# Group (SOP)

## What This Node Is For

`group` creates/edits point/primitive/edge groups using numbers, patterns, bounds, normals, feature edges, and boolean group-combine logic.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/group.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/group/FeaturedEdges.txt`)
- Example OTL internals inspected: yes (`FeaturedEdges.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Build groups to drive downstream SOP scope.
  - Example creates an edge group and uses it to preserve features in PolyReduce.
- Observed (live scene/params/geometry):
  - In `/obj/academy_FeaturedEdges/sphere_object1/group1`, edge-group setup is explicit:
    - `entity=2` (edges)
    - `pattern=p98-99-100-101-82-102-122-141-140-139-138-118-98`
  - Group output geometry counts match source geometry (as expected for non-destructive grouping).
  - Downstream `/polyreduce1` consumes this group via `creases=group1` with `creaseweight=10`.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_FeaturedEdges/sphere_object1/sphere1 -> group1 -> polyreduce1`
- Key parameter names and values:
  - `group1.crname=group1`
  - `group1.entity=2`
  - `group1.pattern=...` (explicit edge sequence)
- Output verification method:
  - `get_parameter_overrides` for `group1` and downstream `polyreduce1`.

## Key Parameters and Interactions

- `entity`: must match intended group class (point/prim/edge).
- `pattern` and `groupop`: deterministic direct selection path.
- `groupedges` + angle/length filters: feature-based edge extraction path.
- `mergeop`: controls replacement vs union/intersection/subtraction with existing groups.

## Practical Use Cases

1. Define precise reduction-preserve edges for decimation.
2. Build reusable selection masks for downstream modeling FX chains.

## Gotchas and Failure Modes

- Wrong group class silently breaks downstream consumers.
- Number/pattern-based groups are brittle when upstream topology changes.
- Complex combines are easy to misread later; prefer clear naming and staged groups.
- Always verify the created group is non-empty before using it in downstream constraints/filters (empty groups can fail silently and look like solver instability).

## Related Nodes

- `groupcopy`
- `grouptransfer`
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
