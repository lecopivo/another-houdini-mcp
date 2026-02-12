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

from tool_modules.registry import get_mutating_commands, get_plugin_handlers
from tool_modules.legacy_plugin_methods import LegacyPluginMethods

class HoudiniMCPServer(LegacyPluginMethods):
    _active_server = None
    MUTATING_COMMANDS = get_mutating_commands() | {
        "delete_node",
        "connect_nodes",
        "remove_connection",
        "set_parameter",
        "execute_hscript",
        "execute_python",
        "create_digital_asset",
        "set_hda_lock_state",
        "save_hda_definition",
        "edit_parameter_interface",
        "set_parameter_conditionals",
        "bind_internal_parameters",
        "set_primitive_type_by_token",
        "set_output_node_index",
        "set_hda_parm_templates",
        "set_hda_parm_default",
        "set_hda_internal_binding",
        "set_hda_internal_parm",
        "save_hda_from_instance",
        "instantiate_hda",
    }

    def __init__(self, host="localhost", port=9876):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def start(self):
        """Start the TCP socket server"""
        if self.running:
            return

        if HoudiniMCPServer._active_server is not None and HoudiniMCPServer._active_server is not self:
            try:
                HoudiniMCPServer._active_server.stop()
            except Exception:
                pass

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.running = True
            HoudiniMCPServer._active_server = self

            print(f"✅ Houdini MCP Server listening on {self.host}:{self.port}")
            print("Ready to receive commands from Claude Code!")

            # Start in background thread
            thread = threading.Thread(target=self._accept_connections, daemon=True)
            thread.start()

        except OSError as e:
            print(f"❌ ERROR: Could not start server on port {self.port}")
            print(f"   {e}")
            print("   Is another instance already running?")

    def stop(self):
        """Stop the TCP socket server"""
        self.running = False
        if self.socket is not None:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.socket.close()
            except OSError:
                pass
            self.socket = None
        if HoudiniMCPServer._active_server is self:
            HoudiniMCPServer._active_server = None
        print("🛑 Houdini MCP Server stopped")

    def _accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                if self.socket is None:
                    break

                client_socket, addr = self.socket.accept()
                print(f"📡 Client connected from {addr}")

                # Handle in new thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_thread.start()

            except OSError:
                if not self.running:
                    break
            except Exception as e:
                if self.running:
                    print(f"❌ Connection error: {e}")

    def _handle_client(self, client_socket):
        """Handle client connection"""
        try:
            while self.running:
                # Read length prefix (4 bytes)
                length_bytes = client_socket.recv(4)
                if not length_bytes:
                    break

                message_length = int.from_bytes(length_bytes, byteorder='big')

                # Read the full message in chunks
                data_bytes = b''
                while len(data_bytes) < message_length:
                    chunk = client_socket.recv(min(4096, message_length - len(data_bytes)))
                    if not chunk:
                        break
                    data_bytes += chunk

                data = data_bytes.decode('utf-8')

                try:
                    command = json.loads(data)
                    print(f"📥 Received: {command.get('type')}")

                    result = self._execute_command(command)
                    response = {"status": "success", "result": result}

                except Exception as e:
                    print(f"❌ Error executing command: {e}")
                    response = {"status": "error", "error": str(e)}

                # Send response with length prefix
                response_json = json.dumps(response).encode('utf-8')
                response_length = len(response_json)
                client_socket.send(response_length.to_bytes(4, byteorder='big'))
                client_socket.send(response_json)

        except Exception as e:
            print(f"❌ Client handler error: {e}")
        finally:
            client_socket.close()
            print("📡 Client disconnected")

    def _execute_command(self, command):
        """Execute Houdini commands"""
        cmd_type = command.get("type")
        params = command.get("params", {})

        handler = self._get_handlers().get(cmd_type)
        if handler is None:
            raise ValueError(f"Unknown command: {cmd_type}")

        if cmd_type in self.MUTATING_COMMANDS:
            with hou.undos.group(f"MCP: {cmd_type}"):
                return handler(params)
        return handler(params)

    def _get_handlers(self):
        """Return command handler dispatch table from per-tool modules."""
        return get_plugin_handlers(self, hou)


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
