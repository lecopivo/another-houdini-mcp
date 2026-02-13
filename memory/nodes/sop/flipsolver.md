# FLIP Solver (SOP)

## What This Node Is For

`flipsolver` advances SOP FLIP liquid state from three core streams plus an optional boundary/ocean stream:

- input 0: sources
- input 1: container
- input 2: collisions
- input 3: optional boundary fields (commonly from `oceanevaluate`)

## Practical Setup Rules

1. Treat inputs `0/1/2` as a synchronized stream contract.
   - Always pass these three streams together through the FLIP chain.
   - Misaligned stream wiring is a common cause of invalid solves.

2. Add source/sink behavior with `flipboundary` only when needed.
   - `flipboundary` belongs in source/sink workflows.
   - For pure ocean-boundary workflows, keep the base stream directly from `flipcontainer` to `flipsolver` on inputs `0/1/2`.

3. Add colliders with `flipcollide` before `flipsolver`.
   - Feed collider geometry to `flipcollide` input 3.
   - Forward collide outputs 0/1/2 to solver 0/1/2.

4. Ocean/open-boundary input uses solver input 3.
   - Typical path: `oceanspectrum -> oceanevaluate -> flipsolver input 3`.
   - This is separate from source/sink logic.

5. Respect scale between domain size and `particlesep`.
   - Too-large `particlesep` relative to domain/collider scale causes coarse, unstable-looking behavior.
   - Start finer for collision-heavy shots, coarser for broad ocean previews.

## Canonical SOP FLIP Build Orders

### A) Source-driven tank (baseline)

1. `flipcontainer`
2. `flipboundary` (input 3 from source geo/volume)
3. `flipsolver`
4. `fluidcompress`
5. `filecache` (optional but recommended)
6. `particlefluidsurface`

Wiring rule:
- Pass 0/1/2 streams from `flipcontainer -> flipboundary -> flipsolver -> fluidcompress`.

### B) Collision-driven FLIP

1. Build baseline A.
2. Insert `flipcollide` between boundary/container stage and solver.
3. Feed collider geometry to `flipcollide` input 3.

Wiring rule:
- `... -> flipcollide -> flipsolver` for streams 0/1/2.

### C) Ocean-boundary FLIP (geo1 style)

1. `box` (or domain geometry)
2. `flipcontainer` (input 0 from domain geometry)
3. `oceanspectrum`
4. `oceanevaluate` (input 1 from `oceanspectrum`)
5. `flipsolver`
6. `fluidcompress`
7. `particlefluidsurface`

Critical wiring:
- `flipcontainer` outputs 0/1/2 -> `flipsolver` inputs 0/1/2
- `oceanevaluate` output 0 -> `flipsolver` input 3

Do not replace the main 0/1/2 path with `flipboundary` for this pattern unless you explicitly need source/sink behavior.

## Parameter Starting Points

Use these as practical defaults, then tune per shot:

- `flipcontainer.particlesep`
  - small/medium domain with collisions: `~0.04-0.08`
  - large ocean-like domain: `~0.12-0.20`
- `flipcontainer.gridscale`: start near default (`2.0`), lower only when needed for detail.
- `flipsolver.boundarytype`: set explicitly when doing ocean/open boundary workflows.
- `oceanevaluate`
  - commonly: `deformgeo=0`, `surface=1`, `vel=1`
  - set size/division controls coherent with tank/domain scale.
- `oceanspectrum`
  - begin with moderate wave frequency (`res` around `8`) and wind speed in a practical range (for example `6-12`) before tuning look.

## Validation Checklist (Per Setup)

1. Connectivity check:
   - confirm each expected input index (especially solver input 3).
2. Frame sampling:
   - inspect frame 1/12/24 point counts and bbox evolution.
3. Coarseness sanity:
   - if collisions look chunky or leaky, reduce `particlesep` first.
4. Ocean sanity:
   - if ocean setup dies to zero points, verify 0/1/2 stream path and domain/evaluate scale.
5. Boundary sanity:
   - if the sim appears unexpectedly source-driven, check that `flipboundary` is not unintentionally in the main 0/1/2 path.

## Practical Gotchas

- `particlesep` mismatch is the most common reason for coarse or unstable collision behavior.
- Ocean branch is easy to miswire: keep base streams from `flipcontainer` directly into solver.
- Compression is lossy by design; always feed compression-aware downstream nodes.
- Colliders should be polygonal/clean and consistent with intended collision mode.

## Related Nodes

- `flipcontainer`
- `flipboundary`
- `flipcollide`
- `fluidcompress`
- `particlefluidsurface`
- `whitewatersource`
- `whitewatersolver`
- `whitewaterpostprocess`
- `oceanspectrum`
- `oceanevaluate`
