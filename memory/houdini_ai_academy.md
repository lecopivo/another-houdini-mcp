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
- Per-node notes location: `memory/nodes/<context>/<node>.md`

## Role of Memory Files

These files are extended, personalized documentation for future work.

- `memory/<context>_context.md`
  - Context-level reference for generalized patterns, heuristics, pitfalls, and cross-node workflows.
  - Should help quickly answer: "How does work typically happen in this context?"

- `memory/nodes/<context>/<node>.md`
  - Node-level reference for reusable setup contracts, key parameter interactions, debug tactics, and production usage guidance.
  - Should help quickly answer: "How do I use this node correctly in real setups?"

- What these files are not:
  - Not chronological logs of actions performed in one scene/session.
  - Not "I clicked X then Y" narratives.

- Recording rule:
  - Convert concrete experiments into transferable lessons: why something failed, how to detect it, and how to fix/prevent it.
  - Put session chronology and restart checkpoints in `short_term_memory.md` only.

## Workflow (Per Node)

1. Pick node from shortlist in `<context>_progress.md`
2. Read official docs in `help/nodes/<context>/<node>.txt`
3. Inspect examples in `help/examples/nodes/<context>/<node>/`
   - if path-based matching misses docs/examples under `help/`, use `search_documentation_files` then `read_documentation_file`
4. Load the `.otl` example in Houdini, create instance, unlock, inspect internals
5. Read instructional metadata inside example networks:
   - node comments
   - sticky notes / post-it notes
6. Inspect meaningful companion nodes used with the target node in the same example network and record reusable patterns
   - if companion findings are substantial, add/update their own node notes under `memory/nodes/<context>/`
7. Before setting parameters during tests, inspect actual parm names first:
   - use `get_node_parameters(..., only_overrides=False)` or `get_parameter_info(...)`
   - avoid guessing tuple names (for example `tx/ty/tz` vs `t`, `divsx/divsy/divsz` vs `divs`)
8. Perform deep live play on the target node (not just smoke check):
   - run baseline probe on a concrete output node
   - change multiple high-impact parameters one at a time
   - probe after each change and capture what changed (topology, attrs, or behavior)
   - include at least one "interaction" test (two parameters together or mode + toggle)
9. Record observed behavior, not just expected behavior
10. Write `memory/nodes/<context>/<node>.md` using `memory/node_study_template.md`
    - Distill observations into generalized guidance, not scene-specific logs.
    - Match the richer reference style used in `memory/nodes/sop/heightfield_erode-2.0.md`:
      - `Intent`
      - `Core Behavior`
      - `Key Parameters` (grouped by subsystem/tab)
      - `Typical Workflow` (with mini graph)
      - `Production Usage` (including measured outcomes)
      - `Gotchas`
      - `Companion Nodes`
      - `Study Validation`
11. Run QA gate from `memory/academy_qa_checklist.md`
12. Update progress files:
    - `memory/houdiin_ai_acedemy_progress.md`
    - `memory/nodes/<context>_progress.md`
13. Update high-level context guide:
    - `memory/<context>_context.md`
    - Add or revise context-level patterns, common pitfalls, and cross-node workflows discovered during node study

## Anti-Sloppy Study Rule

- Do not batch-write generic notes for many nodes after only instantiation checks.
- A node is not considered studied from "load + cook success" alone.
- Complete one node end-to-end before moving to the next:
  1) docs + examples + comments/stickies
  2) deep parameter play with measured before/after observations
  3) write node note immediately
  4) update progress/context/memory
- If multiple nodes are handled in a session, each node must still have independent evidence and findings.

## Node Study Checklist

- Core purpose and where it fits in production workflows
- Clear `Intent` section
- Clear `Core Behavior` section
- Most important parameters and parameter interactions
- `Key Parameters` grouped by subsystem/tab where relevant
- Typical input/output data assumptions
- Typical workflow graph (for example `input -> node -> OUT`)
- Key guidance captured from node comments and sticky notes
- Explicit source-of-truth split:
  - intended behavior (docs/comments/stickies)
  - observed behavior (live network/params/geometry)
  - mismatches if any
- Production guidance and practical defaults where useful
- Measured validation outcomes (counts, attrs, mode behavior, frame behavior)
- Gotchas/failure modes/debug tactics
- Companion/related nodes and when to choose each
- Study validation checklist at end of note

## Definition of Done (Per Node)

A node counts as studied only when all are true:

- Documentation reviewed
- Example OTL(s) reviewed in Houdini
- Node comments and sticky notes reviewed and reflected in notes
- Academy QA checklist completed
- A summary note exists at `memory/nodes/<context>/<node>.md`
- Progress counters updated
- `memory/<context>_context.md` updated with any new context-level insight

## Cadence

- Prefer sequential deep study, one node at a time.
- Optional micro-batches are allowed only if each node is fully completed end-to-end before the next node starts.
- Prefer breadth first (all contexts touched), then depth (high-value contexts)
- Revisit old notes when new context reveals better patterns

## Suggested Priority Order

1. `sop` (largest practical impact)
2. `dop`, `top`, `lop` (simulation/procedural/USD pipelines)
3. `obj`, `vop`, `cop2`
4. `chop`, `out`, `cop`, `shop`
