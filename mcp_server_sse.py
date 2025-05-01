from random import random

from mcp.server import FastMCP
from mcp.server.fastmcp import Context

from shared.mcp_base_server import IzzyMCP

settings = {"host": "127.0.0.1", "port": 3500}
mcp = IzzyMCP("Contoso Medical MCP Service", log_level="DEBUG", **settings)

@mcp.tool(description="Returns the Information from the Service about Contoso Medical")
def get_information(ctx: Context) -> str:
    ctx.info("IZZY CLIENT ID" + ctx.client_id)
    ctx.debug(ctx.session)
    return "The information here is great"

@mcp.tool(description="Retrieves the Current Temperature in Fahrenheit for Contoso Islands")
async def get_temperature(ctx: Context) -> float:
    await ctx.debug(ctx.session)
    print(ctx.request_context)
    return random() * 95

@mcp.tool(description="Calculates the Taxes for a specific amount")
async def calculate_taxes(amount: float, ctx: Context) -> float:
    await ctx.warning("Israel is making some info here")
    await ctx.debug(ctx.session)
    print(ctx.request_context)
    await ctx.error("Israel made some calls here")
    return random() * amount


if __name__ == "__main__":
    mcp.run(transport='sse')