# Delete (SOP)

## What This Node Is For

`delete` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/delete.txt`)
- Example set reviewed: yes (`examples/nodes/sop/delete/DeleteDemo.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: example branch `dissolve_box` equivalent delete path showed 892 pts / 19 prims baseline in tested subnet.
- Live tweak: enabled `userandom` on `delete10`; output changed to 922 pts / 20 prims in active branch.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- delete criteria stack (group + number + random + bounding) can interact in non-obvious ways.
