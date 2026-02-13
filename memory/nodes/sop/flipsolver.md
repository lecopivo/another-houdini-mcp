# FLIP Solver (SOP)

## What This Node Is For

`flipsolver` evolves SOP-based FLIP liquid state over time from container/source/collision/ocean boundary inputs.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/flipsolver.txt`)
- Example set reviewed: companion network study in `/obj/geo1` (multi-branch SOP FLIP reference)
- Node comments read: yes (including key sticky notes around projection/collision behavior)
- Sticky notes read: yes
- QA pass complete: yes (connection-level study across all six branches)

## Source-of-Truth Split

- Intent (docs):
  - Solve FLIP with particle+grid hybrid projection.
  - Consume container streams from `flipcontainer` (sources/container/collisions).
  - Optionally consume ocean boundary data through input 3.
  - Drive downstream surfacing/caching/whitewater from solver outputs.
- Observed (`/obj/geo1`):
  - Repeated branch pattern: `flipcontainer -> (optional flipboundary/flipcollide) -> flipsolver -> fluidcompress -> filecache -> particlefluidsurface`.
  - Input-3 ocean boundary wiring appears in branches 4/5/6 via `oceanevaluate`.
  - `flipboundary` branch variants are used for source/sink/velocity/pressure transfer to the fluid.
  - Whitewater chain is driven from compressed FLIP outputs (`whitewatersource -> whitewatersolver -> whitewaterpostprocess`).
- Mismatches: none.

## Network Patterns Learned from `/obj/geo1`

1. **Minimal tank**
   - `flipcontainer -> flipsolver -> fluidcompress -> filecache -> particlefluidsurface`

2. **Source/Sink injection**
   - Insert `flipboundary` between container and solver.
   - Use boundary input 3 for source/sink geometry/volumes.

3. **Collider integration**
   - Insert `flipcollide` before solver.
   - Use collide input 3 for collision geometry.

4. **Ocean/open boundary**
   - `oceanspectrum -> oceanevaluate -> flipsolver` input 3.
   - Common for large-scale/open-water setups.

5. **Adaptive domain shaping**
   - Upstream VDB preprocessing (`vdbactivate`, `volumewrangle`, masks in subnets) can drive container shaping before solve.

6. **Whitewater extension**
   - Feed compressed liquid/fields to `whitewatersource` then `whitewatersolver`, post with `whitewaterpostprocess`.

## Practical Gotchas

- Keep `particlesep` and `gridscale` consistent between `flipcontainer` and `flipsolver`.
- `flipboundary`/`flipcollide` geometry quality and velocity handling heavily affect stability and splash quality.
- Ocean boundary input (solver input 3) is a different workflow from closed tank waterline setups; avoid mixing assumptions.
- Compression is lossy by design; use nodes that understand compressed data (`particlefluidsurface`, `whitewatersource`).

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
