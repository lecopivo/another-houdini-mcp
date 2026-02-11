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

        if cmd_type == "create_node":
            return self._create_node(params)
        elif cmd_type == "delete_node":
            return self._delete_node(params)
        elif cmd_type == "connect_nodes":
            return self._connect_nodes(params)
        elif cmd_type == "remove_connection":
            return self._remove_connection(params)
        elif cmd_type == "set_parameter":
            return self._set_parameter(params)
        elif cmd_type == "get_scene_info":
            return self._get_scene_info(params)
        elif cmd_type == "get_node_info":
            return self._get_node_info(params)
        elif cmd_type == "get_node_parameters":
            return self._get_node_parameters(params)
        elif cmd_type == "get_parameter_info":
            return self._get_parameter_info(params)
        elif cmd_type == "list_node_categories":
            return self._list_node_categories(params)
        elif cmd_type == "list_node_types":
            return self._list_node_types(params)
        elif cmd_type == "get_node_documentation":
            return self._get_node_documentation(params)
        elif cmd_type == "get_node_connections":
            return self._get_node_connections(params)
        elif cmd_type == "get_folder_info":
            return self._get_folder_info(params)
        elif cmd_type == "execute_hscript":
            return self._execute_hscript(params)
        elif cmd_type == "list_python_commands":
            return self._list_python_commands(params)
        elif cmd_type == "get_python_documentation":
            return self._get_python_documentation(params)
        elif cmd_type == "execute_python":
            return self._execute_python(params)
        elif cmd_type == "search_python_documentation":
            return self._search_python_documentation(params)
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
        """Connect two nodes with specific input/output indices"""
        source_path = params.get("source_path", "")
        dest_path = params.get("dest_path", "")
        source_index = params.get("source_index", 0)
        dest_index = params.get("dest_index", 0)

        source = hou.node(source_path)
        dest = hou.node(dest_path)

        if not source or not dest:
            raise ValueError("Source or destination not found")

        dest.setInput(dest_index, source, source_index)
        print(f"✅ Connected {source_path}[{source_index}] → {dest_path}[{dest_index}]")
        return {"message": f"Connected {source_path}[output {source_index}] to {dest_path}[input {dest_index}]"}

    def _remove_connection(self, params):
        """Remove a specific connection between two nodes"""
        dest_path = params.get("dest_path", "")
        dest_index = params.get("dest_index", 0)

        dest = hou.node(dest_path)
        if not dest:
            raise ValueError(f"Destination node not found: {dest_path}")

        # Check if there's a connection at this input
        current_input = dest.input(dest_index)
        if not current_input:
            raise ValueError(f"No connection at {dest_path} input {dest_index}")

        # Get the source info before disconnecting for logging
        source_path = current_input.path()

        # Find the source output index
        source_output_idx = 0
        for conn in current_input.outputConnections():
            if conn.inputNode() == dest and conn.inputIndex() == dest_index:
                source_output_idx = conn.outputIndex()
                break

        # Disconnect by setting input to None
        dest.setInput(dest_index, None)
        print(f"✅ Removed connection {source_path}[{source_output_idx}] → {dest_path}[{dest_index}]")
        return {
            "message": f"Removed connection from {source_path}[output {source_output_idx}] to {dest_path}[input {dest_index}]",
            "source_path": source_path,
            "source_index": source_output_idx,
            "dest_path": dest_path,
            "dest_index": dest_index
        }

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

    def _get_node_info(self, params):
        """Get detailed information about a node"""
        node_path = params.get("node_path", "")
        node = hou.node(node_path)

        if not node:
            raise ValueError(f"Node not found: {node_path}")

        return {
            "path": node.path(),
            "name": node.name(),
            "type": node.type().name(),
            "type_category": node.type().category().name(),
            "num_inputs": len(node.inputs()),
            "num_outputs": len(node.outputs()),
            "position": node.position(),
            "is_locked": node.isLocked(),
            "is_template": node.isTemplateFlagSet(),
            "comment": node.comment()
        }

    def _get_node_parameters(self, params):
        """Get all parameters and their values from a node"""
        node_path = params.get("node_path", "")
        node = hou.node(node_path)

        if not node:
            raise ValueError(f"Node not found: {node_path}")

        parameters = []
        for parm in node.parms():
            parm_template = parm.parmTemplate()
            parm_info = {
                "name": parm.name(),
                "label": parm_template.label(),
                "type": parm_template.type().name(),
                "value": None,
                "default_value": None,
                "has_expression": parm.isAtDefault() == False and parm.keyframes(),
                "is_locked": parm.isLocked()
            }

            try:
                # Get current value
                if parm_template.type() == hou.parmTemplateType.Toggle:
                    parm_info["value"] = parm.eval()
                elif parm_template.type() == hou.parmTemplateType.Int:
                    parm_info["value"] = parm.eval()
                elif parm_template.type() == hou.parmTemplateType.Float:
                    parm_info["value"] = parm.eval()
                elif parm_template.type() == hou.parmTemplateType.String:
                    parm_info["value"] = parm.eval()
                else:
                    parm_info["value"] = str(parm.eval())

                # Get default value
                parm_info["default_value"] = parm_template.defaultValue()[0] if parm_template.defaultValue() else None
            except:
                parm_info["value"] = "N/A"
                parm_info["default_value"] = "N/A"

            parameters.append(parm_info)

        return {
            "node_path": node_path,
            "node_type": node.type().name(),
            "num_parameters": len(parameters),
            "parameters": parameters
        }

    def _get_parameter_info(self, params):
        """Get information about available parameters for a node type"""
        node_type = params.get("node_type", "")
        category = params.get("category", "Sop")  # Default to SOP (geometry)

        try:
            # Get the node type definition
            if category.lower() == "sop":
                type_category = hou.sopNodeTypeCategory()
            elif category.lower() == "obj":
                type_category = hou.objNodeTypeCategory()
            elif category.lower() == "dop":
                type_category = hou.dopNodeTypeCategory()
            else:
                type_category = hou.sopNodeTypeCategory()

            node_type_def = type_category.nodeType(node_type)
            if not node_type_def:
                raise ValueError(f"Node type not found: {node_type}")

            # Get parameter templates
            parm_templates = node_type_def.parmTemplates()
            parameters = []

            for parm_template in parm_templates:
                parm_info = {
                    "name": parm_template.name(),
                    "label": parm_template.label(),
                    "type": parm_template.type().name(),
                    "help": parm_template.help() if parm_template.help() else "",
                    "num_components": parm_template.numComponents(),
                    "default_value": parm_template.defaultValue() if hasattr(parm_template, 'defaultValue') else None
                }
                parameters.append(parm_info)

            return {
                "node_type": node_type,
                "category": category,
                "description": node_type_def.description() if node_type_def.description() else "",
                "num_parameters": len(parameters),
                "parameters": parameters
            }
        except Exception as e:
            raise ValueError(f"Failed to get parameter info: {str(e)}")

    def _list_node_categories(self, params):
        """List all node categories (contexts) available in Houdini"""
        categories = hou.nodeTypeCategories()

        category_list = []
        for name, category in categories.items():
            category_list.append({
                "name": name,
                "label": category.label() if hasattr(category, 'label') else name
            })

        return {
            "num_categories": len(category_list),
            "categories": category_list
        }

    def _list_node_types(self, params):
        """List all node types in a specific category"""
        category_name = params.get("category", "Sop")

        try:
            # Get the category
            if category_name.lower() == "sop":
                category = hou.sopNodeTypeCategory()
            elif category_name.lower() == "obj" or category_name.lower() == "object":
                category = hou.objNodeTypeCategory()
            elif category_name.lower() == "dop":
                category = hou.dopNodeTypeCategory()
            elif category_name.lower() == "cop2" or category_name.lower() == "cop":
                category = hou.cop2NodeTypeCategory()
            elif category_name.lower() == "chop":
                category = hou.chopNodeTypeCategory()
            elif category_name.lower() == "vop":
                category = hou.vopNodeTypeCategory()
            elif category_name.lower() == "lop":
                category = hou.lopNodeTypeCategory()
            elif category_name.lower() == "top":
                category = hou.topNodeTypeCategory()
            else:
                # Try to get it from the categories dict
                categories = hou.nodeTypeCategories()
                category = categories.get(category_name)
                if not category:
                    raise ValueError(f"Unknown category: {category_name}")

            # Get all node types
            node_types = category.nodeTypes()

            node_type_list = []
            for name, node_type in node_types.items():
                node_type_list.append({
                    "name": name,
                    "description": node_type.description() if node_type.description() else "",
                    "category": category.name()
                })

            return {
                "category": category.name(),
                "num_node_types": len(node_type_list),
                "node_types": node_type_list
            }

        except Exception as e:
            raise ValueError(f"Failed to list node types: {str(e)}")

    def _get_node_documentation(self, params):
        """Get documentation for a specific node type from the help/nodes directory"""
        node_type = params.get("node_type", "")
        category = params.get("category", "sop").lower()

        import os

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct path to documentation file
        doc_file = os.path.join(script_dir, "help", "nodes", category, f"{node_type}.txt")

        if not os.path.exists(doc_file):
            return {
                "node_type": node_type,
                "category": category,
                "documentation": None,
                "error": f"Documentation file not found: {doc_file}"
            }

        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                documentation = f.read()

            return {
                "node_type": node_type,
                "category": category,
                "documentation": documentation,
                "file_path": doc_file
            }
        except Exception as e:
            return {
                "node_type": node_type,
                "category": category,
                "documentation": None,
                "error": f"Failed to read documentation: {str(e)}"
            }

    def _get_node_connections(self, params):
        """Get all input and output connections for a node"""
        node_path = params.get("node_path", "")
        node = hou.node(node_path)

        if not node:
            raise ValueError(f"Node not found: {node_path}")

        # Get inputs
        inputs = []
        for i, input_node in enumerate(node.inputs()):
            if input_node:
                # Find which output index of the source connects to this input
                source_outputs = input_node.outputs()
                source_index = 0
                for out_idx, conn in enumerate(input_node.outputConnections()):
                    if conn.inputNode() == node and conn.inputIndex() == i:
                        source_index = conn.outputIndex()
                        break

                inputs.append({
                    "source_node": input_node.path(),
                    "source_index": source_index
                })
            else:
                inputs.append(None)

        # Get outputs
        outputs = [[] for _ in range(len(node.outputConnections()))]
        for conn in node.outputConnections():
            output_idx = conn.outputIndex()
            # Ensure we have enough output slots
            while len(outputs) <= output_idx:
                outputs.append([])

            outputs[output_idx].append({
                "dest_node": conn.inputNode().path(),
                "dest_index": conn.inputIndex()
            })

        return {
            "node_path": node_path,
            "node_type": node.type().name(),
            "num_inputs": len(node.inputs()),
            "num_outputs": len(node.outputConnections()),
            "inputs": inputs,
            "outputs": outputs
        }

    def _get_folder_info(self, params):
        """Get information about nodes in a specific folder (non-recursive)"""
        folder_path = params.get("folder_path", "/obj")
        folder = hou.node(folder_path)

        if not folder:
            raise ValueError(f"Folder not found: {folder_path}")

        # Get direct children only (non-recursive)
        children = []
        for child in folder.children():
            # Get inputs for this child
            inputs = []
            for i, input_node in enumerate(child.inputs()):
                if input_node:
                    source_outputs = input_node.outputs()
                    source_index = 0
                    for conn in input_node.outputConnections():
                        if conn.inputNode() == child and conn.inputIndex() == i:
                            source_index = conn.outputIndex()
                            break

                    inputs.append({
                        "source_node": input_node.name(),  # Just name for brevity
                        "source_index": source_index
                    })
                else:
                    inputs.append(None)

            # Get outputs for this child
            outputs = [[] for _ in range(max(1, len(child.outputConnections())))]
            for conn in child.outputConnections():
                output_idx = conn.outputIndex()
                while len(outputs) <= output_idx:
                    outputs.append([])

                outputs[output_idx].append({
                    "dest_node": conn.inputNode().name(),  # Just name for brevity
                    "dest_index": conn.inputIndex()
                })

            children.append({
                "name": child.name(),
                "path": child.path(),
                "type": child.type().name(),
                "inputs": inputs,
                "outputs": outputs
            })

        return {
            "folder_path": folder_path,
            "folder_type": folder.type().name() if folder.type() else "root",
            "num_children": len(children),
            "children": children
        }

    def _execute_hscript(self, params):
        """Execute HScript commands"""
        code = params.get("code", "")

        try:
            result = hou.hscript(code)
            return {"output": result[0], "error": result[1]}
        except Exception as e:
            raise ValueError(f"HScript failed: {str(e)}")

    def _list_python_commands(self, params):
        """List all available Python HOM commands from help/hom/hou directory"""
        import os

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Path to the hou documentation directory
        hou_dir = os.path.join(script_dir, "help", "hom", "hou")

        if not os.path.exists(hou_dir):
            return {
                "num_commands": 0,
                "commands": [],
                "error": f"Documentation directory not found: {hou_dir}"
            }

        try:
            # List all .txt files in the hou directory
            commands = []
            for filename in os.listdir(hou_dir):
                if filename.endswith(".txt"):
                    # Remove .txt extension
                    command_name = filename[:-4]
                    commands.append(command_name)

            # Sort alphabetically
            commands.sort()

            return {
                "num_commands": len(commands),
                "commands": commands
            }
        except Exception as e:
            return {
                "num_commands": 0,
                "commands": [],
                "error": f"Failed to list commands: {str(e)}"
            }

    def _get_python_documentation(self, params):
        """Get documentation for a specific Python HOM command"""
        command_name = params.get("command_name", "")

        import os

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct path to documentation file
        doc_file = os.path.join(script_dir, "help", "hom", "hou", f"{command_name}.txt")

        if not os.path.exists(doc_file):
            return {
                "command_name": command_name,
                "documentation": None,
                "error": f"Documentation file not found: {doc_file}"
            }

        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                documentation = f.read()

            return {
                "command_name": command_name,
                "documentation": documentation,
                "file_path": doc_file
            }
        except Exception as e:
            return {
                "command_name": command_name,
                "documentation": None,
                "error": f"Failed to read documentation: {str(e)}"
            }

    def _execute_python(self, params):
        """Execute Python code in Houdini"""
        code = params.get("code", "")

        import sys
        from io import StringIO

        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        result = {
            "return_value": None,
            "output": "",
            "error": ""
        }

        try:
            # Execute the code
            # Use exec for statements, eval for expressions
            try:
                # Try to evaluate as expression first
                return_value = eval(code, {"hou": hou, "__builtins__": __builtins__})
                result["return_value"] = str(return_value) if return_value is not None else None
            except SyntaxError:
                # If that fails, execute as statements
                exec(code, {"hou": hou, "__builtins__": __builtins__})

            # Get captured output
            result["output"] = captured_output.getvalue()

        except Exception as e:
            result["error"] = str(e)
            import traceback
            result["error"] = traceback.format_exc()

        finally:
            # Restore stdout
            sys.stdout = old_stdout

        return result

    def _search_python_documentation(self, params):
        """Search through HOM documentation"""
        search_term = params.get("search_term", "").lower()
        search_type = params.get("search_type", "all").lower()

        import os
        import re

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        hou_dir = os.path.join(script_dir, "help", "hom", "hou")

        if not os.path.exists(hou_dir):
            return {
                "num_results": 0,
                "matches": [],
                "error": f"Documentation directory not found: {hou_dir}"
            }

        matches = []

        try:
            for filename in os.listdir(hou_dir):
                if not filename.endswith(".txt"):
                    continue

                command_name = filename[:-4]
                file_path = os.path.join(hou_dir, filename)

                # Read first 200 lines to get metadata and description
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = ""
                    for i, line in enumerate(f):
                        if i >= 200:  # Limit reading for performance
                            break
                        content += line

                # Extract metadata
                doc_type = None
                description = None
                group = None

                # Parse type
                type_match = re.search(r'^#type:\s*(\w+)', content, re.MULTILINE)
                if type_match:
                    doc_type = type_match.group(1)

                # Parse group
                group_match = re.search(r'^#group:\s*(.+)', content, re.MULTILINE)
                if group_match:
                    group = group_match.group(1).strip()

                # Extract description (usually in triple quotes)
                desc_match = re.search(r'"""(.+?)"""', content, re.DOTALL)
                if desc_match:
                    description = desc_match.group(1).strip()
                    # Clean up description - take first line or first 150 chars
                    description = description.split('\n')[0]
                    if len(description) > 150:
                        description = description[:150] + "..."

                # Determine if this matches based on search_type
                is_match = False

                if search_type == "all":
                    # Search in name, description, and group
                    if search_term in command_name.lower():
                        is_match = True
                    elif description and search_term in description.lower():
                        is_match = True
                    elif group and search_term in group.lower():
                        is_match = True
                elif search_type == "class":
                    # Only match classes
                    if doc_type == "homclass" and search_term in command_name.lower():
                        is_match = True
                elif search_type == "function":
                    # Only match functions
                    if doc_type == "homfunction" and search_term in command_name.lower():
                        is_match = True
                elif search_type == "content":
                    # Search in description only
                    if description and search_term in description.lower():
                        is_match = True

                if is_match:
                    matches.append({
                        "name": command_name,
                        "type": doc_type if doc_type else "unknown",
                        "description": description if description else "",
                        "group": group if group else ""
                    })

            # Sort by relevance (exact matches first, then alphabetical)
            def sort_key(match):
                name = match['name'].lower()
                # Exact match
                if name == search_term:
                    return (0, name)
                # Starts with search term
                elif name.startswith(search_term):
                    return (1, name)
                # Contains search term
                elif search_term in name:
                    return (2, name)
                # Only in description
                else:
                    return (3, name)

            matches.sort(key=sort_key)

            return {
                "num_results": len(matches),
                "matches": matches,
                "search_term": search_term,
                "search_type": search_type
            }

        except Exception as e:
            return {
                "num_results": 0,
                "matches": [],
                "error": f"Search failed: {str(e)}"
            }

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
