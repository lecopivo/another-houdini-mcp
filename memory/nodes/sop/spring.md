# Spring (SOP)

## Intent

`spring` performs lightweight point-mass spring simulation on SOP geometry, using primitive edges as spring constraints plus external/wind/turbulence forces.

## Core Behavior

- Uses input topology as the spring graph; points are the simulated masses.
- Fixed-point groups constrain anchor points and are critical for hanging/flag-style setups.
- Time evaluation depends on simulation state (`timestart`, `timeinc`) and frame progression.
- Point attributes such as `v` are produced/updated during simulation.

## Key Parameters

- `fixed`: anchor group that should not move.
- `external*`, `wind*`, `turb*`, `period`, `seed`: driving forces.
- `mass`, `drag`, `springk`, `tension`: physical response controls.
- `timeinc`, `accurate`: integration quality/stability controls.

## Typical Workflow

```text
grid/mesh -> group (fixed anchors) -> spring -> downstream render/deform
```

- Define anchor points first and verify group membership.
- Reset to start frame before comparing parameter sweeps to avoid stale-sim interpretation.

## Production Usage

- Effective for fast secondary motion (flags, simple cloth-like flutter, wires) where full DOP setup is unnecessary.
- Use `fixed` anchors to preserve attachment constraints.
- Tune large-scale behavior first (`external`, `wind`, `springk`), then add turbulence/detail.

Measured outcomes (`SpringFlag` + live parameter sweeps):
- Example anchor group contained `6` fixed points (`0,10,40,50,80,90`).
- Baseline at frame 24 vs source grid: `94/100` points moved, `0` fixed points moved, max displacement `0.447441`.
- Disabling anchors (`fixed=""`) moved all points (`100/100`) including all fixed-set points (`6/6`), max displacement rose to `0.500971`.
- Force sensitivity:
  - `windx 0.0 -> 2.0 -> 5.0` increased max displacement `0.421049 -> 0.447441 -> 0.936869`.
  - `externaly -0.2 -> -1.2` increased max displacement `0.911086 -> 1.020278`.
- Stiffness sensitivity:
  - `springk 20 -> 100 -> 300` changed max displacement `1.078473 -> 1.020278 -> 0.650146` (stiffer reduced motion amplitude in tested range).

## Gotchas

- Parameter changes can appear ineffective if you do not reset/re-evaluate from start frame.
- Missing or incorrect `fixed` group silently turns anchored setups into free-fall/floating cloth behavior.
- `springk`, `mass`, and `drag` are strongly coupled; tune with consistent force settings for meaningful comparisons.

## Companion Nodes

- `group` for fixed-anchor definition.
- `force` when adding metaball-driven attraction/repulsion via third input.
- `project`/`profile` in flag-style examples where profile motion follows spring-deformed hosts.

## Study Validation

- ✅ Read docs: `nodes/sop/spring.txt`
- ✅ Reviewed example: `examples/nodes/sop/spring/SpringFlag.txt`
- ✅ Inspected stickies and internal network (`grid -> group -> spring`)
- ✅ Ran live force/anchor/stiffness tests with frame-reset evaluation
