# MatchTopology (SOP)

## Intent

`matchtopology` remaps point/primitive numbering on one mesh to match a reference mesh with the same topology contract. It is mainly used to recover stable indexing after sorting/reordering so downstream attribute transfer, caching, or blend workflows line up.

## Core Behavior

- Input 0 is the scrambled target; input 1 is the reference numbering to match.
- Requires matching point/primitive/vertex counts between inputs.
- Solves component correspondence; ambiguous mappings produce warnings and highlighted regions.
- Optional tracking/reference point pairs disambiguate multiple valid matches.

## Key Parameters

- `trackpts` / `refpts`:
  - ordered correspondence hints from input 0 to input 1.
  - primary control for resolving ambiguous components.
- `assumeprimmatch`:
  - faster mode when only point order changed and primitive correspondence is already trusted.

## Typical Workflow

```text
reference_geo -> (copy/sim/sort scramble) -> matchtopology(scrambled, reference) -> index-stable downstream
```

- Keep a known-good reference branch untouched.
- If warnings report ambiguity, add a few robust point correspondences in `trackpts/refpts`.
- Re-check mapping by comparing per-point positions/attributes against reference indices.

## Production Usage

- Use immediately after any operation that reorders points/primitives but preserves underlying connectivity.
- For symmetric shapes, expect ambiguous mappings; always seed tracking points on asymmetric or landmark regions.
- Validate with a numeric check (for example RMS of `P` by point number) before relying on the remapped result.

Measured outcomes (`MatchTopologySphere` example + live `/obj/academy_matchtopology_live`):
- Example network (`sort_B`, `sort_C`) remapped to reference cleanly in shipped setup:
  - `sort_* vs ref` point-number RMS `~1.42419` before matching.
  - `matchtopology_* vs ref` RMS `0.0` after matching.
- Live ambiguity test on reordered polygon sphere (`162 pts / 320 prims`):
  - without tracking hints, `match_ok` produced warning `Connected components had ambiguous matches: they are highlighted.`
  - RMS remained high (`~1.414213`) despite successful cook.
- Disambiguation test:
  - setting `trackpts="44 2 71"` and `refpts="0 1 2"` resolved ambiguity,
  - RMS dropped to `0.0`, warnings cleared.
- Contract-failure test:
  - mismatched reference topology (different sphere frequency) raised errors:
    - `Reference and target geometry have different point counts.`
    - `Reference and target geometry have different primitive counts.`

## Gotchas

- Same counts do not guarantee a unique solution; symmetric components can still be ambiguous.
- A clean cook with warning can still be wrong for your intended mapping; inspect warnings and validate numerically.
- If topology really differs, node errors out (no valid output geometry).
- Vertex winding/order differences can break expected matches; docs suggest trying `reverse` when topologies appear identical but consistency checks fail.

## Companion Nodes

- `sort` for intentional point/primitive reordering tests.
- `reverse` when winding-order inconsistency blocks matching.
- `attribtransfer`/custom wrangles downstream that depend on stable point numbering.

## Study Validation

- ✅ Read docs: `nodes/sop/matchtopology.txt`
- ✅ Reviewed example: `examples/nodes/sop/matchtopology/MatchTopologySphere.txt`
- ✅ Inspected stickies and internal companion setup (`sort`, `matchtopology`, animated switch)
- ✅ Ran live ambiguity/disambiguation/failure tests in `/obj/academy_matchtopology_live`
