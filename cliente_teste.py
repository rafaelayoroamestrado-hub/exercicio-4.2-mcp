import sys
import json

try:
    import asyncio
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def main():
        # sys.executable garante que o servidor use o mesmo Python do Autograder
        params = StdioServerParameters(command=sys.executable, args=["servidor_mcp.py"])
        
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

    dicionario_final = asyncio.run(main())
    json_final = json.dumps(dicionario_final, indent=2)
    
    print("<mcp_test>")
    print(json_final)
    print("</mcp_test>")

except Exception as e:
    # Se o Autograder falhar, capturamos o erro e imprimimos como JSON!
    erro = {"erro_fatal": str(e), "tipo": str(type(e))}
    print("<mcp_test>")
    print(json.dumps(erro))
    print("</mcp_test>")