# Yet Another Houdini MCP Server

Control SideFX Houdini directly from AI coding clients using the Model Context Protocol (MCP).

This project enables AI-assisted 3D content creation by allowing your MCP client to create nodes, set parameters, execute Pythong/HScript commands, and build complex procedural networks in Houdini.

(This is a fork of [Houdini-claudecode-mcp](https://github.com/atayilgun/Houdini-claudecode-mcp) but I didn't like the name and it does not target Claude only)

## Installation

### 1. Clone the Repository

```bash
https://github.com/lecopivo/another-houdini-mcp
cd another-houdini-mcp
```

### 2. Run Setup Script

```bash
./setup.sh
```

The setup script will:
- Detect your Houdini installation
- Copy `$HFS/houdini/help` into local `help/` (excluding `videos/`, `examples/`, `files/`, `images.zip`) and unpack all `help/*.zip`
- Install Python dependencies
- Install an `AI Chat` shelf tab with a `Restart Server` tool and per-client launcher tools in your Houdini user preferences
- Detect installed MCP-capable AI clients and prompt to install for each one

### 3. Use

Start Houdini, enable `AI Chat` shelf:
![Turn on AI Chat shelf][icons/shelf.png]

Click on one of the available AI clients:
![Click on client][icons/shelf2.png]

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Based on [Houdini-claudecode-mcp](https://github.com/atayilgun/Houdini-claudecode-mcp)
- Another Houdini MCP [capoomgit/houdini-mcp](https://github.com/capoomgit/houdini-mcp)
- Refined version [kleer001/houdini-mcp](https://github.com/kleer001/houdini-mcp)
