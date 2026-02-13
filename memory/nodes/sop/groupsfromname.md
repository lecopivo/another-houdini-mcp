# Groups from Name (SOP)

## What This Node Is For

`groupsfromname` converts unique string values in a name attribute into per-value groups (legacy bridge workflow).

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/groupsfromname.txt`)
- Example set reviewed: yes (fallback via companion official examples and live repro)
- Example OTL internals inspected: yes (companion OTL chain from `PartitionBall.otl` plus live repro network)
- Node comments read: yes
- Sticky notes read: yes (none available in local corpus)
- QA pass complete: yes (fallback workflow used: docs + companion usage + live repro)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Build groups from string name values, with prefix/conflict/invalid-name control.
  - Intended mainly for workflows that still require groups.
- Observed (live scene/params/geometry):
  - In `/obj/academy_name_groups_error/groupsfromname1`, primitive `name` values (`part0`, `part1`) generated groups `nm_part0`, `nm_part1` when `groupprefix=nm_`.
  - Existing piece groups (`piece_0`, `piece_1`) remained present, demonstrating additive bridge behavior.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_name_groups_error/name1 -> groupsfromname1 -> output1`
- Key parameter names and values:
  - `groupsfromname1.attribname=name`
  - `groupsfromname1.class=primitive`
  - `groupsfromname1.groupprefix=nm_`
- Output verification method:
  - HOM listing of primitive groups at `groupsfromname1`.

## Key Parameters and Interactions

- `attribname` and `class` must match the source name attr domain.
- `groupprefix` prevents collisions with existing groups.
- `conflict` mode controls replacement vs union when names overlap.

## Practical Use Cases

1. Export or legacy tools that require groups instead of name attrs.
2. Transitional pipelines migrating from group-centric to attr-centric partitioning.

## Gotchas and Failure Modes

- Large disjoint sets as groups are less efficient than string attrs.
- Invalid names may be ignored or remapped; choose invalid-name policy intentionally.
- Local corpus lacks official node-scoped examples; validate in target pipeline.

## Related Nodes

- `name`
- `partition`
- `groupsfromattrib`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
