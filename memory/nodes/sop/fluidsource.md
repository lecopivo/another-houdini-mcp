# Fluid Source (SOP)

## What This Node Is For

`fluidsource` rasterizes source geometry/attributes into simulation-ready volume fields (for example `density`, `temperature`, SDF-style fields, and optional noise-augmented sources).

## Session Status

- Status: deep-studied
- Docs read: partial (`nodes/sop/fluidsource.txt` not present locally; studied via examples + live behavior)
- Example sets reviewed: yes (`examples/nodes/sop/fluidsource/TorusVolume.txt`, `examples/nodes/sop/fluidsource/ColourAdvect.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (example docs + sticky notes):
  - Convert source geometry into fluid fields and feed custom fields (such as color channels) into pyro workflows.
  - In colour-advection workflow, alpha and color fields are built separately and composed in DOPs.
- Observed (live play):
  - **TorusVolume** (`/obj/academy_deep_fluidsource_torus/torus_object1/fluidsource1`):
    - Baseline output: 1 volume primitive named `density`, resolution `(79,19,79)`.
    - `divsize` strongly controls voxel resolution:
      - `0.2` -> `(42,11,42)`
      - `0.05` -> `(154,33,154)`
    - With `make_sdf=1`, voxel range became signed-like (`min ~-2.53`, `max ~-0.0001`), and `invert_sign=1` flipped sign range (`min ~-0.226`, `max ~2.044`).
  - **ColourAdvect**:
    - `colour_alpha` branch outputs `density` volume used as alpha-like mask.
    - merged output contains `density` plus `Cd.x/Cd.y/Cd.z` volumes.
    - `divsize` change on `colour_alpha` changed only `density` resolution (`(52,27,50)` -> `(99,49,96)`), while `Cd.*` stayed at `(10,5,10)` from separate color-volume path.
    - `smoke_source/create_density_volume` outputs both `density` and `temperature` volumes in this setup.
    - `use_noise` interaction:
      - `use_noise=1` produced stronger peaks (`max ~4.30`),
      - `use_noise=0` normalized to near-1 peak (`max ~0.998`).
    - `make_sdf=1` with noise off turned both fields negative SDF-like ranges.
- Mismatches: none.

## Minimum Repro Setup

- Use both examples:
  - `TorusVolume` for core rasterization controls.
  - `ColourAdvect` for multi-field production pattern (`density` + `Cd.*` + DOP composition).
- Validate with:
  - primitive `name` list,
  - per-volume resolution,
  - voxel min/max range checks for mode toggles.

## Key Parameter Interactions

- `divsize` is the primary fidelity/performance lever (resolution scales quickly).
- `make_sdf` and `invert_sign` change field semantics; downstream solvers/compositors must expect matching sign conventions.
- `use_noise` significantly changes source amplitude and source texture.
- In multi-branch setups, different fields may be authored at different resolutions; confirm intentionality before DOP sourcing.

## Gotchas and Failure Modes

- Missing local node-doc file requires example-first validation and explicit docs-status note.
- Mixed field resolutions (`density` vs `Cd.*`) can cause confusing behavior if assumed to be identical.
- Field naming is pipeline-critical in DOP sourcing; verify names (`density`, `temperature`, `Cd.x/y/z`) before blaming solver behavior.
