# Group Copy (SOP)

## What This Node Is For

`groupcopy` transfers point/primitive/edge/vertex groups from source geometry (input 2) onto destination geometry (input 1).

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/groupcopy.txt`)
- Example set reviewed: yes (`examples/nodes/sop/groupcopy/GroupCopyBox.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + example):
  - Copy source groups by index (or optionally by attribute), with conflict policies (`skip`, `overwrite`, `add suffix`).
- Observed (live play):
  - Baseline copy transferred source primitive group `group1` onto destination with expected size (`24` prims).
  - Prefix behavior:
    - `primnameprefix="src_"` renamed result to `src_group1` (same membership size).
  - Conflict-policy behavior (after creating existing `group1` on destination with 6 prims):
    - `skipgroup` -> output `group1` remained `6` (copied group skipped).
    - `overwrite` -> output `group1` became `24`.
    - `addsuffix` -> preserved destination `group1=6` and created copied `group12=24`.
  - Attribute-match toggle (`enablematchbyprimattrib=1`, attr `name`) in this setup did not change resulting copied membership, because geometry remained index-compatible and no explicit primitive attribute map was authored.
- Mismatches: none.

## Minimum Repro Setup

- Example network: `/obj/academy_deep_groupcopy/Group_Copy_SOP_Example`.
- Add a destination-side preexisting group before `groupcopy` to explicitly test name-conflict modes.

## Key Parameter Interactions

- Input roles are fixed:
  - input 1 = destination geometry that passes through,
  - input 2 = source groups provider.
- `primnameprefix` is useful for non-destructive namespace isolation.
- `groupnameconflict` is a high-impact safety control; pick deliberately.
- Attribute matching should only be enabled when both sides have valid, meaningful matching attributes.

## Gotchas and Failure Modes

- Most mistakes come from swapping mental model of input roles.
- Conflict mode defaults can silently keep old groups (`skip`) when users expect overwrite behavior.
- Enabling attribute matching without proper mapping attributes can lead to confusing or effectively unchanged results.
