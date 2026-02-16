# Stitch (SOP)

## Intent

`stitch` pulls adjacent curves/surfaces together to form smooth connected transition regions, useful for seam joining and fabric-like forms.

## Core Behavior

- Works on subsets or patterned primitive groups from input A (and optionally stitches to a surface in input B).
- Supports directional stitching with width, tangent shaping, and bias controls.
- Can wrap last-to-first to close loops.
- Can preserve one side more strongly via bias/fixed-side controls.

## Key Parameters

- `stitch` mode + `inc` (`N`): primitive pattern grouping.
- `wrap`: close-loop stitching behavior.
- `direction`, `tolerance`, `bias`: seam direction and deformation balance.
- `leftuv/rightuv`, `lrwidth`, `lrscale`: stitch placement and tangent profile shaping.
- `sharppartials`, `fixedintersection`: endpoint/seam behavior refinement.

## Typical Workflow

```text
curve/surface strips -> stitch -> cleanup/smooth/subdivide
```

- Select seam candidates precisely, then tune tolerance/bias before advanced tangent scaling.

## Production Usage

- Good for joining stair-stepped/grid-sliced surfaces and for cushioned/parachute-like seam effects.
- `StitchGrid` example shows grid duplication in staircase layout followed by stitch to connect layers.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Incorrect left/right primitive ordering can invert expected seam direction.
- Over-aggressive tangent/width scaling can produce self-overlap near seam ends.
- Pattern-based stitching (`N`) is sensitive to upstream primitive order changes.

## Companion Nodes

- `join`, `fillet`, `bridge` for alternative connection strategies.
- `align` for controlling left/right relationship before stitching.
- `smooth`/`subdivide` for post-seam relaxation.

## Study Validation

- ✅ Read docs: `help/nodes/sop/stitch.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/stitch/StitchGrid.txt`
- ⏳ Live validation pending
