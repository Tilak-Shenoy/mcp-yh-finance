from mcp.server.fastmcp import FastMCP
from .yh_tools import reg_tools
import signal
import sys
from typing import Optional, Any

def create_server() -> FastMCP:
    """Create a FastMCP server."""
    server = FastMCP("Yahoo Finance Server")

    reg_tools(server)

    return server

# Handle SIGINT (Ctrl+C) gracefully
def signal_handler(sig: int, frame: Optional[Any]) -> None:
    print("Shutting down server gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    print("Starting Yahoo Finance Server...")

    server = create_server()

    server.run()

if __name__ == "__main__":
    main()
    



