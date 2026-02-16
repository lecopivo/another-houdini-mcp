# Skin (SOP)

## Intent

`skin` builds surfaces between one or more input cross-section curves (or between two cross-section sets), supporting mixed curve types and multiple assembly modes.

## Core Behavior

- One-input mode skins across ordered curves in input 0.
- Two-input mode performs bilinear-style skinning between U and V cross-section sets.
- Can work with mixed curve types and mismatched point counts.
- `skinops` + `inc` can assemble grouped subsets of curves for patterned surface creation.

## Key Parameters

- `keepshape`: preserve cross-section fidelity vs smoother interpolation.
- `surftype`: output connectivity style.
- `skinops`, `inc`: grouping/stride selection behavior for multi-curve sets.
- `prim`: keep source primitives in output.

## Typical Workflow

```text
cross-section curves (one or two sets) -> skin -> optional transform/shading/cleanup
```

- Ensure curve order and orientation are intentional before skinning.
- Use grouped/stride skin modes for procedural pattern surfaces.

## Production Usage

- Strong for lofted hulls, transitional shells, and patch-style curve networks.
- Use one-input for fast loft chains; two-input for guided U/V boundary interpolation.

Measured outcomes (`SkinBasic` + `SkinCurves`):
- `SkinBasic/one_input/skin1` baseline: `70 pts / 1 prim`.
  - `keepshape 1 -> 0` reduced output to `50 pts / 1 prim` (smoother/less strict section preservation).
  - `prim 0 -> 1` kept sources, increasing output to `120 pts / 6 prims`.
- `SkinBasic/two_inputs/skin2` baseline: `338 pts / 1 prim` with mixed NURBS+polygon inputs (stable output contract across tested connectivity toggles in this setup).
- `SkinCurves/Nurbs/skin14` grouped mode behavior:
  - `skinops=Groups of N`, `N=1/2/3` produced `6/3/2` prims respectively (`122/30/39` points),
  - `skinops` default collapsed to a single-surface style output (`42 pts / 1 prim`).

## Gotchas

- Curve order/orientation mismatches can create twisted or unintuitive skins.
- Grouped skin modes (`skinops`, `inc`) can radically alter primitive count from identical curve inputs.
- `prim=1` appends source curves, which can confuse downstream nodes expecting only skinned surfaces.

## Companion Nodes

- `copy` for procedural one-input section stacks.
- `delete` for selecting boundary subsets in multi-curve two-input setups.
- `rails` as an alternate frame-generation strategy before `skin`.

## Study Validation

- ✅ Read docs: `nodes/sop/skin.txt`
- ✅ Reviewed examples: `examples/nodes/sop/skin/SkinBasic.txt`, `examples/nodes/sop/skin/SkinCurves.txt`
- ✅ Inspected one-input, two-input, grouped-N, circular, and triangular companion branches
- ✅ Ran live keepshape/grouping/keep-prims/connectivity tests with measured topology outcomes
