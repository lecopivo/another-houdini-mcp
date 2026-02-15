# Lattice from Volume (SOP)

## Intent

`latticefromvolume` converts active volume regions into lattice geometry (points/polyline/tet/hex) for deformation workflows, especially with `volumedeform`.

## Core Behavior

- Samples active voxels and emits lattice points with index attrs `ix/iy/iz` and `rest` positions.
- Output topology depends on `Output Type`:
  - points (fastest)
  - polyline (connectivity-aware)
  - tetrahedron/hexahedron (volumetric cell meshes)
- Can expand active region by voxel padding.
- Can sample and emit source volume values as point attrs.

## Key Parameters

- `group`: volume selection.
- `sampling`: center vs corner sampling.
- `expand`: active-region padding in voxels.
- `type`: points/polyline/tet/hex.
- `createattribs`: copy sampled volume values to point attrs.

## Typical Workflow

```text
volume/vdb -> latticefromvolume -> deform lattice -> volumedeform
```

- Generate lattice from same volume stream fed to `volumedeform`.
- Apply lattice-space deformations.
- Use `volumedeform` to transfer deformation back to volumes.

## Production Usage

- Use points mode for performance unless downstream deformer requires connectivity.
- Increase `expand` to ensure border behavior and avoid clipping deformation influence.
- Enable `createattribs` when solver/deformer needs sampled scalar fields on lattice points.

Measured outcomes (`PigLattice` + live validation):
- Example used `type=2` (tetrahedron), producing:
  - `12972` points, `54750` tetrahedra, attrs `ix/iy/iz/rest`.
- Output type sweep on same VDB:
  - points: `12972` pts, `0` prims
  - polyline: `12972` pts, `36803` polygon-line prims
  - tetrahedron: `12972` pts, `54750` tetra prims
  - hexahedron: `12972` pts, `10950` hexa prims
- Expand sweep (points mode):
  - `expand=0`: `9033` pts
  - `expand=1`: `12972` pts
  - `expand=2`: `17560` pts
- `createattribs=1` added sampled volume attr `surface`.

## Gotchas

- Without padding, lattice may miss boundary support needed for robust deforms.
- Some deformers assume connected topology; points-only output can appear to “do nothing” in those tools.
- Volume-attribute sampling changes with center/corner mode; verify expected semantics for downstream math.

## Companion Nodes

- `volumedeform`
- `volumerasterizelattice`
- deformer SOPs (`softtransform`, `bend`, etc.)

## Study Validation

- ✅ Read docs: `nodes/sop/latticefromvolume.txt`
- ✅ Reviewed example: `examples/nodes/sop/latticefromvolume/PigLattice.txt`
- ✅ Ran output-type, expand, and attribute-sampling sweeps with measured counts/attrs
