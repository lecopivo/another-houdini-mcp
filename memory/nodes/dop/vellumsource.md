# Vellum Source (DOP)

## What This Node Is For

`vellumsource` emits new Vellum patches (geometry + constraints bookkeeping) into a running Vellum solve.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/dop/vellumsource.txt`)
- Example set reviewed: fallback companion coverage (no local `help/examples/nodes/dop/vellumsource/` folder)
- QA pass complete: yes (live DOP node instantiation + companion solver study)

## Key Takeaways

- Emission modes (`Only Once`, `Each Frame`, `Each Substep`, `Instance on Points`) are central behavior switches.
- Patch naming and stream naming are critical for per-patch control.
- Sourcing requires synchronized SOP geometry + matching constraint geometry paths.
