# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Support for more Houdini contexts (DOPs, COPs, CHOPs)
- Viewport rendering and screenshot capture
- Geometry data export/import
- Node preset management
- Multi-session support

## [1.0.0] - 2026-01-12

### Added
- Initial release of Houdini MCP Server
- MCP server for Claude Code integration
- Houdini plugin for receiving commands via TCP
- Core MCP tools:
  - `create_node` - Create nodes in Houdini
  - `delete_node` - Delete nodes
  - `connect_nodes` - Connect node outputs to inputs
  - `set_parameter` - Set parameter values
  - `get_scene_info` - Query scene structure
  - `execute_hscript` - Execute HScript commands
- Automatic setup script for macOS, Linux, Windows
- Python dependencies: fastmcp, httpx
- Example scripts:
  - `create_animated_cube.py` - Basic animation example
  - `particle_system.py` - Particle effects with VEX
  - `test_connection.py` - Connection testing utility
- Comprehensive documentation:
  - README with usage examples
  - INSTALL guide with troubleshooting
  - CONTRIBUTING guidelines
  - MIT License
- Cross-platform support (macOS, Linux, Windows)
- Support for Houdini 19.5+

### Technical Details
- TCP socket communication on localhost:9876
- JSON message protocol
- Thread-based connection handling
- FastMCP for MCP server implementation
- Compatible with Python 3.10+

[Unreleased]: https://github.com/YOUR_USERNAME/houdini-mcp/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/YOUR_USERNAME/houdini-mcp/releases/tag/v1.0.0
