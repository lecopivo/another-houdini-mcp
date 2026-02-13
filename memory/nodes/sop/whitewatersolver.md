# Whitewater Solver (SOP)

## What This Node Is For

`whitewatersolver` simulates foam/spray/bubbles from whitewater emission and liquid fields in SOP context.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/whitewatersolver.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` branch 4)

## Key Notes

- Inputs: emission+fluid fields, container, collisions.
- Core controls: `substep`, emission amount/limits, lifespan, buoyancy/advection, wind.
- Foam behavior includes clumping/adhesion/repellants and depth controls.
- Output passes particles + container/collision streams for postprocess alignment.
