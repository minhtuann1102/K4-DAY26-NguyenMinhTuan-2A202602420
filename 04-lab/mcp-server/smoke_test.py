"""Smoke test cho Weather MCP server (Streamable HTTP).

Kết nối tới endpoint MCP, liệt kê tool rồi gọi thử cả 3 tool.

    python smoke_test.py                              # http://localhost:8085/mcp
    python smoke_test.py http://localhost:8086/mcp    # container Docker
    python smoke_test.py https://<service>.run.app/mcp  # Cloud Run
"""

import asyncio
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8085/mcp"

CALLS = [
    ("health_check", {}),
    ("get_current_weather", {"city": "Hanoi"}),
    ("get_forecast", {"city": "Danang", "days": 2}),
]


async def main() -> None:
    print(f"MCP endpoint: {URL}")
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("list_tools ->", [t.name for t in tools.tools])

            for name, args in CALLS:
                result = await session.call_tool(name, args)
                text = "\n".join(c.text for c in result.content if hasattr(c, "text"))
                print(f"\n--- call_tool {name}({args})")
                print(text.strip())


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    asyncio.run(main())
