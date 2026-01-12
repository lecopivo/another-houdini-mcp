# Houdini MCP Server

Control SideFX Houdini directly from Claude Code using the Model Context Protocol (MCP).

This project enables AI-assisted 3D content creation by allowing Claude to create nodes, set parameters, execute HScript commands, and build complex procedural networks in Houdini.

## Features

- **Node Management**: Create, delete, and connect nodes programmatically
- **Parameter Control**: Set and animate node parameters
- **Scene Inspection**: Query scene structure and node information
- **HScript Execution**: Run HScript commands directly in Houdini
- **Real-time Control**: Execute commands while Houdini is running
- **Natural Language Interface**: Describe what you want in plain English

## Architecture

The system consists of two components:

1. **MCP Server** (`houdini_mcp_server.py`): Runs as a Claude Code MCP server, exposes tools to Claude
2. **Houdini Plugin** (`houdini_plugin.py`): Runs inside Houdini, listens for commands via TCP socket

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│ Claude Code │ ◄─MCP──►│ MCP Server       │◄──TCP──►│ Houdini     │
│             │         │ (stdio)          │  :9876  │ Plugin      │
└─────────────┘         └──────────────────┘         └─────────────┘
```

## Requirements

- **Houdini** 19.5 or later (tested with Houdini 21)
- **Python** 3.10+ (included with Houdini)
- **Claude Code** CLI
- **Operating System**: macOS, Linux, or Windows

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/houdini-mcp.git
cd houdini-mcp
```

### 2. Run Setup Script

```bash
./setup.sh
```

The setup script will:
- Detect your Houdini installation
- Install Python dependencies
- Configure Claude Code with the MCP server

### 3. Start the Houdini Plugin

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
Ready to receive commands from Claude Code!
```

## Usage

Once the plugin is running, you can control Houdini from Claude Code using natural language:

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

Claude has access to these tools:

- `create_node(node_type, node_name, parent)` - Create a new node
- `delete_node(node_path)` - Delete a node
- `connect_nodes(source_path, dest_path)` - Connect nodes
- `set_parameter(node_path, param_name, param_value)` - Set parameter values
- `get_scene_info()` - Get information about the scene
- `execute_hscript(code)` - Execute HScript commands

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

### 2. Configure Claude Code

```bash
claude mcp add houdini --transport stdio -- /path/to/houdini/python3 /path/to/houdini_mcp_server.py
```

### 3. Verify Installation

```bash
claude mcp list
claude mcp get houdini
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
claude mcp list

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
├── houdini_mcp_server.py      # MCP server (runs with Claude)
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

- Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/houdini-mcp/issues)
- Discussions: [GitHub Discussions](https://github.com/YOUR_USERNAME/houdini-mcp/discussions)

## Roadmap

- [ ] Support for more Houdini contexts (SOPs, DOPs, COPs, etc.)
- [ ] Viewport rendering and screenshot capture
- [ ] Geometry data export/import
- [ ] Node preset management
- [ ] Multi-session support
- [ ] Web interface for monitoring

---

**Happy procedural modeling with AI! 🎨✨**
