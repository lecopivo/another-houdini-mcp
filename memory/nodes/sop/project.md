# Project (SOP)

## Intent

`project` creates profile curves (curves-on-surface) by projecting input faces onto target surfaces. It is typically an authoring step before `profile`, `trim`, or `bridge` operations.

## Core Behavior

- Input 0 supplies projector faces/curves; input 1 supplies target surfaces.
- Projection can be vector-driven (`axis`/`vector`) or parametric-domain mapping.
- The node generally preserves owner-surface topology while embedding profile data on that surface.
- Downstream nodes (`profile`, `trim`) are usually required to expose/edit/use projected profiles explicitly.

## Key Parameters

- `axis`, `vector`, `projside`: projection direction and side selection contract.
- `cycle`: face/surface sequencing strategy when multiple projectors/surfaces are present.
- `sdivs`, `rtolerance`, `ftolerance`, `order`: profile fitting density/accuracy controls.
- `userange`, `urange1/2`, `vrange1/2`, `maptype`: parametric mapping domain controls.

## Typical Workflow

```text
projector curve/face + target surface -> project -> profile (extract/remap) and/or trim
```

- Author projection first, then validate resulting profile domain with `profile` extraction.
- Apply `trim` only after confirming profile placement and coverage.

## Production Usage

- Treat `project` as profile-authoring metadata step, not a direct topology-edit node.
- For robust QA, probe both owner-surface output and extracted profile output.
- Use non-symmetric projector placement during tests; symmetric setups can hide axis/side differences.

Measured outcomes (`ProjectCurve` + live `/obj/academy_project_live`):
- In official `ProjectCurve`, `project1` output remained surface-stable (`20 pts / 1 prim`), matching the owner-surface contract.
- Live validation with downstream `profile1` extraction showed strong direction sensitivity:
  - baseline (`axis=Z`): `284 pts / 3 prims` extracted profile,
  - `axis=user X`: `18 pts / 2 prims`, mean displacement vs baseline `0.974086`,
  - `axis=user XY`: `90 pts / 21 prims`, mean displacement `0.859498`.
- In this same setup, parametric range controls on `project` (`userange`, `urange*`, `vrange*`, `maptype`) did not change world-space extracted output under the tested projection mode (expected mode-sensitive behavior).

## Gotchas

- Counting points/primitives on `project` output alone can look "unchanged" even when profile data changed significantly.
- Symmetric test setups can falsely suggest `axis`/`projside` do nothing.
- Validate with `profile` extraction (or viewport profile display) before concluding projection parameters are inert.

## Companion Nodes

- `profile` for extraction/remap and direct curve-domain validation.
- `trim` for hole cutting after profile placement is confirmed.
- `primitive` for parametric profile transforms/reversals on owner surfaces.

## Study Validation

- ✅ Read docs: `nodes/sop/project.txt`
- ✅ Reviewed example: `examples/nodes/sop/project/ProjectCurve.txt`
- ✅ Inspected stickies and internal network (`circle -> project -> trim`)
- ✅ Ran live axis/vector/side tests with extracted-profile measurements in `/obj/academy_project_live`
