# Agent Pose from Rig (SOP, KineFX)

## Intent

`kinefx::agentposefromrig` transfers pose data from a SOP skeleton to agent primitives by matching joint names. It is the bridge node for editing/retargeting agent pose in SOP rig tools, then pushing that pose back onto crowd agents.

## Core Behavior

- Input 0: agent primitives to modify.
- Input 1: source skeleton pose to transfer.
- Input 2 (optional): reference skeleton used for delta transfer (reference->current pose difference).
- Keeps agent primitive topology/count stable; updates pose channels and/or root transform behavior.
- Supports scoped updates by agent group, joint pattern, and channel pattern.

## Key Parameters

- `group`: which agent primitives to update.
- `joints`: joint name pattern to limit transfer scope.
- `channels`: channel pattern to filter transferred channels.
- `roottransformmode`:
  - transfer root to primitive transform,
  - apply to root joint,
  - ignore root transfer.
- `rootjoint`: explicit root choice when root-to-primitive mode needs disambiguation.

## Typical Workflow

```text
agent -> agentanimationunpack -> rigpose (or other KineFX edits)
      -> agentposefromrig -> agentclip (optional clip bake/update)
```

- Unpack pose for edit in SOP rig tools.
- Apply pose edits.
- Transfer edited pose back to selected agents.
- Optionally bake/update clips downstream with `agentclip`.

## Production Usage

- Use `group` aggressively to avoid unintentionally updating all agents.
- Use `roottransformmode` deliberately based on whether root motion should move the agent point/primitive or remain in skeleton space.
- Use `joints` for partial-body edits (for example upper-body overrides).

Measured outcomes from `/obj/academy_TransferPoseToAgent/crowd` (after fixing broken loaded asset path refs):
- Geometry contract stayed constant across variants: `5 points / 5 Agent prims` with attrs `P`, `clipoffset`, `agentname`.
- Example nodes use `group="1 3"`; only those agents are modified.
- Root transform mode differences:
  - `roottransformmode=0` changed agent point transforms (agents 1 and 3 moved in `P`, including Y offset).
  - `roottransformmode=1` kept point positions but changed root joint placement in rig space.
  - `roottransformmode=2` ignored root transfer (point positions remained like source agents).
- Joint filtering check:
  - `joints=NoSuchJoint*` produced no pose transfer for selected agents (hips values stayed at source-agent values).
- Reference input check:
  - In this official setup, `agentposefromrig5` (with reference skeleton input) matched `agentposefromrig3` transform results for tested agents/joints.

## Gotchas

- Example assets loaded under renamed OBJ containers may contain stale internal object paths; this can make geometry evaluate as `None` until fixed.
  - In this example, `agent1.objsubnet` and `agent1.locomotionnode` had to be repointed to `/obj/academy_TransferPoseToAgent/...`.
- Root mode misunderstanding is a common source of "my agent moved / did not move" confusion.
- Empty/no-op transfers are often selector mismatches (`group`, `joints`, `channels`) rather than solver failure.

## Companion Nodes

- `kinefx::agentanimationunpack` to extract SOP skeleton pose from agents.
- `kinefx::rigpose` (and other KineFX rig nodes) for pose edits.
- `agentclip::2.0` to bake/update reusable clips after transfer.
- `kinefx::agentfromrig` for initial agent-definition creation from skeleton rigs.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--agentposefromrig.txt`
- ✅ Reviewed example: `examples/nodes/sop/kinefx--agentposefromrig/TransferPoseToAgent.txt`
- ✅ Inspected official network: `/obj/academy_TransferPoseToAgent/crowd`
- ✅ Validated root-transform mode behavior and selector gating (`group`, `joints`)
- ✅ Verified/recorded real-world asset-path failure mode and fix
