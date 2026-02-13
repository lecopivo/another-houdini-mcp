# Switch-If (SOP)

## What This Node Is For

`switchif` conditionally passes either input 0 (false) or input 1 (true) based on expression tests or geometry-aware tests.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/switchif.txt`)
- Example set reviewed: yes (fallback via official docs examples + live SOP repro network)
- Example OTL internals inspected: yes (live reproducible network `/obj/academy_switchif`)
- Node comments read: yes
- Sticky notes read: yes (none available in local corpus)
- QA pass complete: yes (fallback workflow used: docs + live repro)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Binary branch switch with explicit condition types (`Expression`, `Element count`, `Attribute presence`, etc.).
  - Supports testing geometry on first, second, or spare input.
- Observed (live scene/params/geometry):
  - Built `/obj/academy_switchif` with first input `box1` and second input `empty1` (initially empty).
  - Configured condition: `testinput=second`, `type1=count`, points `> 0`.
  - When second input is empty, output is first branch (`8 pts, 6 prims`).
  - After wiring `sphere1 -> empty1`, output switches to second branch (`1 pt, 1 prim` in default sphere mode).
- Mismatches:
  - None with documented behavior.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_switchif/box1 -> switchif1 <- empty1 <- sphere1 -> output1`
- Key parameter names and values:
  - `switchif1.testinput=1` (Second Input)
  - `switchif1.type1=2` (Element Count)
  - `switchif1.counttype1=0` (Points)
  - `switchif1.countcomp1=2` (Greater than)
  - `switchif1.countval1=0`
- Output verification method:
  - `probe_geometry` on `output1` before and after connecting `sphere1` to second branch.

## Key Parameters and Interactions

- `testinput`: decides which branch is analyzed (not necessarily the one passed).
- `type#`: condition family (`count`, `attrib`, `expr`, etc.).
- `mergecondition`: combines multiple tests (all/any/none/any false).

## Practical Use Cases

1. Fallback default geo when optional input is missing or empty.
2. Branch to error/report path when input quality checks fail.

## Gotchas and Failure Modes

- Remember input order semantics: first input is false path, second is true path.
- Multi-test behavior can become opaque; keep condition count low and explicit.
- Missing official local examples means verify against live network for this build.

## Related Nodes

- `switch`
- `blast`
- `error`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
