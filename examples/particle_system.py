#!/usr/bin/env python3
"""
Example: Create a colorful particle system with wind effects

This example demonstrates:
- Scatter points on geometry
- Adding color attributes
- Using VEX for procedural effects
- Creating animated particle systems
"""
import socket
import json

HOST = "localhost"
PORT = 9876

def send_command(cmd):
    """Send command to Houdini plugin"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(json.dumps(cmd).encode('utf-8'))
    response = json.loads(sock.recv(4096).decode('utf-8'))
    sock.close()
    return response

def main():
    print("Creating colorful particle system...\n")

    # 1. Create geometry node
    print("1. Creating geometry container...")
    result = send_command({
        "type": "create_node",
        "params": {
            "node_type": "geo",
            "node_name": "particle_system",
            "parent": "/obj"
        }
    })
    geo_path = result['result']['node_path']
    print(f"   ✅ {geo_path}")

    # 2. Create sphere
    print("2. Creating sphere...")
    result = send_command({
        "type": "create_node",
        "params": {
            "node_type": "sphere",
            "parent": geo_path
        }
    })
    sphere_path = result['result']['node_path']
    print(f"   ✅ {sphere_path}")

    # 3. Scatter points
    print("3. Scattering 3000 points...")
    result = send_command({
        "type": "create_node",
        "params": {
            "node_type": "scatter",
            "parent": geo_path
        }
    })
    scatter_path = result['result']['node_path']

    send_command({
        "type": "connect_nodes",
        "params": {
            "source_path": sphere_path,
            "dest_path": scatter_path
        }
    })

    send_command({
        "type": "set_parameter",
        "params": {
            "node_path": scatter_path,
            "param_name": "npts",
            "param_value": 3000
        }
    })
    print(f"   ✅ 3000 particles created")

    # 4. Add colors
    print("4. Adding rainbow colors...")
    result = send_command({
        "type": "create_node",
        "params": {
            "node_type": "color",
            "parent": geo_path
        }
    })
    color_path = result['result']['node_path']

    send_command({
        "type": "connect_nodes",
        "params": {
            "source_path": scatter_path,
            "dest_path": color_path
        }
    })

    send_command({
        "type": "execute_hscript",
        "params": {
            "code": f"opparm {color_path} colortype ( ramp ) rampattribute ( P )"
        }
    })
    print(f"   ✅ Colors applied")

    # 5. Add wind animation with VEX
    print("5. Adding wind effects...")
    result = send_command({
        "type": "create_node",
        "params": {
            "node_type": "attribwrangle",
            "parent": geo_path
        }
    })
    wrangle_path = result['result']['node_path']

    send_command({
        "type": "connect_nodes",
        "params": {
            "source_path": color_path,
            "dest_path": wrangle_path
        }
    })

    # VEX code for wind and animation
    vex_code = """// Wind animation
float time = @Frame / 48.0;

// Noise-based wind
vector wind = noise(@P * 2.0 + set(time * 2.0, 0, 0)) - 0.5;
@P += wind * 0.5;

// Animated scale
float pulse = sin(time * 6.28 + @ptnum * 0.1) * 0.5 + 0.5;
@pscale = 0.02 + pulse * 0.02;

// Color variation
@Cd = @Cd * (0.7 + pulse * 0.3);
"""

    send_command({
        "type": "set_parameter",
        "params": {
            "node_path": wrangle_path,
            "param_name": "snippet",
            "param_value": vex_code
        }
    })

    send_command({
        "type": "execute_hscript",
        "params": {
            "code": f"opset -d on {wrangle_path}"
        }
    })
    print(f"   ✅ Wind effects added")

    # 6. Set playback
    print("6. Setting up playback...")
    send_command({
        "type": "execute_hscript",
        "params": {
            "code": "tset 1 48"
        }
    })
    print(f"   ✅ Playback configured")

    print("\n" + "="*60)
    print("✨ Particle system created!")
    print("="*60)
    print("\nFeatures:")
    print("  • 3000 colorful particles")
    print("  • Wind-like motion")
    print("  • Pulsing animation")
    print("  • Rainbow gradient colors")
    print("\nIn Houdini:")
    print("  1. Press SPACE to frame the particles")
    print("  2. Press PLAY to see the animation")
    print("  3. Tumble the view to see from different angles")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print("❌ Cannot connect to Houdini on localhost:9876")
        print("Make sure the Houdini plugin is running!")
    except Exception as e:
        print(f"❌ Error: {e}")
