# Partition (SOP)

## What This Node Is For

`partition` creates many groups using a rule expression, commonly from connectivity/piece ids in legacy fracture and DOP object workflows.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/partition.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/partition/PartitionBall.txt`)
- Example OTL internals inspected: yes (`PartitionBall.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Build disjoint groups from a rule (`piece_$PIECE` pattern style).
  - Example passes partitioned groups into RBD Glue object creation.
- Observed (live scene/params/geometry):
  - In `/obj/academy_PartitionBall/dopnet1/sopnet1`, `connectivity1` creates primitive `piece` attribute.
  - `partition1` then creates primitive groups via rule (example currently shows `rule=piece_-1`).
  - Sticky note and network context confirm intended usage for DOP object splitting from SOP groups.
- Mismatches:
  - Current loaded example stores a concrete `rule` value rather than symbolic `piece_$PIECE`, but companion sticky explains intended naming pattern behavior.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_PartitionBall/dopnet1/sopnet1/... -> connectivity1 -> partition1 -> broken_ball_OUT`
- Key parameter names and values:
  - `partition1.rule` (group naming rule)
  - `partition1.entity` (primitive for fracture pieces)
- Output verification method:
  - `probe_geometry` for attribute continuity and `get_parameter_overrides` on `partition1`.

## Key Parameters and Interactions

- `rule`: primary mapping from local vars/attrs to group names.
- `group` + `entity`: scope and class for partitioning.
- Works best directly after connectivity-derived piece ids.

## Practical Use Cases

1. Legacy DOP setups requiring one group per fracture piece.
2. Transitional pipelines where groups are still expected by downstream tools.

## Gotchas and Failure Modes

- Can create many groups and become inefficient at scale.
- Rules based on unstable ids can break reproducibility across topology changes.
- Prefer string `name` attrs for newer pipelines when possible.

## Related Nodes

- `connectivity`
- `name`
- `group`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
