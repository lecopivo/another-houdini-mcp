# Attribute Promote (SOP)

## What This Node Is For

`attribpromote` converts attributes between classes (point/prim/vertex/detail) with controlled aggregation methods.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/attribpromote.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/attribpromote/AttribPromoteSphere.txt`)
- Example OTL internals inspected: yes (`AttribPromoteSphere.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Promote/demote attributes with merge policy (average, min/max, first/last, etc.).
  - Example demonstrates point->primitive then primitive->point transfer.
- Observed (live scene/params/geometry):
  - `attribcreate2` produces point attr `foo`.
  - `attribpromote1` (`inname=foo`, `outclass=primitive`) converts `foo` to primitive attr.
  - `attribpromote2` (`inclass=primitive`, `inname=Cd`) pushes primitive color back to points.
  - Probes confirm class migration exactly as intended.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_AttribPromoteSphere/AttribPromoteSphere/sphere1 -> attribcreate2 -> attribpromote1 -> primitive2 -> attribpromote2`
- Key parameter names and values:
  - `attribpromote1.inname=foo`
  - `attribpromote1.inclass=point` (default)
  - `attribpromote1.outclass=primitive`
  - `attribpromote2.inclass=primitive`, `attribpromote2.inname=Cd`
- Output verification method:
  - `probe_geometry` at each stage to confirm attr class movement.

## Key Parameters and Interactions

- `inname`, `inclass`, `outclass`: primary promotion contract.
- `method`: decides aggregation from many source elements to one destination element.
- `deletein`: useful when replacing source class attr.

## Practical Use Cases

1. Promote point masks to primitive values for face-level operations.
2. Convert primitive shading/analysis attrs back to points for deformation/transfer.

## Gotchas and Failure Modes

- Wrong class assumptions silently produce confusing downstream attribute queries.
- Promotion method strongly changes meaning (e.g., `First` vs `Average`).
- Pattern promotion can unintentionally affect more attrs than expected.

## Companion Finding (from Normal study)

- Promoting point normals to vertex normals is a valid display-merge tactic: point `N` is copied per incident vertex, preserving visual result while satisfying vertex-class expectations of downstream merged branches.

## Related Nodes

- `attribtransfer`
- `attribwrangle`
- `measure`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
