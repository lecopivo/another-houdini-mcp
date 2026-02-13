# Vellum Configure Cloth (Workflow Note)

## Availability in This Build

There is no standalone SOP node type named `vellumconfigurecloth` in this Houdini build.

## Equivalent Setup

Use `vellumconstraints` with:

- `constrainttype=cloth`

and then chain additional `vellumconstraints` nodes for pin/attach/weld/glue as needed.

## Practical Reminder

- Treat “configure cloth” as a preset/workflow on `vellumconstraints`, not a separate node in this environment.
