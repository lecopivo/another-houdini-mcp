# LSystem (SOP)

## Intent

`lsystem` generates recursive/fractal procedural geometry from grammar-like rewrite rules interpreted by turtle commands. It is commonly used for plants/branching forms, but it also works for structured procedural layouts when rules are treated as a compact modeling language.

## Core Behavior

- Rewrites `premise` through enabled rules for `generations`, then interprets resulting string as turtle commands.
- `type` changes output representation (`Skeleton` polylines vs `Tube` geometry).
- Optional leaf inputs (`J`, `K`, `M`) instance connected geometry directly from rule strings.
- Fractional generations can produce continuous growth effects when `contLength`/`contAngl`/`contWidth` are enabled.

## Key Parameters

- Rule system:
  - `premise`, `rule#`: rewrite grammar and recursive substitution behavior.
  - `generations`: recursion depth/growth amount.
- Turtle defaults:
  - `stepinit`/`stepscale`: forward segment length baseline and scale.
  - `angleinit`/`anglescale`: turn/pitch/roll baseline and scale.
  - branch commands (`[ ]`) and turn commands (`+ - & /`) are the primary topology shapers.
- Geometry representation:
  - `type`: skeleton curves vs tube geometry.
  - `pointwidth` (skeleton mode): emits generation/path attributes (`width`, `arc`, `gen`, etc.).
- Variation controls:
  - `randscale`, `randseed`: stochastic branch-length variation with deterministic seed control.
  - `contLength` (and related continuous toggles): smooth in-between behavior for fractional generation values.

## Typical Workflow

```text
premise + rules -> lsystem -> (polywire/copy/sweep/convert) -> OUT
```

- Start with a minimal rule set and low `generations`.
- Validate branching and orientation first (`+/-`, `&/`, `[ ]`), then tune scale/angle defaults.
- Add leaf geometry commands (`J/K/M`) only after base structure is stable.

## Production Usage

- Keep rewrite symbols modular (for example `A` for trunk logic, `B` for branch logic) so growth changes stay local.
- Use skeleton output for early lookdev and simulation-friendly paths; switch to tube only when you need direct volume/surface output.
- For geometry insertion pipelines, treat leaf commands as instancing contracts and verify which leaf input each rule references.

Measured outcomes (`LSystemMaster`, `LsystemBuilding`, and live `/obj/academy_lsystem_live/lsystem1`):
- Generation scaling (skeleton mode): `generations 3 -> 5` changed output from `13 pts / 3 prims` to `40 pts / 9 prims`.
- Representation switch at same rules (`generations=5`):
  - skeleton: `40 pts / 9 prims / 48 verts`
  - tube: `522 pts / 18 prims / 522 verts`.
- Skeleton attribute contract: enabling `pointwidth=1` added point attrs `width`, `segs`, `div`, `lage`, `arc`, `up`, `gen`.
- Fractional-generation interaction (`generations=3.5`):
  - `contLength=0` bbox size ~`(0.4693, 0.7664, 0.4975)`
  - `contLength=1` bbox size ~`(0.3374, 0.6524, 0.3577)`
  - topology stayed constant, but geometric extent changed (continuous growth behavior).
- Leaf insertion contract (`J` with circle on leaf input):
  - without leaf command (`B=&FFFA`): `40 pts / 9 prims`
  - with leaf command (`B=&FFF[fJ]A`): `52 pts / 21 prims`.
- Random variation: `randscale=0.35` with seeds `1` vs `9` kept topology stable (`40/9`) but changed shape extents.

## Gotchas

- Recursive rule growth is exponential; high `generations` can become expensive quickly.
- Rules using `J/K/M` silently do nothing if the corresponding leaf input is not wired.
- Switching `type` late can invalidate downstream assumptions about primitive class/count.
- Fractional `generations` can look inconsistent unless continuous toggles are set intentionally.

## Companion Nodes

- `polywire` to convert skeleton curves into renderable tubes.
- `copy` / `copytopoints` for point-driven instancing on generated structures.
- `group`/`blast`/`attribwrangle` for branch filtering and post-generation shaping.

## Study Validation

- ✅ Read docs: `nodes/sop/lsystem.txt`
- ✅ Reviewed examples: `examples/nodes/sop/lsystem/LSystemMaster.txt`, `examples/nodes/sop/lsystem/LsystemBuilding.txt`
- ✅ Inspected sticky notes and companion-node workflows (including `K` window insertion pattern)
- ✅ Ran live parameter and interaction tests in `/obj/academy_lsystem_live`
