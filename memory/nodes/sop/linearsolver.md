# LinearSolver (SOP)

## Intent

`linearsolver` solves linear algebra problems on geometry-encoded matrices/vectors (solve, decompose, multiply) and writes results back as attributes. It is a core utility node for geometry-processing methods such as Laplacian solves, Poisson problems, and deformation systems.

## Core Behavior

- Reads matrix/vector data from point/prim/detail/volume encodings (dense or sparse) and computes output vectors/decompositions.
- `mode` changes operation contract: solve, decompose, solve-with-decomposition, or multiply.
- Output is usually attribute-based (for example point scalar/vector attribute), not geometry-topology generation.
- Supports pinned unknown entries via `pinnedgroup` (column/row reduction behavior).

## Key Parameters

- Operation:
  - `mode`: `Linear System Solve`, `Decompose`, `Solve with Decomposition`, `Multiply`.
- Solver selection:
  - `useiterativesolver`: iterative vs direct solve path.
  - `iterativesolver` / direct solver controls: choose algorithm family.
  - `solvertolerance`, `solvermaxiter`: convergence controls.
- Matrix contract:
  - `matrixstorage`, encoding parameters, row/col/value attrs.
  - shape controls (`squarematrix`, `rows`, `cols`).
- Vector contract:
  - `vectorsrcattr`: RHS/known vector input attr.
  - `vectordstattr`: result attribute name.
  - `pinnedgroup`, `reducerows`: constrained solve behavior.

## Typical Workflow

```text
matrix + rhs attrs -> linearsolver -> solution attr -> downstream deformation/update
```

- Build/validate matrix and RHS attributes first.
- Configure storage/encoding to match how attributes are authored.
- Solve into explicit destination attr (for example `z`, `deltaP`, `x`).
- Consume the solved field in wrangle/VOP/deformation nodes.

## Production Usage

- Treat matrix/vector attribute naming as a strict interface contract between upstream assembly nodes and `linearsolver`.
- Start with robust direct solves for small/medium systems; switch to iterative for larger sparse systems or when memory is a concern.
- Keep pinned-boundary semantics explicit (`pinnedgroup`, row/col reduction policy) and validate resulting field ranges.

Measured outcomes (`CurveInflation` example, node `/obj/academy_CurveInflation/solve`):
- Baseline output (`mode=solve`) produced `8184 pts / 15407 prims` and solved point attr `z` with range `0.0 .. 0.562163` (mean `0.172899`).
- Solver family comparison on this setup:
  - iterative baseline and direct solve produced matching sampled `z` stats in this build.
  - lowering `solvermaxiter` to `1` remained unchanged for this case (likely easy convergence/problem scaling).
- Constraint interaction test:
  - clearing `pinnedgroup` changed solved field materially (`z max 0.562163 -> 0.730753`, mean `0.172899 -> 0.287632`) while topology stayed constant.
- Output-attribute contract test:
  - renaming `vectordstattr` from `z` to `z_alt` moved the solution to `z_alt` and removed `z` from output attrs.
- Mode contract test:
  - `mode=Decompose` removed solved destination attr `z` from output in this network, while `Solve` and `Multiply` modes kept `z`.

## Gotchas

- Solver success does not guarantee semantically correct setup; wrong encoding/storage attrs can yield plausible but incorrect numbers.
- Missing or incorrect `pinnedgroup` changes boundary-condition behavior dramatically.
- Downstream nodes may silently fail if they expect a specific destination attr name and `vectordstattr` is changed.
- Mode switches can drop/replace expected solution attrs; validate attribute presence after changing `mode`.

## Companion Nodes

- `laplacian` for matrix assembly in smoothing/diffusion systems.
- `attribwrangle` for matrix/RHS construction and post-solve application.
- `measure`/boundary-group tools for deriving constraints in Poisson-style workflows.

## Study Validation

- ✅ Read docs: `nodes/sop/linearsolver.txt`
- ✅ Reviewed example: `examples/nodes/sop/linearsolver/CurveInflation.txt`
- ✅ Inspected network stickies/comments and companion assembly path in `CurveInflation`
- ✅ Ran live solver/mode/contract parameter tests with measured output-field deltas
