# Rest Position (SOP)

## Intent

`rest` stores and manages rest-space attributes so shading/procedural effects can remain stable while geometry deforms.

## Core Behavior

- Primarily writes a point rest-position attribute (default `rest`) in Store mode.
- Can optionally write rest normals (`rnml`) and primitive transform rest attributes.
- Supports rest sourcing from input-1/reference geometry when topology matches.
- Mode controls (`store`, `extract`, `swap`) define whether rest data is written or applied back.

## Key Parameters

- `mode`: Store / Extract / Swap.
- `restattribname`: rest point-attribute name (blank disables rest-position write).
- `nml`, `normalattribname`: rest-normal generation controls.
- `xform` / `quadric` families: primitive transform rest metadata.
- `precision`: storage precision policy for generated attrs.

## Typical Workflow

```text
deforming geo (input0) + reference rest geo (input1 optional) -> rest -> shader/material
```

- Place before or alongside deformation depending on whether reference rest comes from same stream or second-input reference.
- Validate attribute presence (`rest`, optional `rnml`) before relying on shader behavior.

## Production Usage

- Common for procedural wood/noise/solid materials on deforming assets.
- Keep topology consistency strict between deforming and reference inputs.
- Treat rest-attribute naming as a shading contract.

Measured outcomes (`BasicRest` example):
- Baseline Store mode output (`rest1`): `100 pts / 1 prim`, point attrs `P` + `rest`.
- `restattribname=""` removed rest output attribute (point attrs became only `P`).
- Rest normals mode:
  - `nml=0` or `1`: attrs `P, rest` only in this setup,
  - `nml=2` (always): added `rnml`.
- Mode behavior in this example network/build:
  - `mode=store` cooked and probed normally,
  - `mode=extract` and `mode=swap` caused probe failure (`NoneType` geometry in probe path) on this example setup.

## Gotchas

- Do not assume Extract/Swap are safe on all legacy example setups; verify cook/probe behavior explicitly in current build.
- Blank rest attribute name silently disables the core contract.
- Rest normals behavior depends on mode and primitive context; verify `rnml` presence directly.

## Companion Nodes

- `twist` (or other deformers) to generate deformation that demonstrates shader sliding vs rest locking.
- `timeshift` for explicit rest-frame sourcing to input 1.
- `material`/shader assignment for visual verification.

## Study Validation

- ✅ Read docs: `nodes/sop/rest.txt`
- ✅ Reviewed example: `examples/nodes/sop/rest/BasicRest.txt`
- ✅ Inspected stickies and object-level companion setup (`shopnet/light/cam/material`)
- ✅ Ran live mode and attribute-contract tests on `rest1`
