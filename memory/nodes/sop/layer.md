# Layer (SOP)

## Intent

`layer` switches/defines active attribute layers so downstream SOPs can write/read parallel attribute sets (classically multiple UV/texture layers) without overwriting base-layer data.

## Core Behavior

- Sets layer context metadata on geometry via detail attributes (notably `layercount`, `currentlayer`).
- Downstream layer-aware nodes (for example UV assignment and layered shading workflows) interpret standard attribute names (`uv`, `Cd`, etc.) in the active layer context.
- Enables multi-layer shading pipelines where each layer maps to different texture/procedural inputs.

## Key Parameters

- `layer`: active layer index.

## Typical Workflow

```text
base geo -> uv/project (layer 1) -> layer (set 2) -> uv/project (layer 2) -> layered shader
```

- Author first UV/attribute layer.
- Switch to layer 2+ before creating additional UV/attribute sets.
- Use layered shader/material that reads corresponding layer channels.

## Production Usage

- Keep layer transitions explicit near each layer-writing operation.
- Validate detail attrs (`layercount`, `currentlayer`) in debug passes.
- Prefer consistent layer-index conventions across asset/shader teams.

Measured outcomes (`MultiTexture`, `MultiUV` examples):
- `layer` node introduced detail attrs `layercount` and `currentlayer`.
- In `MultiTexture`, `layer=2` produced `layercount=2/currentlayer=2` before second UV projection.
- Layer parameter sweep changed metadata contract:
  - `layer=1` -> `layercount=1/currentlayer=1`
  - `layer=2` -> `layercount=2/currentlayer=2`
  - `layer=3` -> `layercount=3/currentlayer=3`
- `MultiUV` example demonstrated layered primitive attrs (for example `Alpha2`) and layered UV assignment pipeline.

## Gotchas

- Node-level geometry probes may still show a single visible `uv` attribute name; layered handling relies on layer metadata and layer-aware consumers.
- Missing/incorrect layer switches can silently overwrite intended layer-specific texture coordinates.
- Official SOP node help file for `layer` is not present in the current local docs corpus; examples and in-scene behavior become primary references.

## Companion Nodes

- UV nodes (`uvproject`, `texture`)
- Material/shader nodes supporting layered channels
- legacy layered-surface shader workflows shown in examples

## Study Validation

- ✅ Reviewed examples: `MultiTexture`, `MultiUV`
- ✅ Inspected layer metadata behavior and layer-index sweeps
- ✅ Captured docs-corpus gap (no `nodes/sop/layer.txt` in local help)
