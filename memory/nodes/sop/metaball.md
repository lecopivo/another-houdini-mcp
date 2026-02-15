# Metaball (SOP)

## Intent

`metaball` creates implicit blobby fields that merge, separate, or subtract based on overlap, weight, and kernel shape. It is used for organic forms, influence fields, and procedural field composition workflows.

## Core Behavior

- Outputs implicit metaball primitives (not polygon surfaces by default).
- Multiple metaballs interact when merged; overlapping fields blend to form a shared iso-surface.
- `metaweight` controls influence strength and supports negative values (subtractive/pusher behavior).
- `kernel` and exponent controls (`expxy`, `expz`) reshape field falloff and silhouette.

## Key Parameters

- Placement/size:
  - `tx/ty/tz`, `rx/ry/rz`, `radx/rady/radz`.
- Field strength and model:
  - `metaweight` (positive attract/additive, negative subtractive tendency).
  - `kernel` (`wyvill`, `blinn`, `elendt`, `hart`, etc.).
- Shape family:
  - `expxy`, `expz` for superquadric “squarish/starish” variations.
- Mode:
  - field-radius vs threshold-radius interpretation.

## Typical Workflow

```text
metaball(s) -> merge -> (optional metaExpression detail attr) -> convert -> downstream mesh workflow
```

- Build/position multiple metaballs and merge them for interaction.
- Use `convert` when downstream nodes require explicit polygon/NURBS geometry.
- For advanced composition, author detail string `metaExpression` to combine groups/primitives via `sum/max/min`.

## Production Usage

- Keep metaballs implicit during lookdev for flexibility; convert late for topology-dependent steps.
- Use negative/low weights for carving or local attenuation without extra boolean-style ops.
- Treat `kernel` and exponent changes as artistic shape controls that can significantly alter meshed output density.

Measured outcomes (`BlendMetaballs`, `MetaExpression`, and live `/obj/academy_metaball_live`):
- Overlap distance test (after convert to polygons): moving second metaball `tx 0.3 -> 1.5` increased overall X extent and reduced central blending continuity in counts/shape (`pts/prims 40/42 -> 48/52` for farther separation states).
- Weight interaction (`metaB` at `tx=0.6`):
  - `weight 0.5` -> `24 pts / 26 prims`
  - `weight 2.0` -> `40 pts / 42 prims`
  - `weight -1.0` -> `24 pts / 26 prims` with contracted combined extent.
- Kernel sweep (`metaweight=2.0`):
  - `wyvill`: `40/42`
  - `blinn`: `24/26`
  - `elendt`: `40/42` with larger Y/Z extent
  - `hart`: `40/42`.
- Superquadric exponent sweep on one metaball (`expxy=expz`):
  - `0.5` expanded silhouette (`40/42`, larger bbox)
  - `1.0` baseline (`40/42`)
  - `2.0` contracted/star-like behavior (`24/26`).
- Meta-expression composition (example `meta_expressions`, converted per expression):
  - `min("meta1","meta2")` -> `12/14`
  - `max("meta1","meta2")` -> `24/28`
  - `sum(0,1)` -> `32/34`
  - `sum(0,1,2,2,2,2,2,3,4)` -> `84/86`
  - `min(max("meta1","meta2"), max("meta3","meta4"))` -> `0/0` (empty result case).

## Gotchas

- Implicit metaball output can hide complexity until conversion; always validate post-convert counts/shape when pipeline depends on explicit mesh.
- `metaExpression` must be a detail string attribute named exactly `metaExpression`.
- Some expression combinations can yield empty output after conversion (valid but easy to misread as failure).
- Viewport level-of-detail strongly affects interactive appearance/perceived smoothness.

## Companion Nodes

- `merge` for field interaction.
- `convert` for polygonization.
- `metagroups` / attribute creation nodes for `metaExpression` authoring.
- `magnet` as a downstream consumer of metaball influence fields.

## Study Validation

- ✅ Read docs: `nodes/sop/metaball.txt`
- ✅ Reviewed examples: `examples/nodes/sop/metaball/BlendMetaballs.txt`, `examples/nodes/sop/metaball/MetaExpression.txt`
- ✅ Inspected stickies and companion nodes (`point`, `merge`, meta-expression attrib variants)
- ✅ Ran live overlap/weight/kernel/exponent tests and expression-driven conversion comparisons
