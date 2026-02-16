# RBD Bullet Solver (SOP)

## Intent

`rbdbulletsolver` runs rigid-body Bullet simulations through a SOP wrapper, combining pieces, constraints, collisions, forces, guiding, visualization, and output controls.

## Core Behavior

- Input contract: render/sim pieces (1), constraints (2), optional proxy sim geo (3), collisions (4), optional guiding geometry (5).
- Wraps Bullet DOP solve with SOP-friendly controls and editable force/solver hooks.
- Supports emission/replication, break-threshold logic, and guided simulation blending/release.
- Exposes rich debug visualizers and viewport inspector tooling for constraints/guide states.

## Key Parameters

- Simulation controls: world scale, time scale, global/bullet substeps, constraint iterations.
- Piece/collision properties: collision shape/padding, physical parameters, overwrite attrs.
- Constraint controls: break thresholds by mode, attribute updates, broken-constraint export.
- Guide controls: method (velocity vs target velocity), blend/release thresholds, neighbor logic.
- Output controls: impact data extraction and attribute transfer to geometry/proxy outputs.

## Typical Workflow

```text
packed pieces + constraints (+proxy/collision/guide) -> rbdbulletsolver -> unpack/deformpieces/render
```

- Ensure consistent `name` attribute typing before solve.
- Tune substeps/iterations and collision shape representation before advanced guiding.

## Production Usage

- Mainline SOP destruction solver for packed RBD pipelines with optional guide-driven choreography.
- `RBDBulletSolver` example set covers diverse use cases.
- `GuidedRBDBulletSolver` demonstrates guided-sim behavior.

Measured outcomes:
- Live Houdini simulation measurements are pending in this session.

## Gotchas

- Mixed point/primitive `name` attribute types can break or corrupt solver matching.
- World scale affects thresholds and VEX-space assumptions; custom logic must account for scaling.
- Guiding requires meaningful piece transforms/clusters; a single deforming mesh guide is insufficient without clustering.

## Companion Nodes

- `rbdconfigure`, `rbdconstraintsfromlines/curves/rules`, `rbdconstraintproperties`.
- `rbdguidesetup` for external guide preprocessing.
- `rbddeformpieces`, `rbdunpack` for post-sim reconstruction.

## Study Validation

- ✅ Read docs: `help/nodes/sop/rbdbulletsolver.txt`
- ✅ Reviewed examples: `help/examples/nodes/sop/rbdbulletsolver/RBDBulletSolver.txt`, `help/examples/nodes/sop/rbdbulletsolver/GuidedRBDBulletSolver.txt`
- ⏳ Live validation pending
