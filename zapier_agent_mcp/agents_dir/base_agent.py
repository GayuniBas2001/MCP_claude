import asyncio
import os
import shutil
import subprocess
import time
from typing import Any

from agents import Agent, Runner, gen_trace_id, trace
# from agents.mcp import MCPServerSettings, MCPServerSse
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings

# # Define Zapier MCP server settings
# ZAPIER_MCP = MCPServerSettings(
#     command="npx",
#     args=[
#         "mcp-remote",
#         "https://actions.zapier.com/mcp/sk-ak-DBmR4BcjJApuOBFQu6SG4kPTjj/sse",
#     ],
# )

async def run(mcp_server: MCPServer):
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        mcp_servers=[mcp_server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    # Use the `add` tool to add two numbers
    message = "Could you please send an email to gayunibas@gmail.com and tell them that I am running late?. Use available MCP server tools if necessary."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

async def main():
    async with MCPServerSse(
        name="Zapier MCP Server",
        params={
            "url": "https://actions.zapier.com/mcp/sk-ak-DBmR4BcjJApuOBFQu6SG4kPTjj/sse",
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Zapier MCP Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/{trace_id}\n")
            await run(server)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error running the example: {e}")
