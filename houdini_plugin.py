#!/usr/bin/env python3
"""
Houdini MCP Plugin
Runs inside Houdini and listens for commands from the MCP server

To use:
1. Open Houdini
2. Go to Windows → Python Shell
3. Run:
   import sys
   sys.path.append('/path/to/houdini-mcp')
   from houdini_plugin import HoudiniMCPServer
   server = HoudiniMCPServer()
   server.start()
"""

import json
import socket
import threading
import sys

try:
    import hou
except ImportError:
    print("ERROR: This script must be run inside Houdini!")
    print("Open Houdini, go to Windows → Python Shell, and run this script")
    sys.exit(1)

class HoudiniMCPServer:
    def __init__(self, host="localhost", port=9876):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def start(self):
        """Start the TCP socket server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.running = True

            print(f"✅ Houdini MCP Server listening on {self.host}:{self.port}")
            print("Ready to receive commands from Claude Code!")

            # Start in background thread
            thread = threading.Thread(target=self._accept_connections, daemon=True)
            thread.start()

        except OSError as e:
            print(f"❌ ERROR: Could not start server on port {self.port}")
            print(f"   {e}")
            print("   Is another instance already running?")

    def _accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                client_socket, addr = self.socket.accept()
                print(f"📡 Client connected from {addr}")

                # Handle in new thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_thread.start()

            except Exception as e:
                if self.running:
                    print(f"❌ Connection error: {e}")

    def _handle_client(self, client_socket):
        """Handle client connection"""
        try:
            while self.running:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break

                try:
                    command = json.loads(data)
                    print(f"📥 Received: {command.get('type')}")

                    result = self._execute_command(command)
                    response = {"status": "success", "result": result}

                except Exception as e:
                    print(f"❌ Error executing command: {e}")
                    response = {"status": "error", "error": str(e)}

                client_socket.send(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print(f"❌ Client handler error: {e}")
        finally:
            client_socket.close()
            print("📡 Client disconnected")

    def _execute_command(self, command):
        """Execute Houdini commands"""
        cmd_type = command.get("type")
        params = command.get("params", {})

        if cmd_type == "create_node":
            return self._create_node(params)
        elif cmd_type == "delete_node":
            return self._delete_node(params)
        elif cmd_type == "connect_nodes":
            return self._connect_nodes(params)
        elif cmd_type == "set_parameter":
            return self._set_parameter(params)
        elif cmd_type == "get_scene_info":
            return self._get_scene_info(params)
        elif cmd_type == "execute_hscript":
            return self._execute_hscript(params)
        else:
            raise ValueError(f"Unknown command: {cmd_type}")

    def _create_node(self, params):
        """Create a new node"""
        node_type = params.get("node_type", "")
        node_name = params.get("node_name", "")
        parent_path = params.get("parent", "/obj")

        parent = hou.node(parent_path)
        if not parent:
            raise ValueError(f"Parent not found: {parent_path}")

        node = parent.createNode(node_type, node_name)
        print(f"✅ Created node: {node.path()}")

        return {
            "node_path": node.path(),
            "node_name": node.name(),
            "node_type": node.type().name()
        }

    def _delete_node(self, params):
        """Delete a node"""
        node_path = params.get("node_path", "")
        node = hou.node(node_path)

        if not node:
            raise ValueError(f"Node not found: {node_path}")

        node.destroy()
        print(f"✅ Deleted node: {node_path}")
        return {"message": f"Deleted: {node_path}"}

    def _connect_nodes(self, params):
        """Connect two nodes"""
        source_path = params.get("source_path", "")
        dest_path = params.get("dest_path", "")
        source_index = params.get("source_index", 0)
        dest_index = params.get("dest_index", 0)

        source = hou.node(source_path)
        dest = hou.node(dest_path)

        if not source or not dest:
            raise ValueError("Source or destination not found")

        dest.setInput(dest_index, source, source_index)
        print(f"✅ Connected {source_path} → {dest_path}")
        return {"message": f"Connected {source_path} to {dest_path}"}

    def _set_parameter(self, params):
        """Set a parameter value"""
        node_path = params.get("node_path", "")
        param_name = params.get("param_name", "")
        param_value = params.get("param_value", "")

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        parm = node.parm(param_name)
        if not parm:
            raise ValueError(f"Parameter not found: {param_name}")

        parm.set(param_value)
        print(f"✅ Set {node_path}.{param_name} = {param_value}")
        return {"message": f"Set {param_name} = {param_value}"}

    def _get_scene_info(self, params):
        """Get scene information"""
        scene = hou.node("/")
        nodes = []

        for node in scene.allSubChildren():
            nodes.append({
                "path": node.path(),
                "name": node.name(),
                "type": node.type().name()
            })

        return {
            "num_nodes": len(nodes),
            "nodes": nodes,
            "file_path": hou.hipFile.path() if hou.hipFile.path() else "untitled"
        }

    def _execute_hscript(self, params):
        """Execute HScript commands"""
        code = params.get("code", "")

        try:
            result = hou.hscript(code)
            return {"output": result[0], "error": result[1]}
        except Exception as e:
            raise ValueError(f"HScript failed: {str(e)}")

# Start the server
if __name__ == "__main__":
    # Check if already running
    if 'houdini_mcp_server' in globals():
        print("⚠️  Server already running! Use houdini_mcp_server.running = False to stop it")
    else:
        server = HoudiniMCPServer()
        server.start()

        # Store in global so it persists
        globals()['houdini_mcp_server'] = server

        print("\n" + "="*60)
        print("Houdini MCP Plugin is running!")
        print("You can now use Claude Code to control Houdini")
        print("="*60)
        print("\nTo stop: houdini_mcp_server.running = False")
        print("="*60 + "\n")
