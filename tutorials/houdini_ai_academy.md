# Houdini AI Academy

## Goal

Build practical, reusable understanding of all Houdini node contexts by studying:

1. Official node documentation in `help/nodes/<context>/<node>.txt`
2. Official example assets in `help/examples/nodes/<context>/<node>/*.otl`
3. Hands-on behavior in Houdini after loading/unlocking the example OTLs

The output of this work is a context-wide progress record plus one practical tutorial note per studied node.

## Scope

- Contexts covered: `chop`, `cop`, `cop2`, `dop`, `lop`, `obj`, `out`, `shop`, `sop`, `top`, `vop`
- Node selection source: `help/examples/nodes/<context>/`
- Per-node notes location: `tutorials/nodes/<context>/<node>.md`

## Workflow (Per Node)

1. Pick node from shortlist in `<context>_progress.md`
2. Read official docs in `help/nodes/<context>/<node>.txt`
3. Inspect examples in `help/examples/nodes/<context>/<node>/`
4. Load the `.otl` example in Houdini, create instance, unlock, inspect internals
5. Test variations and record observed behavior, not just expected behavior
6. Write `tutorials/nodes/<context>/<node>.md`
7. Update progress files:
   - `tutorials/houdiin_ai_acedemy_progress.md`
   - `tutorials/nodes/<context>_progress.md`
8. Update high-level context guide:
   - `tutorials/<context>_context.md`
   - Add or revise context-level patterns, common pitfalls, and cross-node workflows discovered during node study

## Node Study Checklist

- Core purpose and where it fits in production workflows
- Most important parameters and parameter interactions
- Typical input/output data assumptions
- Minimum reproducible setup
- At least 2 practical use cases
- Gotchas/failure modes/debug tactics
- Related nodes and when to choose each

## Definition of Done (Per Node)

A node counts as studied only when all are true:

- Documentation reviewed
- Example OTL(s) reviewed in Houdini
- A summary note exists at `tutorials/nodes/<context>/<node>.md`
- Progress counters updated
- `tutorials/<context>_context.md` updated with any new context-level insight

## Cadence

- Work in batches of 3-8 nodes per session
- Prefer breadth first (all contexts touched), then depth (high-value contexts)
- Revisit old notes when new context reveals better patterns

## Suggested Priority Order

1. `sop` (largest practical impact)
2. `dop`, `top`, `lop` (simulation/procedural/USD pipelines)
3. `obj`, `vop`, `cop2`
4. `chop`, `out`, `cop`, `shop`
