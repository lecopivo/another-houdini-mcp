# The Other Houdini MCP Server

Control SideFX Houdini directly from AI coding clients using the Model Context Protocol (MCP).

This project enables AI-assisted 3D content creation by allowing your MCP client to create nodes, set parameters, execute Pythong/HScript commands, and build complex procedural networks in Houdini.

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

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Based on [Houdini-claudecode-mcp](https://github.com/atayilgun/Houdini-claudecode-mcp)
- Another Houdini MCP [capoomgit/houdini-mcp](https://github.com/capoomgit/houdini-mcp)
- Refined version [kleer001/houdini-mcp](https://github.com/kleer001/houdini-mcp)
