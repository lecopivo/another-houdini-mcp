
# Quick Start Guide

Get up and running with Houdini MCP in 5 minutes!

## Step 1: Install (2 minutes)

```bash
git clone https://github.com/YOUR_USERNAME/houdini-mcp.git
cd houdini-mcp
./setup.sh
```

## Step 2: Start Houdini (1 minute)

1. Open Houdini
2. Go to `Windows → Python Shell`
3. Paste these lines:

```python
import sys
sys.path.append('/path/to/houdini-mcp')  # Update this path!
from houdini_plugin import HoudiniMCPServer
server = HoudiniMCPServer()
server.start()
```

You should see: ✅ `Houdini MCP Server listening on localhost:9876`

## Step 3: Test It! (2 minutes)

### Option A: Use Claude Code

Open Claude Code and try:
```
Create a cube in Houdini
```

### Option B: Run Example Script

```bash
python3 examples/create_animated_cube.py
```

## What You Can Do

Try these commands in Claude Code:

**Basic Objects:**
```
Create a sphere at position (5, 0, 0)
```

**Animation:**
```
Make the sphere rotate 360 degrees over 48 frames
```

**Complex Effects:**
```
Create a particle system with 3000 points and rainbow colors
```

**Procedural Networks:**
```
Create a scatter node with 1000 points on a sphere,
add color ramp, and make particles pulse over time
```

## Tips

1. **Keep Houdini Plugin Running**: Don't close the Python Shell where you started the server

2. **Press SPACE**: In Houdini viewport to frame your objects

3. **Press PLAY**: To see animations (▶ button at bottom)

4. **Explore Nodes**: Double-click nodes in Network Editor to see inside

5. **Ask Claude**: Natural language works! Just describe what you want

## Troubleshooting

**Can't connect?**
- Make sure Houdini is open
- Make sure the plugin is running (see Step 2)
- Check for "✅ listening on localhost:9876" message

**Nothing appearing?**
- Press U key to go to /obj level in Network Editor
- Look for newly created nodes on the left side

**Errors in Houdini?**
- Check the Python Shell for error messages
- Red exclamation marks on nodes indicate errors
- Click the error icon to see details

## Next Steps

- Read the full [README](README.md) for more examples
- Check out [examples/](examples/) directory
- Try the [particle_system.py](examples/particle_system.py) example
- Read [INSTALL.md](INSTALL.md) for detailed setup

## Need Help?

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Documentation: Check other .md files

Happy creating! 🎨✨
