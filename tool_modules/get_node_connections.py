from typing import Any, Optional
import json

TOOL_NAME = "get_node_connections"
IS_MUTATING = False

send_command = None

def get_node_connections(node_path: str) -> str:
    """
    Get all input and output connections for a specific node

    Use this for detailed connection analysis of a specific node.
    For a broader view of connections in a folder, use get_folder_info() instead.

    Args:
        node_path: Full path to the node (e.g., '/obj/geo1/box1')

    Returns:
        Information about node's input and output connections
    """
    result = send_command({
        "type": "get_node_connections",
        "params": {"node_path": node_path}
    })

    output = f"🔗 Connections for {result['node_path']}\n"
    output += f"   Type: {result['node_type']}\n\n"

    output += f"Inputs ({result['num_inputs']}):\n"
    if result['inputs']:
        for idx, inp in enumerate(result['inputs']):
            if inp:
                output += f"  [{idx}] ← {inp['source_node']} (output {inp['source_index']})\n"
            else:
                output += f"  [{idx}] (not connected)\n"
    else:
        output += "  (no inputs)\n"

    output += f"\nOutputs ({result['num_outputs']}):\n"
    if result['outputs']:
        for idx, outputs_list in enumerate(result['outputs']):
            if outputs_list:
                output += f"  [{idx}] → "
                connections = [f"{conn['dest_node']} (input {conn['dest_index']})" for conn in outputs_list]
                output += ", ".join(connections) + "\n"
            else:
                output += f"  [{idx}] (not connected)\n"
    else:
        output += "  (no outputs)\n"

    return output


def register_mcp_tool(mcp, send_command_impl, legacy_bridge_functions=None, tool_decorator=None):
    global send_command
    send_command = send_command_impl
    decorator = tool_decorator or mcp.tool
    decorator()(get_node_connections)


def execute_plugin(params, server, hou):
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
