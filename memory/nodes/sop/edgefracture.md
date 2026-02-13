# Edge Fracture (SOP)

## What This Node Is For

`edgefracture` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/edgefracture.txt`)
- Example set reviewed: yes (`examples/nodes/sop/edgefracture/EdgeFracture.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: fracture example branch output 8641 pts / 14486 prims.
- Live tweak: increased `initialpieces` 50 -> 51 on first fracture stage; active display branch remained stable.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- multi-stage fracture setups can hide per-stage changes unless probing targeted stage nodes.
