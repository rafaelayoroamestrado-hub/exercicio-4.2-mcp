import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]
            
            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})
            
            resultado_criar = json.loads(criar.content[0].text)
            resultado_listar = json.loads(listar.content[0].text)
            
            if not isinstance(resultado_listar, list):
                resultado_listar = [resultado_listar]
            
            return {
                "tools": nomes,
                "criar_resultado": resultado_criar,
                "listar_resultado": resultado_listar
            }

if __name__ == "__main__":
    dicionario_final = asyncio.run(main())
    
    # Transforma em JSON em uma ÚNICA linha (sem o indent=2)
    json_final = json.dumps(dicionario_final)
    
    # Imprime as tags e o JSON tudo colado na mesma linha
    print(f"<mcp_test>{json_final}</mcp_test>")