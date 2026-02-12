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
- `get_node_connections`
- `get_scene_info`

### Node Graph Editing
- `create_node`
- `delete_node`
- `connect_nodes`
- `remove_connection`
- `set_parameter`

### Node and Parameter Discovery
- `list_node_categories`
- `list_node_types`
- `get_parameter_info`
- `get_node_parameters`
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
- Review `tutorials/index.md` first to refresh workflow memory.
- Use relevant files in `tutorials/` before inventing a new approach.
- If you struggle with something and then finally solve it, suggest updating the appropriate tutorial in `tutorials/` with that lesson.

## Tooling Improvement Expectations
- If you struggle to perform a repeated task and finally manage it via custom scripting/workarounds, suggest adding or improving a dedicated MCP tool.
- Tool additions/updates must be kept in sync across both files:
  - `houdini_plugin.py` (command implementation/dispatch)
  - `houdini_mcp_server.py` (MCP tool exposure/wrapper)
- Prefer proposing reusable, general-purpose tools over one-off script snippets.

## Session Memory Expectations
- When implementing new tools or changing tool behavior, record current progress and restart checkpoints in `short_term_memory.md`.
- The user may restart the agent at any time; always keep `short_term_memory.md` up to date so work can resume immediately.
