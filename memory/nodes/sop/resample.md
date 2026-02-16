# Resample (SOP)

## Intent

`resample` rebuilds curve-like primitives into controlled point spacing or segment counts, with options for arc/chord measurement and point-only output.

## Core Behavior

- Converts supported curve inputs (poly/NURBS/Bezier and other convertible primitives) into resampled polygonal representations.
- Supports two main density contracts:
  - maximum segment length (`dolength` + `length`),
  - maximum segment count (`dosegs` + `segs`).
- `measure` affects spacing interpretation (`Along Arc` vs `Along Chord`).
- `onlypoints=1` emits point clouds without curve primitives.

## Key Parameters

- `dolength`, `length`: edge length targeting.
- `dosegs`, `segs`: segment-count targeting.
- `measure`: arc vs chord measurement.
- `last`: maintain original end vertex.
- `allequal`: equalize final segment length.
- `onlypoints`: points-only output mode.

## Typical Workflow

```text
curve(s) -> resample -> downstream sweep/path/particle/scatter operations
```

- Pick one controlling mode first (length or segment count).
- Use `measure` to match desired geometric fidelity model.

## Production Usage

- Standard preprocessing before sweep/wire/curve-driven FX where spacing uniformity matters.
- Segment-count mode is useful for deterministic topology contracts.
- Length mode is useful for physical scale consistency across differently sized curves.

Measured outcomes (`ResampleLines` example):
- Baselines:
  - `max_segment_length/resample3`: `93 pts / 3 prims`.
  - `max_number_segments/resample4`: `33 pts / 3 prims`.
  - `even_length_segments_along_chord/resample2`: `92 pts / 3 prims`.
- Length sweep (`resample3`, keyframes disabled temporarily):
  - `length 0.3 -> 0.12 -> 0.05` yielded `39 -> 93 -> 217` points.
- `last` behavior:
  - `last=1`: `217 pts`, full end reach preserved,
  - `last=0`: `214 pts`, endpoint-span reduced (`bbox X shrank 3.27551 -> 3.246534`).
- Segment sweep (`resample4`):
  - `segs 4 -> 10 -> 20` yielded `15 -> 33 -> 63` points.
- Measure comparison (`resample2`):
  - `measure arc=0`: `93 pts`,
  - `measure chord=1`: `92 pts`.
- Points-only mode (`onlypoints=1`) emitted `217 pts / 0 prims`.

## Gotchas

- Animated demo parameters (length/segment count) can hide manual edits until keyframes are cleared.
- `last=0` may miss exact original endpoint, which can break endpoint-dependent downstream constraints.
- Arc vs chord differences can be subtle in counts but still meaningful for shape fidelity.

## Companion Nodes

- `sweep` for curve-to-surface generation after spacing regularization.
- `convert` when upstream primitive types need explicit polygon conversion control.
- `curve`/`font` in example-style multi-curve comparison setups.

## Study Validation

- ✅ Read docs: `nodes/sop/resample.txt`
- ✅ Reviewed example: `examples/nodes/sop/resample/ResampleLines.txt`
- ✅ Inspected all example branches and sticky guidance (arc/chord, length/segments)
- ✅ Ran live length/segment/last/measure/points-only sweeps with measured outputs
