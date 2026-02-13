# Tet Conform (SOP)

## What This Node Is For

`tetconform` builds a conforming tetrahedral mesh from closed surface geometry.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/tetconform.txt`)
- Example set reviewed: fallback companion coverage (no local `help/examples/nodes/sop/tetconform/` folder)
- QA pass complete: yes (live tetrahedralization check)

## Source-of-Truth Split

- Intent: generate tet meshes suitable for volumetric simulation workflows.
- Observed: `/obj/academy_tetconform/OUT` produced `5887` tetrahedron prims (`Tetrahedron` primitive type) from a polygon sphere input.
- Mismatches: none.

## Practical Notes

- Prefer `tetconform` over legacy tetrahedralize for robust conforming results.
- Tune quality/sizing parameters based on simulation target (speed vs fidelity).
