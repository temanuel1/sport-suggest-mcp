import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server


server = Server("sport-suggest-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools."""
    return []


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Call a tool."""
    raise ValueError(f"Unknown tool: {name}")


async def async_main():
    """Async main function"""
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr, flush=True)
        raise


def main():
    """Entry point for the CLI"""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
