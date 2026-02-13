# Extract Transform (SOP)

## What This Node Is For

`extracttransform` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/extracttransform.txt`)
- Example set reviewed: yes (`examples/nodes/sop/extracttransform/ExtractAnimatedTransform.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: extract output points carried transform attrs (`P`,`orient`,`pivot`,`name`).
- Live tweak: enabled `computedistortion`; added `distortion` point attribute while point count stayed 10.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- this node outputs transform metadata points, so attribute contract is primary output.
