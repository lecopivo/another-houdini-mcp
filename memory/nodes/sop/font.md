# Font (SOP)

## What This Node Is For

`font` generates text geometry from installed font files (Unicode-aware), with controls for primitive type, spacing, slant, alignment, and optional glyph metadata attributes.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/font.txt`)
- Example sets reviewed: yes (`examples/nodes/sop/font/FontBasic.txt`, `examples/nodes/sop/font/BubblyFont.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + stickies):
  - Support polygon, bezier, or mixed glyph generation; animate text/spacing/slant; optionally emit glyph-index attributes.
  - Mixed mode uses Bezier for curved glyphs and polygon for straight-only glyphs in examples.
- Observed (live play):
  - Primitive type impacts tessellation density:
    - `translate` node (`TRANSLATE`): `type=2` -> `206 pts`, `type=1` -> `172 pts` (same prim count).
  - `addattrib=1` adds primitive attrs `textsymbol` and `textindex` as documented.
  - Level-of-detail can massively change point count on curved glyphs:
    - text `OOOO`, `lod=0.05` -> `32 pts`
    - text `OOOO`, `lod=1.0` -> `416 pts`
  - Control-character text can generate empty output:
    - `characters` example node with control glyph string produced `0 pts`; setting text to `A` produced `12 pts`.
  - Oblique angle visibly alters glyph shape/bounds without changing topology in tested setup.
  - Example gotcha: some demo parameters are expression-driven (for animation), so manual value setting may appear ineffective unless expression behavior is accounted for.
- Mismatches: none.

## Minimum Repro Setup

- Use `FontBasic` for parameter-focused behavior and `BubblyFont` for mixed-style animated presentation patterns.
- Probe representative font nodes directly (not only downstream merges) after each parameter change.

## Key Parameter Interactions

- `type` and `lod` jointly control tessellation complexity and performance.
- `text` content (especially control characters/newline usage) can produce empty or multiline outputs.
- `addattrib` is critical when downstream needs stable glyph metadata mapping.
- Spacing/slant controls (`tracking*`, `oblique`) may be animated by expressions in examples; inspect expression state before concluding parameter edits failed.

## Gotchas and Failure Modes

- Empty text output is often valid (unsupported/control glyph), not a cook error.
- High `lod` on long curved text can explode point counts quickly.
- Example networks frequently use animated expressions (`$F`, sine/cosine); manual overrides require awareness of time-dependent parameter state.
