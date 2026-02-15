# Rig Doctor (SOP, KineFX)

## Intent

`kinefx::rigdoctor` stabilizes and validates SOP skeleton data after topology/name edits, then emits a clean, optimization-friendly rig contract for downstream KineFX nodes.

## Core Behavior

- Freezes skeleton topology at stash/time-shift snapshot.
- Copies animated attrs to frozen topology while optionally freezing selected attrs.
- Repairs point-name issues (missing names, spaces/duplicates sanitization).
- Emits hierarchy helper attrs (`parent_idx`, `child_indices`, `eval_ord`).
- Can initialize/derive transforms for skeletons missing proper transform attrs.

## Key Parameters

### Freeze Time Dependent Attributes
- `method` (`Stash` vs `Time Shift`) and `frame`.
- `freezeattribs`: attrs that stay constant from frozen snapshot.

### Point Names
- `initmissingnames` + `nameprefix`.
- `sanitizenames` (spaces -> underscores, duplicate handling).
- optional input-name preservation (`storeinputname`).

### Hierarchy
- `debughierarchy`, `onfailure` (warning/error).
- `outputparentidx`, `outputchildindices`, `outputevalord`.

### Transformations
- `inittransforms`.
- `convertinstanceattribs` (`pscale`, `N/up`, etc -> transform).
- `reorienttochild`, `ref_vector`.

## Typical Workflow

```text
topology/name edits -> rigdoctor -> downstream rig/clip/deform nodes
```

- Place Rig Doctor after joint add/remove/reparent operations.
- Enable name/hierarchy repair and emit helper attrs.
- Freeze attrs intentionally to reduce downstream instability.

## Production Usage

- Use as a breakpoint node after structural rig edits.
- Keep sanitization on unless pipeline requires exact raw names.
- Emit hierarchy attrs during debug/authoring, disable later if unnecessary.

Measured outcomes (live validation; no official example asset available for this node):
- Input names intentionally broken: `['root','arm joint','arm joint','', 'tip']`.
- Default Rig Doctor output names: `['root','arm_joint','arm_joint','point_0','tip']` (spaces sanitized + missing initialized).
- With `sanitizenames=0` and `initmissingnames=0`, raw names pass through unchanged.
- Output point attrs included hierarchy helpers by default in this build: `parent_idx`, `child_indices`, `eval_ord`.
- With `inittransforms=1` + `convertinstanceattribs=1`, transform attrs persisted and reflected instance inputs (for `pscale=1.5`, transform was 1.5-scaled matrix).

## Gotchas

- `rigdoctor` may appear to "change names unexpectedly" when sanitization/init options are on; this is by design.
- If downstream tools depend on exact source names, either disable sanitization or store original names first.
- Lack of official example means you should validate with a small synthetic rig before applying to production character data.

## Companion Nodes

- `kinefx::deletejoints`, `kinefx::parentjoints`, `kinefx::skeleton`.
- `kinefx::rigattribwrangle` / `kinefx::rigattribvop` for post-cleanup procedural edits.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--rigdoctor.txt`
- ✅ Confirmed no official node example listing from `list_example_nodes`
- ✅ Built live validation network and tested name/hierarchy/transform repair behaviors
