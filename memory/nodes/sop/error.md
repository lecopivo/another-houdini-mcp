# Error (SOP)

## What This Node Is For

`error` passes geometry through unchanged while emitting message/warning/error notices for validation and user feedback.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/error.txt`)
- Example set reviewed: yes (fallback via official docs examples + live repro)
- Example OTL internals inspected: yes (live reproducible network `/obj/academy_name_groups_error`)
- Node comments read: yes
- Sticky notes read: yes (none available in local corpus)
- QA pass complete: yes (fallback workflow used: docs + live repro)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Report notices from inside SOP/asset networks without modifying geometry.
  - Severity controls whether cooking continues.
- Observed (live scene/params/geometry):
  - In `/obj/academy_name_groups_error/error1`, with `enable1=1`, `errormsg1` set, and `severity1=1`, output geometry passes through unchanged and warning is reported.
  - Switching `severity1=2` causes downstream geometry probe to fail (cook-stopping error behavior).
  - Returning to `severity1=1` restores normal pass-through output.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_name_groups_error/groupsfromname1 -> error1 -> output1`
- Key parameter names and values:
  - `error1.errormsg1="Demo notice from Error SOP"`
  - `error1.enable1=1`
  - `error1.severity1=1|2`
- Output verification method:
  - `probe_geometry` and HOM `warnings()` checks.

## Key Parameters and Interactions

- `enable#`: gate each notice.
- `severity#`: message/warning/error behavior.
- `errormsg#`: user-facing diagnostics text.

## Practical Use Cases

1. Guard optional/invalid inputs in HDAs with clear feedback.
2. Stop downstream cooking only for unrecoverable states.

## Gotchas and Failure Modes

- Overusing error severity can make iterative authoring painful.
- Empty messages with enabled notices can be confusing to users.
- Local corpus lacks official node-scoped examples; validate in asset contexts.

## Related Nodes

- `switchif`
- `switch`
- `null`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
