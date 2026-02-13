# Ocean Evaluate (SOP)

## What This Node Is For

`oceanevaluate` evaluates one or more ocean spectra on geometry/volumes/points and outputs displacements, velocity, and optional fields.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/oceanevaluate.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` branches 4/5/6)

## Key Notes

- Input 1 receives merged `oceanspectrum` volumes.
- Can output deformed geometry, velocity, cusp attributes, and ocean fields (`surface`, `vel`, etc.).
- Downsample/max-resolution controls are important for sim-preview speed.
- In SOP FLIP setups, often feeds `flipsolver` input 3 as open-water boundary signal.
