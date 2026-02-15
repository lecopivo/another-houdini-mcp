# `groupfindpath` – Group Find Path

## Intent
Constructs groups for paths between elements (points, edges, or primitives), minimizing turns and distance. Useful for creating selection paths through geometry topology, with collision avoidance and various path-ending behaviors.

## Key Parameters
- `group`: Base Group – ordered sequence of elements defining the path waypoints
- `grouptype`: Group Type – element type for constructed path (Points/Edges/Primitives)
- `pathcontroltype`: Path Type – how path is specified:
  - `controls`: Paths through each base group element in order
  - `starts`: Loops/rings starting from base group elements
  - `startend`: Paths between start/end pairs in base group
- `operation`: Path Ending – termination behavior:
  - `path`: Stop at End – shortest path only
  - `extendedpath`: Extend to Edge – extend as far as possible
  - `closedpath`: Close Path – find secondary path back to start
- `usecolgroup`, `colgroup`, `colgrouptype`: collision group to avoid during path construction
- `avoidprevious`: Avoid Self Intersection – prevent paths from crossing already-constructed elements

## Observed Behavior (Live Tests)
**Baseline** (`pathcontroltype=controls`, `operation=closedpath`, `usecolgroup=1`):
- Input: grid (100pts/81prims), base_edges group (3 edges: 15-16, 35-36, 75-76), collision_prims group (prims 22-23)
- Output: path_result edge group with 39 edges

**After `pathcontroltype=starts`**:
- path_result edges increased to 52 (starting from each base edge creates separate loops)

**After `usecolgroup=0`**:
- path_result edges remained 39 (collision removal had minimal impact in this test layout)

## Typical Usage

### Finding paths through waypoints
```
grid -> group(edges) -> groupfindpath(pathcontroltype=controls)
```
Creates edge paths connecting specified edges in order.

### Creating loops from seed elements
```
geometry -> group(seed_edges) -> groupfindpath(pathcontroltype=starts, operation=closedpath)
```
Generates closed loops starting from each seed edge.

### Avoiding specific regions
```
geometry -> group(waypoints + collision) -> groupfindpath(usecolgroup=1, colgroup=collision)
```
Path avoids elements in the collision group.

## Gotchas
1. **Empty base group**: produces empty output group (no paths constructed)
2. **Unreachable waypoints**: if collision group blocks connectivity, paths may be incomplete or missing (check warnings)
3. **Group type mismatch**: ensure base group type matches `grouptype` parameter or results may be empty
4. **Path type interaction**: `pathcontroltype=starts` interprets base group as individual starting points rather than ordered waypoints

## Related Nodes
- `findshortestpath`: lower-level path finding between specific start/end
- `groupexpand`: grow groups by connectivity steps
- `group`: create base group and collision group inputs
- `groupcombine`: merge multiple path results

## Memory Notes
- Path construction priority follows base group element order when `avoidprevious=1`
- Edge path style (`edgestyle`) allows restricting to loops-only or rings-only when finding edge paths
