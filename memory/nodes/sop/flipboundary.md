# FLIP Boundary (SOP)

## Intent

`flipboundary` injects or removes FLIP particles through source/sink boundary logic driven by geometry or volumes, with velocity/pressure-based control.

## Core Behavior

- Operates on FLIP stream tuple 0/1/2 and optional boundary geometry on input 3.
- Supports two modes:
  - `Source`: emit particles
  - `Sink`: remove particles (with optional suction-like behavior)
- Boundary solve style is configurable (`none`, `velocity`, `pressure`).
- Can derive additional velocity from emitter/sink deformation.

## Key Parameters

- `type`: source vs sink.
- `boundarytype`: none / velocity / pressure.
- pressure controls (`pressure`, `hydro_pressure`, waterline offsets/bands).
- velocity controls (`velocity`, `normalvel`, `computevel`, `scalevel`).
- `activate`: temporal gating.

## Typical Workflow

```text
flipcontainer streams + source/sink geometry -> flipboundary -> flipsolver
```

- Keep upstream 0/1/2 streams connected and synchronized.
- Feed emitter/sink geometry to input 3.
- Choose pressure mode for fill-level style behavior; velocity mode for directional sourcing.

## Production Usage

- Pressure sourcing is useful for controlled filling; velocity sourcing for continuous jets/overflow behavior.
- In sink setups, negative pressure/velocity can create suction-like removal.
- Turn on deformation velocity handling for moving/deforming emitters.

Measured outcomes (live FLIP test network):
- Source vs sink mode at frame8 (same setup):
  - source: `17677` pts
  - sink: `17516` pts
- Boundary method sweep (source mode) produced measurable but subtle count differences in this setup:
  - none: `17652` pts
  - velocity: `17670` pts
  - pressure: `17662` pts

## Gotchas

- `flipboundary` is optional; only use when you need source/sink behavior.
- Keep source geometry placement consistent with intended fill direction and waterline semantics.
- Stream miswiring (0/1/2) can look like boundary failure even when node is correct.

## Companion Nodes

- `flipcontainer`
- `flipcollide`
- `flipsolver`

## Study Validation

- ✅ Read docs: `nodes/sop/flipboundary.txt`
- ✅ No official node example listing in current corpus
- ✅ Validated source/sink and boundary-mode behavior in live FLIP chain
