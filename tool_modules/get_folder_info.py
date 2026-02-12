"""get_folder_info tool definition shared between bridge and plugin."""

TOOL_NAME = "get_folder_info"
IS_MUTATING = False


def register_mcp_tool(mcp, send_command, legacy_bridge_functions=None, tool_decorator=None):
    decorator = tool_decorator or mcp.tool

    @decorator()
    def get_folder_info(folder_path: str = "/obj") -> str:
        """
        **PRIMARY ENTRY POINT** - Get information about nodes in a specific folder

        THIS IS THE MAIN TOOL TO EXPLORE AND UNDERSTAND THE HOUDINI SCENE.
        Always start here when you need to understand what's in a scene.

        This tool shows you all nodes in a specific location with their connections,
        allowing you to navigate the scene hierarchy step by step.

        Navigation guide:
        - Start with "/" to see the root level
        - Use "/obj" to see all object-level nodes (default)
        - Use "/obj/geo1" to see inside a geometry node
        - Use "/stage" for USD/Solaris nodes
        - Use "/ch" for channel operators

        This is NON-RECURSIVE - it only shows direct children, making it fast
        and easy to navigate complex scenes level by level.

        Args:
            folder_path: Path to folder/node (e.g., '/', '/obj', '/obj/geo1')

        Returns:
            List of all nodes in the folder with their connections
        """
        result = send_command(
            {
                "type": TOOL_NAME,
                "params": {"folder_path": folder_path},
            }
        )

        output = f"📁 Folder: {result['folder_path']}\n"
        output += f"   Type: {result['folder_type']}\n"
        output += f"   Children: {result['num_children']}\n\n"

        if result["num_children"] == 0:
            output += "   (empty)\n"
            return output

        output += "Nodes:\n"
        for node in result["children"]:
            output += f"\n  📦 {node['name']} ({node['type']})\n"
            output += f"     Path: {node['path']}\n"

            if node.get("inputs"):
                output += "     Inputs: "
                input_strs = []
                for idx, inp in enumerate(node["inputs"]):
                    if inp:
                        input_strs.append(f"[{idx}]←{inp['source_node']}")
                output += ", ".join(input_strs) if input_strs else "(none connected)"
                output += "\n"

            if node.get("outputs"):
                has_outputs = any(node["outputs"])
                if has_outputs:
                    output += "     Outputs: "
                    output_strs = []
                    for idx, outputs_list in enumerate(node["outputs"]):
                        if outputs_list:
                            for conn in outputs_list:
                                output_strs.append(f"[{idx}]→{conn['dest_node']}")
                    output += ", ".join(output_strs)
                    output += "\n"

        return output


def execute_plugin(params, server, hou):
    folder_path = params.get("folder_path", "/obj")
    folder = hou.node(folder_path)

    if not folder:
        raise ValueError(f"Folder not found: {folder_path}")

    children = []
    for child in folder.children():
        inputs = []
        for i, input_node in enumerate(child.inputs()):
            if input_node:
                source_index = 0
                for conn in input_node.outputConnections():
                    if conn.inputNode() == child and conn.inputIndex() == i:
                        source_index = conn.outputIndex()
                        break

                inputs.append({
                    "source_node": input_node.name(),
                    "source_index": source_index,
                })
            else:
                inputs.append(None)

        outputs = [[] for _ in range(max(1, len(child.outputConnections())))]
        for conn in child.outputConnections():
            output_idx = conn.outputIndex()
            while len(outputs) <= output_idx:
                outputs.append([])

            outputs[output_idx].append({
                "dest_node": conn.inputNode().name(),
                "dest_index": conn.inputIndex(),
            })

        children.append(
            {
                "name": child.name(),
                "path": child.path(),
                "type": child.type().name(),
                "inputs": inputs,
                "outputs": outputs,
            }
        )

    return {
        "folder_path": folder_path,
        "folder_type": folder.type().name() if folder.type() else "root",
        "num_children": len(children),
        "children": children,
    }
