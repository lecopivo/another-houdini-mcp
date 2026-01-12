#!/usr/bin/env python3
"""
Test connection to Houdini MCP plugin

Run this script to verify that:
1. Houdini is running
2. The plugin is loaded
3. The connection works
"""
import socket
import json
import sys

HOST = "localhost"
PORT = 9876

def main():
    print("🔍 Testing connection to Houdini MCP Plugin...")
    print(f"   Host: {HOST}")
    print(f"   Port: {PORT}\n")

    try:
        # Connect
        print("📡 Connecting...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((HOST, PORT))
        print("   ✅ Connected successfully!\n")

        # Send test command
        print("📤 Sending test command (get_scene_info)...")
        command = {
            "type": "get_scene_info",
            "params": {}
        }
        sock.send(json.dumps(command).encode('utf-8'))

        # Receive response
        print("📥 Waiting for response...")
        response_data = sock.recv(4096).decode('utf-8')
        response = json.loads(response_data)

        if response.get("status") == "success":
            print("   ✅ Command executed successfully!\n")

            result = response.get("result", {})
            print("="*60)
            print("📊 Scene Information:")
            print("="*60)
            print(f"   File: {result.get('file_path', 'unknown')}")
            print(f"   Total nodes: {result.get('num_nodes', 0)}")

            nodes = result.get('nodes', [])
            if nodes:
                print(f"\n   First 5 nodes:")
                for node in nodes[:5]:
                    print(f"     • {node['path']} ({node['type']})")

            print("="*60)
            print("\n✅ Connection test PASSED!")
            print("   Houdini MCP is working correctly!\n")
        else:
            print(f"   ❌ Command failed: {response.get('error', 'unknown error')}")
            sys.exit(1)

        sock.close()

    except socket.timeout:
        print("\n❌ Connection timeout")
        print("   The plugin may be slow to respond or not running")
        sys.exit(1)

    except ConnectionRefusedError:
        print(f"\n❌ Cannot connect to Houdini on {HOST}:{PORT}")
        print("\nPossible issues:")
        print("  1. Houdini is not running")
        print("  2. The MCP plugin is not loaded in Houdini")
        print("\nTo fix:")
        print("  1. Open Houdini")
        print("  2. Go to Windows → Python Shell")
        print("  3. Run these commands:")
        print("")
        print("     import sys")
        print("     sys.path.append('/path/to/houdini-mcp')")
        print("     from houdini_plugin import HoudiniMCPServer")
        print("     server = HoudiniMCPServer()")
        print("     server.start()")
        print("")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
