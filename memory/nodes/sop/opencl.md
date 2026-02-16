# OpenCL (SOP)

## Intent

`opencl` runs custom OpenCL kernels over geometry/attributes/volumes, enabling high-performance GPU/CPU compute directly inside SOP networks.

## Core Behavior

- Compiles and executes user-provided kernels from snippet or external file.
- Binds constants, ramps, attributes, volumes, and VDBs to kernel parameters by order.
- Supports optional write-back second-pass kernel to avoid race-condition write hazards.
- Supports iteration loops and workset-driven execution patterns.

## Key Parameters

- Kernel source controls: `usecode`, `kernelfile`, `kernelcode`, `kernelname`, `kerneloptions`.
- Compile/runtime controls: `recompile`, precision mode, finish behavior.
- Execution domain: `runover`, workset attrs, `iterations`, time/timestep injection.
- Binding table controls: parameter type/class/read-write/optional/default behavior.
- Safety/perf: force alignment for volumes, optional attributes, workgroup optimization.

## Typical Workflow

```text
geometry/volume -> opencl (custom kernel) -> downstream SOP evaluation
```

- Start from generated kernel signature, then iteratively bind only necessary read/write data.
- Disable `recompile` after development to avoid heavy recook costs.

## Production Usage

- High-value for custom accelerators where VEX/VOP pipelines are insufficient or too slow.
- `SimpleOpenCLSOPSnippets` example demonstrates attribute and volume/VDB manipulation via snippet kernels.

Measured outcomes:
- Live Houdini kernel execution measurements are pending in this session.

## Gotchas

- Binding is positional, not name-based; mismatched order silently breaks logic.
- Optional/default bindings change function signature; regenerate kernel stubs after table edits.
- Frequent compile-option changes can trigger expensive recompiles.

## Companion Nodes

- `gasopencl` for DOP-side OpenCL acceleration.
- `attribcast` for precision control feeding OpenCL binds.
- VDB/volume SOPs for bound field workflows.

## Study Validation

- ✅ Read docs: `help/nodes/sop/opencl.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/opencl/SimpleOpenCLSOPSnippets.txt`
- ⏳ Live validation pending
