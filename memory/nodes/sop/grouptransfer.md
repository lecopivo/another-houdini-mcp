# `grouptransfer` – Group Transfer

## Intent
Transfers groups between two pieces of geometry based on proximity. Maps destination elements (primitives/points/edges) to nearest source elements and creates corresponding groups in the destination.

## Key Parameters
- Input 0: destination geometry (receives transferred groups)
- Input 1: source geometry (provides groups to transfer)
- `primgroups`: source primitive groups to transfer (empty = all)
- `ptgroups`: source point groups to transfer (empty = all)
- `edgegroups`: source edge groups to transfer (empty = all)
- `primpre`, `ptpre`, `edgepre`: prefixes for destination group names
- `groupnameconflict`: conflict resolution method:
  - `skip`: skip conflicted group
  - `overwrite`: replace existing group
  - `suffix`: add numerical suffix (group2, group3, etc.)
- `threshold`: distance threshold – elements beyond this distance won't map
- `createemptygroups`: create empty groups if no elements map

## Observed Behavior (Example)
**Example setup**:
- Input 0: spheres (destination)
- Input 1: boxes with primitive groups (source)
- Behavior: spheres receive groups based on proximity to grouped boxes
- Source geometry (input 1) does NOT pass through – only used for proximity mapping
- Output geometry = input 0 with new groups added

## Typical Usage

### Transferring selections between LODs
```
high_res_geo -> input0(grouptransfer) input1 <- low_res_geo_with_groups
```
High-res geometry receives groups based on proximity to low-res selections.

### Rigging group transfer
```
deformed_geo -> input0(grouptransfer) input1 <- rest_geo_with_groups
```
Deformed geometry gets groups from rest pose based on closest point matching.

### Prefix to avoid conflicts
```
grouptransfer(primpre="transferred_")
```
Creates groups like `transferred_group1` instead of `group1`.

### Distance-filtered transfer
```
grouptransfer(threshold=0.1)
```
Only maps destination elements within 0.1 units of source group elements.

## Gotchas
1. **Source geometry visibility**: input 1 geometry does NOT appear in output – only groups are transferred
2. **Empty groups**: if no destination elements are close enough to source group, output group may be empty (unless `createemptygroups=1`)
3. **Topology mismatch is OK**: source and destination can have completely different topology (example: sphere vs box)
4. **Order preservation**: if source group is ordered, destination group will also be ordered by mapped element then proximity
5. **Group class mismatch**: transferring primitive groups requires primitives on both sides; can't transfer prim group to points

## Related Nodes
- `groupcopy`: copy groups within same geometry based on element correspondence
- `attribtransfer`: transfer attributes (not just groups) by proximity
- `group`: create source groups before transfer
- `grouppromote`: convert group element types after transfer

## Memory Notes
- Useful for retopology workflows where you want to preserve named selections
- Conflict resolution with `suffix` mode keeps incrementing until unique name found
- Distance threshold allows selective transfer (only nearby elements)
- Ordered group transfer maintains relative ordering from source
