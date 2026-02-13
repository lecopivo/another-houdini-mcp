# Name (SOP)

## What This Node Is For

`name` writes string identity attributes (usually `name`) on points/primitives/vertices, enabling scalable piece selection and partitioning.

## Session Status

- Status: in progress
- Docs read: yes (`help/nodes/sop/name.txt`)
- Example set reviewed: no (no `help/examples/nodes/sop/name/` in local corpus)
- Example OTL internals inspected: no
- Node comments read: yes
- Sticky notes read: yes (none available in local corpus)
- QA pass complete: partial (example-set gap)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Assign or edit naming attrs; provide group-to-name conversion path.
  - Name attrs are generally more scalable than disjoint groups.
- Observed (live scene/params/geometry):
  - In `/obj/academy_name_groups_error/name1`, explicit naming by groups produced primitive `name` values `part0` and `part1`.
  - Input groups came from `partition` over connectivity-labeled pieces.
  - Downstream `groupsfromname` successfully regenerated prefixed groups from the `name` attr.
- Mismatches:
  - `Name from Group` mode did not produce expected values in this custom test; explicit group/name entries were reliable.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_name_groups_error/merge1 -> connectivity1 -> partition1 -> name1 -> groupsfromname1`
- Key parameter names and values:
  - `name1.class=primitive`
  - `name1.numnames=2`
  - `name1.group1=piece_0`, `name1.name1=part0`
  - `name1.group2=piece_1`, `name1.name2=part1`
- Output verification method:
  - HOM check of unique primitive `name` values at `name1`.

## Key Parameters and Interactions

- `attribname` + `class`: identity channel and domain.
- Explicit naming entries are deterministic and easy to debug.
- `name` pairs naturally with `groupsfromname` and piece pipelines.

## Practical Use Cases

1. Create robust piece labels for packed/sim/export workflows.
2. Replace large disjoint group sets with scalable string identity attrs.

## Gotchas and Failure Modes

- Mixed/overlapping group membership can make implicit naming ambiguous.
- Legacy group workflows may still require conversion back via `groupsfromname`.
- Local corpus lacks official node-scoped examples; validate per production setup.

## Related Nodes

- `groupsfromname`
- `partition`
- `assemble`

## Academy QA Checklist

- [x] Official docs reviewed
- [ ] Example files reviewed
- [ ] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
