# Laplacian (SOP)

## Intent

`laplacian` builds a discrete Laplacian matrix (and optional mass/diffusion forms) for mesh processing workflows, typically solved with `linearsolver`.

## Core Behavior

- Outputs sparse matrix rows as point attributes (`col`, `value`) in LIL row-major style.
- Optional diffusion form outputs `I + tL` (or `M + tML` with separate mass).
- `Separate Mass` can produce symmetric systems for efficient solvers.
- Supports multiple Laplacian definitions (Cotan, Mean Value, Wachspress, Tutte).

## Key Parameters

- `mode`: Laplacian definition.
- `separatemass`: output/retain mass matrix separately for symmetric solve form.
- `diffusion` + `diffusioncoeff`: emit diffusion matrix and control step size.
- `epsilon`: numerical robustness for degenerate cases.
- output attr names: `colattrib`, `valueattrib`, `massattrib`.

## Typical Workflow

```text
mesh -> laplacian -> linearsolver -> updated attribute (often P)
```

- Build matrix with desired Laplacian mode.
- Solve for target vector (`P`, or custom RHS) in `linearsolver`.
- Iterate for smoothing/diffusion effects.

## Production Usage

- Default to Cotan for most geometry-processing tasks.
- Prefer symmetric forms (with separate mass) when solver supports them.
- Keep diffusion coefficient conservative for explicit/forward-style updates.

Measured outcomes (`LaplacianSmoothing` example):
- Forward Euler branch (`I+tL` solve on `P`) and backward branch (`M+tML` style via RHS mass handling) both produced smoothed geometry.
- Forward coefficient sensitivity (100 iterations) showed instability growth:
  - `t=0.0001` stable shrink (`max |P| ~0.4998`)
  - `t=0.01` overshoot (`max |P| ~0.657`)
  - `t=0.05` severe expansion (`max |P| ~2.3475`)
- Backward branch tolerated larger magnitude steps and remained numerically stable in tested range:
  - `t=-0.01` strong smoothing (`max |P| ~0.2382`)
  - `t=-0.05` collapsed near origin (`max |P| ~0.0`) without NaN/Inf.

## Gotchas

- Large forward diffusion steps can diverge quickly even when solves succeed numerically.
- Matrix construction and solver interpretation must agree on storage/encoding settings.
- Triangular meshes are generally faster for some Laplacian formulations.

## Companion Nodes

- `linearsolver`
- `attribwrangle` (RHS setup)
- remesh/triangulation preprocessors for solver robustness

## Study Validation

- ✅ Read docs: `nodes/sop/laplacian.txt`
- ✅ Reviewed example: `examples/nodes/sop/laplacian/LaplacianSmoothing.txt`
- ✅ Inspected forward/backward Euler branches and solver settings
- ✅ Performed diffusion-coefficient sweeps with measured stability outcomes
