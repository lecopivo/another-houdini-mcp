# Switch (SOP)

## What This Node Is For

`switch` routes one of multiple input branches to output, usually driven by an int parameter, expression, or animation.

## Session Status

- Status: in progress
- Docs read: yes (`help/nodes/sop/switch.txt`)
- Example set reviewed: no (no `help/examples/nodes/sop/switch/` in local corpus)
- Example OTL internals inspected: no
- Node comments read: yes
- Sticky notes read: yes (none available in local corpus)
- QA pass complete: partial (example-set gap)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Pass only the selected input index.
  - Commonly driven by expression/keyframes for procedural branching.
- Observed (live scene/params/geometry):
  - Built `/obj/academy_switch` with two branches (`box1`, `xform1<-sphere1`) into `switch1`.
  - `switch1.input=0` outputs box branch (`8 pts, 6 prims`).
  - `switch1.input=1` outputs sphere branch (`1 pt, 1 prim`) in this default sphere mode.
  - Out-of-range behavior in this build clamps to valid range:
    - `input=-1` behaves like input 0.
    - `input=3` behaves like highest connected input (1).
- Mismatches:
  - No mismatch with core intent; local example assets are missing.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_switch/box1 -> switch1 <- xform1 <- sphere1 -> output1`
- Key parameter names and values:
  - `switch1.input=0|1`
  - stress checks: `switch1.input=-1`, `switch1.input=3`
- Output verification method:
  - `probe_geometry` on `output1` for each input value.

## Key Parameters and Interactions

- `input`: single selector controlling active branch.
- Input wiring order determines branch index meaning.
- Expressions on `input` are the main pattern for conditional routing.

## Practical Use Cases

1. Toggle between heavy and lightweight branches for viewport/debug.
2. Expose mode switches in HDAs without duplicating downstream logic.

## Gotchas and Failure Modes

- Branch index changes when rewiring inputs; guard with comments/naming.
- Different branch attribute schemas can cause downstream instability.
- Missing local examples means behavior should be validated per build/network.

## Related Nodes

- `switchif`
- `merge`
- `blast`

## Academy QA Checklist

- [x] Official docs reviewed
- [ ] Example files reviewed
- [ ] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
