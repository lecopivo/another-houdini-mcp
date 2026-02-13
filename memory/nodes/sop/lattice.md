# Lattice (SOP)

## What This Node Is For

`lattice` deforms incoming geometry using a cage-style control volume. You shape the cage, and the enclosed geometry follows smoothly.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/lattice.txt`)
- Example set notes reviewed: yes (`BallBounce`, `DeformLattice`, `LatticePerChunk`)
- Hands-on SOP test: yes (custom network at `/obj/academy_lattice`)
- Example OTL internals inspected in Houdini: yes

## Practical Use Cases

- broad shape adjustment after modeling
- non-destructive secondary deformation pass
- art-directable silhouette changes before fine-detail operations

## Typical Workflow

1. Feed target geometry into `lattice`
2. Provide or generate a lattice cage around the geometry
3. Move cage control points to drive deformation
4. Add downstream cleanup if needed (normals/topology checks)

## First Practical Setup (Observed)

Network used:

- `source_sphere` -> input 0 of `lattice1`
- `rest_cage` (`bound` from `source_sphere`) -> input 1 of `lattice1`
- `deformed_cage` (`xform` from `rest_cage`) -> input 2 of `lattice1`
- `lattice1` -> `OUT` (`outputidx = 0`)

Parameters used:

- `rest_cage.dodivs = 1`
- `rest_cage.divsx/divsy/divsz = 3/3/3`
- `lattice1.divsx/divsy/divsz = 3/3/3`
- `deformed_cage.ty = 0.35`
- `deformed_cage.sx/sy/sz = 1.2/0.8/1.2`
- `source_sphere` primitive type switched to polygon

Observed output change:

- Source bbox: min `(-1.000, -0.951, -1.000)`, max `(1.000, 0.951, 1.000)`
- Lattice output bbox: min `(-1.200, -0.411, -1.200)`, max `(1.200, 1.111, 1.200)`

This confirms the cage transform is driving the source deformation.

## Example OTL Inspection Notes

### DeformLattice.otl

- Asset type: `DeformLattice` (Object HDA).
- Core pattern:
  - `sphere1` is the deform target.
  - `box1` is the rest lattice.
  - grouped cage points (`Lattice1 -> Lattice2 -> Lattice3`) feed chained transforms (`xform1 -> xform2 -> xform3`) to create deformed lattice input.
  - `lattice1` wiring follows canonical order: target (0), rest lattice (1), deformed lattice (2).
- Important setting: `lattice1.divsx/divsy/divsz = 2/2/2` (must match box divisions).

### BallBounce.otl

- Asset type: `BallBounce` (Object HDA with `ball` and `floor` geos).
- Core pattern:
  - `ball/sphere1` is deformed with `lattice1`.
  - `ball/box1` is rest cage, and `spring1` drives the deformed cage over time.
  - `spring1` references collision geometry via `object_merge1.objpath1 = ../../floor/grid1`.
- Important setting: very coarse lattice (`divs = 1/1/1`) for broad squash/stretch behavior.

### LatticePerChunk.otl

- Asset type: `LatticePerChunk` (Object HDA).
- Core pattern:
  - fractured sphere pieces are generated (`break1`, `break2`, `connectivity1`, `partition1`).
  - `foreach__build_lattice_boxes` creates per-piece lattice cages (`bound1` with `divs=3/3/3`, oriented bbox on).
  - `foreach1` applies a lattice per partition piece using group-driven `blast` filtering (`group = lattice_`).
  - animated cage perturbation comes from `mountain1` and `xform1` before feeding deformed cages.
- Important setting: `foreach1/lattice1` has `radius ~ 0.58` and `bspheres = 1` (point-radius visualization on), emphasizing point-method influence control per chunk.

## Sticky Notes Read (Post-its)

Sticky-note text was explicitly extracted from network items (not just node comments):

- `DeformLattice`:
  - one top-level overview note plus eight SOP-level notes.
  - content reinforces the 3-input lattice contract and explains the three lattice point groups and their animated transform strategies (sine/cosine-driven motion).

- `BallBounce`:
  - three object-level notes and five notes inside `ball`.
  - notes describe the same data-flow pattern (`sphere1`, `box1`, `spring1`) and document spring-simulation intent (accuracy, drag, gain settings).
  - one sticky states external force Y is `0.8`; this appears inconsistent with current visible `spring1` parms (no exposed external-force value in the inspected parameter set), so treat that value as descriptive/tutorial text rather than a validated live parameter.

- `LatticePerChunk`:
  - three README-style sticky notes (top level, inside `sphere_object1`, and inside `foreach__build_lattice_boxes`).
  - they confirm the intended workflow: fracture first, then foreach-based per-fragment lattice deformation, then jitter/motion.

## Gotchas

- if the cage does not properly enclose the region, deformation can look incomplete or unstable
- very coarse cages produce smooth but low-control deformations
- dense/complex geometry can amplify small cage edits
- tuple parameters are often split (`tx/ty/tz`, `divsx/divsy/divsz`), so setting aggregate names like `t` or `divs` can fail depending on tool wrappers

## What To Verify In Examples

- how cage resolution affects control quality
- how local vs global cage edits propagate through the mesh
- interaction with downstream nodes (e.g., smoothing/remeshing)

## Related Nodes

- `bend`, `twist`, `bulge` for procedural single-mode deformations
- `edit` for direct point-level edits
- `latticefromvolume` for volume-driven lattice setup patterns
