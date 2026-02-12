# Lattice (SOP)

## What This Node Is For

`lattice` deforms incoming geometry using a cage-style control volume. You shape the cage, and the enclosed geometry follows smoothly.

## Practical Use Cases

- broad shape adjustment after modeling
- non-destructive secondary deformation pass
- art-directable silhouette changes before fine-detail operations

## Typical Workflow

1. Feed target geometry into `lattice`
2. Provide or generate a lattice cage around the geometry
3. Move cage control points to drive deformation
4. Add downstream cleanup if needed (normals/topology checks)

## Gotchas

- if the cage does not properly enclose the region, deformation can look incomplete or unstable
- very coarse cages produce smooth but low-control deformations
- dense/complex geometry can amplify small cage edits

## What To Verify In Examples

- how cage resolution affects control quality
- how local vs global cage edits propagate through the mesh
- interaction with downstream nodes (e.g., smoothing/remeshing)

## Related Nodes

- `bend`, `twist`, `bulge` for procedural single-mode deformations
- `edit` for direct point-level edits
- `latticefromvolume` for volume-driven lattice setup patterns
