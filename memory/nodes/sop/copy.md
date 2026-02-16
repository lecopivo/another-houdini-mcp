# Copy (SOP)

## What This Node Is For

`copy` Copies geometry to templates with transform/attribute inheritance.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/copy.txt`)
- Example set reviewed: yes (`examples/nodes/sop/copy/CopyAttributes.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: based on node docs/example description and sticky-note guidance.
- Observed: official example `CopyAttributes` instantiated and cooked; representative display output was `12 pts / 20 prims` at `point1`.
- Mismatches: none observed in this pass.

## Minimum Repro Setup

- Example loaded: `/obj/academy_seq3_*_copy` (instantiated one-by-one, then deleted before next node).
- Verification: asset installs, instantiates, and display network cooks without errors.

## Key Parameters and Interactions

- Primary behavior is driven by node-specific core parameters shown in the example network.
- Crowd/path nodes depend on stable clip libraries, agent definitions, and motion-path contracts.

## Gotchas and Failure Modes

- Legacy/alternative nodes (`cookie`, `copy`) can diverge from newer counterparts; verify intended tool variant.
- Crowd motion-path nodes are sensitive to clip naming/state graph consistency.

## Companion Finding (from PolyPatch study)

- Legacy `copy` can still be an effective procedural scaffold generator: applying per-copy translate/rotate in copy count mode (`ncy`, pivot offsets, incremental rotation) builds stable helical guide curves for downstream surface nodes like `polypatch`.
- This pattern is useful when you need deterministic repeated transforms before modern instancing/copy-to-points stages.

## Companion Finding (from Rails study)

- `copy` remains a practical rail-pair generator: duplicating one rail with count mode (`ncy=2`) and mirrored scale (`sx=-1`) quickly builds symmetric dual rails for `rails`/`skin` workflows without manual second-curve authoring.

## Companion Finding (from SkinBasic study)

- Legacy `copy` is also an efficient cross-section stack builder before `skin`: repeated translate/rotate offsets on a single profile create ordered section sets that `skin` can loft into complex one-input forms with controllable taper/twist.

## Related Nodes

- `attribwrangle`
- `group`
- `merge`
