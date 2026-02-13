# Copy to Points (SOP)

## What This Node Is For

`copytopoints` copies source geometry (input 0) onto destination/template points (input 1), with optional per-point transform and attribute-driven variation.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/copytopoints.txt`)
- Example set reviewed: yes (fallback via companion official example `help/examples/nodes/sop/copy/CopyTemplateAttribs.txt`)
- Example OTL internals inspected: yes (`CopyTemplateAttribs.otl` as related copy workflow)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes (fallback workflow used: docs + companion example + live repro)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Copy source geo to each target point.
  - Support orientation/scale/attribute transfer from target points.
  - `Pack and Instance` should switch from duplicated topology to packed-instance style output.
- Observed (live scene/params/geometry):
  - In `/obj/academy_copytopoints`, `box1 (8 pts, 6 prims)` copied to `grid1 (100 pts)` yields `800 pts, 600 prims`.
  - Enabling `copytopoints1.pack=1` changes output to packed-like representation: `100 pts, 100 prims, 100 verts`.
  - Related legacy example (`/obj/academy_CopyTemplateAttribs`) confirms template-attribute transfer pattern and includes explanatory sticky notes.
- Mismatches:
  - No behavioral mismatch found; only documentation/example mismatch (no node-scoped official `copytopoints` example folder in this local corpus).

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_copytopoints/box1 -> (0) copytopoints1 <- (1) grid1 -> output1`
- Key parameter names and values:
  - `copytopoints1.pack=0` (baseline), then `copytopoints1.pack=1`
  - `copytopoints1.transform=1` (default)
- Output verification method:
  - `probe_geometry` on `box1`, `grid1`, and `output1`.

## Key Parameters and Interactions

- `pack`: biggest topology/performance switch (full duplicate geo vs packed-instance style output).
- `transform`: enables orientation/transform usage from target point attrs.
- `targetgroup` and `sourcegroup`: cheap scope controls before adding heavier logic.
- `doattr` and attribute mapping fields (`setpt`, `mulpt`, etc.): target attribute propagation rules.

## Observed Behavior Snapshot

From `/obj/academy_copytopoints/output1`:

- `pack=0`: `points=800`, `prims=600`, `vertices=2400`
- `pack=1`: `points=100`, `prims=100`, `vertices=100`

Interpretation:
- With unpacked copies, topology scales by source topology x target point count.
- With packing enabled, output tracks one packed primitive per target point.

## Practical Use Cases

1. Scatter and instance props (rocks/plants/debris) onto terrain points.
2. Drive per-instance variation from point attributes (`pscale`, `orient`, custom attrs).

## Gotchas and Failure Modes

- Example corpus may provide legacy `copy` examples rather than direct `copytopoints` examples.
- Large target point counts can explode memory if `pack=0`.
- If copies ignore expected orientation/scale, verify template-point attrs and `transform` state first.

## Related Nodes

- `copy`
- `duplicate`
- `scatter`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
