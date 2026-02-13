# DOP Import Records (SOP)

## What This Node Is For

`dopimportrecords` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/dopimportrecords.txt`)
- Example set reviewed: yes (`examples/nodes/sop/dopimportrecords/dopimportrecordsexample.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: `import_positions` branch output 11 points with many imported record attributes.
- Live tweak: changed `field` from `*` to `P`; point count stayed 11 but imported attribute set reduced to core ids + P.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- field filtering changes attribute payload, not necessarily geometry size.
