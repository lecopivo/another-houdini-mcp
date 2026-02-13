# Ocean Spectrum (SOP)

## What This Node Is For

`oceanspectrum` generates wave spectrum volumes (`phase`, `frequency`, `amplitude`) used by `oceanevaluate`.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/oceanspectrum.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` branches 4/5/6)

## Key Notes

- Primary quality dial: `resolution exponent` (power-of-two volume resolution).
- Wind model/settings shape energy distribution and directionality.
- Multiple spectra can be layered before evaluate.
- Can apply masks/noise and point-driven wave instancing behaviors.
