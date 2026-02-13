# Vellum Configure Hair (Workflow Note)

## Availability in This Build

There is no standalone SOP node type named `vellumconfigurehair` in this Houdini build.

## Equivalent Setup

Use `vellumconstraints` with:

- `constrainttype=hair`

then add a second `vellumconstraints` stage for pins (`constrainttype=pin`) when roots must stay anchored.

## Practical Reminder

- Empty pin groups are a common failure mode; verify non-empty group membership before solving.
