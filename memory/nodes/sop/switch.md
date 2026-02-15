# Switch (SOP)

## What This Node Is For

`switch` routes one of multiple input branches to output, usually driven by an int parameter, expression, or animation.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/switch.txt`)
- Example set reviewed: yes (fallback via companion official example `help/examples/nodes/sop/copy/StampRandom.txt`)
- Example OTL internals inspected: yes (`StampRandom.otl` companion network includes animated/expression-driven `switch1`)
- Node comments read: yes
- Sticky notes read: yes (none available in local corpus)
- QA pass complete: yes (fallback workflow used: docs + companion example + live repro)

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
  - Companion official example `/obj/academy_StampRandom/StampRandom/switch1` uses an expression-driven `input` to randomize template selection under Copy stamping.
- Mismatches:
  - No mismatch with core intent.
  - Out-of-range clamping behavior is build-specific and should be re-checked when Houdini version changes.

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

## Companion Finding (from PolySoup study)

- `switch` is useful as a diagnostics/perf toggle for heavy geometry optimization branches.
- In `PolysoupTorus`, switching raw vs polysoup kept point count fixed (`4,000,000`) while changing primitive/vertex load dramatically:
  - raw: `4,000,000 prims / 16,000,000 verts`
  - polysoup: `1 prim / 4,000,000 verts`.
- This makes `switch` a practical pattern for A/B viewport-debug branches before final export.

## Related Nodes

- `switchif`
- `merge`
- `blast`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
