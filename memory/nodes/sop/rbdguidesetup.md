# RBD Guide Setup (SOP)

## Intent

`rbdguidesetup` prepares guide-related attributes on packed RBD pieces (and optional constraints) for guided Bullet simulations.

## Core Behavior

- Assigns each sim piece to guide pieces by proximity (near point or near surface).
- Writes guide control attrs such as strength, blend, and neighbor data.
- Supports distance-based strength falloff and optional VEX-based attr customization.
- Can remove intra-guide constraints between differing guide clusters.

## Key Parameters

- Setup: group, start/end frame, guide assignment mode, max distance.
- Strength controls: base strength, distance-to-strength remap, blend attribute generation.
- Neighbor controls: seeded surface neighbor detection, min-neighbor thresholds, ensure-neighbor.
- Constraint filter/removal: remove inter-cluster constraints by group.

## Typical Workflow

```text
packed sim pieces + constraints + guide geometry -> rbdguidesetup -> rbdbulletsolver (guiding enabled)
```

- Capture guide assignment at a stable start frame.
- Validate guide clusters and neighbor counts before running long sims.

## Production Usage

- Used to choreograph fracture sims toward animated guide geometry while preserving breakaway behavior.
- `RBDGuideSetup` example demonstrates setup used with `rbdguide`/guided Bullet workflows.

Measured outcomes:
- Live Houdini simulation measurements are pending in this session.

## Gotchas

- Guide geometry must be decomposed into meaningful transformable pieces; a single deforming mesh guide is insufficient.
- Neighbor detection quality is sensitive to point seeding density and search radius.
- Over-aggressive intra-guide constraint removal can destabilize partially guided systems.

## Companion Nodes

- `rbdbulletsolver` (guide controls and release behavior).
- `rbdguide` DOP for lower-level guide behavior.

## Study Validation

- ✅ Read docs: `help/nodes/sop/rbdguidesetup.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/rbdguidesetup/RBDGuideSetup.txt`
- ⏳ Live validation pending
