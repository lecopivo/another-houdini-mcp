# Houdini MCP Server

Control SideFX Houdini directly from AI coding clients using the Model Context Protocol (MCP).

This project enables AI-assisted 3D content creation by allowing your MCP client to create nodes, set parameters, execute HScript commands, and build complex procedural networks in Houdini.

## Features

### 🚀 Unlimited Power - Do ANYTHING in Houdini!

This tool gives your MCP client **full access** to Houdini's capabilities:

- **ALL Contexts**: SOPs, DOPs, COPs, CHOPs, VOPs, ROPs, LOPs - Everything!
- **Any Node Type**: Geometry, simulations, compositing, animation, rendering
- **Full HScript Access**: Execute any Houdini command with `execute_hscript`
- **VEX Code**: Write custom procedural logic inline
- **Simulations**: Particles, fluids, pyro, cloth, RBD, crowds
- **Complex Networks**: Build intricate procedural systems
- **Real-time Control**: Execute commands while Houdini is running
- **Natural Language**: Just describe what you want in plain English

### Core MCP Tools

- **Node Management**: Create, delete, and connect nodes programmatically
- **Parameter Control**: Set and animate node parameters with expressions
- **Scene Inspection**: Query scene structure and node information
- **HScript Execution**: Run ANY HScript command directly in Houdini
- **Network Building**: Connect complex node chains automatically

## Architecture

The system consists of two components:

1. **MCP Server** (`houdini_mcp_server.py`): Runs as a stdio MCP server, exposes tools to your AI client
2. **Houdini Plugin** (`houdini_plugin.py`): Runs inside Houdini, listens for commands via TCP socket

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│ AI Client   │ ◄─MCP──►│ MCP Server       │◄──TCP──►│ Houdini     │
│             │         │ (stdio)          │  :9876  │ Plugin      │
└─────────────┘         └──────────────────┘         └─────────────┘
```

## Requirements

- **Houdini** 19.5 or later (tested with Houdini 21)
- **Python** 3.10+ (included with Houdini)
- **MCP-capable AI client CLI** (for example: `claude`, `codex`, `opencode`)
- **Operating System**: macOS, Linux, or Windows

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/atayilgun/Houdini-claudecode-mcp.git
cd Houdini-claudecode-mcp
```

### 2. Run Setup Script

```bash
./setup.sh
```

The setup script will:
- Detect your Houdini installation
- Copy `$HFS/houdini/help` into local `help/` (excluding `videos/`, `examples/`, `files/`, `images.zip`) and unpack all `help/*.zip`
- Install Python dependencies
- Optionally install an `AI Chat` shelf tab with a `Restart Server` tool and per-client launcher tools in your Houdini user preferences
- Detect installed MCP-capable AI clients and prompt to install for each one

### 3. Start the Houdini Plugin

You can either use the `AI Chat` shelf tab (`Restart Server` and client launchers) if you installed it during setup, or run manually:

1. **Open Houdini**
2. Go to **Windows → Python Shell**
3. Run these commands in the Python Shell:

```python
import sys
sys.path.append('/path/to/houdini-mcp')  # Replace with your actual path
from houdini_plugin import HoudiniMCPServer
server = HoudiniMCPServer()
server.start()
```

You should see:
```
✅ Houdini MCP Server listening on localhost:9876
Ready to receive commands from your AI client!
```

## Usage

Once the plugin is running, you can control Houdini from your AI client using natural language:

### Basic Examples

**Create objects:**
```
Create a cube in Houdini
```

**Multiple objects:**
```
Create a sphere at position (5, 0, 0) and a cube at the origin
```

**Animation:**
```
Make the cube move from X=0 to X=10 over 48 frames
```

**Complex procedural setups:**
```
Create a particle system with 5000 points scattered on a sphere,
add colorful gradients, and make them flow like wind
```

### Available MCP Tools

Your AI client has access to these tools:

**Node Management:**
- `create_node(node_type, node_name, parent)` - Create a new node
- `delete_node(node_path)` - Delete a node
- `connect_nodes(source_path, dest_path)` - Connect nodes

**Parameter Control:**
- `set_parameter(node_path, param_name, param_value)` - Set parameter values
- `get_node_parameters(node_path, show_defaults)` - Get all parameters and values from a node
- `get_parameter_info(node_type, category)` - Get available parameters for a node type

**Scene & Node Inspection:**
- `get_scene_info()` - Get information about the scene
- `get_node_info(node_path)` - Get detailed information about a specific node

**Advanced:**
- `execute_hscript(code)` - Execute HScript commands

### New in This Version

The latest update adds powerful parameter inspection tools that make it much easier to work with Houdini nodes:

**Before:** You had to know the exact parameter names (like `radx`, `rady`, `radz` for sphere radius)

**Now:** You can:
1. Query what parameters a node type supports with `get_parameter_info('sphere')`
2. See all current parameter values with `get_node_parameters('/obj/geo1/sphere1')`
3. Get detailed node information including connections with `get_node_info('/obj/geo1')`

This makes it much easier to:
- Discover correct parameter names before setting them
- Debug why parameters aren't working as expected
- Understand existing scenes and nodes
- Build complex procedural setups without memorizing parameter names

## Examples

See the `examples/` directory for Python scripts that demonstrate various capabilities:

- `create_animated_cube.py` - Basic animation example
- `particle_system.py` - Advanced particle effects
- `procedural_network.py` - Building complex node networks

## Manual Setup (Alternative)

If the setup script doesn't work for your system:

### 1. Install Dependencies

```bash
# Using Houdini's Python
/path/to/houdini/python3 -m pip install fastmcp httpx --user
```

### 2. Configure Your AI Client

Claude Code:

```bash
claude mcp add houdini --transport stdio -- /path/to/houdini/python3 /path/to/houdini_mcp_server.py
```

Codex:

```bash
codex mcp add houdini -- /path/to/houdini/python3 /path/to/houdini_mcp_server.py
```

OpenCode (`opencode.json` in your project):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "houdini": {
      "type": "local",
      "command": ["/path/to/houdini/python3", "/path/to/houdini_mcp_server.py"],
      "enabled": true
    }
  }
}
```

### 3. Verify Installation

```bash
<client> mcp list
# Optional (supported by some clients like claude/codex)
<client> mcp get houdini
```

## Troubleshooting

### Port Already in Use

If you see `Address already in use` error:
- Make sure no other instance of the plugin is running
- Change the port in both `houdini_mcp_server.py` and `houdini_plugin.py`

### Cannot Connect to Houdini

- Verify Houdini is running
- Verify the plugin is loaded in Houdini's Python Shell
- Check firewall settings

### MCP Server Not Found

```bash
# Check if server is registered
<client> mcp list

# If not listed, run setup again
./setup.sh
```

### Python Import Errors

Make sure you're using Houdini's Python, not your system Python:
```bash
/Applications/Houdini/Current/Frameworks/Python.framework/Versions/Current/bin/python3 --version
```

## Development

### Project Structure

```
houdini-mcp/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── setup.sh                    # Installation script
├── houdini_mcp_server.py      # MCP server (runs with your AI client)
├── houdini_plugin.py          # Plugin (runs in Houdini)
└── examples/                  # Example scripts
    ├── create_animated_cube.py
    ├── particle_system.py
    └── procedural_network.py
```

### Running Tests

Test the connection:
```python
python3 examples/test_connection.py
```

### Adding New Tools

To add a new MCP tool:

1. Add the tool decorator and function in `houdini_mcp_server.py`:
```python
@mcp.tool()
def your_new_tool(param1: str, param2: int) -> str:
    """Tool description"""
    result = send_command({
        "type": "your_command",
        "params": {"param1": param1, "param2": param2}
    })
    return f"Result: {result}"
```

2. Add the command handler in `houdini_plugin.py`:
```python
def _execute_command(self, command):
    cmd_type = command.get("type")
    if cmd_type == "your_command":
        return self._your_command_handler(command.get("params", {}))
```

## Security Considerations

- The plugin accepts commands from localhost only by default
- HScript execution should be used carefully as it runs code directly in Houdini
- Always review generated code before executing
- Consider network security if opening to non-localhost connections

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Powered by [Anthropic's Model Context Protocol](https://modelcontextprotocol.io/)
- Made for [SideFX Houdini](https://www.sidefx.com/)

## Support

- Issues: [GitHub Issues](https://github.com/atayilgun/Houdini-claudecode-mcp/issues)
- Discussions: [GitHub Discussions](https://github.com/atayilgun/Houdini-claudecode-mcp/discussions)

## What Can It Do?

**Short answer: EVERYTHING!**

The tool already has full access to Houdini through `execute_hscript` and can:

✅ **Create any node in any context** (SOPs, DOPs, COPs, CHOPs, VOPs, etc.)
✅ **Build simulations** (Pyro, FLIP fluids, RBD, Vellum, Wire, etc.)
✅ **Composite images** (COP networks, color correction, effects)
✅ **Animate anything** (Keyframes, CHOPs, expressions, motion paths)
✅ **Write VEX code** (Custom attributes, procedural geometry, deformers)
✅ **Manage renders** (ROPs, render settings, batch rendering)
✅ **Query scene data** (Node info, parameter values, geometry attributes)
✅ **Execute Python in Houdini** (Via HScript's python command)

**Example capabilities:**
- "Create a pyro explosion simulation"
- "Set up a FLIP water tank with collision objects"
- "Build a procedural building generator with multiple levels"
- "Create a particle system with custom VEX forces"
- "Set up a COP network to add glow and color grade"

## Future Enhancements

These are convenience features, not limitations:

- [ ] Direct viewport rendering API (currently use HScript)
- [ ] Binary geometry data transfer (currently use file I/O)
- [ ] Node preset library management
- [ ] Multi-session support for team workflows
- [ ] Web dashboard for monitoring

---

**Happy procedural modeling with AI! 🎨✨**
