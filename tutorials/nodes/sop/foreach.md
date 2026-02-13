# For-Each Loop (SOP)

## What This Node Is For

For-each SOP workflows iterate over pieces or counts using `block_begin` + `block_end` to run the same node chain repeatedly, then gather results (merge or feedback).

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/block_begin.txt`, `help/nodes/sop/block_end.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/foreach/AttributeShuffle.txt`, `help/examples/nodes/sop/foreach/ForEachExamples.txt`)
- Example OTL internals inspected: yes (`AttributeShuffle.hda`, `ForEachExamples.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - `block_begin` defines loop source/mode (feedback, piece extraction, metadata).
  - `block_end` defines iteration mode and gather mode (feedback vs merge).
  - AttributeShuffle example warns about primitive ordering changes in merge loops.
- Observed (live scene/params/geometry):
  - `/obj/academy_AttributeShuffle/geo1` contains canonical `foreach_begin1 (block_begin)` + `foreach_end1 (block_end)` wiring.
  - Overridden loop controls match piece-loop pattern:
    - `foreach_begin1.method=1`, `foreach_begin1.blockpath=../foreach_end1`
    - `foreach_end1.itermethod=1`, `foreach_end1.method=1`, `foreach_end1.attrib=piece`, `templatepath=../foreach_begin1`
  - `probe_geometry` confirms looped output at `foreach_end1`: `576 pts, 288 prims`; post-processing `attribcopy1` reduces to `288 pts, 288 prims` while keeping `piece`/`Cd` semantics.
  - ForEachExamples includes one sticky note summarizing group/number/attribute loop methods.
- Mismatches:
  - In this build, two legacy `foreach` subnet branches in `ForEachExamples` return no probe geometry at subnet output (likely example wiring/context nuance), while AttributeShuffle block-based example validates cleanly.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_AttributeShuffle/geo1/attribcreate1 -> foreach_begin1 -> color1 -> foreach_end1 -> attribcopy1`
- Key parameter names and values:
  - `foreach_begin1.method=1` (Extract Piece or Point)
  - `foreach_end1.itermethod=1` (By Pieces)
  - `foreach_end1.method=1` (Merge Each Iteration)
  - `foreach_end1.attrib=piece`
- Output verification method:
  - `probe_geometry` on `foreach_end1` and downstream `attribcopy1`.

## Key Parameters and Interactions

- `block_begin.method` + `block_end.itermethod`: decide count-based vs piece-based iteration.
- `block_end.method`: feedback accumulation vs merge per iteration.
- `blockpath`/`templatepath`: explicit loop pairing and piece source wiring.
- `attrib` + `class`: piece identity source (string/int partition attrs by prim/point).

## Practical Use Cases

1. Per-piece procedural transforms/colors on fractured assets.
2. Iterative feedback effects (repeat smooth/deform/grow) with deterministic pass count.

## Gotchas and Failure Modes

- Missing/mis-set `blockpath` or `templatepath` silently breaks loop semantics.
- Merge loops can reorder primitive numbering; preserve IDs before/after if order matters.
- Legacy `foreach` subnet examples may not always expose geometry directly at outer subnet output for probe tools.

## Related Nodes

- `block_begin`
- `block_end`
- `connectivity`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
