# Delete (SOP)

## What This Node Is For

`delete` culls points/primitives/edges using a stacked filter system (group, number mode, bounding, normal, degenerate, random).

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/delete.txt`)
- Example sets reviewed: yes (`examples/nodes/sop/delete/DeleteDemo.txt`, `examples/nodes/sop/delete/DeleteFan.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + examples):
  - Use one node for many deletion styles (pattern/range/expression/bounding/random) across different entities.
  - `DeleteFan` highlights range-driven primitive culling rhythm (`Select x of y`).
  - `DeleteDemo` shows point and primitive workflows in parallel.
- Observed (live parameter play):
  - `DeleteFan` (`/obj/academy_deepcare_deletefan/fan/delete1`):
    - Baseline (`select1=1`, `select2=2`): `13 pts / 6 prims`.
    - `select2=3`: `13 pts / 8 prims`.
    - `negate=1` after that: `11 pts / 5 prims`.
  - `DeleteDemo` points branch (`/obj/academy_deepcare_delete/pts_range/delete3`):
    - Baseline: `320 pts / 18 prims`.
    - `select1=1`, `select2=2`: `480 pts / 18 prims`.
    - `userandom=1`, `percent=10`: `913 pts / 20 prims` in that active branch.
  - `DeleteDemo` prim branch (`/obj/academy_deepcare_delete/prims_range/delete3`):
    - Baseline: `520 pts / 10 prims`.
    - `keeppoints=1`: `960 pts / 10 prims` (expected orphan-point retention).
    - Small bounding volume enabled (`affectvolume=1`, `size=0.4`): `960 pts / 20 prims` in current stacked-rule state.
- Mismatches: none, but behavior is highly dependent on the full active rule stack.

## Minimum Repro Setup

- Load one official example, inspect a target `delete` node, then probe before/after each key parameter change.
- Good starter nodes:
  - `/obj/.../fan/delete1` (`DeleteFan`) for clear range behavior.
  - `/obj/.../pts_range/delete3` and `/obj/.../prims_range/delete3` (`DeleteDemo`) for points-vs-prims comparisons.

## Key Parameter Interactions (Practical)

- `entity` changes the semantic of almost every other option.
- `groupop` (pattern/range/expression) and `negate` combine first-order selection behavior.
- `userandom` + `percent` is applied on top of other active selectors; results can look counterintuitive if number/bounding modes are still enabled.
- `keeppoints` only matters when deleting primitives/edges and you want to preserve unreferenced points.
- Multiple filter families can be active simultaneously; always inspect all enabled sections before diagnosing output.

## Gotchas and Failure Modes

- Biggest pitfall: forgetting previous filters are still active, then misattributing the result to the last changed parameter.
- Point/primitive counts alone can mislead when `keeppoints` is on; check both counts and intended entity type.
- For simpler predictable culling, `blast` is often safer; use `delete` when you explicitly need its multi-criteria stack.
