#!/usr/bin/env python3
"""
Example: Create an animated cube that moves and rotates

This example demonstrates:
- Creating geometry nodes
- Adding animation expressions
- Setting playback range
"""
import socket
import json

HOST = "localhost"
PORT = 9876

def send_command(cmd):
    """Send command to Houdini plugin"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))

        payload = json.dumps(cmd).encode('utf-8')
        sock.send(len(payload).to_bytes(4, byteorder='big'))
        sock.send(payload)

        length_bytes = sock.recv(4)
        if not length_bytes:
            raise RuntimeError("Connection closed while reading response length")

        response_length = int.from_bytes(length_bytes, byteorder='big')
        response_bytes = b''
        while len(response_bytes) < response_length:
            chunk = sock.recv(min(4096, response_length - len(response_bytes)))
            if not chunk:
                raise RuntimeError("Connection closed while reading response body")
            response_bytes += chunk

        return json.loads(response_bytes.decode('utf-8'))
    finally:
        sock.close()

def main():
    print("Creating animated cube...\n")

    # 1. Create geometry node
    print("1. Creating geometry node...")
    result = send_command({
        "type": "create_node",
        "params": {
            "node_type": "geo",
            "node_name": "animated_cube",
            "parent": "/obj"
        }
    })
    geo_path = result['result']['node_path']
    print(f"   ✅ Created: {geo_path}")

    # 2. Create box inside geometry
    print("2. Creating box...")
    result = send_command({
        "type": "create_node",
        "params": {
            "node_type": "box",
            "node_name": "cube",
            "parent": geo_path
        }
    })
    print(f"   ✅ Created: {result['result']['node_path']}")

    # 3. Add animation - X translation
    print("3. Animating X position...")
    result = send_command({
        "type": "execute_hscript",
        "params": {
            "code": f"opparm {geo_path} tx ( '$F/48*10' )"
        }
    })
    print(f"   ✅ Cube will move from X=0 to X=10")

    # 4. Add animation - Y rotation
    print("4. Animating Y rotation...")
    result = send_command({
        "type": "execute_hscript",
        "params": {
            "code": f"opparm {geo_path} ry ( '$F/48*360' )"
        }
    })
    print(f"   ✅ Cube will rotate 360 degrees")

    # 5. Set playback range
    print("5. Setting playback range...")
    result = send_command({
        "type": "execute_hscript",
        "params": {
            "code": "tset 1 48"
        }
    })
    print(f"   ✅ Playback set to frames 1-48")

    print("\n" + "="*60)
    print("✨ Animated cube created successfully!")
    print("="*60)
    print("\nIn Houdini:")
    print("  1. Press SPACE to frame the view")
    print("  2. Press PLAY to watch the animation")
    print("  3. The cube moves and rotates over 48 frames")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print("❌ Cannot connect to Houdini on localhost:9876")
        print("Make sure the Houdini plugin is running!")
    except Exception as e:
        print(f"❌ Error: {e}")
