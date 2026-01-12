# Installation Guide

Complete installation instructions for Houdini MCP Server.

## Prerequisites

### Required Software

- **Houdini** 19.5 or later (tested with Houdini 21)
  - Download from [sidefx.com](https://www.sidefx.com/download/)
  - Apprentice, Indie, or Commercial versions supported

- **Claude Code** CLI
  - Install from [claude.com/claude-code](https://claude.com/claude-code)

- **Python** 3.10+ (included with Houdini)

### System Requirements

- **macOS**: 10.14 or later
- **Linux**: Ubuntu 18.04+ or equivalent
- **Windows**: Windows 10 or later

## Installation Methods

### Method 1: Automatic Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/houdini-mcp.git
   cd houdini-mcp
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

   The script will:
   - Detect your Houdini installation
   - Install Python dependencies
   - Configure Claude Code MCP server

3. **Verify installation:**
   ```bash
   claude mcp list
   ```

   You should see `houdini` in the list with status `✓ Connected`

### Method 2: Manual Setup

If the automatic setup doesn't work for your system:

#### Step 1: Find Houdini Python

**macOS:**
```bash
/Applications/Houdini/Current/Frameworks/Python.framework/Versions/Current/bin/python3
```

**Linux:**
```bash
/opt/hfs/current/python/bin/python3
```

**Windows:**
```powershell
C:\Program Files\Side Effects Software\Houdini <version>\python39\python.exe
```

#### Step 2: Install Dependencies

```bash
<houdini-python-path> -m pip install fastmcp httpx --user
```

#### Step 3: Configure Claude Code

```bash
claude mcp add houdini --transport stdio -- <houdini-python-path> <path-to>/houdini_mcp_server.py
```

Example:
```bash
claude mcp add houdini --transport stdio -- \
  /Applications/Houdini/Current/Frameworks/Python.framework/Versions/Current/bin/python3 \
  /path/to/houdini-mcp/houdini_mcp_server.py
```

#### Step 4: Verify

```bash
claude mcp get houdini
```

## Starting the Houdini Plugin

After installation, you need to run the plugin inside Houdini:

1. **Open Houdini**

2. **Open Python Shell:**
   - Go to `Windows → Python Shell`

3. **Load the plugin:**
   ```python
   import sys
   sys.path.append('/path/to/houdini-mcp')  # Replace with your actual path
   from houdini_plugin import HoudiniMCPServer
   server = HoudiniMCPServer()
   server.start()
   ```

4. **Verify it's running:**
   You should see:
   ```
   ✅ Houdini MCP Server listening on localhost:9876
   Ready to receive commands from Claude Code!
   ```

## Testing the Installation

### Test 1: Connection Test

```bash
cd houdini-mcp
python3 examples/test_connection.py
```

Expected output:
```
✅ Connected successfully!
✅ Command executed successfully!
📊 Scene Information:
   File: untitled.hip
   Total nodes: 9
```

### Test 2: Create Animated Cube

```bash
python3 examples/create_animated_cube.py
```

In Houdini:
- You should see a new `animated_cube` node
- Press SPACE to frame the view
- Press PLAY to see animation

### Test 3: Claude Code Integration

In Claude Code, try:
```
Create a sphere in Houdini
```

If everything is working, Claude will create a sphere in your Houdini scene!

## Platform-Specific Notes

### macOS

- Houdini is typically installed in `/Applications/Houdini/`
- If you have multiple Houdini versions, `/Applications/Houdini/Current` points to the default version
- Make sure you have Xcode Command Line Tools installed

### Linux

- Houdini is typically installed in `/opt/hfs<version>/`
- You may need to source the Houdini environment:
  ```bash
  source /opt/hfs<version>/houdini_setup
  ```

### Windows

- Houdini is typically installed in `C:\Program Files\Side Effects Software\`
- Use PowerShell or Git Bash for the installation
- Replace forward slashes with backslashes in paths

## Troubleshooting

### "Cannot find Houdini installation"

Set the `HOUDINI_PYTHON` environment variable:
```bash
export HOUDINI_PYTHON=/path/to/houdini/python3
./setup.sh
```

### "Claude command not found"

Install Claude Code CLI:
1. Download from [claude.com/claude-code](https://claude.com/claude-code)
2. Follow the installation instructions
3. Verify: `claude --version`

### "Address already in use"

Another instance is running:
1. Check if Houdini plugin is already loaded
2. Restart Houdini
3. Try again

### "Module 'hou' not found"

You're not using Houdini's Python:
- Make sure you're using the Python that comes with Houdini
- Don't use your system Python or a virtual environment

### Permission Errors

On macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

## Uninstallation

To remove Houdini MCP:

```bash
claude mcp remove houdini
```

To remove Python packages:
```bash
<houdini-python> -m pip uninstall fastmcp httpx
```

## Next Steps

- Read the [README](README.md) for usage examples
- Check out [examples/](examples/) for sample scripts
- Join discussions on GitHub

## Getting Help

- GitHub Issues: Report bugs and request features
- GitHub Discussions: Ask questions and share tips
- Documentation: Check the README for more information
