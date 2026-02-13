# Blast (SOP)

## What This Node Is For

`blast` deletes selected geometry components (points/primitives/edges/breakpoints), most often as a fast isolate/remove step in modeling and procedural branches.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/blast.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/blast/TorusBlast.txt`)
- Example OTL internals inspected: yes (`TorusBlast.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Delete by group pattern + group type.
  - `Delete Non Selected` inverts behavior for quick isolation.
  - Example emphasizes interactive point-list removal.
- Observed (live scene/params/geometry):
  - Example node `/obj/academy_TorusBlast/TorusBlast/blast1` uses point-mode deletion (`grouptype=3`) and group `6-7 16 86-87 96-97`.
  - Input torus: `100 pts, 100 prims`; blast result: `93 pts, 91 prims`.
  - Enabling inversion (`negate=1`) isolates selection to `7 pts, 3 prims`.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_TorusBlast/TorusBlast/torus1 -> blast1`
- Key parameter names and values:
  - `blast1.group="6-7 16 86-87 96-97"`
  - `blast1.grouptype=3`
  - `blast1.negate=0|1`
- Output verification method:
  - `probe_geometry` on `torus1` and `blast1`.

## Key Parameters and Interactions

- `group`: exact deletion/isolation target.
- `grouptype`: point/primitive/edge/breakpoint interpretation.
- `negate`: switch between delete-selection and keep-selection.
- `fillhole`: optional capping behavior for point-based deletes.

## Practical Use Cases

1. Isolate problem regions for debugging downstream SOP chains.
2. Remove procedural subsets quickly before branching into alternate operations.

## Gotchas and Failure Modes

- Wrong `grouptype` can silently target unintended elements.
- Inversion (`negate`) is powerful but easy to leave on accidentally.
- For heavily procedural setups, prefer deterministic group generation upstream.

## Related Nodes

- `delete`
- `dissolve`
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
