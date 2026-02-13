# AGENTS.md

## What This MCP Does
This project provides a Houdini MCP server and plugin that let an agent inspect, build, edit, and validate Houdini scenes and HDAs programmatically.

You can use it to:
- Explore scene structure and node connections
- Create/delete/connect nodes
- Read/set node parameters
- Execute HScript or Python (HOM) when needed
- Inspect local Houdini documentation in `help/`
- Build validation workflows around geometry and node behavior

## Tools Available

### Scene and Node Exploration
- `get_folder_info`
- `get_node_info`
- `get_node_presentation`
- `get_node_connections`
- `get_scene_info`
- `get_sticky_notes`

### Node Graph Editing
- `create_node`
- `delete_node`
- `connect_nodes`
- `remove_connection`
- `set_parameter`

### Example and HDA Loading
- `install_hda_file`
- `list_example_nodes`
- `instantiate_example_asset`
- `load_example`
- `instantiate_hda`

### Node and Parameter Discovery
- `list_node_categories`
- `list_node_types`
- `get_parameter_info`
- `get_node_parameters`
- `get_parameter_overrides`
- `get_node_documentation`

### Python/HScript Execution
- `execute_python`
- `execute_hscript`

### HOM (Python API) Documentation
- `list_python_commands`
- `search_python_documentation`
- `get_python_documentation`

### Local Documentation File Tools (`help/`)
- `search_documentation_files`
- `read_documentation_file`

## Documentation Expectations
- Before implementing or changing behavior, look up relevant docs.
- Use documentation tools first, then fallback to ad-hoc scripts.
- The project documentation corpus is in `help/`.

## Tutorials Expectations
- Review `memory/index.md` first to refresh workflow memory.
- Use relevant files in `memory/` before inventing a new approach.
- When working in a specific context (for example SOP), refresh context memory first by reading `memory/<context>_context.md` (for example `memory/sop_context.md`).
- When working on a specific node, refresh node memory first by reading `memory/nodes/<context>/<node>.md` if it exists.
- Treat `memory/<context>_context.md` and `memory/nodes/<context>/<node>.md` as extended documentation, not activity logs.
- `memory/<context>_context.md` should contain generalized context-level rules, patterns, heuristics, pitfalls, and cross-node workflows.
- `memory/nodes/<context>/<node>.md` should contain reusable node-level guidance: intent, setup contracts, parameter interactions, debug tactics, and production usage notes.
- Do not record raw chronological "what I clicked/did" logs in these files; abstract concrete experiences into general lessons.
- If an experiment reveals a failure mode, record the transferable rule (why it failed, how to detect, how to fix), not scene-specific narration.
- Keep session chronology and restart checkpoints in `short_term_memory.md` only.
- When reviewing an example scene for a target node, inspect all meaningful companion nodes in that example network (not just the target node) and capture reusable patterns in memory notes.
- If companion-node findings are strong enough, add or update their own `memory/nodes/<context>/<node>.md` files even if they were not the primary study target.
- Do not defer companion-node note updates: while studying one node, proactively edit other node memory notes in the same session when you discover meaningful behavior, patterns, parameters, or edge cases.
- If you struggle with something and then finally solve it, suggest updating the appropriate tutorial in `memory/` with that lesson.

## Tooling Improvement Expectations
- If you struggle to perform a repeated task and finally manage it via custom scripting/workarounds, suggest adding or improving a dedicated MCP tool.
- Tool additions/updates should be implemented as per-tool modules under `tool_modules/`.
- Register new tool modules in `tool_modules/registry.py` (module import + `TOOL_MODULES` entry).
- In this architecture, routine tool additions usually do **not** require edits to `houdini_plugin.py` or `houdini_mcp_server.py`.
- Edit `houdini_plugin.py` / `houdini_mcp_server.py` only for framework-level behavior changes (transport, server lifecycle, global wiring/instructions, etc.).
- Prefer proposing reusable, general-purpose tools over one-off script snippets.

## Session Memory Expectations
- When implementing new tools or changing tool behavior, record current progress and restart checkpoints in `short_term_memory.md`.
- The user may restart the agent at any time; always keep `short_term_memory.md` up to date so work can resume immediately.
