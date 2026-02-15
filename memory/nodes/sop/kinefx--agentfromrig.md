# Agent from Rig (SOP, KineFX)

## Intent

`kinefx::agentfromrig` builds a crowd agent primitive from a SOP skeleton hierarchy, establishing the rig definition that downstream crowd tools use for layers, clips, and simulation.

## Core Behavior

- Converts an input skeleton into an `Agent` primitive definition.
- Can emit `agentname` point attribute for type identification.
- Can freeze rig extraction to a chosen rest frame for performance/stability.
- Can optionally auto-add `__locomotion__` joint required by locomotive clip workflows.
- Can import transform groups from point groups/attributes for weighted rig subsets.

## Key Parameters

- `createagentname` / `agentname`: controls whether agent type tag is written and what value is used.
- `userestframe` / `restframe`: locks rig build to specific frame to avoid per-frame rig rebuild.
- `userestposeattrib` / `restposeattrib`: use point rest-transform attribute for rig rest pose.
- `createlocomotionjoint`: inserts `__locomotion__` when missing.
- `pointgroups`, `pointattribs`: import transform groups from skeleton grouping/weights.

## Typical Workflow

```
scenecharacterimport -> agentfromrig -> agentlayer -> agentclip -> crowdsource
```

- Build base agent from skeleton rig first.
- Add geometry layer(s) with `agentlayer`.
- Add clip(s) with `agentclip`.
- Use `agentprep/crowdsource` for simulation handoff.

## Production Usage

- Enable `userestframe` for animated input rigs to prevent unnecessary time-dependent rig reconstruction.
- Keep `createlocomotionjoint=1` when planning to use locomotive clips.
- Use explicit `agentname` values to maintain robust multi-agent pipelines.

Measured outcomes from `/obj/academy_AgentFromSOPs/agent_setup/create_agent`:
- Baseline output: `1` point / `1` `Agent` prim, with point attribs `P`, `agentname`.
- `createagentname=0` removed `agentname` point attribute (`['P']` only).
- `createlocomotionjoint=1` -> rig transforms `27`, includes `__locomotion__`.
- `createlocomotionjoint=0` -> rig transforms `26`, no `__locomotion__`.
- `userestframe=1` produced stable rest transform across frames (`Hips` unchanged frame 1 vs 20).
- `userestframe=0` made rig rest transform time-dependent (`Hips` transform changed frame 1 vs 20).

## Gotchas

- Time-dependent input + `userestframe=0` can cause downstream performance issues due to rig rebuild behavior.
- Missing locomotion joint can break expected behavior in locomotive clip workflows.
- `agentname` is easy to overlook; missing names can cause brittle crowd-type routing later.

## Companion Nodes

- `kinefx::scenecharacterimport` for source skeleton/skin import.
- `agentlayer::2.0` to add render/deform geometry.
- `agentclip::2.0` and KineFX motionclip nodes for animation authoring.
- `kinefx::agentposefromrig` to transfer animated rig poses back to agent instances.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--agentfromrig.txt`
- ✅ Reviewed example: `examples/nodes/sop/kinefx--agentfromrig/AgentFromSOPs.txt`
- ✅ Inspected official network branch: `/obj/academy_AgentFromSOPs/agent_setup`
- ✅ Validated parameter interactions for `createagentname`, `createlocomotionjoint`, and `userestframe`
