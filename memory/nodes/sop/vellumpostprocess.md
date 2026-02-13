# Vellum Post-Process (SOP)

## What This Node Is For

`vellumpostprocess` applies common post-sim cleanup/enhancement for Vellum results:

- weld application
- smoothing/subdivision
- detangle correction
- optional stress attribute baking

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/vellumpostprocess.txt`)
- Example set reviewed: fallback companion coverage (no local `help/examples/nodes/sop/vellumpostprocess/` folder)
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs): non-destructive finishing step after `vellumsolver`; supports visual diagnostics and cleaner render geometry.
- Observed (live): in `/obj/academy_vellumconstraints_grain/post`, defaults preserved particle topology and attributes from solver output.
- Mismatches: none.

## Minimum Repro Setup

- `vellumsolver -> vellumpostprocess -> OUT`
- Optional constraints on input 1 for guide/attribute bake workflows.

## Gotchas and Failure Modes

- Detangle/smooth can alter final shape subtly; validate hero shots.
- If constraint input is missing, some visualization/bake features are limited.
