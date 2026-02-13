# Vellum Rest Blend (DOP)

## What This Node Is For

`vellumrestblend` blends current constraint rest states toward simulation or external rest targets during solve.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/dop/vellumrestblend.txt`)
- Example set reviewed: companion SOP example (`help/examples/nodes/sop/vellumrestblend/BasicRestBlend.txt`)
- QA pass complete: yes

## Source-of-Truth Split

- Intent: controlled rest-state updates (plasticity-like behavior or directed shape retargeting).
- Observed: `BasicRestBlend` companion network demonstrates both current-state baking and external animated rest updates inside solver internals.
- Mismatches: none.

## Practical Notes

- Update frequency (`single frame`/`frame`/`substep`) is a major quality-performance dial.
- Works well with per-group constraint targeting for selective rest updates.
