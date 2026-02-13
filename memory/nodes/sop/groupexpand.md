# Group Expand (SOP)

## What This Node Is For

`groupexpand` grows or shrinks a base group by topological steps, with optional constraints (normals, connectivity, collision, flood behavior).

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/groupexpand.txt`)
- Example set reviewed: yes (`examples/nodes/sop/groupexpand/GroupExpandBasic.txt`)
- Example HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + sticky):
  - Expand/shrink groups by step count, optionally restricting growth by normal spread angle.
- Observed (live play on `/obj/academy_deep_groupexpand/groupexpand1`):
  - Baseline: output primitive group `out` size `78`.
  - Step behavior:
    - `numsteps=2` -> `out=33`.
    - `numsteps=-2` (shrink) -> `out=0`.
  - Normal constraint behavior:
    - with `bynormal=1`, `normalangle=10`, and `numsteps=2` -> growth nearly blocked (`out=1`).
    - relaxing to `normalangle=60` restored broad growth.
  - Step attribute behavior:
    - enabling `usestepattrib` with name `growstep` created primitive attrib with expected step staging (`min=-1`, `max=5` in tested state), useful for debugging expansion wavefront.
  - Disabling normal restriction (`bynormal=0`) slightly increased growth vs constrained case at same steps in this setup (`34` vs `33`).
- Mismatches: none.

## Minimum Repro Setup

- Example network: sphere + polyextrude with seeded primitive base group.
- Test sequence:
  - vary `numsteps` positive/negative,
  - tighten/loosen `normalangle` with `bynormal` on,
  - enable step attribute and inspect range.

## Key Parameter Interactions

- `numsteps` sign controls expand vs shrink.
- `bynormal` + `normalangle` can strongly gate growth across sharp features.
- `usestepattrib` converts expansion into analyzable staged data.
- Group type correctness matters; wrong class selection yields confusing no-op behavior.

## Gotchas and Failure Modes

- Shrink with small starting groups can collapse to empty quickly.
- Normal constraints can look like failure when angle is too tight.
- Flood-fill/constraint settings can override naive expectation of step-limited growth.
