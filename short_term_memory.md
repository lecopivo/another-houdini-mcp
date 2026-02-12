## Short-Term Memory

- Runtime behavior uses the currently running Houdini Python process.
- Edits to `houdini_plugin.py` do not take effect until the Houdini MCP server is restarted (or Houdini is restarted).

### Patched

- `houdini_plugin.py` `get_node_info`:
  - Removed `node.isLocked()` usage (invalid on many non-HDA nodes).
  - Lock state now applies only to HDA-backed nodes:
    - `is_hda = node.type().definition() is not None`
    - `is_locked = bool(node.isLockedHDA())` for HDA nodes
    - `is_locked = None` for non-HDA nodes (not applicable)
  - `position` is now serialized as `[x, y]` list (JSON-safe).

- `houdini_plugin.py` `get_node_connections`:
  - Output destination mapping uses `conn.outputNode()` (correct downstream node for `node.outputConnections()`).

- `houdini_mcp_server.py` `get_node_info` formatting:
  - Shows lock as `N/A (non-HDA)` when `is_locked` is `None`.

### Known test scene

- `/obj/mcp_verify1/box1 -> /obj/mcp_verify1/null1`

### After restart, re-test first

1. `get_node_info('/obj/mcp_verify1/box1')`
   - Expect no crash and `Locked: N/A (non-HDA)`.
2. `get_node_connections('/obj/mcp_verify1/box1')`
   - Expect output `[0] -> /obj/mcp_verify1/null1 (input 0)`.

### Verification status (2026-02-12)

- Re-tested in active runtime:
  - `get_node_info('/obj/mcp_verify1/box1')` returns successfully with `Locked: N/A (non-HDA)`.
  - `get_node_connections('/obj/mcp_verify1/box1')` reports `[0] -> /obj/mcp_verify1/null1 (input 0)`.
- These fixes are confirmed working in the currently connected Houdini session.
