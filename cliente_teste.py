import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            tool_names = [tool.name for tool in tools_result.tools]
            criar_resultado = await session.call_tool("criar_tarefa", arguments={"titulo": "tarefa via mcp"})
            listar_resultado = await session.call_tool("listar_tarefas", arguments={})
            envelope = {
                "tools": tool_names,
                "criar_resultado": json.loads(criar_resultado.content[0].text),
                "listar_resultado": json.loads(listar_resultado.content[0].text)
            }
            print(json.dumps(envelope, indent=2, ensure_ascii=False))
if __name__ == "__main__":
    asyncio.run(main())
