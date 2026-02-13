# Guide Deform (SOP)

## What This Node Is For

`guidedeform` deforms geometry using rest vs animated skin and/or guide curves.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/guidedeform.txt`)
- Example set reviewed: fallback companion coverage (no local `help/examples/nodes/sop/guidedeform/` folder)
- QA pass complete: yes (live skin mode + guide capture/deform mode repro)

## Source-of-Truth Split

- Intent: preserve guide/skin-driven deformation for hair or arbitrary geometry across four modes (`skin`, `capturedeform`, `capture`, `deform`).
- Observed:
  - `/obj/academy_guidedeform` validates `skin` mode (rest skin + animated skin delta).
  - `/obj/academy_guidedeform_guides` validates guide workflows using sparse animated guides driving denser hair curves.
  - `capturedeform` output and `capture -> deform` two-stage output match exactly (pointwise), confirming docs workflow.
- Mismatches: none.

## Minimum Repro Setup

- 5-input pattern:
  - input 0: geometry to deform
  - input 1: rest skin
  - input 2: animated skin
  - input 3: rest guides
  - input 4: animated guides
- Guide workflow repro:
  - `hair_copy` (20 curves) deformed by `guide_copy_rest` (5 curves) -> `guide_anim_xf`
  - one-node path: `mode=capturedeform`
  - two-node path: `mode=capture` then `mode=deform`

Frame validation snapshot (`OUT_CAPTURE_DEFORM`, avg point displacement vs undeformed hair):
- f1: `0.0091` (max `0.0130`)
- f24: `0.1858` (max `0.2676`)
- f48: `0.2405` (max `0.3474`)
- f72: `0.1394` (max `0.1968`)

Two-stage parity:
- `OUT_CAPTURE_DEFORM` vs `OUT_TWO_STAGE` max point delta = `0.0` at sampled frames.

## Gotchas

- Rest and animated inputs must match topology.
- The node has dedicated guide inputs (3/4); wiring only 0/1/2 means guides are not being provided through their intended connectors.
- In guide workflows, weak guide animation can look like node failure; verify actual guide motion first.
- `capture` alone only prepares weighting metadata; visible deformation requires a downstream `deform` pass.
- For production hair, ensure orient/guide attributes are valid if using guide-based modes.
