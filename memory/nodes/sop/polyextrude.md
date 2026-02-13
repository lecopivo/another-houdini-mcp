# Poly Extrude (SOP)

## What This Node Is For

`polyextrude` extrudes polygon faces or edges to create thickness, side walls, and controlled shape changes (distance, inset, twist, divisions, and front transforms).

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/polyextrude.txt`, legacy `help/nodes/sop/polyextrude-.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/polyextrude/PolyextrudeTube.txt`)
- Example OTL internals inspected: yes (`PolyextrudeTube.hda`)
- Node comments read: yes
- Sticky notes read: yes (none present in this example)
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Extrude faces/edges with distance + inset + twist controls.
  - Support global and local-style control patterns.
  - Example asset contrasts global-style and local-style polyextrude setups.
- Observed (live scene/params/geometry):
  - `PolyextrudeTube` contains two object branches (`global`, `local`) each driven by `polyextrude::2.0`.
  - Global branch primarily uses distance/inset with front transform disabled.
  - Local branch enables front transform and non-uniform front scaling.
  - No sticky-note/post-it items were present in this example network.
- Mismatches:
  - None found; example behavior matched docs/comments.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_polyextrude/grid1 -> polyextrude1 -> output1`
- Key parameter names and values:
  - `grid1.rows=5`, `grid1.cols=5`
  - `polyextrude1.dist=0.5`
  - `polyextrude1.inset=0.2`
  - `polyextrude1.divs=4`
  - `polyextrude1.outputfront=0` (for cap-removal check)
- Output verification method:
  - Live HOM geometry probes (point/prim counts + bbox size deltas).

## Key Parameters and Interactions

- `dist`: primary extrusion distance.
- `inset`: shrinks/expands extrusion front for face extrusions.
- `divs`: adds rows along extrusion side walls.
- `outputfront` / `outputback` / `outputside`: control cap/side generation.
- `xformfront` + `scale*`/`rotate*`/`translate*`: additional front transform after base extrusion.
- `group` + split controls: scope and partition how components are extruded.

## Observed Behavior Snapshot

From `/obj/academy_polyextrude/polyextrude1`:

- `baseline`: `points=25`, `prims=16`, `size=(10.000,0.000,10.000)`
- `dist=0.5`: `points=41`, `prims=32`, `size=(10.000,0.500,10.000)`
- `dist=0.5,inset=0.2`: `points=41`, `prims=32`, `size=(10.000,0.500,10.000)`
- `divs=4`: `points=89`, `prims=80`, `size=(10.000,0.500,10.000)`
- `outputfront=0`: `points=80`, `prims=64`, `size=(10.000,0.500,10.000)`

Interpretation:
- Distance and divisions materially change topology.
- Inset changed face shape but not the overall bbox in this case.
- Disabling front cap reduced primitive count as expected.

## Example OTL Inspection Notes

`/obj/academy_PolyextrudeTube`:

- `global/polyextrude1` observed overrides:
  - `dist=0.8`, `inset=0.322`, `xformfront=0`
- `local/polyextrude1` observed overrides:
  - `extrusionmode=1`, `dist=1.0`, `inset=0.35`, `xformfront=1`, `scaley=0.75`
- Node comments explicitly describe global vs local control intent.
- Sticky notes: none found.

## Practical Use Cases

1. Add thickness and side walls to hard-surface panels.
2. Create stylized profile changes on selected face/edge groups.

## Gotchas and Failure Modes

- Parameter names differ between legacy/newer variants (`dist` vs old translate fields), so inspect live parms before setting.
- `inset` may visually change profile without changing bbox size; rely on topology and visual checks, not bbox alone.
- Group/split settings can merge or separate extrusion regions in non-obvious ways.

## Related Nodes

- `extrude`
- `polybridge`
- `peak`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
