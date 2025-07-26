import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
    Prompt,
    PromptMessage,
    PromptArgument,
)
from mcp.server.stdio import stdio_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("unlock-reso-mcp")

# Initialize the MCP server
server = Server("unlock-reso-mcp")


# Tool handlers
@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="calculate",
            description="Perform basic arithmetic calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The arithmetic operation to perform",
                    },
                    "a": {
                        "type": "number",
                        "description": "First number",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number",
                    },
                },
                "required": ["operation", "a", "b"],
            },
        ),
        Tool(
            name="get_weather",
            description="Get weather information for a location (mock data)",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or location",
                    },
                },
                "required": ["location"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent | ImageContent]:
    """Handle tool execution."""
    if name == "calculate":
        operation = arguments["operation"]
        a = arguments["a"]
        b = arguments["b"]
        
        result = None
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b != 0:
                result = a / b
            else:
                return [TextContent(type="text", text="Error: Division by zero")]
        
        return [TextContent(type="text", text=f"Result: {result}")]
    
    elif name == "get_weather":
        location = arguments["location"]
        # Mock weather data
        weather_data = {
            "location": location,
            "temperature": "72°F",
            "condition": "Partly cloudy",
            "humidity": "65%",
            "wind": "10 mph",
        }
        
        return [
            TextContent(
                type="text",
                text=f"Weather in {location}:\n"
                     f"Temperature: {weather_data['temperature']}\n"
                     f"Condition: {weather_data['condition']}\n"
                     f"Humidity: {weather_data['humidity']}\n"
                     f"Wind: {weather_data['wind']}"
            )
        ]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


# Resource handlers
@server.list_resources()
async def list_resources() -> List[EmbeddedResource]:
    """List available resources."""
    return [
        EmbeddedResource(
            uri="config://settings",
            name="Application Settings",
            description="Current application configuration",
            mimeType="application/json",
        ),
        EmbeddedResource(
            uri="data://sample",
            name="Sample Data",
            description="Example data for demonstration",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource."""
    if uri == "config://settings":
        settings = {
            "version": "0.1.0",
            "debug": True,
            "max_retries": 3,
            "timeout": 30,
        }
        return json.dumps(settings, indent=2)
    
    elif uri == "data://sample":
        sample_data = {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "user"},
                {"id": 3, "name": "Charlie", "role": "user"},
            ],
            "stats": {
                "total_users": 3,
                "active_sessions": 2,
                "last_updated": "2024-01-15T10:30:00Z",
            },
        }
        return json.dumps(sample_data, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri}")


# Prompt handlers
@server.list_prompts()
async def list_prompts() -> List[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="analyze_code",
            description="Analyze code for potential improvements",
            arguments=[
                PromptArgument(
                    name="language",
                    description="Programming language",
                    required=True,
                ),
                PromptArgument(
                    name="code",
                    description="Code to analyze",
                    required=True,
                ),
            ],
        ),
        Prompt(
            name="generate_summary",
            description="Generate a summary of provided text",
            arguments=[
                PromptArgument(
                    name="text",
                    description="Text to summarize",
                    required=True,
                ),
                PromptArgument(
                    name="max_length",
                    description="Maximum length of summary in words",
                    required=False,
                ),
            ],
        ),
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: Optional[Dict[str, str]] = None) -> Prompt:
    """Get a specific prompt with filled arguments."""
    if name == "analyze_code":
        language = arguments.get("language", "") if arguments else ""
        code = arguments.get("code", "") if arguments else ""
        
        return Prompt(
            name="analyze_code",
            description="Analyze code for potential improvements",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please analyze the following {language} code and suggest improvements:\n\n```{language}\n{code}\n```\n\nConsider aspects like:\n1. Code quality and readability\n2. Performance optimizations\n3. Best practices\n4. Potential bugs or issues\n5. Security considerations"
                    ),
                )
            ],
        )
    
    elif name == "generate_summary":
        text = arguments.get("text", "") if arguments else ""
        max_length = arguments.get("max_length", "100") if arguments else "100"
        
        return Prompt(
            name="generate_summary",
            description="Generate a summary of provided text",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please provide a concise summary of the following text in no more than {max_length} words:\n\n{text}\n\nFocus on the key points and main ideas."
                    ),
                )
            ],
        )
    
    else:
        raise ValueError(f"Unknown prompt: {name}")


# Logging configuration
@server.set_logging_level()
async def set_logging_level(level: LoggingLevel) -> None:
    """Set the logging level of the server."""
    logging.getLogger().setLevel(level.value.upper())
    logger.info(f"Logging level set to {level.value}")


async def main():
    """Run the MCP server."""
    logger.info("Starting unlock-reso-mcp server...")
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
