# Boolean (SOP)

## What This Node Is For

`boolean::2.0` combines two polygonal inputs using union/intersect/subtract/shatter/seam/custom/detect/resolve operations.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/boolean.txt`)
- Example set reviewed: yes (fallback via companion official examples: `help/examples/nodes/sop/foreach/cheese.txt`, `help/examples/nodes/sop/surfsect/SurfsectBasic.txt`)
- Example OTL internals inspected: yes (companion OTLs `cheese.otl`, `SurfsectBasic.otl`)
- Node comments read: yes
- Sticky notes read: yes (none available in local example corpus for this node)
- QA pass complete: yes (fallback workflow used: docs + companion examples + live repro)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Perform robust polygon booleans across solid/surface assumptions.
  - Support classic operations plus custom-depth, seam extraction, and detect/debug modes.
  - Emphasize clean solids and stable seam handling.
- Observed (live scene/params/geometry):
  - Built `/obj/academy_boolean` with overlapping boxes and `boolean::2.0`.
  - With `xformB.tx=0.8`, menu mapping confirms:
    - `booleanop=0` Union
    - `booleanop=1` Intersect
    - `booleanop=2` Subtract
  - Geometry probes + bbox checks:
    - Union (`op=0`): `16 pts, 14 prims`, bbox `1.800 x 1.000 x 1.000`
    - Intersect (`op=1`): `8 pts, 6 prims`, bbox `0.200 x 1.000 x 1.000`
    - Subtract (`op=2`): `8 pts, 6 prims`, bbox `0.800 x 1.000 x 1.000`
  - Companion official examples show boolean-style workflows in-context:
    - `/obj/academy_cheese/Cheese/foreach1/cookie1` (`boolop=3`) inside a foreach loop.
    - `/obj/academy_SurfsectBasic/example/surfsect1` (`boolop=2`) demonstrating subtract-style surface boolean behavior.
- Mismatches:
  - No operational mismatch found in tested union/intersect/subtract subset.
  - Direct node-scoped boolean examples are missing in the local corpus; companion examples use `cookie`/`surfsect` boolean operations.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_boolean/boxA -> boolean1 <- xformB <- boxB -> output1`
- Key parameter names and values:
  - `xformB.tx=0.8`
  - `boolean1.booleanop=0|1|2`
  - `boolean1.subtractchoices=1` (tested, no topology change in this symmetric box setup)
- Output verification method:
  - `probe_geometry` on `output1` and HOM bbox checks.

## Key Parameters and Interactions

- `booleanop`: primary mode switch.
- `asurface`/`bsurface`: solid vs surface interpretation.
- `subtractchoices`: which side of subtraction to output.
- `detriangulate`, `collapsetinyedges`, `lengththreshold`: output cleanliness and seam tolerance controls.

## Practical Use Cases

1. Hard-surface cutouts (A-B) for paneling and mechanical detail.
2. Intersection/seam extraction for procedural contact lines and masks.

## Gotchas and Failure Modes

- Ambiguous/dirty solids (non-manifold/inverted normals) can produce confusing results.
- Tiny near-coincident edges can create micro-polys; tune seam-collapse settings when needed.
- Primitive counts alone can be misleading; confirm bbox/shape semantics per operation.

## Related Nodes

- `booleanfracture`
- `clip`
- `polycut`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
