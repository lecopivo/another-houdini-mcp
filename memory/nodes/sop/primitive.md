# Primitive (SOP)

## What This Node Is For

`primitive` edits primitive transforms/properties and writes primitive-level attributes such as `Cd`, alpha, crease, and volume metadata.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/primitive.txt`)
- Example set reviewed: yes (`examples/nodes/sop/primitive/PrimitiveColors.txt`)
- Example OTL internals inspected: yes (`PrimitiveColors.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: perform per-primitive property edits and template-relative operations.
- Observed:
  - Live repro `/obj/academy_primitive_live`: enabling color write (`doclr=1`, RGB set) added primitive `Cd`.
  - Official example `/obj/academy_PrimitiveColors` confirms `rand($PR+...)` and `prim()`-driven cross-node primitive color workflows.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_primitive_live/box1 -> primitive1 -> OUT_PRIMITIVE`
- Key parms: `doclr`, `diffr/diffg/diffb`, transform toggles, volume/VDB sections when needed.
- Verification: `probe_geometry` primitive attribute list includes `Cd`.

## Key Parameters and Interactions

- Attribute toggles (`doclr`, etc.) must be enabled before values are authored.
- Node is primitive-centric; class mismatch with downstream point ops is common.
- Volume/VDB sections make this node useful outside polygon-only pipelines.

## Gotchas and Failure Modes

- Confusing primitive vs point color can hide intended results.
- Local variables/expressions are primitive-index dependent; topology changes alter outcomes.

## Related Nodes

- `point`
- `vertex`
- `xform`
