# unlock-reso-mcp

An MCP (Model Context Protocol) server implementation with example tools, resources, and prompts.

## Features

### Tools
- **calculate**: Perform basic arithmetic operations (add, subtract, multiply, divide)
- **get_weather**: Get mock weather information for a location

### Resources
- **config://settings**: Application configuration settings
- **data://sample**: Sample user and statistics data

### Prompts
- **analyze_code**: Analyze code for potential improvements
- **generate_summary**: Generate a summary of provided text

## Installation

1. Install dependencies:
```bash
uv pip install -e .
```

## Usage

### Running the server

```bash
python -m main
```

Or after installation:
```bash
unlock-reso-mcp
```

### Configuring with Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "unlock-reso-mcp": {
      "command": "python",
      "args": ["-m", "main"],
      "cwd": "/path/to/unlock-reso-mcp"
    }
  }
}
```

Or if installed:
```json
{
  "mcpServers": {
    "unlock-reso-mcp": {
      "command": "unlock-reso-mcp"
    }
  }
}
```

## Development

To modify the server, edit `main.py` and add your own:

1. **Tools**: Add new tools in `list_tools()` and implement handlers in `call_tool()`
2. **Resources**: Add new resources in `list_resources()` and implement readers in `read_resource()`
3. **Prompts**: Add new prompts in `list_prompts()` and implement them in `get_prompt()`

## Example Usage

Once configured in Claude Desktop, you can use the MCP server features:

### Using Tools
- "Calculate 42 * 7"
- "What's the weather in San Francisco?"

### Using Resources
- "Show me the application settings"
- "Get the sample data"

### Using Prompts
- "Analyze this Python code for improvements"
- "Generate a summary of this article"