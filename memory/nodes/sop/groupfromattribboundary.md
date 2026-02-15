# `groupfromattribboundary` – Group from Attribute Boundary

## Intent
Creates groups containing the boundaries of specified attributes and/or base groups. Identifies edges/points/primitives where attribute values change or where group boundaries exist.

## Key Parameters
- `groupname`: output group name
- `boundarytype`: Group Type – element type for output group (Points/Edges/Primitives)
- `group`: Base Group – restricts boundary search to this region (optional)
- `grouptype`: Base Group Type – type of elements in base group
- `attrib`: attribute(s) to find boundaries for (can be point/prim/vertex attributes)
- `tol`: tolerance for floating-point attribute comparisons
- `includeunshared`: include edges referenced by only one polygon (geometry boundary)
- `removedegen`: remove degenerate boundary edges from output

## Observed Behavior (Example)
**Example setup**:
- Input: grid (100pts/81prims) with prim `Cd` attribute + base group (prims 39-44, 48-53, 57-62, 66-71, 75-80)
- Parameters: `attrib=Cd`, base group specified
- Output: edge group containing:
  - boundaries of the base group (where selected/unselected prims meet)
  - boundaries of the `Cd` attribute within the base group (where color changes)

## Typical Usage

### Finding color seams
```
geometry -> color(pattern) -> groupfromattribboundary(attrib=Cd, boundarytype=edge)
```
Creates edge group at color boundaries.

### Isolating selection perimeter
```
geometry -> group(selection) -> groupfromattribboundary(group=selection, boundarytype=edge)
```
Outputs edges forming the boundary of the selection group.

### Combining attribute and group boundaries
```
geometry -> group + attribcreate -> groupfromattribboundary(group=selection, attrib=myattr)
```
Output includes both group boundary and attribute boundary edges.

### Finding open edges
```
geometry -> groupfromattribboundary(includeunshared=1, boundarytype=edge)
```
Captures geometry boundary (unshared edges) without attribute filtering.

## Gotchas
1. **Empty attrib parameter with no base group**: may produce empty output if geometry has no unshared edges and no attribute boundaries
2. **Tolerance too tight**: floating-point attributes may create unexpected boundaries if `tol` is too small for precision
3. **Attribute class matters**: ensure attribute exists on correct class (point/prim/vertex); wrong class yields empty output
4. **Base group conversion**: base group is converted to `boundarytype` before processing, which may change boundary semantics

## Related Nodes
- `group`: create base group input
- `groupexpand`: grow boundary groups by connectivity
- `attribcreate`: generate test attributes
- `groupfindpath`: construct paths through boundary elements

## Memory Notes
- Useful for UV seam detection (`attrib=uv`)
- When `primsbyattribbndpts=1` (primitives mode), includes all prims touching attribute boundary points, not just those with boundary edges
- `includecurveunshared` controls whether all curve edges or only endpoints are included when `includeunshared=1`
