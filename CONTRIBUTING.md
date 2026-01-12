# Contributing to Houdini MCP

Thank you for your interest in contributing to Houdini MCP! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/houdini-mcp.git
cd houdini-mcp
./setup.sh
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

## Testing

Before submitting a pull request:

1. Test with the examples:
   ```bash
   python3 examples/test_connection.py
   python3 examples/create_animated_cube.py
   ```

2. Verify your changes work with different Houdini versions if possible

3. Check for any error messages in the Houdini Python Shell

## Submitting Changes

1. Ensure your code follows the style guidelines
2. Write clear, descriptive commit messages
3. Include examples or documentation for new features
4. Reference any related issues in your PR description

## Reporting Bugs

When reporting bugs, please include:

- Your operating system and version
- Houdini version
- Python version
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any error messages or logs

## Feature Requests

We welcome feature requests! Please:

- Check if the feature has already been requested
- Clearly describe the feature and its use case
- Explain why it would be useful to others

## Questions?

- Open a GitHub Discussion for general questions
- Use GitHub Issues for bug reports and feature requests

Thank you for contributing! 🎉
