# MaskByFeature (SOP)

## Intent

`maskbyfeature` builds point-mask attributes from directional visibility, shadows, and ambient occlusion so downstream nodes can localize effects (scatter/deform/color) to lit, exposed, or occluded regions.

## Core Behavior

- Casts rays onto input-0 geometry using either a direction vector or point sources from input 1.
- Can optionally include shadowing (self and/or input-3 casters) and ambient occlusion.
- Writes one or more mask attributes (`combined`, `direction`, `shadow`, `ao`) to points.
- Output topology is unchanged; behavior is attribute-authoring.

## Key Parameters

- Output contract:
  - `usecombinedmask`, `usedirectionmask`, `useshadowmask`, `useaomask`.
  - corresponding attribute-name parms (`combinedmaskattrib`, etc.).
- Directional solve:
  - `directionfrom` (`Vector` vs `Point Cloud`), `direction`, `sourcepoints`, `maxsourcepoints`.
  - `maxangle` limits glancing-angle contribution.
- Shadows:
  - `castshadows`, `selfshadows`, `samples`, `bluriterations`, `rayoffset`.
- Ambient occlusion:
  - `enableao`, `aosamples`, `aobias`, AO blur/sample settings.
- Remap:
  - per-mask ramps to reshape/contrast mask output values.

## Typical Workflow

```text
surface (+ optional light points / shadow casters) -> maskbyfeature -> downstream mask consumer
```

- Emit named masks explicitly (avoid relying on default names when multiple masks are enabled).
- Validate attribute ranges before driving downstream thresholds.
- Add shadow casters on input 3 when required by art direction.

## Production Usage

- Use `directionfrom=Point Cloud` for art-directable “light source points” workflows.
- Keep directional and combined masks separate while tuning; combine only when final behavior is approved.
- AO is often better used as a secondary layer (multiplicative/threshold) rather than sole mask.

Measured outcomes (`MaskByFeatureBasic` example, node `/obj/academy_MaskByFeatureBasic/shadowmask1`):
- Baseline output wrote point `Cd` mask only (`2986` pts), with `Cd` mean `0.1855`.
- Enabling directional output (`usedirectionmask=1`) added `dir_mask` (mean `0.2562`) while preserving `Cd` mask.
- Direction interaction (vector mode):
  - `maxangle 90 -> 20` reduced directional concentration strongly (`dir_mask` mean `0.2562 -> 0.0479`).
  - flipping vector `Y 1 -> -1` collapsed combined mask in this setup (`Cd` mean `0.1855 -> 0.0000`) while `dir_mask` remained non-zero (mean `0.1427`).
- Direction source mode switch (`Vector -> Point Cloud`) changed combined response (`Cd` mean `0.1855 -> 0.1635`).
- Combined/shadow interaction:
  - with shadows off (`castshadows=0`), combined mask matched directional mask mean (`0.2561`).
  - with self-shadows on, combined mean dropped to `0.1635` while directional mean stayed `0.2561`.
- AO layer test (`enableao=1`, `aosamples=8`) emitted `ao_mask` (`mean 0.7085`) and reduced combined mask mean further to `0.1408`.

## Gotchas

- Attribute-name collisions are easy: using the same name for multiple mask outputs can overwrite expected channels.
- Direction vector orientation mistakes can produce near-empty combined masks even when directional mask still has values.
- Too-low sample counts can add noise; tune blur/sample together before judging mask quality.
- Downstream nodes may expect `[0,1]` masks; remap ramps can intentionally exceed expected contrast if not checked.

## Companion Nodes

- `scatteralign` for mask-driven distribution.
- `attribwrangle` / `attribadjust*` for post-mask remapping and compositing.
- occluder-prep nodes (`merge`, boolean/modeling ops) for input-3 shadow casters.

## Study Validation

- ✅ Read docs: `nodes/sop/maskbyfeature.txt`
- ✅ Reviewed example: `examples/nodes/sop/maskbyfeature/MaskByFeatureBasic.txt`
- ✅ Inspected stickies and companion setup (`testgeometry_pighead`, point-source input via `add1`)
- ✅ Ran live parameter interaction tests on direction/shadow/AO outputs with measured attribute statistics
