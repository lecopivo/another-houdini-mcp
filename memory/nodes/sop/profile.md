# Profile (SOP)

## Intent

`profile` extracts profile curves embedded on a surface (typically after `project`) or remaps those profiles in UV-space to reposition/scale them procedurally.

## Core Behavior

- Operates on surface profile data; it is commonly used after `project` authored profile curves on a deforming host surface.
- In extraction mode, it outputs stand-alone profile geometry either in world-space (`parametric=0`) or as a planar UV-image (`parametric=1`).
- In remap workflows, UV range controls can animate profile placement on the host while preserving host geometry topology.
- Extraction fitting options (`smooth`, `sdivs`, `order`, `tolerance`) control reconstructed curve density/shape.

## Key Parameters

- `parametric`: extraction mode switch.
  - `0`: world-space extraction that follows host deformation.
  - `1`: planar UV-image extraction in XY (stable for edit/reproject workflows).
- `smooth`, `sdivs`, `order`, `tolerance`: spline fitting controls for extracted world-space curves.
- `keepsurf`, `delprof`: control whether the owner surface and original embedded profile are kept in extraction output.
- `urange1/2`, `vrange1/2`: remap profile into a UV subdomain (often expression-driven for animation).
- `maptype`: mapping mode (`unif`, `chordlen`) for remap behavior.

## Typical Workflow

```text
curve profile -> project (onto host surface) -> profile (extract or remap) -> trim/bridge/secondary modeling
```

- Build profile-on-surface first with `project`.
- Choose extraction for downstream curve modeling or choose remap for animated profile placement on the same surface.
- If extraction output is used downstream, lock fitting density early to avoid accidental topology drift.

## Production Usage

- Good for profile-driven panel cuts/trim prep where profile curves must follow simulated/deforming cloth-like hosts.
- Useful UV-domain edit loop: extract parametrically, edit in XY, then reproject.
- Expression-driven remap ranges are a lightweight way to animate profile region changes without changing host mesh topology.

Measured outcomes (`FlagProfiles` example + live parameter sweeps):
- Example network split:
  - `extract/profile1` produced extracted curve output (`69 pts / 1 prim`) from projected flag profile.
  - `uniform/profile2` kept host mesh contract (`49 pts / 1 prim`) while remap ranges animated profile placement.
- `parametric` extraction behavior:
  - `parametric=0`: world-space curve followed spring-deformed flag (`frame 1 center ~(-0.0003,0.0003,0.0)` -> `frame 24 center ~(0.5342,0.0372,0.1790)`, point count changed `69 -> 81`).
  - `parametric=1`: planar XY extraction remained stable across animation (`10 pts / 1 prim`, center `(0.5,0.5,0.0)` at both frames).
- Fitting density sweep (`parametric=0, smooth=1`):
  - `sdivs=5` -> `56 pts`,
  - `sdivs=20` -> `78 pts`.
- `smooth` off gave low-density direct extraction (`11 pts / 1 prim`) without spline fitting.
- `keepsurf=1` merged owner surface with extracted profile (`127 pts / 2 prims`).
- Remap branch in this asset changed profile metadata placement while geometry stayed topologically identical to projected host (`49 pts / 1 prim`, mean point displacement vs project = `0.0`).

## Gotchas

- `profile` can appear to do "nothing" in remap setups when you only inspect host geometry counts; profile-domain changes may be metadata/visualization-level.
- Animated expressions on `urange`/`vrange` can mask manual tweaks; clear or inspect keyframes first.
- World-space extraction (`parametric=0`) can change point count over time when host deformation/fitting changes.
- If downstream tools expect stable point counts, prefer planar parametric extraction or lock fitting strategy intentionally.

## Companion Nodes

- `project`: authors the embedded profile domain that `profile` extracts/remaps.
- `group` + `spring`: common host-surface deformation chain (flag-style examples) used to validate profile follow behavior.
- `trim` / `bridge`: typical next steps after profile extraction.

## Study Validation

- ✅ Read docs: `nodes/sop/profile.txt`
- ✅ Reviewed example: `examples/nodes/sop/profile/FlagProfiles.txt`
- ✅ Inspected internals and sticky notes across `uniform`, `extract`, and `No_profile` branches
- ✅ Ran live extraction/remap/fitting/frame-follow tests with measured geometry outcomes
