# Crowdmotionpathavoid (SOP)

## What This Node Is For

`crowdmotionpathavoid` Applies collision/avoidance filtering to crowd motion paths.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/crowdmotionpathavoid.txt`)
- Example set reviewed: yes (`examples/nodes/sop/crowdmotionpathavoid/MotionPathAvoidanceFiltering.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: based on node docs/example description and sticky-note guidance.
- Observed: official example `MotionPathAvoidanceFiltering` instantiated and cooked; representative display output was `4800 pts / 20 prims` at `apply_avoidance`.
- Mismatches: none observed in this pass.

## Minimum Repro Setup

- Example loaded: `/obj/academy_seq3_*_crowdmotionpathavoid` (instantiated one-by-one, then deleted before next node).
- Verification: asset installs, instantiates, and display network cooks without errors.

## Key Parameters and Interactions

- Primary behavior is driven by node-specific core parameters shown in the example network.
- Crowd/path nodes depend on stable clip libraries, agent definitions, and motion-path contracts.

## Gotchas and Failure Modes

- Legacy/alternative nodes (`cookie`, `copy`) can diverge from newer counterparts; verify intended tool variant.
- Crowd motion-path nodes are sensitive to clip naming/state graph consistency.

## Related Nodes

- `attribwrangle`
- `group`
- `merge`
