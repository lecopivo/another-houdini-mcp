# File (SOP)

## What This Node Is For

`file` reads, writes, and caches geometry on disk, and can act as a pass-through or delayed-load boundary in SOP pipelines.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/file.txt`)
- Example set reviewed: yes (`examples/nodes/sop/file/PackedPoints.txt`)
- Example OTL internals inspected: yes (`PackedPoints.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - With input connected, `filemode` controls read/write/no-op behavior.
  - Packed-disk workflows reduce memory and can support motion blur sample loading.
  - Example emphasizes generating disk samples first (`make_files`) and then reading packed geometry for instancing.
- Observed (live scene/params/geometry):
  - In `/obj/academy_file_live`, writing works in `filemode=2` to `/tmp/academy_file_live.bgeo.sc`; file was created on disk.
  - Switching to `filemode=1` (read) ignored connected input changes and kept cached disk result (`8 pts / 6 prims`).
  - Switching to `filemode=3` (no operation) passed through current input geometry instead (sphere input produced `1 pt / 1 prim`).
  - Official example `/obj/academy_PackedPoints/geo1` confirms packed-point instancing pattern: `file1` + `copy1` over `scatter1` with ROP nodes for sample generation.
- Mismatches:
  - None observed.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_file_live/box1 -> file1 -> OUT_FILE`
  - additional input swap test: `sphere1 -> file1`
- Key parameter names and values:
  - `file1.file = "/tmp/academy_file_live.bgeo.sc"`
  - `file1.filemode = 2` (write), then `1` (read), then `3` (no-op)
- Output verification method:
  - `probe_geometry` on `OUT_FILE` per mode + shell check for physical file existence.

## Key Parameters and Interactions

- `filemode` is the primary behavior switch when input exists.
- `missingframe` matters for resilient cache networks; use no-geometry mode where downstream must keep cooking.
- `loadtype` + `viewportlod` define memory/perf profile for heavy datasets.
- Packed sequence modes require intentional frame-range/index setup for interpolation and motion blur behavior.

## Practical Use Cases

1. Cache heavy SOP branches once, then re-read for interactive downstream iteration.
2. Use packed disk primitives for lightweight viewport/render instancing of repeated assets.

## Gotchas and Failure Modes

- Forgetting mode changes is a common failure: node can look wired but still be reading stale cache.
- Relative cache paths can break across machines; use consistent path policy/environment variables.
- Packed display settings can hide full-geo issues in viewport; validate final render/path when debugging.

## Related Nodes

- `filecache`
- `filemerge`
- `dopio`
- `vellumio`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
