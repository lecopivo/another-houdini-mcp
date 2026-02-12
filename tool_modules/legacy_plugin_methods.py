"""Legacy Houdini plugin method implementations extracted from houdini_plugin.py."""

import hou

class LegacyPluginMethods:
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

        # Lock state is only meaningful for HDA-backed nodes.
        is_hda = node.type().definition() is not None
        is_locked = None
        if is_hda:
            lock_fn = getattr(node, "isLockedHDA", None)
            if callable(lock_fn):
                try:
                    is_locked = bool(lock_fn())
                except Exception:
                    is_locked = None

        return {
            "path": node.path(),
            "name": node.name(),
            "type": node.type().name(),
            "type_category": node.type().category().name(),
            "num_inputs": len(node.inputs()),
            "num_outputs": len(node.outputs()),
            "position": [node.position()[0], node.position()[1]],
            "is_hda": is_hda,
            "is_locked": is_locked,
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

            # In HOM's NodeConnection naming, outputNode() is the downstream node.
            dest_node = conn.outputNode()
            outputs[output_idx].append({
                "dest_node": dest_node.path() if dest_node else None,
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
        allow_dangerous = bool(params.get("allow_dangerous", False))

        import sys
        import textwrap
        from io import StringIO

        normalized_code = textwrap.dedent(code).strip()
        flattened_code = " ".join(
            line.strip() for line in normalized_code.splitlines() if line.strip()
        )

        dangerous_patterns = [
            "hou.exit",
            "os.remove",
            "os.unlink",
            "shutil.rmtree",
            "subprocess",
            "os.system",
            "os.popen",
            "__import__",
        ]

        if not allow_dangerous:
            lowered = normalized_code.lower()
            for pattern in dangerous_patterns:
                if pattern in lowered:
                    raise ValueError(
                        "Dangerous pattern detected in execute_python: "
                        f"'{pattern}'. Set allow_dangerous=True to override."
                    )

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
                return_value = eval(normalized_code, {"hou": hou, "__builtins__": __builtins__})
                result["return_value"] = str(return_value) if return_value is not None else None
            except SyntaxError:
                # If that fails, execute as statements
                try:
                    exec(normalized_code, {"hou": hou, "__builtins__": __builtins__})
                except SyntaxError:
                    # Fallback for line-break formatting issues from some clients
                    exec(flattened_code, {"hou": hou, "__builtins__": __builtins__})

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

    def _search_documentation_files(self, params):
        """Search files under the local help directory by path and optional content."""
        import fnmatch
        import os
        import re

        query = params.get("query", "").strip().lower()
        file_pattern = params.get("file_pattern", "*.txt")
        search_content = bool(params.get("search_content", True))
        search_mode = str(params.get("search_mode", "any")).lower()
        max_results = int(params.get("max_results", 30))
        max_results = max(1, min(max_results, 200))
        context_chars = int(params.get("context_chars", 100))
        context_chars = max(20, min(context_chars, 400))

        if not query:
            return {
                "num_results": 0,
                "results": [],
                "error": "query is required"
            }

        if search_mode not in ("any", "all"):
            return {
                "num_results": 0,
                "results": [],
                "error": "search_mode must be 'any' or 'all'"
            }

        query_terms = [term for term in re.split(r"\s+", query) if term]
        if not query_terms:
            query_terms = [query]

        script_dir = os.path.dirname(os.path.abspath(__file__))
        help_dir = os.path.join(script_dir, "help")

        if not os.path.isdir(help_dir):
            return {
                "num_results": 0,
                "results": [],
                "error": f"Documentation directory not found: {help_dir}"
            }

        results = []

        for root, _, files in os.walk(help_dir):
            for filename in files:
                if not fnmatch.fnmatch(filename, file_pattern):
                    continue

                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, help_dir)
                rel_path_lower = rel_path.lower()

                path_matches = [term for term in query_terms if term in rel_path_lower]
                content_matches = []
                snippet = ""

                content = ""
                content_lower = ""
                if search_content:
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read(120000)
                        content_lower = content.lower()
                        content_matches = [term for term in query_terms if term in content_lower]
                    except Exception:
                        continue

                if search_mode == "all":
                    matched_terms = set(path_matches) | set(content_matches)
                    is_match = all(term in matched_terms for term in query_terms)
                else:
                    is_match = bool(path_matches or content_matches)

                if is_match:
                    matched_in = []
                    score = 0
                    if path_matches:
                        matched_in.append("path")
                        score += 100 + 10 * len(path_matches)
                    if content_matches:
                        matched_in.append("content")
                        score += 20 + 3 * len(content_matches)

                    snippet_term = None
                    for term in query_terms:
                        if term in content_lower:
                            snippet_term = term
                            break

                    if snippet_term:
                        idx = content_lower.find(snippet_term)
                        start = max(0, idx - context_chars)
                        end = min(len(content), idx + len(snippet_term) + context_chars)
                        snippet = content[start:end].replace("\n", " ").strip()

                    results.append({
                        "rel_path": rel_path,
                        "file_path": file_path,
                        "matched_in": "+".join(matched_in),
                        "matched_terms": sorted(set(path_matches + content_matches)),
                        "score": score,
                        "snippet": snippet,
                        "size_bytes": os.path.getsize(file_path),
                    })

                if len(results) >= max_results:
                    break

            if len(results) >= max_results:
                break

        results.sort(key=lambda item: (-item.get("score", 0), item["rel_path"]))

        return {
            "query": query,
            "query_terms": query_terms,
            "file_pattern": file_pattern,
            "search_content": search_content,
            "search_mode": search_mode,
            "help_dir": help_dir,
            "num_results": len(results),
            "results": results
        }

    def _read_documentation_file(self, params):
        """Read a documentation file from the local help directory."""
        import os

        rel_path = params.get("path", "").strip()
        max_chars = int(params.get("max_chars", 20000))
        max_chars = max(500, min(max_chars, 200000))

        if not rel_path:
            return {
                "error": "path is required"
            }

        script_dir = os.path.dirname(os.path.abspath(__file__))
        help_dir = os.path.join(script_dir, "help")
        normalized_rel = os.path.normpath(rel_path).lstrip("/")
        file_path = os.path.abspath(os.path.join(help_dir, normalized_rel))

        if not file_path.startswith(os.path.abspath(help_dir) + os.sep):
            return {
                "error": "path must stay within the help directory"
            }

        if not os.path.isfile(file_path):
            return {
                "error": f"Documentation file not found: {normalized_rel}",
                "help_dir": help_dir
            }

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(max_chars + 1)

        truncated = len(content) > max_chars
        if truncated:
            content = content[:max_chars]

        return {
            "path": normalized_rel,
            "file_path": file_path,
            "content": content,
            "truncated": truncated,
            "max_chars": max_chars,
            "size_bytes": os.path.getsize(file_path)
        }

    def _create_digital_asset(self, params):
        """Create a digital asset from an existing node or export/update an existing HDA definition."""
        import os

        node_path = params.get("node_path", "")
        definition_name = params.get("definition_name", "")
        description = params.get("description", "")
        hda_file_path = params.get("hda_file_path", "")
        min_inputs = int(params.get("min_inputs", 0))
        max_inputs = int(params.get("max_inputs", 0))

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        if not definition_name:
            raise ValueError("definition_name is required")

        if not hda_file_path:
            raise ValueError("hda_file_path is required")

        hda_file_path = os.path.abspath(hda_file_path)
        os.makedirs(os.path.dirname(hda_file_path), exist_ok=True)

        existing_def = node.type().definition()

        if existing_def is None:
            node = node.createDigitalAsset(
                name=definition_name,
                hda_file_name=hda_file_path,
                description=description if description else node.name(),
                min_num_inputs=min_inputs,
                max_num_inputs=max_inputs,
            )
        else:
            # Existing HDA node: export/copy definition to requested target.
            existing_def.copyToHDAFile(
                hda_file_path,
                new_name=definition_name,
                new_menu_name=description if description else existing_def.description(),
            )

        definition = node.type().definition()
        definition.updateFromNode(node)

        return {
            "node_path": node.path(),
            "node_type": node.type().nameWithCategory(),
            "definition_name": definition.nodeTypeName(),
            "description": definition.description(),
            "hda_file_path": definition.libraryFilePath(),
        }

    def _set_hda_lock_state(self, params):
        """Lock or unlock an HDA instance."""
        node_path = params.get("node_path", "")
        locked = bool(params.get("locked", True))

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        definition = node.type().definition()
        if definition is None:
            raise ValueError(f"Node is not a digital asset instance: {node_path}")

        if locked:
            node.matchCurrentDefinition()
        else:
            node.allowEditingOfContents()

        return {
            "node_path": node.path(),
            "requested_locked": locked,
            "matches_current_definition": node.matchesCurrentDefinition(),
        }

    def _save_hda_definition(self, params):
        """Save the current node contents/parameters back into its HDA definition."""
        node_path = params.get("node_path", "")

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        definition = node.type().definition()
        if definition is None:
            raise ValueError(f"Node is not a digital asset instance: {node_path}")

        definition.updateFromNode(node)

        return {
            "node_path": node.path(),
            "definition_name": definition.nodeTypeName(),
            "hda_file_path": definition.libraryFilePath(),
        }

    def _get_hda_definition_info(self, params):
        """Get definition information for an HDA instance."""
        node_path = params.get("node_path", "")

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        definition = node.type().definition()
        if definition is None:
            return {
                "node_path": node.path(),
                "is_hda_instance": False,
            }

        return {
            "node_path": node.path(),
            "is_hda_instance": True,
            "node_type": node.type().nameWithCategory(),
            "definition_name": definition.nodeTypeName(),
            "description": definition.description(),
            "library_file_path": definition.libraryFilePath(),
            "matches_current_definition": node.matchesCurrentDefinition(),
            "is_editable_inside_locked_hda": node.isEditableInsideLockedHDA(),
        }

    def _create_parm_template_from_spec(self, spec):
        """Build a parameter template from a simple declarative spec."""
        parm_type = str(spec.get("type", "float")).lower()
        name = spec.get("name")
        label = spec.get("label", name)

        if not name:
            raise ValueError("Parameter spec missing required field: name")

        num_components = int(spec.get("num_components", 1))
        default_value = spec.get("default_value")

        if parm_type == "float":
            if default_value is None:
                default_value = tuple(0.0 for _ in range(num_components))
            parm = hou.FloatParmTemplate(name, label, num_components, default_value=tuple(default_value))
        elif parm_type == "int":
            if default_value is None:
                default_value = tuple(0 for _ in range(num_components))
            parm = hou.IntParmTemplate(name, label, num_components, default_value=tuple(default_value))
        elif parm_type == "string":
            if default_value is None:
                default_value = tuple("" for _ in range(num_components))
            parm = hou.StringParmTemplate(name, label, num_components, default_value=tuple(default_value))
        elif parm_type == "toggle":
            if default_value is None:
                default_value = True if spec.get("default_value", False) else False
            parm = hou.ToggleParmTemplate(name, label, default_value=bool(default_value))
        elif parm_type == "menu":
            menu_items = tuple(spec.get("menu_items", []))
            menu_labels = tuple(spec.get("menu_labels", menu_items))
            default_menu_index = int(spec.get("default_value", 0))
            parm = hou.MenuParmTemplate(
                name,
                label,
                menu_items=menu_items,
                menu_labels=menu_labels,
                default_value=default_menu_index,
            )
        else:
            raise ValueError(f"Unsupported parameter type: {parm_type}")

        # Optional limits. Not all parm template types expose limit APIs.
        if "min" in spec and hasattr(parm, "setMinValue"):
            parm.setMinValue(spec["min"])
        if "max" in spec and hasattr(parm, "setMaxValue"):
            parm.setMaxValue(spec["max"])
        if hasattr(parm, "setMinIsStrict"):
            parm.setMinIsStrict(bool(spec.get("min_strict", False)))
        if hasattr(parm, "setMaxIsStrict"):
            parm.setMaxIsStrict(bool(spec.get("max_strict", False)))

        # Optional naming scheme for tuples.
        naming_scheme = spec.get("naming_scheme")
        if naming_scheme:
            scheme_map = {
                "xyzw": hou.parmNamingScheme.XYZW,
                "base1": hou.parmNamingScheme.Base1,
                "base0": hou.parmNamingScheme.Base0,
                "rgba": hou.parmNamingScheme.RGBA,
                "uvw": hou.parmNamingScheme.UVW,
            }
            scheme = scheme_map.get(str(naming_scheme).lower())
            if scheme is None:
                raise ValueError(f"Unsupported naming_scheme: {naming_scheme}")
            if hasattr(parm, "setNamingScheme"):
                parm.setNamingScheme(scheme)

        # Optional conditionals.
        hide_when = spec.get("hide_when")
        disable_when = spec.get("disable_when")
        if hide_when:
            parm.setConditional(hou.parmCondType.HideWhen, hide_when)
        if disable_when:
            parm.setConditional(hou.parmCondType.DisableWhen, disable_when)

        help_text = spec.get("help")
        if help_text:
            parm.setHelp(str(help_text))

        return parm

    def _edit_parameter_interface(self, params):
        """Edit node parameter interface from a declarative schema."""
        node_path = params.get("node_path", "")
        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        folder_name = params.get("folder_name", "custom_controls")
        folder_label = params.get("folder_label", "Custom Controls")
        clear_folder = bool(params.get("clear_folder", True))
        append_at_end = bool(params.get("append_at_end", True))
        parameter_specs = params.get("parameters", [])

        if not isinstance(parameter_specs, list):
            raise ValueError("parameters must be a list")

        ptg = node.parmTemplateGroup()

        if clear_folder:
            try:
                ptg.remove(folder_name)
            except Exception:
                pass

        folder = hou.FolderParmTemplate(folder_name, folder_label)
        for spec in parameter_specs:
            parm_template = self._create_parm_template_from_spec(spec)
            folder.addParmTemplate(parm_template)

        if append_at_end:
            ptg.append(folder)
        else:
            ptg.insertBefore((0,), folder)

        node.setParmTemplateGroup(ptg)

        return {
            "node_path": node.path(),
            "folder_name": folder_name,
            "folder_label": folder_label,
            "num_parameters_added": len(parameter_specs),
        }

    def _set_parameter_conditionals(self, params):
        """Set hide/disable conditionals on an existing parameter template."""
        node_path = params.get("node_path", "")
        param_name = params.get("param_name", "")
        hide_when = params.get("hide_when")
        disable_when = params.get("disable_when")

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")
        if not param_name:
            raise ValueError("param_name is required")

        ptg = node.parmTemplateGroup()
        parm_template = ptg.find(param_name)
        if parm_template is None:
            raise ValueError(f"Parameter template not found: {param_name}")

        if hide_when is not None:
            parm_template.setConditional(hou.parmCondType.HideWhen, str(hide_when))
        if disable_when is not None:
            parm_template.setConditional(hou.parmCondType.DisableWhen, str(disable_when))

        ptg.replace(param_name, parm_template)
        node.setParmTemplateGroup(ptg)

        return {
            "node_path": node.path(),
            "param_name": param_name,
            "hide_when": hide_when,
            "disable_when": disable_when,
        }

    def _bind_internal_parameters(self, params):
        """Bind internal parameters to controller parameters via expressions."""
        node_path = params.get("node_path", "")
        bindings = params.get("bindings", [])

        root = hou.node(node_path) if node_path else None
        if node_path and root is None:
            raise ValueError(f"Node not found: {node_path}")
        if not isinstance(bindings, list):
            raise ValueError("bindings must be a list")

        applied = 0
        for binding in bindings:
            target_node_ref = binding.get("target_node", "")
            target_parm_name = binding.get("target_parm", "")
            expression = binding.get("expression")
            language_raw = str(binding.get("language", "hscript")).lower()
            source_parm = binding.get("source_parm", "")

            if not target_node_ref or not target_parm_name:
                raise ValueError("Each binding requires target_node and target_parm")

            if target_node_ref.startswith("/"):
                target_node = hou.node(target_node_ref)
            elif root:
                target_node = root.node(target_node_ref)
            else:
                target_node = None

            if target_node is None:
                raise ValueError(f"Target node not found: {target_node_ref}")

            target_parm = target_node.parm(target_parm_name)
            if target_parm is None:
                raise ValueError(f"Target parameter not found: {target_node.path()}.{target_parm_name}")

            if expression is None:
                if not source_parm:
                    raise ValueError("Each binding requires either expression or source_parm")
                expression = f'ch("../{source_parm}")'

            if language_raw == "python":
                language = hou.exprLanguage.Python
            else:
                language = hou.exprLanguage.Hscript

            target_parm.setExpression(str(expression), language)
            applied += 1

        return {
            "node_path": root.path() if root else None,
            "num_bindings_applied": applied,
        }

    def _set_primitive_type_by_token(self, params):
        """Set primitive node 'type' parameter using a menu token (e.g. polymesh)."""
        node_path = params.get("node_path", "")
        token = str(params.get("token", ""))

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")
        if not token:
            raise ValueError("token is required")

        type_parm = node.parm("type")
        if type_parm is None:
            raise ValueError(f"Node has no 'type' parameter: {node_path}")

        valid_tokens = tuple(type_parm.menuItems())
        if token not in valid_tokens:
            raise ValueError(f"Invalid token '{token}'. Valid tokens: {valid_tokens}")

        type_parm.set(token)

        return {
            "node_path": node.path(),
            "token": type_parm.evalAsString(),
            "label": type_parm.menuLabels()[type_parm.eval()],
        }

    def _set_output_node_index(self, params):
        """Set the output index for an output node."""
        node_path = params.get("node_path", "")
        output_index = int(params.get("output_index", 0))

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        parm = node.parm("outputidx")
        if parm is None:
            raise ValueError(f"Node has no outputidx parameter: {node_path}")

        parm.set(output_index)

        return {
            "node_path": node.path(),
            "output_index": parm.eval(),
        }

    def _validate_hda(self, params):
        """Validate common HDA expectations and return diagnostics."""
        node_path = params.get("node_path", "")
        rules = params.get("rules", {})

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        errors = []
        warnings = []
        checks = []

        definition = node.type().definition()
        require_definition = bool(rules.get("require_definition", True))
        if require_definition and definition is None:
            errors.append("Node is not an HDA instance")
        checks.append({"check": "is_hda_instance", "ok": definition is not None})

        require_match = bool(rules.get("require_match_definition", False))
        matches_definition = node.matchesCurrentDefinition() if definition else False
        if require_match and not matches_definition:
            errors.append("Node does not match current definition")
        checks.append({"check": "matches_current_definition", "ok": matches_definition})

        required_parameters = rules.get("required_parameters", [])
        for parm_name in required_parameters:
            ok = node.parm(parm_name) is not None
            checks.append({"check": f"has_parameter:{parm_name}", "ok": ok})
            if not ok:
                errors.append(f"Missing parameter: {parm_name}")

        required_internal_nodes = rules.get("required_internal_nodes", [])
        for rel_path in required_internal_nodes:
            internal = node.node(rel_path)
            ok = internal is not None
            checks.append({"check": f"has_internal_node:{rel_path}", "ok": ok})
            if not ok:
                errors.append(f"Missing internal node: {rel_path}")

        expected_output_indices = rules.get("expected_output_indices", [])
        for entry in expected_output_indices:
            rel_node = entry.get("node", "")
            expected = int(entry.get("index", 0))
            internal = node.node(rel_node)
            ok = False
            if internal is not None and internal.parm("outputidx") is not None:
                ok = (internal.parm("outputidx").eval() == expected)
            checks.append({"check": f"output_index:{rel_node}", "ok": ok})
            if not ok:
                errors.append(f"Output index mismatch for {rel_node}, expected {expected}")

        primitive_type_expectations = rules.get("primitive_type_expectations", [])
        for entry in primitive_type_expectations:
            rel_node = entry.get("node", "")
            expected_token = str(entry.get("token", ""))
            internal = node.node(rel_node)
            ok = False
            if internal is not None and internal.parm("type") is not None:
                ok = (internal.parm("type").evalAsString() == expected_token)
            checks.append({"check": f"primitive_type:{rel_node}", "ok": ok})
            if not ok:
                errors.append(f"Primitive type mismatch for {rel_node}, expected {expected_token}")

        if definition and not definition.libraryFilePath():
            warnings.append("Definition has no library file path")

        return {
            "node_path": node.path(),
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "checks": checks,
        }

    def _find_node_type(self, type_name):
        """Find a Houdini node type by name across all categories."""
        if not type_name:
            return None

        normalized = str(type_name)
        if "/" in normalized:
            normalized = normalized.split("/")[-1]

        categories = hou.nodeTypeCategories()
        for _, category in categories.items():
            node_type = category.nodeType(normalized)
            if node_type is not None:
                return node_type
        return None

    def _resolve_hda_definition(self, params):
        """Resolve an HDA definition from node_path, type_name, or definition_name."""
        node_path = params.get("node_path")
        if node_path:
            node = hou.node(node_path)
            if not node:
                raise ValueError(f"Node not found: {node_path}")
            definition = node.type().definition()
            if definition is None:
                raise ValueError(f"Node is not an HDA instance: {node_path}")
            return node, definition

        type_name = params.get("type_name") or params.get("definition_name")
        node_type = self._find_node_type(type_name)
        if node_type is None:
            raise ValueError(f"HDA type not found: {type_name}")
        definition = node_type.definition()
        if definition is None:
            raise ValueError(f"Type has no HDA definition: {type_name}")
        return None, definition

    def _parm_template_to_dict(self, template):
        """Convert a parm template to a serializable dictionary."""
        parm_type = template.type().name().lower()
        data = {
            "name": template.name(),
            "label": template.label(),
            "type": parm_type,
        }

        if hasattr(template, "numComponents"):
            data["num_components"] = template.numComponents()

        if hasattr(template, "defaultValue"):
            try:
                data["default_value"] = list(template.defaultValue())
            except Exception:
                pass

        if hasattr(template, "menuItems"):
            try:
                data["menu_items"] = list(template.menuItems())
                data["menu_labels"] = list(template.menuLabels())
            except Exception:
                pass

        if hasattr(template, "minValue"):
            try:
                data["min"] = template.minValue()
                data["max"] = template.maxValue()
                data["min_strict"] = template.minIsStrict()
                data["max_strict"] = template.maxIsStrict()
            except Exception:
                pass

        if template.type() == hou.parmTemplateType.Folder:
            children = []
            try:
                for child in template.parmTemplates():
                    children.append(self._parm_template_to_dict(child))
            except Exception:
                pass
            data["children"] = children

        try:
            conditionals = template.conditionals()
            if conditionals:
                if hou.parmCondType.HideWhen in conditionals:
                    data["hide_when"] = conditionals[hou.parmCondType.HideWhen]
                if hou.parmCondType.DisableWhen in conditionals:
                    data["disable_when"] = conditionals[hou.parmCondType.DisableWhen]
        except Exception:
            pass

        return data

    def _create_parm_template_from_tree(self, spec):
        """Build parm templates with optional folder nesting from a declarative schema."""
        parm_type = str(spec.get("type", "float")).lower()
        if parm_type != "folder":
            return self._create_parm_template_from_spec(spec)

        folder_name = spec.get("name")
        folder_label = spec.get("label", folder_name)
        if not folder_name:
            raise ValueError("Folder spec requires name")

        folder = hou.FolderParmTemplate(folder_name, folder_label)
        for child in spec.get("children", []):
            folder.addParmTemplate(self._create_parm_template_from_tree(child))
        return folder

    def _get_hda_parm_templates(self, params):
        """Get parameter templates from an HDA definition."""
        _, definition = self._resolve_hda_definition(params)
        ptg = definition.parmTemplateGroup()
        templates = [self._parm_template_to_dict(entry) for entry in ptg.entries()]

        return {
            "definition_name": definition.nodeTypeName(),
            "library_file_path": definition.libraryFilePath(),
            "num_top_level_templates": len(templates),
            "templates": templates,
        }

    def _set_hda_parm_templates(self, params):
        """Set parameter templates on an HDA definition."""
        node, definition = self._resolve_hda_definition(params)
        templates = params.get("templates", [])
        replace_all = bool(params.get("replace_all", True))

        if not isinstance(templates, list):
            raise ValueError("templates must be a list")

        if replace_all:
            ptg = hou.ParmTemplateGroup()
        else:
            ptg = definition.parmTemplateGroup()

        for spec in templates:
            ptg.append(self._create_parm_template_from_tree(spec))

        definition.setParmTemplateGroup(ptg)

        if node is not None and bool(params.get("sync_instance", True)):
            node.matchCurrentDefinition()

        return {
            "definition_name": definition.nodeTypeName(),
            "library_file_path": definition.libraryFilePath(),
            "num_top_level_templates": len(definition.parmTemplateGroup().entries()),
            "replace_all": replace_all,
        }

    def _set_hda_parm_default(self, params):
        """Set a single default value on an HDA definition parameter template."""
        node, definition = self._resolve_hda_definition(params)
        param_name = params.get("param_name", "")
        default_value = params.get("default_value")

        if not param_name:
            raise ValueError("param_name is required")
        if default_value is None:
            raise ValueError("default_value is required")

        ptg = definition.parmTemplateGroup()
        template = ptg.find(param_name)
        if template is None:
            raise ValueError(f"Parameter template not found: {param_name}")

        parm_type = template.type()
        if parm_type == hou.parmTemplateType.Toggle:
            template.setDefaultValue(bool(default_value))
        elif parm_type == hou.parmTemplateType.Menu:
            template.setDefaultValue(int(default_value))
        else:
            num_components = template.numComponents() if hasattr(template, "numComponents") else 1
            if isinstance(default_value, (list, tuple)):
                value_tuple = tuple(default_value)
            else:
                value_tuple = tuple(default_value for _ in range(num_components))
            if len(value_tuple) != num_components:
                raise ValueError(
                    f"default_value length mismatch for {param_name}. "
                    f"Expected {num_components}, got {len(value_tuple)}"
                )
            template.setDefaultValue(value_tuple)

        ptg.replace(param_name, template)
        definition.setParmTemplateGroup(ptg)

        if node is not None and bool(params.get("sync_instance", True)):
            node.matchCurrentDefinition()

        return {
            "definition_name": definition.nodeTypeName(),
            "param_name": param_name,
            "default_value": default_value,
        }

    def _set_hda_internal_binding(self, params):
        """Set an expression binding on an internal parameter of an HDA instance."""
        hda_node_path = params.get("hda_node_path", "")
        internal_node = params.get("internal_node", "")
        internal_parm = params.get("internal_parm", "")
        source_parm = params.get("source_parm")
        expression = params.get("expression")
        language_raw = str(params.get("language", "hscript")).lower()

        hda_node = hou.node(hda_node_path)
        if not hda_node:
            raise ValueError(f"HDA node not found: {hda_node_path}")
        if hda_node.type().definition() is None:
            raise ValueError(f"Node is not an HDA instance: {hda_node_path}")
        if not internal_node or not internal_parm:
            raise ValueError("internal_node and internal_parm are required")

        if bool(params.get("unlock", True)):
            hda_node.allowEditingOfContents()

        target_node = hda_node.node(internal_node)
        if target_node is None:
            raise ValueError(f"Internal node not found: {hda_node_path}/{internal_node}")

        target_parm = target_node.parm(internal_parm)
        if target_parm is None:
            raise ValueError(f"Internal parameter not found: {target_node.path()}.{internal_parm}")

        if expression is None:
            if not source_parm:
                raise ValueError("Either source_parm or expression is required")
            expression = f'ch(\"../{source_parm}\")'

        language = hou.exprLanguage.Python if language_raw == "python" else hou.exprLanguage.Hscript
        target_parm.setExpression(str(expression), language)

        if bool(params.get("save_definition", True)):
            hda_node.type().definition().updateFromNode(hda_node)
        if bool(params.get("relock", True)):
            hda_node.matchCurrentDefinition()

        return {
            "hda_node_path": hda_node.path(),
            "target_parm_path": f"{target_node.path()}.{internal_parm}",
            "expression": str(expression),
            "language": "python" if language == hou.exprLanguage.Python else "hscript",
        }

    def _set_hda_internal_parm(self, params):
        """Set a value or expression on an internal parameter of an HDA instance."""
        hda_node_path = params.get("hda_node_path", "")
        internal_node = params.get("internal_node", "")
        internal_parm = params.get("internal_parm", "")
        param_value = params.get("param_value")
        expression = params.get("expression")
        language_raw = str(params.get("language", "hscript")).lower()

        hda_node = hou.node(hda_node_path)
        if not hda_node:
            raise ValueError(f"HDA node not found: {hda_node_path}")
        if hda_node.type().definition() is None:
            raise ValueError(f"Node is not an HDA instance: {hda_node_path}")
        if not internal_node or not internal_parm:
            raise ValueError("internal_node and internal_parm are required")

        if bool(params.get("unlock", True)):
            hda_node.allowEditingOfContents()

        target_node = hda_node.node(internal_node)
        if target_node is None:
            raise ValueError(f"Internal node not found: {hda_node_path}/{internal_node}")

        target_parm = target_node.parm(internal_parm)
        if target_parm is None:
            raise ValueError(f"Internal parameter not found: {target_node.path()}.{internal_parm}")

        if expression is not None:
            language = hou.exprLanguage.Python if language_raw == "python" else hou.exprLanguage.Hscript
            target_parm.setExpression(str(expression), language)
        else:
            target_parm.set(param_value)

        if bool(params.get("save_definition", True)):
            hda_node.type().definition().updateFromNode(hda_node)
        if bool(params.get("relock", True)):
            hda_node.matchCurrentDefinition()

        return {
            "hda_node_path": hda_node.path(),
            "target_parm_path": f"{target_node.path()}.{internal_parm}",
            "value": target_parm.evalAsString() if target_parm.parmTemplate().type() == hou.parmTemplateType.String else target_parm.eval(),
        }

    def _save_hda_from_instance(self, params):
        """Save the HDA definition from an instance, with optional relock."""
        node_path = params.get("node_path", "")
        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")
        definition = node.type().definition()
        if definition is None:
            raise ValueError(f"Node is not an HDA instance: {node_path}")

        definition.updateFromNode(node)
        if bool(params.get("relock", True)):
            node.matchCurrentDefinition()

        return {
            "node_path": node.path(),
            "definition_name": definition.nodeTypeName(),
            "library_file_path": definition.libraryFilePath(),
            "matches_current_definition": node.matchesCurrentDefinition(),
        }

    def _instantiate_hda(self, params):
        """Instantiate an HDA node in a given parent network."""
        type_name = params.get("type_name") or params.get("definition_name")
        parent_path = params.get("parent_path", "/obj")
        node_name = params.get("node_name", "")

        parent = hou.node(parent_path)
        if not parent:
            raise ValueError(f"Parent not found: {parent_path}")

        node_type = self._find_node_type(type_name)
        if node_type is None:
            raise ValueError(f"HDA type not found: {type_name}")

        node = parent.createNode(node_type.name(), node_name)

        if bool(params.get("set_display", False)) and hasattr(node, "setDisplayFlag"):
            try:
                node.setDisplayFlag(True)
                node.setRenderFlag(True)
            except Exception:
                pass

        return {
            "node_path": node.path(),
            "node_type": node.type().nameWithCategory(),
            "definition_name": node.type().definition().nodeTypeName() if node.type().definition() else None,
        }

    def _geometry_stats(self, node):
        """Get basic geometry stats from a SOP node."""
        geometry = node.geometry()
        return {
            "points": len(geometry.points()),
            "prims": len(geometry.prims()),
            "vertices": sum(prim.numVertices() for prim in geometry.prims()),
            "point_attributes": sorted([attrib.name() for attrib in geometry.pointAttribs()]),
            "prim_attributes": sorted([attrib.name() for attrib in geometry.primAttribs()]),
            "detail_attributes": sorted([attrib.name() for attrib in geometry.globalAttribs()]),
        }

    def _probe_geometry(self, params):
        """Probe geometry output metrics for a node."""
        node_path = params.get("node_path", "")
        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")

        stats = self._geometry_stats(node)
        return {
            "node_path": node.path(),
            "stats": stats,
        }

    def _validate_hda_behavior(self, params):
        """Validate HDA behavior by probing geometry across parameterized test cases."""
        node_path = params.get("node_path", "")
        cases = params.get("cases", [])
        comparisons = params.get("comparisons", [])
        require_point_attributes = params.get("require_point_attributes", [])

        node = hou.node(node_path)
        if not node:
            raise ValueError(f"Node not found: {node_path}")
        if not isinstance(cases, list) or len(cases) == 0:
            raise ValueError("cases must be a non-empty list")

        # Save initial parm values for all params touched by cases.
        tracked_parms = set()
        for case in cases:
            for parm_name in case.get("set_parameters", {}).keys():
                tracked_parms.add(parm_name)
        saved_values = {}
        for parm_name in tracked_parms:
            parm = node.parm(parm_name)
            if parm is not None:
                saved_values[parm_name] = parm.eval()

        case_results = {}
        errors = []
        checks = []

        try:
            for case in cases:
                name = case.get("name", "")
                if not name:
                    raise ValueError("Each case requires a non-empty name")

                for parm_name, value in case.get("set_parameters", {}).items():
                    parm = node.parm(parm_name)
                    if parm is None:
                        raise ValueError(f"Parameter not found on node: {parm_name}")
                    parm.set(value)

                stats = self._geometry_stats(node)
                case_results[name] = stats

                for attr_name in require_point_attributes:
                    ok = attr_name in stats["point_attributes"]
                    checks.append({"check": f"{name}:has_point_attr:{attr_name}", "ok": ok})
                    if not ok:
                        errors.append(f"Case '{name}' missing point attribute '{attr_name}'")

            op_map = {
                "gt": lambda a, b: a > b,
                "ge": lambda a, b: a >= b,
                "lt": lambda a, b: a < b,
                "le": lambda a, b: a <= b,
                "eq": lambda a, b: a == b,
                "ne": lambda a, b: a != b,
            }

            for comparison in comparisons:
                case_a = comparison.get("a")
                case_b = comparison.get("b")
                metric = comparison.get("metric", "points")
                op = str(comparison.get("op", "gt")).lower()

                if case_a not in case_results or case_b not in case_results:
                    raise ValueError(f"Invalid comparison cases: {case_a}, {case_b}")
                if metric not in ("points", "prims", "vertices"):
                    raise ValueError(f"Unsupported metric for comparison: {metric}")
                if op not in op_map:
                    raise ValueError(f"Unsupported comparison op: {op}")

                left = case_results[case_a][metric]
                right = case_results[case_b][metric]
                ok = op_map[op](left, right)
                checks.append({
                    "check": f"{case_a}.{metric} {op} {case_b}.{metric}",
                    "ok": ok,
                    "left": left,
                    "right": right,
                })
                if not ok:
                    errors.append(
                        f"Behavior check failed: {case_a}.{metric} ({left}) "
                        f"{op} {case_b}.{metric} ({right})"
                    )
        finally:
            for parm_name, value in saved_values.items():
                parm = node.parm(parm_name)
                if parm is not None:
                    parm.set(value)

        return {
            "node_path": node.path(),
            "valid": len(errors) == 0,
            "errors": errors,
            "checks": checks,
            "case_results": case_results,
        }
