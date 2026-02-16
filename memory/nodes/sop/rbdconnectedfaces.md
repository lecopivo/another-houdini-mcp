# RBD Connected Faces (SOP)

## Intent

`rbdconnectedfaces` records opposite-face connectivity metadata on fractured interior faces (and can emit constraints) so downstream tools can detect/handle newly disconnected fracture regions.

## Core Behavior

- Searches for connected interior face counterparts and stores partner references.
- Can store linkage as primitive-level or vertex-level attributes.
- Optional face-name mode stores stable name-based linkage for index-changing pipelines.
- Can generate constraints between connected faces, with transfer/scaling options.

## Key Parameters

- Group filters: `group`, `interiorgroup`, target geometry selection.
- Mode: primitive vs vertex connected-face storage.
- Attribute names: face index/name and distance fields.
- Constraint generation: max constraints, keep/transfer behavior, strength/stiffness scaling.

## Typical Workflow

```text
fractured interior faces -> rbdconnectedfaces -> rbddisconnectedfaces / rbdbulletsolver constraints
```

- Capture connectivity before major topology/index-changing operations.
- Prefer face-name mode when merging/unpacking can reorder primitive numbers.

## Production Usage

- Useful in destruction pipelines to track whether previously adjacent interior faces have separated.
- `RBDConnectedFaces` example demonstrates paired usage with `rbddisconnectedfaces`.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Primitive-index-only linkage can become invalid after merge/unpack/reindex operations.
- Constraint transfer/scaling needs careful setup when generating multiple replacement links per pair.

## Companion Nodes

- `rbddisconnectedfaces` for separation detection.
- `rbdconstraintproperties`, `rbdbulletsolver` for simulation integration.

## Study Validation

- ✅ Read docs: `help/nodes/sop/rbdconnectedfaces.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/rbdconnectedfaces/RBDConnectedFaces.txt`
- ⏳ Live validation pending
