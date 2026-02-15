# IsoOffset (SOP)

## Intent

Convert geometry to an implicit field and extract different representations from that field: polygonal iso shell, fog volume, signed distance field (SDF), or interior tetra/cube discretization.

## Core Behavior

- Builds an internal field from source geometry, then emits a chosen output contract.
- Supports both surface-style outputs and simulation-ready volume outputs.
- Tetra/cube branch enables volumetric discretization workflows (fracture-like or softbody prep).
- Sampling resolution strongly controls detail, stability, and cost.

## Key Parameters

- `output`: top-level mode switch (Iso Surface / Fog / SDF / Tetra Mesh).
- `mode`: field construction method (`Ray Intersect`, `Minimum`, point-cloud-like, implicit proxies, etc.).
- `samplediv` and `divsize`: primary resolution controls.
- `tetratype`: tetra/cube flavor when tetra branch is active.
- `offset`: iso extraction distance from original surface.
- `laserscan`, `fixsigns`, `forcebounds`: sign and robustness controls for SDF generation.

## Typical Workflow

```
source_geo -> isooffset -> OUT
```

- Pick `output` based on downstream consumer first.
- Set sampling density for required fidelity.
- For SDF/fog workflows, validate volume resolution and sign behavior.
- For tetra workflows, verify primitive class and counts before downstream assumptions.

## Production Usage

- For solver handoff, prefer SDF and verify sign quality (`fixsigns`/`forcebounds` as needed).
- For brick/tile looks, tetra/cube branch plus connectivity/primitive ops is effective (as in `Brickify`).
- For `mode=Minimum`, ensure positive `offset`; this mode is unsigned and zero offset can return empty iso output.

Measured outcomes:
- `output=0` iso surface -> polygon mesh (`128 pts / 128 prims` in live torus test).
- `output=1/2` fog/SDF -> single volume primitive (`1 prim`).
- `output=3` tetra branch + `samplediv=30`:
  - `tetratype=0`: dense polygonized tetra-style result (`21560` prims).
  - `tetratype=1`: true tetrahedra (`10144` `Tetrahedron` prims).
  - `tetratype=2`: cube-style polygon output (`22368` prims).
- `mode=Minimum, offset=0` -> empty output; `offset=0.05` -> valid shell (`1478 pts / 1536 prims`).
- SDF resolution scaled with sampling: `samplediv=20 -> (20,9,20)`, `samplediv=60 -> (60,23,60)`.

## Gotchas

- Empty results are often valid parameter outcomes, not cook errors.
- Fog and SDF can both appear as one primitive; inspect resolution/values instead of count-only checks.
- Coarse sampling can remove expected tetra content.

## Companion Nodes

- `connectivity`, `primitive`, `facet` in brick/tile post-processing chains.
- `volumevisualize` / visualizers for volumetric QA.
- `vdbfrompolygons` as modern alternative in many SDF pipelines when VDB workflows are preferred.

## Study Validation

- ✅ Read docs: `nodes/sop/isooffset.txt`
- ✅ Reviewed examples: `Brickify`, `SquabVolume`
- ✅ Probed output-mode contracts and tetra subtype behavior
- ✅ Verified `mode + offset` interaction and SDF resolution scaling
