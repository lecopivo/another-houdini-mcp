# Output (SOP)

## What This Node Is For

`output` marks/controls explicit subnetwork outputs and output indices.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/output.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/output/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: make output contracts explicit and independent of temporary display flags.
- Observed: in `/obj/academy_output_live`, `outputidx` materially affects behavior; with `output1.outputidx=0` probe failed in this top-level test chain, restoring `outputidx=1` returned valid pass-through (`8 pts / 6 prims`).
- Mismatches: none, but top-level behavior confirms index sensitivity.

## Minimum Repro Setup

- Node graph: `/obj/academy_output_live/box1 -> output1 -> OUT_OUTPUT`
- Key parms: `outputidx`.
- Verification: `probe_geometry` after index changes.

## Key Parameters and Interactions

- `outputidx` should be treated as a stable API contract.
- Duplicate/misaligned indices can break parent extraction/object-merge expectations.

## Gotchas and Failure Modes

- Dynamic/index-expression usage is fragile; prefer explicit switch logic upstream.
- In multi-output subnetworks, undocumented index changes can silently break consumers.

## Related Nodes

- `subnet`
- `object_merge`
- `null`
