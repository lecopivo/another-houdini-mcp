# File Cache (SOP)

## What This Node Is For

`filecache` writes and reloads SOP geometry caches with versioning/load controls around a single node interface.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/filecache.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/filecache/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: cache expensive SOP branches and optionally decouple from upstream cooking.
- Observed: `/obj/academy_filecache_live` with connected input passes geometry in live mode; turning `loadfromdisk=1` without existing cache files outputs empty geometry (`0 pts / 0 prims`) in this setup.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_filecache_live/box1 -> filecache1 -> OUT_FILECACHE`
- Key parms: `loadfromdisk`, `timedependent`, `basename/basedir`, `version`, `execute`.
- Verification: `probe_geometry` before/after `loadfromdisk` toggle.

## Key Parameters and Interactions

- `loadfromdisk` is the central mode switch.
- Versioning is safest when cache path is constructed mode.
- Missing-frame policy should be explicit for robust playback networks.

## Gotchas and Failure Modes

- Enabling load mode before writing cache can appear as broken upstream geometry.
- Cache path/version collisions can silently read stale data.

## Related Nodes

- `file`
- `vellumio`
- `dopio`
